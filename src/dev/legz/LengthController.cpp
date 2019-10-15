/**
 * @file LengthController.h
 * @brief Implementation of class LengthController
 * @author Hany Hamed
 * This was built over one of the source codes of NTRTsim codes
 */

// This module
#include "LengthController.h"
#include "nlohmann/json.hpp"


// The C++ Standard Library
#include <cassert>
#include <stdexcept>
#include <time.h>
#include <iostream>
#include <fstream>
#include <string>
#include <math.h>


#define HOST_NAME "localhost"
#define PORT_NUM 10022
#define MAX_BUFF_SIZE 5000
#define EPS 0.00001  

bool all_reached_target = true;

using namespace std;
using json = nlohmann::json;


LengthController::LengthController(const double length) :
  m_length(length)
{
  if (length < 0.0)
    {
      throw std::invalid_argument("Negative length");
    }

}

LengthController::~LengthController()
{
}	

void LengthController::onSetup(legzModel& subject)
{
  LengthController::tcp_com = new TCP(HOST_NAME, PORT_NUM);

  LengthController::tcp_com->setup();
  JSON_Structure::setup();
  m_controllers.clear(); //clear vector of controllers
  start_lengths.clear(); //vector of randomized restlengths
    
  //get all of the tensegrity structure's cables
  actuators = subject.getAllActuators();
  rods = subject.getAllRods();


  printf("Number of actuators: %d , Number of Rods: %d\n", actuators.size(), rods.size());
  // std::cout<<rods[1]->getTags()[0][1]<<"\n";

  //Attach a tgBasicController to each actuator
  for (size_t i = 0; i < actuators.size(); ++i)
  {
    tgBasicActuator * const pActuator = actuators[i];
    assert(pActuator != NULL);  //precondition
    //instantiate controllers for each cable
    tgBasicController* m_lenController = new tgBasicController(pActuator, m_length);
    //add controller to vector
    m_controllers.push_back(m_lenController);
    //generate random end restlength
    double start_length = actuators[i]->getStartLength();
    printf("Actutor of string #%d -> start Lenght: %lf\n", i, start_length);
    start_lengths.push_back(start_length);
    actuators_states.push_back(0);
    target_lengths.push_back(0);
  }
}

//This function is being activated each step
void LengthController::onStep(legzModel& subject, double dt)
{

  if (dt <= 0.0) {
    throw std::invalid_argument("dt is not positive");
  }
  else {
    globalTime += dt;
    if(globalTime > 0){ //delay start of cable actuation
      if(toggle==0){    //print once when motors start moving
        cout << endl << "Activating Cable Motors -------------------------------------" << endl;
	      toggle = 1;   //is used like a state flag ---- set it to 2 to disable the movement
      }

      /**
       * Observations:
       *    1 - Cables' lengths
       *    2 - Center of Mass for rods
       *    3 - Time
       * */
      else if(toggle == 1){
        // TODO: I don't know if it is better and will be faster not to write to the json object all the time but write to a local array then convert it
        
        // It has been reversed in order to make an action then get an observation of the action

        // Part 2: Read the upcoming orders from the python module
        char buffer[MAX_BUFF_SIZE];
        bzero(&buffer,MAX_BUFF_SIZE);
        LengthController::tcp_com->read_TCP(buffer,MAX_BUFF_SIZE);
        // printf("###Recieved: %s \n",buffer);
        json read = JSON_Structure::stringToJson(buffer);
        // std::cout<<"REAL: "<<actuators[2]->getCurrentLength()<<std::endl;

        // std::cout<<read["Controllers_val"][2]<<std::endl;
        // TODO: Here is taking the length of the cable from the python module, but in other versions we will send from the python just the change not the cable's length
        //set new targets
        if(all_reached_target == true){
          all_reached_target = false;
          for(int i = 0; i < actuators.size(); i++){
            target_lengths[i] = actuators[i]->getRestLength() + (double)read["Controllers_val"][i];
          }
        }

        for(int i = 0; i < actuators.size(); i++){
          if(((double) read["Controllers_val"][i]) == 0)
            continue;
          
          printf("Controller#%dERR:%lf\n",i,abs(actuators[i]->getRestLength() - target_lengths[i]));
          std::cout<<"REAL: Current :"<<actuators[i]->getCurrentLength()<<": Rest :"<<actuators[i]->getRestLength()<<std::endl;
          std::cout<<"Target: "<<target_lengths[i]<<std::endl;

          // m_controllers[i]->control(dt,((double) read["Controllers_val"][i]));
          m_controllers[i]->control(dt, target_lengths[i]);
          actuators[i]->moveMotors(dt);
          // printf("%d\n", actuators.size());
          // printf("#%d -> %lf\n, -> %lf", i, (double) read["Controllers_val"][i], 5);
          // printf("ERR:%lf\n",abs(actuators[i]->getCurrentLength()- (double)read["Controllers_val"][i]));
          if( abs(actuators[i]->getRestLength() - target_lengths[i]) <= EPS){
            all_reached_target = true;
            printf("Reached\n");
          }
        }



        // Part 1: Write the observations to the python module
        // Get the observation
        //(1) Center of Mass
        for(int i = 0; i < rods.size(); i++){
          double CMS[3] = {0,0,0};
          CMS[0] += rods[i]->centerOfMass().getX();
          CMS[1] += rods[i]->centerOfMass().getY();
          CMS[2] += rods[i]->centerOfMass().getZ();
          // printf("%lf %lf %lf \n", CMS[0],CMS[1], CMS[2]);
          JSON_Structure::setCenterOfMass(i, CMS[0],CMS[1],CMS[2]);
        }
        



        
        //This part will be done in python side
        // 1-Convert the orientation from the quaternion to the rotation matrix
        // 2-Get the end-effector from transforming the vector from the center of mass
        //    to the end point (this vector is in terms of orientation of the center of mass
        //    coordinate system. So, we will just multiply the transformation matrix with this
        //    vector as the vecotr is known as the length is know between the two end-points
        //    then we will get the end-effector point.


        // Actions will be distributed in the python script, the observation will only be the coordinate of the end-effector and the cable's lenghts at the moment
        //    that's for Q-learning
        // std::cout<<rods[1]->getDescendants()
        // (2) Get the orientation


        for(int i = 0; i < rods.size(); i++){
          btVector3 orientation = rods[i]->orientation();
          // std::cout<<orientation[0]<<":"<<orientation[1]<<":"<<orientation[2]<<":"<<orientation[3]<<std::endl;
          JSON_Structure::setOrientation(i, orientation[0], orientation[1], orientation[2], orientation[3]);
        } 

        // (3) Get the length of targeting cables
        for(int i = 0; i < actuators.size(); i++){
          JSON_Structure::setController(i, (int) (actuators[i]->getRestLength()*10000) /10000.0);
        }

        // (4) Get the reached flag
        JSON_Structure::setFlags(0, (int) all_reached_target);

        // (5) Set the time stamp
        JSON_Structure::setTime(((int)(globalTime*1000)) /1000.0);

        std::string json_string = JSON_Structure::jsonToString();
        // std::cout<<"String to be sent"<<json_string<<std::endl;
        LengthController::tcp_com->write_TCP((void*) json_string.c_str());
        
      }
    }
  }

}


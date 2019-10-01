/**
 * @file LengthController.h
 * @brief Implementation of class LengthController
 * @author Hany Hamed
 * This was built over one of the source codes of NTRTsim codes
 */

// This module
#include "LengthController.h"

// The C++ Standard Library
#include <cassert>
#include <stdexcept>
#include <time.h>
#include <iostream>
#include <fstream>
#include <string>
#include <math.h>


#define HOST_NAME "localhost"
#define PORT_NUM 10023

using namespace std;

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
    if(globalTime > 2){ //delay start of cable actuation
      if(toggle==0){    //print once when motors start moving
        cout << endl << "Activating Cable Motors -------------------------------------" << endl;
	      toggle = 1;   //is used like a state flag
      }
      // First move
      else if(toggle==1){
        toggle = 2;
        // double dLength = 10;
        // int target_actuator = 5;
        // double target_length = max(0.0, start_lengths[target_actuator] - dLength);

        // printf("Actuator #%d -> Start length: %lf , target length: %lf\n",target_actuator, start_lengths[target_actuator], target_length);
        // m_controllers[target_actuator]->control(dt,target_length);
        // actuators[target_actuator]->moveMotors(dt);

        // //This to confirm that it had been changed
        // if(actuators[target_actuator]->getRestLength()!=target_length)
        //   toggle = 1;

        int num_target_actuators = 2;
        double dLength[] = {20, 20};
        int target_actuator[] = {2, 5};
        double target_length[2];
        for(int i = 0; i < num_target_actuators; i++){
          target_length[i] = max(0.0, start_lengths[target_actuator[i]] - dLength[i]);
          // printf("Actuator #%d -> Start length: %lf , target length: %lf\n",target_actuator[i], start_lengths[target_actuator[i]], target_length[i]);
        }
        bool all_reached_target = true;
        for(int i = 0; i < num_target_actuators; i++){
          m_controllers[target_actuator[i]]->control(dt,target_length[i]);
          actuators[target_actuator[i]]->moveMotors(dt);
          if(actuators[target_actuator[i]]->getRestLength()!=target_length[i])
            all_reached_target = false;
        }

        if(!all_reached_target)
          toggle = 1;
      }
      // Second move
      else if(toggle==2){
        toggle = 1;
        int num_target_actuators = 2;
        double dLength[] = {-15, -15};
        int target_actuator[] = {2, 5};
        double target_length[2];
        for(int i = 0; i < num_target_actuators; i++){
          target_length[i] = max(0.0, start_lengths[target_actuator[i]] - dLength[i]);
          // printf("Actuator #%d -> Start length: %lf , current length: %lf, target length: %lf\n",target_actuator[i], start_lengths[target_actuator[i]], actuators[target_actuator[i]]->getRestLength(), target_length[i]);
        }
        bool all_reached_target = true;
        for(int i = 0; i < num_target_actuators; i++){
          m_controllers[target_actuator[i]]->control(dt,target_length[i]);
          actuators[target_actuator[i]]->moveMotors(dt);
          if(actuators[target_actuator[i]]->getRestLength()!=target_length[i])
            all_reached_target = false;
        }

        if(!all_reached_target)
          toggle = 2;

      }

        double CMS[3] = {0,0,0};
        // for(int i = 0; i < rods.size(); i++){
        CMS[0] += rods[4]->centerOfMass().getX();
        CMS[1] += rods[4]->centerOfMass().getY();
        CMS[2] += rods[4]->centerOfMass().getZ();

        CMS[0] /= (double) rods.size();
        CMS[1] /= (double) rods.size();
        CMS[2] /= (double) rods.size();

        std::cout<<rods[4]->orientation()[0]<<":"<<rods[4]->orientation()[1]<<":"<<rods[4]->orientation()[2]<<":"<<rods[4]->orientation()[3]<<std::endl;
        
        // Convert the orientation from the quaternion to the rotation matrix

        // Get the end-effector from transforming the vector from the center of mass
        //    to the end point (this vector is in terms of orientation of the center of mass
        //    coordinate system. So, we will just multiply the transformation matrix with this
        //    vector as the vecotr is known as the length is know between the two end-points
        //    then we will get the end-effector point.


        // Actions will be distributed in the python script, the observation will only be the coordinate of the end-effector
        //    that's for Q-learning

        JSON_Structure::setController(0,14);
        JSON_Structure::setCenterOfMass(CMS[0],CMS[1],CMS[2]);
        printf("%lf %lf %lf \n", CMS[0],CMS[1], CMS[2]);
        std::string json_string = JSON_Structure::jsonToString();
        // std::cout<<"String to be sent"<<json_string<<std::endl;

        LengthController::tcp_com->write_TCP((void*) json_string.c_str());
        char buffer[500];
        bzero(&buffer,500);
        LengthController::tcp_com->read_TCP(buffer,500);
        // printf("Recieved: %s \n",buffer);
        // std::cout<<JSON_Structure::stringToJson(buffer)["Controllers"][0]<<std::endl;

    }
  }

}


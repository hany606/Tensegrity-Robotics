/**
 * @file LengthController.h
 * @brief Implementation of class LengthController
 * @author Hany Hamed
 * This was built over one of the source codes of NTRTsim codes
 */

// This module
#include "LengthController.h"
#include "nlohmann/json.hpp"

#include <core/tgSpringCableActuator.h>




// The C++ Standard Library
#include <cassert>
#include <stdexcept>
#include <time.h>
#include <iostream>
#include <fstream>
#include <string>
#include <math.h>


// #define HOST_NAME "localhost"
// #define PORT_NUM 10042
#define MAX_BUFF_SIZE 5000
#define EPS 0.00001  
#define SMALL_EPS(eps) EPS/1000.0

using namespace std;
using json = nlohmann::json;

json read;
bool all_reached_target = true;
// double last_all_reached_time = 0;   // This is used to indicate if there is a stuck or not in the length of the cable
vector <double> last_error;  //actuators.size()



// It has been extracted by some nodes that connect betwee nthe controllers of the cabels
//    and some nodes has been swaped inplace in order to get all the nodes in the first index of the 
//    anchor list to uniform and ease the access to the data 
int end_points_map[]={0,1,2,3,0,4};

LengthController::LengthController(const char* host, const long long port): host_name(host), port_num(port){

}

LengthController::~LengthController()
{
}	

void LengthController::onSetup(JumperModel& subject)
{
  // freopen("records_testing/record.txt","w",stdout); //For debugging
  LengthController::tcp_com = new TCP(host_name, port_num);
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
    last_error.push_back(0);
  }

}

//This function is being activated each step
void LengthController::onStep(JumperModel& subject, double dt)
{

  if (dt <= 0.0) {
    throw std::invalid_argument("dt is not positive");
  }
  else {
    globalTime += dt;
    if(globalTime > 0){ //delay start of cable actuation
      if(toggle==0){    //print once when motors start moving
        cout << endl << "Activating Cable Motors -------------------------------------" << endl;
        std::cout<<"End Point"<<0<<"\nPoint:"<<actuators[0]->getAnchors_mod()[1]->getWorldPosition()<<"\n----------------------\n";
        for(int i = 1; i < 6; i++){
            btVector3 end_point = actuators[end_points_map[i]]->getAnchors_mod()[0]->getWorldPosition();
            std::cout<<"End Point"<<i<<"\nPoint:"<<end_point<<"\n----------------------\n";
        }
        // std::cout<<"CMS: "<<rods[0]->centerOfMass()<<"\tPoint1:"<<actuators[3]->getAnchors_mod()[0]->getWorldPosition()<<"or:"<<actuators[3]->getAnchors_mod()[1]->getWorldPosition()<<"\tPoint2:"<<actuators[0]->getAnchors_mod()[0]->getWorldPosition()<<"or:"<<actuators[0]->getAnchors_mod()[1]->getWorldPosition()<<"\n";
        // std::cout<<rods[1]->length()<<"\n";
        toggle = 1;   //is used like a state flag ---- set it to 2 to disable the movement
      }
      // Debugging mode
      if(toggle == 2){
        //actuators[0] between point 1,6
        //actuators[3] between point 0,4
        //rod[0] between point 0,1
        // std::cout<<"CMS: "<<rods[0]->centerOfMass()<<"\nPoint1:"<<actuators[3]->getAnchors_mod()[0]->getWorldPosition()<<"\nPoint2:"<<actuators[0]->getAnchors_mod()[0]->getWorldPosition()<<"\n";
        // std::cout<<rods[1]->length()<<"\n";
        // std::cout<<rods[1]->getPRigidBody()<<"\n";
      }
      /**
       * Observations:
       *    1 - Cables' lengths
       *    2 - Center of Mass for rods
       *    3 - Time
       * */
      
      else if(toggle == 1){

        // Part 1: Read the upcoming orders from the python module
        if(all_reached_target == true){
          char buffer[MAX_BUFF_SIZE];
          bzero(&buffer,MAX_BUFF_SIZE);
          LengthController::tcp_com->read_TCP(buffer,MAX_BUFF_SIZE);
          read = JSON_Structure::stringToJson(buffer);
        }

        //set new targets
        if(all_reached_target == true){
          all_reached_target = false;
          for(int i = 0; i < actuators.size(); i++){
            target_lengths[i] = actuators[i]->getRestLength() + (double)read["Controllers_val"][i];
          }
        }

        int counter = 0;
        int reached_counter = 0;
        for(int i = 0; i < actuators.size(); i++){
          if(((double) read["Controllers_val"][i]) == 0)
            continue;
          
          counter++;
          double error_sign = actuators[i]->getRestLength() - target_lengths[i];
          double error = fabs(error_sign);
          // if(error == last_error[i]){
          double stuck_err = last_error[i] - error;
          // that the error is equal to the last_error and the last_error was greater than the current error and the error was decreasing and the target length is smaller than the current which means that it is going to decrease more
          if( (actuators[i]->getRestLength() == 0.1  && target_lengths[i] <= actuators[i]->getRestLength()) ||(fabs(stuck_err) < SMALL_EPS(EPS) && stuck_err > 0 && error_sign > 0 )){ //changed
            // while (1);
            printf("!!!!Stuck: %d\n",i);
            // all_reached_target = true;  //TODO: This is wrong, it should just flag the controller reach flag not all
            reached_counter++;
            printf("Controller#%d\tError: %lf\n", i, error);
            std::cout<<"Current Length: "<<actuators[i]->getCurrentLength()<<"\tRest Length: "<<actuators[i]->getRestLength()<<"\tTarget: "<<target_lengths[i]<<std::endl;
            continue;
          }
          printf("Controller#%d\tError: %lf\n", i, error);
          std::cout<<"Current Length: "<<actuators[i]->getCurrentLength()<<"\tRest Length: "<<actuators[i]->getRestLength()<<"\tTarget: "<<target_lengths[i]<<std::endl;

          // m_controllers[i]->control(dt,((double) read["Controllers_val"][i]));
          m_controllers[i]->control(dt, target_lengths[i]);
          actuators[i]->moveMotors(dt);
          // printf("%d\n", actuators.size());
          // printf("#%d -> %lf\n, -> %lf", i, (double) read["Controllers_val"][i], 5);
          // printf("ERR:%lf\n",abs(actuators[i]->getCurrentLength()- (double)read["Controllers_val"][i]));
          if(error <= EPS){
            // all_reached_target = true;
            reached_counter++;
            read["Controllers_val"][i] = 0;
            printf("Reached%d\n", i);
          }
          last_error[i] = error;
        }

        if(reached_counter == counter)
          all_reached_target = true;
        if(counter == 0)
          all_reached_target = true;


        if(all_reached_target == true){
          printf("\n--------------------------------------------------------\n");
          // (1) Get the end-points
          JSON_Structure::setEndPoints(0,actuators[0]->getAnchors_mod()[1]->getWorldPosition());
          for(int i = 1; i < 6; i++){
            btVector3 end_point = actuators[end_points_map[i]]->getAnchors_mod()[0]->getWorldPosition();
            JSON_Structure::setEndPoints(i,end_point);
            // std::cout<<"End Point"<<i<<"\nPoint:"<<end_point<<"\n----------------------\n";
          }

          // (2) Get the length of targeting cables
          for(int i = 0; i < actuators.size(); i++){
            JSON_Structure::setController(i, (int) (actuators[i]->getRestLength()*10000) /10000.0);
          }

          // (3) Get the reached flag
          JSON_Structure::setFlags(0, (int) all_reached_target);

          // (4) Set the time stamp
          JSON_Structure::setTime(((int)(globalTime*1000)) /1000.0);

          std::string json_string = JSON_Structure::jsonToString();
          // std::cout<<"String to be sent"<<json_string<<std::endl;
          LengthController::tcp_com->write_TCP((void*) json_string.c_str());
        }
      }
    }
  }

}


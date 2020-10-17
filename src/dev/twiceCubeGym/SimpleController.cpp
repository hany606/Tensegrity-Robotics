/**
 * @file SimpleController.h
 * @brief Implementation of class SimpleController
 * @author Hany Hamed
 * This was built over one of the source codes of NTRTsim codes
 */

// This module
#include "SimpleController.h"
#include <core/tgSpringCableActuator.h>


// The C++ Standard Library
#include <cassert>
#include <stdexcept>
#include <time.h>
#include <iostream>
#include <fstream>
#include <string>
#include <math.h>
#include <algorithm>

#define MAX_BUFF_SIZE 5000
#define MAX_LENGTH_PERCENT 5

using namespace std;
using json = nlohmann::json;


json read_json;
vector <btVector3> last_positions;


int nodes_num = 24;
int endpoints_mapping [24][2] = {{0, 0}, {1, 0}, {2, 0}, {3, 0}, {4, 0}, {5, 0}, {6, 0}, {7, 0}, {0, 1}, {1, 1}, {2, 1}, {3, 1}, {4, 1}, {5, 1}, {6, 1}, {7, 1}, {16, 1}, {17, 1}, {18, 1}, {19, 1}, {20, 1}, {21, 1}, {22, 1}, {23, 1}};
int active_actuators_num = 8;
int active_actuators [8] = {0, 1, 2, 3, 4, 5, 6, 7};

// control_type: 0 for rest_Simple control and 1 for current_Simple control
SimpleController::SimpleController(const char* host, const long long port): host_name(host), port_num(port){

}

SimpleController::~SimpleController()
{
}	

void SimpleController::onSetup(TwiceCubeGymModel& subject)
{

  std::cout<<"\nStarting communication through TCP: "<<host_name<<port_num<<"\n";//DEBUG
  SimpleController::tcp_com = new TCP(host_name, port_num);
  SimpleController::tcp_com->setup();
  std::cout<<"Finished Setup the communication\n";//DEBUG

  JsonStructure::setup();
  m_controllers.clear(); //clear vector of controllers
  max_lengths.clear(); //vector of randomized restlengths

    
  //get all of the tensegrity structure's cables
  actuators = subject.getAllActuators();
  rods = subject.getAllRods();

  printf("Number of actuators: %d , Number of Rods: %d\n", (int) actuators.size(), (int) rods.size());//DEBUG
  // std::cout<<rods[1]->getTags()[0][1]<<"\n";

  //Attach a tgBasicController to each actuator
  for (size_t i = 0; i < actuators.size(); ++i)
  {
    tgBasicActuator * const pActuator = actuators[i];
    assert(pActuator != NULL);  //precondition
    //instantiate controllers for each cable
    tgBasicController* m_lenController = new tgBasicController(pActuator);
    //add controller to vector
    m_controllers.push_back(m_lenController);
  }

  for(int i = 0; i < active_actuators_num; i++){
    double start_length = actuators[active_actuators[i]]->getRestLength();
    max_lengths.push_back(MAX_LENGTH_PERCENT*start_length);
    target_lengths.push_back(0);
    printf("Actutor of string #%d -> start Lenght: %lf\n", (int) active_actuators[i], start_length);//DEBUG
  }

  for(int i = 0; i < nodes_num; i++){
    if(endpoints_mapping[i][0] < 0){
      std::cout<<"Cannot find node with index: "<<i<<"\n";
      continue;
    }

    btVector3 node = actuators[endpoints_mapping[i][0]]->getAnchors_mod()[endpoints_mapping[i][1]]->getWorldPosition();
    last_positions.push_back(node);
  }

}

//This function is being activated each step
void SimpleController::onStep(TwiceCubeGymModel& subject, double dt)
{

  if (dt <= 0.0) {
    throw std::invalid_argument("dt is not positive");
  }
  else {
    globalTime += dt;
    if(globalTime > 0){ //delay start of cable actuation
      if(toggle==0){    //print once when motors start moving        
        std::cout<<"Nodes:\n";
        for(int i = 0; i < nodes_num; i++){
          if(endpoints_mapping[i][0] < 0){
            std::cout<<"Cannot find node with index: "<<i<<"\n";
            continue;
          }

          btVector3 node = actuators[endpoints_mapping[i][0]]->getAnchors_mod()[endpoints_mapping[i][1]]->getWorldPosition();
          
          std::cout<<"Node "<<i<<":"<< node<<"\n";
        }

        // std::cout<<"End Points:\n";
        // for(int i = 0; i < actuators.size(); i++){
        //     btVector3 end_point1 = actuators[i]->getAnchors_mod()[0]->getWorldPosition();
        //     btVector3 end_point2 = actuators[i]->getAnchors_mod()[1]->getWorldPosition();
            
        //     std::cout<<"Cable"<<i<<"-anchor-1: "<<end_point1<<"\n";
        //     std::cout<<"Cable"<<i<<"-anchor-2: "<<end_point2<<"\n";
                   
        // }
        SimpleController::CoM = btVector3(0.0, 0.0, 0.0);
        for(int i = 0; i <rods.size(); i++){
          SimpleController::CoM += rods[i]->centerOfMass();
        }
        SimpleController::CoM /= double(rods.size());
        std::cout<<"CoM: "<<SimpleController::CoM;
        std::cout << endl << "--------------------------------------------------------------------------" << endl;
        toggle = 1;
      }
      if(toggle == 1){
        // Part 1: Read the upcoming orders from the python module
        char buffer[MAX_BUFF_SIZE];
        bzero(&buffer,MAX_BUFF_SIZE);
        SimpleController::tcp_com->read_TCP(buffer,MAX_BUFF_SIZE);
        read_json = JsonStructure::stringToJson(buffer);

        // Control the cables part
        controlRestLength(read_json, dt);

        // (1) Get the end-points
        for(int i = 0; i < nodes_num; i++){
          if(endpoints_mapping[i][0] < 0)
            continue;

          btVector3 node = actuators[endpoints_mapping[i][0]]->getAnchors_mod()[endpoints_mapping[i][1]]->getWorldPosition();
          // relative to the inital CoM
          btVector3 node_relative = node - SimpleController::CoM;
          // JsonStructure::setNode(i,node);
          JsonStructure::setNode(i,node_relative);

          // Calculate the velocities of the end points (nodes of the rods)
          btVector3 node_velocity = (node - last_positions[i])/dt;
          JsonStructure::setNodeVelocity(i, node_velocity);
          last_positions[i] = node;
        }


        // (2) Get the length of targeting cables
        for(int i = 0; i < actuators.size(); i++){
          JsonStructure::setRestCableLength(i, (int) (actuators[i]->getRestLength()*10000) /10000.0);
          JsonStructure::setCurrentCableLength(i, (int) (actuators[i]->getCurrentLength()*10000) /10000.0);
        }

        // (4) Set the time stamp
        JsonStructure::setTime(((int)(globalTime*1000)) /1000.0);

        std::string json_string = JsonStructure::jsonToString();
        SimpleController::tcp_com->write_TCP((void*) json_string.c_str());
        
      }

    }
  }

}

void SimpleController::calcTargetLengths(json read_json){
  for(int j = 0; j < active_actuators_num; j++){
    int i = active_actuators[j];
    // Discrete action space and for cotinous delta lengths
    target_lengths[i] = actuators[i]->getRestLength() + (double)read_json["controllers_val"][i];
    if (target_lengths[i] < 0.0) {
      target_lengths[i] = 0.0;
    }
    // Only this clamping while controlling the rest_lengths
    if (target_lengths[i] > max_lengths[i]){
      target_lengths[i] = max_lengths[i];
      printf("Reached the limit\n");
    }

    // Continuous action space for lengths
    // target_lengths[i] = (double)read_json["Controllers_val"][i];

  }
}

void SimpleController::controlRestLength(json read_json, double dt){
  //set new targets
  SimpleController::calcTargetLengths(read_json);

  for(int j = 0; j < active_actuators_num; j++){
    int i = active_actuators[j];
    if(((double) read_json["controllers_val"][i]) == 0)
      continue;

    std::cout<<"Current Length:"<<i<<": "<<actuators[i]->getCurrentLength()<<"\tRest Length: "<<actuators[i]->getRestLength()<<"\tTarget: "<<target_lengths[i]<<std::endl;

    // m_controllers[i]->control(dt,((double) read_json["Controllers_val"][i]));
    m_controllers[i]->control(dt, target_lengths[i]);
    actuators[i]->moveMotors(dt);
    // printf("%d\n", actuators.size());
    // printf("#%d -> %lf\n, -> %lf", i, (double) read_json["Controllers_val"][i], 5);
    // printf("ERR:%lf\n",abs(actuators[i]->getCurrentLength()- (double)read_json["Controllers_val"][i]));
  }
  std::cout<<"-------------------------------------\n";

}
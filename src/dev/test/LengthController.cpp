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

#define HOST_NAME "localhost"
#define PORT_NUM 10023

// ROS libraries

// #include "ros/ros.h"
// #include "jsoncpp/json/json.h"



// using namespace std;

LengthController::LengthController(const double length) :
  m_length(length)
{ 
  LengthController::rosBridge = new ROS_Bridge();
  if (length < 0.0)
    {
      throw std::invalid_argument("Negative length");
    }
}

LengthController::~LengthController()
{
}	

void LengthController::onSetup(sixBarsModel& subject)
{
  LengthController::tcp_com = new TCP(HOST_NAME, PORT_NUM);

  LengthController::tcp_com->setup();
  JSON_Structure::setup();
  m_controllers.clear(); //clear vector of controllers
  start_lengths.clear(); //vector of randomized restlengths
  
  //get all of the tensegrity structure's cables
  actuators = subject.getAllActuators();

  //Attach a tgBasicController to each actuator
  for (size_t i = 0; i < actuators.size(); ++i)
    {
      tgBasicActuator * const pActuator = actuators[i];
      assert(pActuator != NULL);
      //instantiate controllers for each cable
      tgBasicController* m_lenController = new tgBasicController(pActuator, m_length);
      //add controller to vector
      m_controllers.push_back(m_lenController);
      //generate random end restlength
      double start_length = actuators[i]->getStartLength();
      printf("Start Lenght %d: %lf\n", (int) i,  start_length);
      start_lengths.push_back(start_length);
      rosBridge->setController(i,start_length);
    }

}

//This function is being activated each step
void LengthController::onStep(sixBarsModel& subject, double dt)
{

  if (dt <= 0.0) {
    throw std::invalid_argument("dt is not positive");
  }
  else {
    globalTime += dt;
    if(globalTime > 2){ //delay start of cable actuation
      if(toggle==0){    //print once when motors start moving
        std::cout << std::endl << "Activating Cable Motors (Randomized Lengths) -------------------------------------" << std::endl;
	      toggle = 1;   //is used like a state flag
      }
      if(toggle==1){
        // subject.getCentroid();
        toggle = 2;
        m_controllers[0]->control(dt,9);
        actuators[0]->moveMotors(dt);
        rosBridge->setController(0,9);

        // std::cout<<"Shrink\n";
        //This to confirm that it had been changed
        if(actuators[0]->getRestLength()!=9)
          toggle = 1;
      }
      if(toggle==2){
        toggle = 1;
        // subject.getCentroid();
        // std::cout<<subject.getTgStrucutre().getCentroid()<<"\n";
        double CMS[3] = {0,0,0};
        for(int i = 0; i < subject.getAllRods().size(); i++){
          CMS[0] += subject.getAllRods()[i]->centerOfMass().getX();
          CMS[1] += subject.getAllRods()[i]->centerOfMass().getY();
          CMS[2] += subject.getAllRods()[i]->centerOfMass().getZ();
        }
        CMS[0] /= (double) subject.getAllRods().size();
        CMS[1] /= (double) subject.getAllRods().size();
        CMS[2] /= (double) subject.getAllRods().size();
        // std::cout<<subject.getTgStrucutre().getNodes()[0].getX()<<"\n";
        // std::cout<<subject.getAllRods()[0]->centerOfMass()<<"\n";
        // subject.getTgStrucutre();
        // subject.m_
        m_controllers[0]->control(dt,14);
        actuators[0]->moveMotors(dt);
        rosBridge->setController(0,14);
        JSON_Structure::setController(0,14);
        JSON_Structure::setCenterOfMass(CMS[0],CMS[1],CMS[2]);
        printf("STrING: %s\n",JSON_Structure::jsonToString());
        LengthController::tcp_com->write_TCP((void*) JSON_Structure::jsonToString());
        char buffer[500];
        bzero(&buffer,500);
        LengthController::tcp_com->read_TCP(buffer,500);
        // printf("Recieved: %s \n",buffer);
        std::cout<<JSON_Structure::stringToJson(buffer)["Controllers"][0]<<std::endl;
        // std::cout<<"Increase\n";
        //This to confirm that it had been changed
        if(actuators[0]->getRestLength()!= 14)
          toggle = 2;
      }
    }
  }

}



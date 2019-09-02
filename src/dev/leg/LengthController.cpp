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

void LengthController::onSetup(legModel& subject)
{

  m_controllers.clear(); //clear vector of controllers
  rand_lengths.clear(); //vector of randomized restlengths
  start_lengths.clear(); //vector of randomized restlengths
  
  //set seeds
  srand(time(NULL));
  srand48(time(NULL));
  
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
      printf("Start Lenght: %lf", start_length);
      start_lengths.push_back(start_length);
      //Randomization new lenghts process
      double rand_max = start_length*0.25; //maximum pos. deviation from start length
      double rand_min = -start_length*0.35; //maximum neg. deviation from start length
      double gen_len = drand48()*(rand_max-rand_min) + rand_min + start_length;
      
      printf("randLength : %d - %lf\n", i, gen_len);

      rand_lengths.push_back(gen_len);  //This have the lengths of the strings in its compact way.
    }
}

//This function is being activated each step
void LengthController::onStep(legModel& subject, double dt)
{

  if (dt <= 0.0) {
    throw std::invalid_argument("dt is not positive");
  }
  else {
    globalTime += dt;
    if(globalTime > 2){ //delay start of cable actuation
      if(toggle==0){    //print once when motors start moving
        cout << endl << "Activating Cable Motors (Randomized Lengths) -------------------------------------" << endl;
	      toggle = 1;   //is used like a state flag
      }
      if(toggle==1){
        toggle = 2;
        m_controllers[0]->control(dt,12);
        actuators[0]->moveMotors(dt);

        //This to confirm that it had been changed
        if(actuators[0]->getRestLength()!=12)
          toggle = 1;
        /*
        for(int i = 0; i<actuators.size(); i++){
          m_controllers[i]->control(dt,rand_lengths[i]);
          actuators[i]->moveMotors(dt);

          //This to confirm that it had been changed
          if(actuators[i]->getRestLength()!=rand_lengths[i])
            toggle = 1;
        }	
        */
      }
      if(toggle==2){
        toggle = 1;
        m_controllers[0]->control(dt,10);
        actuators[0]->moveMotors(dt);

        //This to confirm that it had been changed
        if(actuators[0]->getRestLength()!=10)
          toggle = 2;
        /*
        for(int i = 0; i<actuators.size(); i++){
          m_controllers[i]->control(dt,start_lengths[i]);
          actuators[i]->moveMotors(dt);
          //This to confirm that it had been changed
          if(actuators[i]->getRestLength()!=start_lengths[i])
            toggle = 2;
        }
        */
      }
    }
  }

}


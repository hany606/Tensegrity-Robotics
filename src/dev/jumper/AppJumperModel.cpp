/*
 * Copyright © 2012, United States Government, as represented by the
 * Administrator of the National Aeronautics and Space Administration.
 * All rights reserved.
 * 
 * The NASA Tensegrity Robotics Toolkit (NTRT) v1 platform is licensed
 * under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0.
 * 
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
 * either express or implied. See the License for the specific language
 * governing permissions and limitations under the License.
*/

/**
 * @file AppJumperModel.cpp
 * @brief Contains the definition function main() for the Three strut
 * tensegrity Jumper example application
 * @author Brian Tietz
 * $Id$
 */

// This application
#include "JumperModel.h"
#include "LengthController.h"
// This library
#include "core/terrain/tgBoxGround.h"
#include "core/tgModel.h"
#include "core/tgSimViewGraphics.h"
#include "core/tgSimulation.h"
#include "core/tgWorld.h"
// Bullet Physics
#include "LinearMath/btVector3.h"
// The C++ Standard Library
#include <iostream>
#include <string>

/**
 * The entry point.
 * @param[in] argc the number of command-line arguments
 * @param[in] argv argv[0] is the executable name
 * @return 0
 */
int main(int argc, char** argv)
{
    std::cout << "AppJumperModel" << std::endl;

    // First create the ground and world. Specify ground rotation in radians
    const double yaw = 0.0;
    const double pitch = 0.0;
    const double roll = 0.0;
    const tgBoxGround::Config groundConfig(btVector3(yaw, pitch, roll));
    // the world will delete this
    tgBoxGround* ground = new tgBoxGround(groundConfig);
    
    const tgWorld::Config config(981); // gravity, cm/sec^2
    tgWorld world(config, ground);

    // Second create the view
    const double timestep_physics = 0.001; // seconds
    const double timestep_graphics = 1.f/60.f; // seconds
    tgSimViewGraphics view(world, timestep_physics, timestep_graphics, "Tensegrity Jumping Robot");

    // Third create the simulation
    tgSimulation simulation(view);

    // Fourth create the models with their controllers and add the models to the
    // simulation
    const int z = std::stoi(argv[4]);

    btVector3 starting_coordinates (std::stoi(argv[4]),std::stoi(argv[5]),std::stoi(argv[6]));
    double starting_angle = std::stod(argv[7]);
    JumperModel* const myModel = new JumperModel(starting_coordinates,starting_angle);

    const char* host_name = argv[1];
    const long long  port_num = std::stoll(argv[2]);
    const int control_type = std::stoi(argv[3]);
    printf("host_name: %s\t port_num: %s\t control_type: %s\n starting_coordinates: %s\t starting_angle: %s\n", argv[1], argv[2], argv[3], argv[4], argv[5]);
    LengthController* const myController = new LengthController(host_name, port_num, control_type);
    myModel->attach(myController);


    // Add the model to the world
    simulation.addModel(myModel);
    
    simulation.run();

    //Teardown is handled by delete, so that should be automatic
    return 0;
}

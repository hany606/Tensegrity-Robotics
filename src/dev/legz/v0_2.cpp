//Before the rotating
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
 * @file legzModel.cpp
 * @brief Contains the definition of the members of the class legzModel.
 * $Id$
 */

// This module
#include "legzModel.h"
// This library
#include "core/tgBasicActuator.h"
#include "core/tgRod.h"
#include "tgcreator/tgBuildSpec.h"
#include "tgcreator/tgBasicActuatorInfo.h"
#include "tgcreator/tgRodInfo.h"
#include "tgcreator/tgStructure.h"
#include "tgcreator/tgStructureInfo.h"
// The Bullet Physics library
#include "LinearMath/btVector3.h"
// The C++ Standard Library
#include <stdexcept>

/**
 * Anonomous namespace so we don't have to declare the config in
 * the header.
 */
namespace
{
    /**
     * Configuration parameters so they're easily accessable.
     * All parameters must be positive.
     */
    const struct Config
    {
        double density;
        double radius;
        double stiffness;
        double damping;
        double pretension;
        double legz_length;
        bool hist;
        double maxTension;

    } c =
   {
    //    0.2,     // density (mass / length^3)
    //    0.20,     // radius (length)
    //    1000.0,   // stiffness (mass / sec^2)
    //    20.0,     // damping (mass / sec)
    //    12000.0,     // pretension (mass * length / sec^2)
    //    20.0,     // legz_height (length)

       0.2,     // density (mass / length^3)
       0.20,     // radius (length)
       1000.0,   // stiffness (mass / sec^2)
       20.0,     // damping (mass / sec)
       5000.0,     // pretension (mass * length / sec^2)
       20.0,        //length of bar
       0,           // history logging (boolean)
       30000,       // max tension

    // 0.2,     // density (mass / length^3)
    // 0.31,     // radius (length)
    // 1,   // stiffness (mass / sec^2)
    // 1,     // damping (mass / sec)
    // 20,     // pretension (mass * length / sec^2)
    // 1,     // legz_height (length)
  };
} // namespace

legzModel::legzModel() :
tgModel() 
{
}

legzModel::~legzModel()
{
}

void legzModel::addNodes(tgStructure& s, double length)
{
    // // bottom right
    // s.addNode(-edge / 2.0, 0, 0); // 1
    // // bottom left
    // s.addNode( edge / 2.0, 0, 0); // 2
    // // bottom front
    // s.addNode(0, 0, width); // 3
    // // top right
    // s.addNode(-edge / 2.0, height, 0); // 4
    // // top left
    // s.addNode( edge / 2.0, height, 0); // 5
    // // top front
    // s.addNode(0, height, width); // 6

    //First parameter is the distance between them, second is the end points
    s.addNode(length/5.0, 1*length/2.0, 0);
    s.addNode(length/5.0, -1*length/2.0, 0);
    //2 = 1 but up same z,y 
    s.addNode(-length/5.0, 1*length/2.0, 0);
    s.addNode(-length/5.0, -1*length/2.0,  0);

    //3 parallel to z-axis  in the middle of 1 & 2
    //for the x I am not sure 1.5
    //last paramter is controlling the length of the bar
    s.addNode(0, length/5.0, length*1.0);
    s.addNode(0, length/5.0, -length*1.3);
    //4 = 3 but right same y,z
    s.addNode(0, -length/5.0, length*1.0);
    s.addNode(0, -length/5.0, -length*1.3);
    
    //5 parallel to y 8,3
    //1st parameter is the end points, 3rd parameter is the distance between the center of the robot
    s.addNode(-length/2.0, 0, 3*length/5.0);
    // s.addNode(-length*1.0, 0, length/4.0);
    s.addNode(length*1.0, 0, 3*length/5.0);
    //6 = 5 but backward and smaller 8,1
    s.addNode(-length/3.0, 0, -length/8.0);
    s.addNode(length/3.0, 0, -length/8.0);
    //7 = 6 but more backward 11/8,1
    s.addNode(-length/3.0, 0, -7*length/8.0);
    s.addNode(length/3.0, 0, -7*length/8.0);

    //First parameter is the distance between them, second is the end points, last one is the distance from the center of the robot
    //8 = 1 but backward 
    s.addNode(length/5.0, 1*length/2.0, -6*length/8.0);
    s.addNode(length/5.0, -1*length/2.0, -6*length/8.0);

    s.addNode(-length/5.0, 1*length/2.0, -6*length/8.0);
    s.addNode(-length/5.0, -1*length/2.0, -6*length/8.0);

}

void legzModel::addRods(tgStructure& s)
{
    for(int i = 0; i < 18;){
        s.addPair( i++,  i++, "rod");
    }

}

void legzModel::addMuscles(tgStructure& s)
{
    // // Bottom Triangle
    // s.addPair(0, 1,  "muscle");
    // s.addPair(1, 2,  "muscle");
    // s.addPair(2, 0,  "muscle");
    
    // // Top
    // s.addPair(3, 4, "muscle");
    // s.addPair(4, 5,  "muscle");
    // s.addPair(5, 3,  "muscle");

    // //Edges
    // s.addPair(0, 3, "muscle");
    // s.addPair(1, 4,  "muscle");
    // s.addPair(2, 5,  "muscle");

    // s.addPair(0, 9,  "muscle");
    // // s.addPair(0, 5,  "muscle"); //#NO
    // s.addPair(0, 4,  "muscle");
    // s.addPair(0, 11,  "muscle");
    // s.addPair(1, 9,  "muscle");
    // s.addPair(1, 6,  "muscle");

    // s.addPair(1, 11,  "muscle");

    
    // s.addPair(4, 9,  "muscle");
    // s.addPair(6, 9,  "muscle");

    // // s.addPair(1, 7,  "muscle"); //#NO
    // s.addPair(11, 7,  "muscle");
    // s.addPair(11, 5,  "muscle");

    // s.addPair(6, 3,  "muscle"); //#
    // s.addPair(4, 3,  "muscle"); //#

    // // s.addPair(7, 3,  "muscle"); //#NO
    // // s.addPair(5, 3,  "muscle"); //#NO

    // s.addPair(8, 6,  "muscle");
    // s.addPair(8, 4,  "muscle");
    // s.addPair(8, 2,  "muscle");
    // s.addPair(8, 3,  "muscle");

    // s.addPair(10, 2,  "muscle");
    // s.addPair(10, 3,  "muscle");

    // s.addPair(10, 5,  "muscle");
    // s.addPair(10, 7,  "muscle");

    // s.addPair(13, 5,  "muscle");
    // s.addPair(13, 7,  "muscle");
    // s.addPair(12, 5,  "muscle");
    // s.addPair(12, 7,  "muscle");
    // s.addPair(13, 15,  "muscle");
    // s.addPair(13, 14,  "muscle");
    // s.addPair(12, 17,  "muscle");
    // s.addPair(12, 16,  "muscle");

    // s.addPair(11, 14,  "muscle");
    // s.addPair(11, 15,  "muscle");
    // s.addPair(11, 17,  "muscle"); //#
    // s.addPair(11, 16,  "muscle"); //#
    // s.addPair(10, 16,  "muscle");
    // s.addPair(10, 17,  "muscle");


    // s.addPair(10, 15,  "muscle");   //#
    // s.addPair(10, 14,  "muscle");   //#

    // s.addPair(14, 5,  "muscle");
    // s.addPair(15, 7,  "muscle");
    // s.addPair(16, 5,  "muscle");
    // s.addPair(17, 7,  "muscle");

    s.addPair(1, 6,  "muscle");
    s.addPair(1, 11,  "muscle");
    s.addPair(1, 9,  "muscle");
    s.addPair(0, 4,  "muscle");
    s.addPair(0, 11,  "muscle");
    s.addPair(0, 9,  "muscle");
    s.addPair(9, 6,  "muscle");
    s.addPair(9, 4,  "muscle");
    s.addPair(11, 7,  "muscle");
    s.addPair(11, 5,  "muscle");
    s.addPair(6, 3,  "muscle");
    s.addPair(6, 8,  "muscle");
    s.addPair(4, 2,  "muscle");
    s.addPair(4, 8,  "muscle");
    s.addPair(7, 10,  "muscle");
    s.addPair(5, 10,  "muscle");
    s.addPair(3, 10,  "muscle");
    s.addPair(3, 8,  "muscle");
    s.addPair(2, 10,  "muscle");
    s.addPair(2, 8,  "muscle");
    s.addPair(13, 7,  "muscle");
    s.addPair(13, 5,  "muscle");
    s.addPair(12, 7,  "muscle");
    s.addPair(12, 5,  "muscle");
    s.addPair(7, 17,  "muscle");
    s.addPair(7, 15,  "muscle");
    s.addPair(5, 16,  "muscle");
    s.addPair(5, 14,  "muscle");
    s.addPair(13, 15,  "muscle");
    s.addPair(13, 14,  "muscle");
    s.addPair(12, 17,  "muscle");
    s.addPair(12, 16,  "muscle");
    s.addPair(10, 15,  "muscle");
    s.addPair(10, 14,  "muscle");
    s.addPair(11, 17,  "muscle");
    s.addPair(11, 16,  "muscle");


    //?
    //?
    //?
    //?

}

void legzModel::setup(tgWorld& world)
{
    // Define the configurations of the rods and strings
    // Note that pretension is defined for this string
    const tgRod::Config rodConfig(c.radius, c.density);
    // const tgSpringCableActuator::Config muscleConfig(c.stiffness, c.damping, c.pretension);
     const tgBasicActuator::Config muscleConfig(c.stiffness, c.damping, c.pretension,
        c.hist, c.maxTension);
    // Create a structure that will hold the details of this model
    tgStructure s;
    
    // Add nodes to the structure
    addNodes(s, c.legz_length);
    
    // Add rods to the structure
    addRods(s);
    
    // Add muscles to the structure
    addMuscles(s);
    
    // Move the structure so it doesn't start in the ground
    s.move(btVector3(0, 10, 0));
    
    // Create the build spec that uses tags to turn the structure into a real model
    tgBuildSpec spec;
    spec.addBuilder("rod", new tgRodInfo(rodConfig));
    spec.addBuilder("muscle", new tgBasicActuatorInfo(muscleConfig));
    
    // Create your structureInfo
    tgStructureInfo structureInfo(s, spec);

    // Use the structureInfo to build ourselves
    structureInfo.buildInto(*this, world);

    // We could now use tgCast::filter or similar to pull out the
    // models (e.g. muscles) that we want to control. 
    allActuators = tgCast::filter<tgModel, tgSpringCableActuator> (getDescendants());
    
    // Notify controllers that setup has finished.
    notifySetup();
    
    // Actually setup the children
    tgModel::setup(world);
}

void legzModel::step(double dt)
{
    // Precondition
    if (dt <= 0.0)
    {
        throw std::invalid_argument("dt is not positive");
    }
    else
    {
        // Notify observers (controllers) of the step so that they can take action
        notifyStep(dt);
        tgModel::step(dt);  // Step any children
    }
}

void legzModel::onVisit(tgModelVisitor& r)
{
    // Example: m_rod->getRigidBody()->dosomething()...
    tgModel::onVisit(r);
}

const std::vector<tgSpringCableActuator*>& legzModel::getAllActuators() const
{
    return allActuators;
}
    
void legzModel::teardown()
{
    notifyTeardown();
    tgModel::teardown();
}

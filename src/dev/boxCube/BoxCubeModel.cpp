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
 * @file BoxCubeModel.cpp
 * @brief Contains the definition of the members of the class BoxCubeModel.
 * $Id$
 */

// This module
#include "BoxCubeModel.h"
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

#define _USE_MATH_DEFINES
#include <math.h>

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
        double box_density;
        double cube_density;
        double box_radius;
        double cube_radius;
        double stiffness;
        double damping;
        double pretension;
        double box_side_lengths[3];
        double cube_side_lengths[3];
        bool hist;
        double maxTension;
        double targetVelocity;

    }c = {

       20.0,     // density (mass / length^3)
       0.2,
       0.20,     // radius (length)
       0.20,
       1000.0,   // stiffness (mass / sec^2)
       30.0,     // damping (mass / sec)
       5000.0,     // pretension (mass * length / sec^2)
       {50.0, 50.0, 50.0},        //length of a side of the box
       {20.0, 20.0, 20.0},        //lenght of a side of the cube 
       0,           // history logging (boolean)
       30000,       // max tension
       30           // target velocity
    };
}

BoxCubeModel::BoxCubeModel() : tgModel()
{

}

BoxCubeModel::~BoxCubeModel()
{
}

void BoxCubeModel::addNodes(tgStructure& s)
{
    // y z x

    double offset = c.box_radius+10;
    // Box
    // The bottom base
    s.addNode(c.box_side_lengths[1]/2.0, offset, c.box_side_lengths[0]/2.0);
    s.addNode(-c.box_side_lengths[1]/2.0, offset, c.box_side_lengths[0]/2.0);
    s.addNode(-c.box_side_lengths[1]/2.0, offset, -c.box_side_lengths[0]/2.0);
    s.addNode(c.box_side_lengths[1]/2.0, offset, -c.box_side_lengths[0]/2.0); 
    
       10.0,     // damping (mass / sec)

    // The top base
    s.addNode(c.box_side_lengths[1]/2.0, c.box_side_lengths[2]+offset, c.box_side_lengths[0]/2.0);
    s.addNode(-c.box_side_lengths[1]/2.0, c.box_side_lengths[2]+offset, c.box_side_lengths[0]/2.0);
    s.addNode(-c.box_side_lengths[1]/2.0, c.box_side_lengths[2]+offset, -c.box_side_lengths[0]/2.0);
    s.addNode(c.box_side_lengths[1]/2.0, c.box_side_lengths[2]+offset, -c.box_side_lengths[0]/2.0); 
    
    // Cube
    double cube_center[] = {0.0, 0.0, (c.box_side_lengths[2]/2.0)+offset, }; //x y z
    
    // s.addNode(cube_center[1], cube_center[2], cube_center[0]);
    
    // The bottom base
    s.addNode(cube_center[1]+c.cube_side_lengths[1]/2.0, cube_center[2]-c.cube_side_lengths[2]/2.0, cube_center[0]+c.cube_side_lengths[0]/2.0);
    s.addNode(cube_center[1]-c.cube_side_lengths[1]/2.0, cube_center[2]-c.cube_side_lengths[2]/2.0, cube_center[0]+c.cube_side_lengths[0]/2.0);
    s.addNode(cube_center[1]-c.cube_side_lengths[1]/2.0, cube_center[2]-c.cube_side_lengths[2]/2.0, cube_center[0]-c.cube_side_lengths[0]/2.0);
    s.addNode(cube_center[1]+c.cube_side_lengths[1]/2.0, cube_center[2]-c.cube_side_lengths[2]/2.0, cube_center[0]-c.cube_side_lengths[0]/2.0); 
    

    // The top base
    s.addNode(cube_center[1]+c.cube_side_lengths[1]/2.0, cube_center[2]+c.cube_side_lengths[2]/2.0, cube_center[0]+c.cube_side_lengths[0]/2.0);
    s.addNode(cube_center[1]-c.cube_side_lengths[1]/2.0, cube_center[2]+c.cube_side_lengths[2]/2.0, cube_center[0]+c.cube_side_lengths[0]/2.0);
    s.addNode(cube_center[1]-c.cube_side_lengths[1]/2.0, cube_center[2]+c.cube_side_lengths[2]/2.0, cube_center[0]-c.cube_side_lengths[0]/2.0);
    s.addNode(cube_center[1]+c.cube_side_lengths[1]/2.0, cube_center[2]+c.cube_side_lengths[2]/2.0, cube_center[0]-c.cube_side_lengths[0]/2.0); 


}


void BoxCubeModel::addRods(tgStructure& s)
{
    // Box
    // Bottom base
    s.addPair(0,1,"box_rod");
    s.addPair(1,2,"box_rod");
    s.addPair(2,3,"box_rod");
    s.addPair(3,0,"box_rod");
    

    // Top base
    s.addPair(4,5,"box_rod");
    s.addPair(5,6,"box_rod");
    s.addPair(6,7,"box_rod");
    s.addPair(7,4,"box_rod");
    
    // Sides
    s.addPair(0,4,"box_rod");
    s.addPair(1,5,"box_rod");
    s.addPair(2,6,"box_rod");
    s.addPair(3,7,"box_rod");
    

    //Cube  +8 indecies
    // Bottom base
    s.addPair(8,9,"cube_rod");
    s.addPair(9,10,"cube_rod");
    s.addPair(10,11,"cube_rod");
    s.addPair(11,8,"cube_rod");
    
    // Top base
    s.addPair(12,13,"cube_rod");
    s.addPair(13,14,"cube_rod");
    s.addPair(14,15,"cube_rod");
    s.addPair(15,12,"cube_rod");
    
    // Sides
    s.addPair(8,12,"cube_rod");
    s.addPair(9,13,"cube_rod");
    s.addPair(10,14,"cube_rod");
    s.addPair(11,15,"cube_rod");
    
    
    
}

void BoxCubeModel::addMuscles(tgStructure& s)
{
    // Cube_i  = Box_i + 8
    // s.addPair(0,8, "muscle");
    // s.addPair(1,9, "muscle");
    // s.addPair(2,10, "muscle");
    // s.addPair(3,11, "muscle");
    // s.addPair(4,12, "muscle");
    // s.addPair(5,13, "muscle");
    // s.addPair(6,14, "muscle");
    // s.addPair(7,15, "muscle");

    for(int i = 0; i <= 7; i++){
        s.addPair(i, i+8, "muscle");
    }

    // For the center of the cube (but not worked as there is no object of sphere)
    // for(int i = 0; i <= 7; i++){
    //     s.addPair(i, 8, "muscle");
    // }

}

void BoxCubeModel::setup(tgWorld& world)
{
    // Define the configurations of the rods and strings
    // Note that pretension is defined for this string
    const tgRod::Config box_rod_config(c.box_radius, c.box_density);
    const tgRod::Config cube_rod_config(c.cube_radius, c.cube_density);

    // const tgRod::Config square_rod_config(c.square_side_radius, c.density*10);

    
    // const tgSpringCableActuator::Config muscleConfig(c.stiffness, c.damping, c.pretension);
    const tgBasicActuator::Config muscleConfig(c.stiffness, c.damping, c.pretension,
        c.hist, c.maxTension, c.targetVelocity);

    
    // Create a structure that will hold the details of this model
    tgStructure s;
    

    //Note!!!: we can add different tension for the strings by adding the rods with different tags
    //  and add another Builder for that tag


    // Add nodes to the structure
    addNodes(s);
    
    // Add rods to the structure
    addRods(s);
    
    // Add muscles to the structure
    addMuscles(s);
    
    // Create the build spec that uses tags to turn the structure into a real model
    tgBuildSpec spec;
    spec.addBuilder("box_rod", new tgRodInfo(box_rod_config));
    spec.addBuilder("cube_rod", new tgRodInfo(cube_rod_config));

    spec.addBuilder("muscle", new tgBasicActuatorInfo(muscleConfig));
    
    // Create your structureInfo
    tgStructureInfo structureInfo(s, spec);

    // Use the structureInfo to build ourselves
    structureInfo.buildInto(*this, world);

    // We could now use tgCast::filter or similar to pull out the
    // models (e.g. muscles) that we want to control. 
    allActuators = tgCast::filter<tgModel, tgBasicActuator> (getDescendants());
    allRods = tgCast::filter<tgModel, tgRod> (getDescendants());

    // Notify controllers that setup has finished.
    notifySetup();
    
    // Actually setup the children
    tgModel::setup(world);
}

void BoxCubeModel::step(double dt)
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

void BoxCubeModel::onVisit(tgModelVisitor& r)
{
    // Example: m_rod->getRigidBody()->dosomething()...
    tgModel::onVisit(r);
}

std::vector<tgBasicActuator*>& BoxCubeModel::getAllActuators()
{
    return allActuators;
}

std::vector<tgRod*>& BoxCubeModel::getAllRods()
{
    return allRods;
}




void BoxCubeModel::teardown()
{
    notifyTeardown();
    tgModel::teardown();
}

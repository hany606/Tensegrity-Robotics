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
 * @file SimpleModel.cpp
 * @brief Contains the definition of the members of the class SimpleModel.
 * $Id$
 */

// This module
#include "SimpleModel.h"
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


// Note: "Box" is meant to be the outer cube, "Cube" is meant to be the innner cube

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
        double box_rod_radius;
		double box_rod_density;
		double cube_rod_radius;
		double cube_rod_density;
		double box_cube_stiffness;
		double box_cube_damping;
		double box_cube_pretension;
		double box_cube_maxTension;
		double box_cube_targetVelocity;
		double cube_cube_stiffness;
		double cube_cube_damping;
		double cube_cube_pretension;
		double cube_cube_maxTension;
		double cube_cube_targetVelocity;
		

    }c = {

        0.2,
		20.0,
		0.2,
		0.4,
		1000.0,
		20.0,
		500.0,
		30000,
		3,
		1000.0,
		20.0,
		100.0,
		30000,
		3,
		
       
    };
}

SimpleModel::SimpleModel() : tgModel()
{

}

SimpleModel::~SimpleModel()
{
}

void SimpleModel::addNodes(tgStructure& s)
{
    // y z x
    s.addNode(25.0, 1.8346, 25.0);
	s.addNode(-25.0, 1.8346, 25.0);
	s.addNode(-25.0, 1.8346, -25.0);
	s.addNode(25.0, 1.8346, -25.0);
	s.addNode(25.0, 51.8346, 25.0);
	s.addNode(-25.0, 51.8346, 25.0);
	s.addNode(-25.0, 51.8346, -25.0);
	s.addNode(25.0, 51.8346, -25.0);
	s.addNode(10.0, 16.834600000000002, 10.0);
	s.addNode(-10.0, 16.834600000000002, 10.0);
	s.addNode(-10.0, 16.834600000000002, -10.0);
	s.addNode(10.0, 16.834600000000002, -10.0);
	s.addNode(10.0, 36.8346, 10.0);
	s.addNode(-10.0, 36.8346, 10.0);
	s.addNode(-10.0, 36.8346, -10.0);
	s.addNode(10.0, 36.8346, -10.0);
	
}


void SimpleModel::addRods(tgStructure& s)
{
    s.addPair(0, 1, "box_rod");
	s.addPair(1, 2, "box_rod");
	s.addPair(2, 3, "box_rod");
	s.addPair(3, 0, "box_rod");
	s.addPair(4, 5, "box_rod");
	s.addPair(5, 6, "box_rod");
	s.addPair(6, 7, "box_rod");
	s.addPair(7, 4, "box_rod");
	s.addPair(0, 4, "box_rod");
	s.addPair(1, 5, "box_rod");
	s.addPair(2, 6, "box_rod");
	s.addPair(3, 7, "box_rod");
	s.addPair(8, 12, "cube_rod");
	s.addPair(9, 13, "cube_rod");
	s.addPair(10, 14, "cube_rod");
	s.addPair(11, 15, "cube_rod");
	
}

void SimpleModel::addMuscles(tgStructure& s)
{
    s.addPair(0, 8, "box_cube_muscle");
	s.addPair(1, 9, "box_cube_muscle");
	s.addPair(2, 10, "box_cube_muscle");
	s.addPair(3, 11, "box_cube_muscle");
	s.addPair(4, 12, "box_cube_muscle");
	s.addPair(5, 13, "box_cube_muscle");
	s.addPair(6, 14, "box_cube_muscle");
	s.addPair(7, 15, "box_cube_muscle");
	s.addPair(8, 9, "cube_cube_muscle");
	s.addPair(9, 10, "cube_cube_muscle");
	s.addPair(10, 11, "cube_cube_muscle");
	s.addPair(11, 8, "cube_cube_muscle");
	s.addPair(12, 13, "cube_cube_muscle");
	s.addPair(13, 14, "cube_cube_muscle");
	s.addPair(14, 15, "cube_cube_muscle");
	s.addPair(15, 12, "cube_cube_muscle");
	    
}

void SimpleModel::setup(tgWorld& world)
{
    // Create the build spec that uses tags to turn the structure into a real model
    tgBuildSpec spec;
    
    // Define the configurations of the rods and strings
    const tgRod::Config box_rod_config(0.2, 20.0);
	spec.addBuilder("box_rod", new tgRodInfo(box_rod_config));
	const tgRod::Config cube_rod_config(0.2, 0.4);
	spec.addBuilder("cube_rod", new tgRodInfo(cube_rod_config));
	const tgBasicActuator::Config box_cube_muscle_config(1000.0, 20.0, 500.0, 0, 30000, 3);
	spec.addBuilder("box_cube_muscle", new tgBasicActuatorInfo(box_cube_muscle_config));
	const tgBasicActuator::Config cube_cube_muscle_config(1000.0, 20.0, 100.0, 0, 30000, 3);
	spec.addBuilder("cube_cube_muscle", new tgBasicActuatorInfo(cube_cube_muscle_config));
	

    
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

void SimpleModel::step(double dt)
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

void SimpleModel::onVisit(tgModelVisitor& r)
{
    // Example: m_rod->getRigidBody()->dosomething()...
    tgModel::onVisit(r);
}

std::vector<tgBasicActuator*>& SimpleModel::getAllActuators()
{
    return allActuators;
}

std::vector<tgRod*>& SimpleModel::getAllRods()
{
    return allRods;
}




void SimpleModel::teardown()
{
    notifyTeardown();
    tgModel::teardown();
}
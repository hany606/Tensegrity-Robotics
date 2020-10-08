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
 * @file TwiceCubeModel.cpp
 * @brief Contains the definition of the members of the class TwiceCubeModel.
 * $Id$
 */

// This module
#include "TwiceCubeModel.h"
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
        double rod_radius;
		double rod_density;
		double rod_payload_radius;
		double rod_payload_density;
		double spring_stiffness;
		double spring_damping;
		double spring_pretension;
		double spring_maxTension;
		double spring_targetVelocity;
		

    }c = {

        0.7,
		0.00036326987547825504,
		1.0,
		0.0001326291192432374,
		1750,
		15.0,
		0.0,
		30000,
		3,
		
       
    };
}

TwiceCubeModel::TwiceCubeModel() : tgModel()
{

}

TwiceCubeModel::~TwiceCubeModel()
{
}

void TwiceCubeModel::addNodes(tgStructure& s)
{
    // y z x
    s.addNode(-47.4, 4.0, -47.4);
	s.addNode(-47.4, 4.0, 47.4);
	s.addNode(47.4, 4.0, -47.4);
	s.addNode(47.4, 4.0, 47.4);
	s.addNode(-47.4, 102.0, -47.4);
	s.addNode(-47.4, 102.0, 47.4);
	s.addNode(47.4, 102.0, -47.4);
	s.addNode(47.4, 102.0, 47.4);
	s.addNode(-15.2, 37.8, -15.2);
	s.addNode(-15.2, 37.8, 15.2);
	s.addNode(15.2, 37.8, -15.2);
	s.addNode(15.2, 37.8, 15.2);
	s.addNode(-15.2, 68.2, -15.2);
	s.addNode(-15.2, 68.2, 15.2);
	s.addNode(15.2, 68.2, -15.2);
	s.addNode(15.2, 68.2, 15.2);
	s.addNode(-1.0, 52.0, -1.0);
	s.addNode(-1.0, 52.0, 1.0);
	s.addNode(1.0, 52.0, -1.0);
	s.addNode(1.0, 52.0, 1.0);
	s.addNode(-1.0, 54.0, -1.0);
	s.addNode(-1.0, 54.0, 1.0);
	s.addNode(1.0, 54.0, -1.0);
	s.addNode(1.0, 54.0, 1.0);
	
}


void TwiceCubeModel::addRods(tgStructure& s)
{
    s.addPair(0, 1, "rod");
	s.addPair(1, 3, "rod");
	s.addPair(3, 2, "rod");
	s.addPair(2, 0, "rod");
	s.addPair(0, 4, "rod");
	s.addPair(1, 5, "rod");
	s.addPair(2, 6, "rod");
	s.addPair(3, 7, "rod");
	s.addPair(4, 5, "rod");
	s.addPair(5, 7, "rod");
	s.addPair(7, 6, "rod");
	s.addPair(6, 4, "rod");
	s.addPair(12-4, 16-4, "rod");
	s.addPair(13-4, 17-4, "rod");
	s.addPair(14-4, 18-4, "rod");
	s.addPair(15-4, 19-4, "rod");
	s.addPair(20-4, 21-4, "rod_payload");
	s.addPair(21-4, 23-4, "rod_payload");
	s.addPair(23-4, 22-4, "rod_payload");
	s.addPair(22-4, 20-4, "rod_payload");
	s.addPair(20-4, 24-4, "rod_payload");
	s.addPair(21-4, 25-4, "rod_payload");
	s.addPair(22-4, 26-4, "rod_payload");
	s.addPair(23-4, 27-4, "rod_payload");
	s.addPair(24-4, 25-4, "rod_payload");
	s.addPair(25-4, 27-4, "rod_payload");
	s.addPair(27-4, 26-4, "rod_payload");
	s.addPair(26-4, 24-4, "rod_payload");
	
}

void TwiceCubeModel::addMuscles(tgStructure& s)
{
    s.addPair(0, 8, "spring_muscle");
	s.addPair(1, 9, "spring_muscle");
	s.addPair(2, 10, "spring_muscle");
	s.addPair(3, 11, "spring_muscle");
	s.addPair(4, 12, "spring_muscle");
	s.addPair(5, 13, "spring_muscle");
	s.addPair(6, 14, "spring_muscle");
	s.addPair(7, 15, "spring_muscle");
	s.addPair(8, 9, "spring_muscle");
	s.addPair(9, 11, "spring_muscle");
	s.addPair(11, 10, "spring_muscle");
	s.addPair(10, 8, "spring_muscle");
	s.addPair(12, 13, "spring_muscle");
	s.addPair(13, 15, "spring_muscle");
	s.addPair(15, 14, "spring_muscle");
	s.addPair(14, 12, "spring_muscle");
	s.addPair(8, 16, "spring_muscle");
	s.addPair(9, 17, "spring_muscle");
	s.addPair(10, 18, "spring_muscle");
	s.addPair(11, 19, "spring_muscle");
	s.addPair(12, 20, "spring_muscle");
	s.addPair(13, 21, "spring_muscle");
	s.addPair(14, 22, "spring_muscle");
	s.addPair(15, 23, "spring_muscle");
	    
}

void TwiceCubeModel::setup(tgWorld& world)
{
    // Create the build spec that uses tags to turn the structure into a real model
    tgBuildSpec spec;
    
    // Define the configurations of the rods and strings
    const tgRod::Config rod_config(c.rod_radius, c.rod_density);
	spec.addBuilder("rod", new tgRodInfo(rod_config));
	const tgRod::Config rod_payload_config(c.rod_payload_radius, c.rod_payload_density);
	spec.addBuilder("rod_payload", new tgRodInfo(rod_payload_config));
	const tgBasicActuator::Config spring_muscle_config(c.spring_stiffness, c.spring_damping, c.spring_pretension, 0, c.spring_maxTension, c.spring_targetVelocity);
	spec.addBuilder("spring_muscle", new tgBasicActuatorInfo(spring_muscle_config));
	

    
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

void TwiceCubeModel::step(double dt)
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

void TwiceCubeModel::onVisit(tgModelVisitor& r)
{
    // Example: m_rod->getRigidBody()->dosomething()...
    tgModel::onVisit(r);
}

std::vector<tgBasicActuator*>& TwiceCubeModel::getAllActuators()
{
    return allActuators;
}

std::vector<tgRod*>& TwiceCubeModel::getAllRods()
{
    return allRods;
}




void TwiceCubeModel::teardown()
{
    notifyTeardown();
    tgModel::teardown();
}
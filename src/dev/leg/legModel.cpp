/**
 * @file legModel.cpp
 * @brief Contains the definition of the members of the class legModel.
 * This file is built over one of the examples from NTRTsim from NASA
 */

// This module
#include "legModel.h"
// This library
#include "core/tgBasicActuator.h"
#include "core/tgString.h"
#include "tgcreator/tgBuildSpec.h"
#include "tgcreator/tgBasicActuatorInfo.h"
#include "tgcreator/tgRodInfo.h"
#include "tgcreator/tgStructure.h"
#include "tgcreator/tgStructureInfo.h"
// The Bullet Physics library
#include "LinearMath/btVector3.h"
// The C++ Standard Library
#include <stdexcept>
#include<stdio.h>

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
        double length;
        bool hist;
        double maxTension;
        double targetVelocity;
    } c =
   {
       0.2,     // density (mass / length^3)
       0.31,     // radius (length)
       1000.0,   // stiffness (mass / sec^2)
       10.0,     // damping (mass / sec)
       500.0,     // pretension (mass * length / sec^2)
       10.0,        //length of bar
       0,           // history logging (boolean)
       10000,       // max tension
       1,         // target actuator velocity
  };
} // namespace

legModel::legModel() :
tgModel() 
{
}

legModel::~legModel()
{
}

void legModel::addNodes(tgStructure& s, double length)
{   

    //Bar 1 Vertical
    s.addNode(-0.5*length,length,length);
    s.addNode(-0.5*length,length,-length);
    //Bar 2 Vertical
    s.addNode(0.5*length,length,length);
    s.addNode(0.5*length,length,-length);

    // Bar 3 Horizontal
    s.addNode(-length,1.5*length,0);
    s.addNode(length,1.5*length,0);
    //Bar 4 Horizontal
    s.addNode(-length,0.5*length,0);
    s.addNode(length,0.5*length,0);


    //Bar 3D
    s.addNode(0,2*length,-0.5*length);
    s.addNode(0,0,-0.5*length);
    //Bar 3D
    s.addNode(0,2*length,0.5*length);
    s.addNode(0,0,0.5*length);

}

void legModel::addRods(tgStructure& s)
{
    s.addPair( 0,  1, tgString("rod num", 0));
    s.addPair( 2,  3, tgString("rod num", 1));
    s.addPair( 4,  5, tgString("rod num", 2));
    s.addPair( 6,  7, tgString("rod num", 3));
    s.addPair( 8,  9, tgString("rod num", 4));
    s.addPair( 10,  11, tgString("rod num", 5));

}

void legModel::addActuators(tgStructure& s)
{
    //Each node is connected with 4 Strings/Cables/Muscles
    //Which means it should be repeated only four times
    //-1 means redundent and not use it it already has been configured
    //as a,b = b,a (unodred pairs)
    //rows means the starting node and the columns is the index of the cell
    //cell value is the end node
    int pairs[12][4] = {{4,6,10,11},{4,6,8,9},         //0,1
                        {5,7,10,11},{5,7,8,9},         //2,3
                        {-1,-1,8,10},{-1,-1,8,10},     //4,5
                        {-1,-1,9,11},{-1,-1,9,11},     //6,7
                        {-1,-1,-1,-1},{-1,-1,-1,-1},   //8,9
                        {-1,-1,-1,-1},{-1,-1,-1,-1}    //10,11
    };
    int counter = 0;
    for(int i = 0; i < 12; i++){
        for(int j = 0; j < 4; j++){
            if(pairs[i][j] == -1)
                continue;
            s.addPair(i,pairs[i][j], tgString("actuator num", counter));
            counter++;
            printf("%d - %d\n",i,pairs[i][j]);
        }
    }
}


void legModel::setup(tgWorld& world)
{
    // Define the configurations of the rods and strings
    // Note that pretension is defined for this string
    const tgRod::Config rodConfig(c.radius, c.density);
    // const tgSpringCableActuator::Config muscleConfig(c.stiffness, c.damping, c.pretension);
    const tgBasicActuator::Config actuatorConfig(c.stiffness, c.damping, c.pretension,
        c.hist, c.maxTension, c.targetVelocity);
    // Create a structure that will hold the details of this model
    tgStructure s;
    
    // Add nodes to the structure
    addNodes(s,c.length);
    
    // Add rods to the structure
    addRods(s);
    
    // Add muscles to the structure
    addActuators(s);
    
    // Move the structure so it doesn't start in the ground
    s.move(btVector3(0, 10, 0));
    
    // Create the build spec that uses tags to turn the structure into a real model
    tgBuildSpec spec;
    spec.addBuilder("rod", new tgRodInfo(rodConfig));
    // spec.addBuilder("muscle", new tgBasicActuatorInfo(muscleConfig));
    spec.addBuilder("actuator", new tgBasicActuatorInfo(actuatorConfig));

    // Create your structureInfo
    tgStructureInfo structureInfo(s, spec);

    // Use the structureInfo to build ourselves
    structureInfo.buildInto(*this, world);

    // Get the rod rigid bodies for controller
    std::vector<tgRod*> rods = legModel::find<tgRod>("rod");
    // for (int i = 0; i < rods.size(); i++) {
    //     allRods.push_back(legModel::find<tgRod>(tgString("rod num", i))[0]);    
    // }
    allRods = tgCast::filter<tgModel, tgRod> (getDescendants());
    
        
    // Get the actuators for controller
    std::vector<tgBasicActuator*> actuators = legModel::find<tgBasicActuator>("actuator");
    for (int i = 0; i < rods.size(); i++) {
        allActuators.push_back(legModel::find<tgBasicActuator>(tgString("actuator num", i))[0]);    
    }
    // We could now use tgCast::filter or similar to pull out the
    // models (e.g. muscles) that we want to control. 
    // allActuators = tgCast::filter<tgModel, tgSpringCableActuator> (getDescendants());
    
    // Notify controllers that setup has finished.
    notifySetup();
    
    // Actually setup the children
    tgModel::setup(world);
}

void legModel::step(double dt)
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

void legModel::onVisit(tgModelVisitor& r)
{
    // Example: m_rod->getRigidBody()->dosomething()...
    tgModel::onVisit(r);
}

std::vector<tgBasicActuator*>& legModel::getAllActuators()
{
    return allActuators;
}

std::vector<tgRod*>& legModel::getAllRods()
{
    return allRods;
}

void legModel::teardown()
{
    notifyTeardown();
    tgModel::teardown();
}

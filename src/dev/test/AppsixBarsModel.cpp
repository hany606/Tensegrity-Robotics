/**
 * @file AppsixBarsModel.cpp
 * @brief Contains the definition function main() for the Three strut
 * tensegrity 6 Bars strucutre
 * @author Hany Hamed
 */

// This application
#include "sixBarsModel.h"
// The controller
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


/**
 * The entry point.
 * @param[in] argc the number of command-line arguments
 * @param[in] argv argv[0] is the executable name
 * @return 0
 */
int main(int argc, char** argv)
{
    std::cout << "AppsixBarsModelTest" << std::endl;

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
    tgSimViewGraphics view(world, timestep_physics, timestep_graphics);

    // Third create the simulation
    tgSimulation simulation(view);

    // Fourth create the models with their controllers and add the models to the
    // simulation
    sixBarsModel* const myModel = new sixBarsModel();

    // Create the controller
    LengthController* const myController = new LengthController(200);
    
    // Attach controller to the model
    myModel->attach(myController);

    // Add the model to the world * $Id$
    simulation.addModel(myModel);


    simulation.run();
    //Teardown is handled by delete, so that should be automatic
    return 0;
}

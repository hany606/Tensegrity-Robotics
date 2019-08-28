#ifndef SIX_BARS_MODEL_H
#define SIX_BARS_MODEL_H

/**
 * @file sixBarsModel.h
 * @brief Defines a 6 strut 24 string tensegrity model
 * @author Hany Hamed
 * @version 1.0
 * This file is built over one of the examples from NTRTsim from NASA
 */

// This library
#include "core/tgModel.h"
#include "core/tgSubject.h"
#include "core/tgBasicActuator.h"
#include "core/tgRod.h"
#include "tgcreator/tgNode.h"
#include "tgcreator/tgBuildSpec.h"
#include "tgcreator/tgBasicActuatorInfo.h"
#include "tgcreator/tgRodInfo.h"
#include "tgcreator/tgStructure.h"
#include "tgcreator/tgStructureInfo.h"
// The C++ Standard Library
#include <vector>

// Forward declarations
class tgSpringCableActuator;
class tgModelVisitor;
class tgStructure;
class tgWorld;

/**
 * A class that constructs a six bar tensegrity structure using the tools
 * in tgcreator. This iteration avoids using a controller and instead
 * uses the new ability to define pretension in a
 * tgBasicActuator's constructor
 */
class sixBarsModel : public tgSubject<sixBarsModel>, public tgModel
{
public: 
    
    /**
     * The only constructor. Configuration parameters are within the
     * .cpp file in this case, not passed in. 
     */
    sixBarsModel();
    
    /**
     * Destructor. Deletes controllers, if any were added during setup.
     * Teardown handles everything else.
     */
    virtual ~sixBarsModel();
    
    /**
     * Create the model. Place the rods and strings into the world
     * that is passed into the simulation. This is triggered
     * automatically when the model is added to the simulation, when
     * tgModel::setup(world) is called (if this model is a child),
     * and when reset is called. Also notifies controllers of setup.
     * @param[in] world - the world we're building into
     */
    virtual void setup(tgWorld& world);
    
    /**
     * Undoes setup. Deletes child models. Called automatically on
     * reset and end of simulation. Notifies controllers of teardown
     */
    virtual void teardown();
    
    /**
     * Step the model, its children. Notifies controllers of step.
     * @param[in] dt, the timestep. Must be positive.
     */
    virtual void step(double dt);
    
    /**
     * Receives a tgModelVisitor and dispatches itself into the
     * visitor's "render" function. This model will go to the default
     * tgModel function, which does nothing.
     * @param[in] r - a tgModelVisitor which will pass this model back
     * to itself 
     */
    virtual void onVisit(tgModelVisitor& r);
    void getCentroid();
    tgStructure getTgStrucutre();

     /**
     * Return a vector of all actuators for the controllers to work with.
     * @return A vector of all of the actuatorsy
     */
    std::vector<tgBasicActuator*>& getAllActuators();

    /**
     * Return a vector of all rod bodies for the controllers to work with.
     * @return A vector of all of the rod rigid bodies
     */
    std::vector<tgRod*>& getAllRods();

      
private:
    
    /**
     * A function called during setup that determines the positions of
     * the nodes based on construction parameters. Rewrite this function
     * for your own models
     * @param[in] s: A tgStructure that we're building into
     * @param[in] edge: the X distance of the base points
     * @param[in] width: the Z distance of the base triangle
     * @param[in] height: the Y distance along the axis of the sixBars
     */
    static void addNodes(tgStructure& s, double length);
    
    /**
     * A function called during setup that creates rods from the
     * relevant nodes. Rewrite this function for your own models.
     * @param[in] s A tgStructure that we're building into
     */
    static void addRods(tgStructure& s);
    
    /**
     * A function called during setup that creates muscles (Strings) from
     * the relevant nodes. Rewrite this function for your own models.
     * @param[in] s A tgStructure that we're building into
     */
    static void addMuscles(tgStructure& s);
    
    /**
     * A function called during setup that creates actuators (Strings) from
     * the relevant nodes. Rewrite this function for your own models.
     * @param[in] s A tgStructure that we're building into
     */
    static void addActuators(tgStructure& s);

private:    
    /**
     * A list of all of the spring cable actuators. Will be empty until most of the way
     * through setup when it is filled using tgModel's find methods
     */
    tgStructure s;
    std::vector<tgBasicActuator*> allActuators;
    /**
     * A list of all of the rods. Will be empty until most of the way
     * through setup when it is filled using tgModel's find methods
     */
    std::vector<tgRod*> allRods;
};

#endif 

// sixBars_MODEL_H

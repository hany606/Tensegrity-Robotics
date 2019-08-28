#ifndef LENGTH_CONTROLLER_H
#define LENGTH_CONTROLLER_H

/**
 * @file LengthController.h
 * @brief Contains the definition of class LengthController.
 * @author Hany Hamed
 * This was built over one of the source codes of NTRTsim codes
 */


#include "sixBarsModel.h"
// This library
#include "core/tgObserver.h"
#include "controllers/tgBasicController.h"
#include "core/tgBasicActuator.h"
// The C++ Standard Library
#include <vector>

// Forward declarations
class sixBarsModel;

class LengthController : public tgObserver<sixBarsModel>
{
public:
	
	/**
	 * Construct a LengthTensionController.
	 * @param[in] tension, a double specifying the desired tension
	 * throughougt structure. Must be non-negitive
	 */
    LengthController(const double length = 400);
    
    /**
     * Nothing to delete, destructor must be virtual
     */
    virtual ~LengthController();
    
    virtual void onSetup(sixBarsModel& subject);
    
    /**
     * Apply the length controller. Called by notifyStep(dt) of its
     * subject.
     * @param[in] subject - the RPModel that is being controlled. Must
     * have a list of allMuscles populated
     * @param[in] dt, current timestep must be positive
     */
    virtual void onStep(sixBarsModel& subject, double dt);

    std::vector<tgBasicController*> m_controllers; //instantiate vector of controllers
    std::vector<double> rand_lengths; //instantiate vector of random restlengths
    std::vector<double> start_lengths; //instantiate vector of random restlengths
    std::vector<tgBasicActuator*> actuators;
    
private:
	
    const double m_length;
    double globalTime = 0;
    int toggle;

};

#endif LENGTH_CONTROLLER_H

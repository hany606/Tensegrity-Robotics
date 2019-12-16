#ifndef LENGTH_CONTROLLER_H
#define LENGTH_CONTROLLER_H

/**
 * @file LengthController.h
 * @brief Contains the definition of class LengthController.
 * @author Hany Hamed
 * This was built over one of the source codes of NTRTsim codes
 */


#include "JumperModel.h"
// This library
#include "core/tgObserver.h"
#include "controllers/tgBasicController.h"
#include "core/tgBasicActuator.h"
#include "tgcreator/tgNode.h"

// The C++ Standard Library
#include <vector>

#include "TCP.h"
#include "JSON_Structure.h"

// Forward declarations
class JumperModel;

class LengthController : public tgObserver<JumperModel>
{
public:
	
	/**
	 * Construct a LengthTensionController.
	 * @param[in] tension, a double specifying the desired tension
	 * throughougt structure. Must be non-negitive
	 */
    LengthController(const char* host, const long long port);
    
    /**
     * Nothing to delete, destructor must be virtual
     */
    virtual ~LengthController();
    
    virtual void onSetup(JumperModel& subject);
    
    /**
     * Apply the length controller. Called by notifyStep(dt) of its
     * subject.
     * @param[in] subject - the RPModel that is being controlled. Must
     * have a list of allMuscles populated
     * @param[in] dt, current timestep must be positive
     */
    virtual void onStep(JumperModel& subject, double dt);

    std::vector<tgBasicController*> m_controllers; //instantiate vector of controllers
    std::vector<double> start_lengths; //instantiate vector of random restlengths
    std::vector<tgBasicActuator*> actuators;
    std::vector<tgRod*> rods;
    std::vector<double> target_lengths;

private:
	
    double m_length = 200;
    const int port_num;
    const char* host_name;
    double globalTime = 0;
    int toggle;
    std::vector<int> actuators_states;
    TCP* tcp_com;
};

#endif

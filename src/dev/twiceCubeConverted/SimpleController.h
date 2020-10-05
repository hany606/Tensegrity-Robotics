#ifndef Simple_CONTROLLER_H
#define Simple_CONTROLLER_H

/**
 * @file SimpleController.h
 * @brief Contains the definition of class SimpleController.
 * @author Hany Hamed
 * This was built over one of the source codes of NTRTsim codes
 */


#include "TwiceCubeModel.h"
// This library
#include "core/tgObserver.h"
#include "controllers/tgBasicController.h"
#include "core/tgBasicActuator.h"
#include "tgcreator/tgNode.h"

// The C++ Standard Library
#include <vector>
#include <string>


#include "nlohmann/json.hpp"


#include "TCP.h"
#include "JsonStructure.h"




// Forward declarations
class TwiceCubeModel;

class SimpleController : public tgObserver<TwiceCubeModel>
{
public:
	
	/**
	 * Construct a SimpleTensionController.
	 * @param[in] tension, a double specifying the desired tension
	 * throughougt structure. Must be non-negitive
	 */
    SimpleController(const char* host, const long long port);
    
    /**
     * Nothing to delete, destructor must be virtual
     */
    virtual ~SimpleController();
    
    virtual void onSetup(TwiceCubeModel& subject);
    
    /**
     * Apply the Simple controller. Called by notifyStep(dt) of its
     * subject.
     * @param[in] subject - the RPModel that is being controlled. Must
     * have a list of allMuscles populated
     * @param[in] dt, current timestep must be positive
     */
    virtual void onStep(TwiceCubeModel& subject, double dt);


    std::vector<tgBasicController*> m_controllers; //instantiate vector of controllers
    std::vector<tgBasicActuator*> actuators;
    std::vector<tgRod*> rods;

private:
    
    const int port_num;
    const char* host_name;
    double globalTime = 0;
    int toggle = 0;
    TCP* tcp_com;

};

#endif
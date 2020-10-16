#ifndef JSONSTRUCTURE_G
#define JSONSTRUCTURE_G
#include "nlohmann/json.hpp"
#include <string>
#include <LinearMath/btVector3.h>

namespace JsonStructure
{
    namespace{
        nlohmann::json jsonFile;
    }

    void setup();
    void setup(nlohmann::json jsonFile);
    void setRestCableLength(int num, double val);
    void setCurrentCableLength(int num, double val);

    // void setCenterOfMass(int num, double x, double y, double z);
    // void setOrientation(int num, double i, double j, double k, double w);
    void setNode(int num, btVector3 end_point);
    void setNodeVelocity(int num, btVector3 end_point);


    void setFlags(int index, int value);
    void setTime(double t);
    std::string jsonToString();
    nlohmann::json stringToJson(char *s);

}


#endif
#ifndef JSON_STRUCTURE_G
#define JSON_STRUCTURE_G
#include "nlohmann/json.hpp"
#include <string>
namespace JSON_Structure
{
    namespace{
        nlohmann::json jsonFile;
    }

    void setup();
    void setup(nlohmann::json jsonFile);
    void setController(int num, double val);
    void setCenterOfMass(double x, double y, double z);
    void setOrientation(double i, double j, double k, double w);
    void setFlags(int index, int value);
    std::string jsonToString();
    nlohmann::json stringToJson(char *s);

}


#endif
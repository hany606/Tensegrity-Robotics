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
    std::string jsonToString();
    nlohmann::json stringToJson(char *s);

}


#endif
#include "JSON_Structure.h"


using json = nlohmann::json;

void JSON_Structure::setup(){
    JSON_Structure::jsonFile = {
        {"Controllers", 
            {0,10,0,0,0,0}
        },
        {"Center_of_Mass", {0,0,0}}
    };
}
void JSON_Structure::setup(json jsonFile){
    JSON_Structure::jsonFile = jsonFile;
}

void JSON_Structure::setController(int num, double val){
    JSON_Structure::jsonFile["Controllers"][num] = val;
}

void JSON_Structure::setCenterOfMass(double x, double y, double z){
    JSON_Structure::jsonFile["Center_of_Mass"] = {x,y,z};
}

const char* JSON_Structure::jsonToString(){
    return ((JSON_Structure::jsonFile.dump()).c_str());
}

nlohmann::json JSON_Structure::stringToJson(char *s){
    return (json::parse(s));
}

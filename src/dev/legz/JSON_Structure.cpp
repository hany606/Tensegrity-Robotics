#include "JSON_Structure.h"
#include<stdio.h>
#include<iostream>
#include<string>


using json = nlohmann::json;

void JSON_Structure::setup(){
    JSON_Structure::jsonFile = {
        {"Controllers", 
            {0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0}
        },
        {"Center_of_Mass", {0.,0.,0.}},
        {"Orientation", {0.,0.,0.,0.}},
        {"Flags", {0,0,0}}
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

void JSON_Structure::setOrientation(double i, double j, double k, double w){
    JSON_Structure::jsonFile["Orientation"] = {i,j,k,w};
}

void JSON_Structure::setFlags(int index, int value){
    JSON_Structure::jsonFile["Flags"][index] = value;
}

std::string JSON_Structure::jsonToString(){
    std::string value = JSON_Structure::jsonFile.dump();
    return value;
}

nlohmann::json JSON_Structure::stringToJson(char *s){
    return (json::parse(s));
}

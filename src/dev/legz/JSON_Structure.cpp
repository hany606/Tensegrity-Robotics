#include "JSON_Structure.h"
#include<stdio.h>
#include<iostream>
#include<string>


using json = nlohmann::json;

void JSON_Structure::setup(){
    JSON_Structure::jsonFile = {
        {"Cables_lengths", 
            {0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0}
        },
        {"Center_of_Mass", {{0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.},
                            {0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.}, {0.,0.,0.}}},

        {"Orientation", {{0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.},
                         {0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.}, {0.,0.,0.,0.}}},
        {"Flags", {1,0,0}},
        {"Time", 0.},
        {"ZFinished", 1}
    };

}
void JSON_Structure::setup(json jsonFile){
    JSON_Structure::jsonFile = jsonFile;
}

void JSON_Structure::setController(int num, double val){
    JSON_Structure::jsonFile["Controllers"][num] = val;
}

void JSON_Structure::setCenterOfMass(int num, double x, double y, double z){
    JSON_Structure::jsonFile["Center_of_Mass"][num] = {x,y,z};
}

void JSON_Structure::setOrientation(int num, double i, double j, double k, double w){
    JSON_Structure::jsonFile["Orientation"][num] = {i,j,k,w};
}

void JSON_Structure::setFlags(int index, int value){
    JSON_Structure::jsonFile["Flags"][index] = value;
}

void JSON_Structure::setTime(double t){
    JSON_Structure::jsonFile["Time"] = t;
}

std::string JSON_Structure::jsonToString(){
    std::string value = JSON_Structure::jsonFile.dump();
    return value;
}

nlohmann::json JSON_Structure::stringToJson(char *s){
    return (json::parse(s));
}

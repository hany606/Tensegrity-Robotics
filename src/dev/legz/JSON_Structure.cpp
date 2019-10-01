#include "JSON_Structure.h"
#include<stdio.h>
#include<iostream>
#include<string>


using json = nlohmann::json;

void JSON_Structure::setup(){
    JSON_Structure::jsonFile = {
        {"Controllers", 
            {10,20,30,40,50,60}
        },
        {"Center_of_Mass", {0,0,0}}
    };
    JSON_Structure::jsonFile["Controllers"][1] = 100;
    // std::cout<<JSON_Structure::jsonFile["Controllers"][1]<<std::endl;
    // printf("0000Part of the json: %lf\n", JSON_Structure::jsonFile["Controllers"][1]);

}
void JSON_Structure::setup(json jsonFile){
    JSON_Structure::jsonFile = jsonFile;
}

void JSON_Structure::setController(int num, double val){
    JSON_Structure::jsonFile["Controllers"][num] = val;
    // std::cout<<JSON_Structure::jsonFile["Controllers"][0]<<std::endl;
    // printf("0000Part of the json: %lf\n%lf\n", val, JSON_Structure::jsonFile["Controllers"][num]);

}

void JSON_Structure::setCenterOfMass(double x, double y, double z){
    JSON_Structure::jsonFile["Center_of_Mass"] = {x,y,z};
}

std::string JSON_Structure::jsonToString(){
    // std::cout<<JSON_Structure::jsonFile["Center_of_Mass"]<<std::endl;

    // std::cout<<JSON_Structure::jsonFile.dump()<<std::endl;
    std::string value = JSON_Structure::jsonFile.dump();
    // std::cout<<value<<std::endl;
    // printf("The json before return: %s\n", value);
    return value;
}

nlohmann::json JSON_Structure::stringToJson(char *s){
    return (json::parse(s));
}

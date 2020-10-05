#include "JsonStructure.h"
#include<stdio.h>
#include<iostream>
#include<string>



using json = nlohmann::json;

void JsonStructure::setup(){
    JsonStructure::jsonFile = {
        {"rest_cables_lengths", 
            {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
        },
        {"current_cables_lengths", 
            {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
        },
        {"nodes",
            {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
        },
        {"flags", {1,0,0}},
        {"time", 0.},
        {"z_finished", 1}
    };

}
void JsonStructure::setup(json jsonFile){
    JsonStructure::jsonFile = jsonFile;
}

void JsonStructure::setRestCableLength(int num, double val){
    JsonStructure::jsonFile["rest_cables_lengths"][num] = val;
}

void JsonStructure::setCurrentCableLength(int num, double val){
    JsonStructure::jsonFile["current_cables_lengths"][num] = val;
}

void JsonStructure::setNodes(int num, btVector3 end_point){
    JsonStructure::jsonFile["nodes"][num][0] = end_point[0];
    JsonStructure::jsonFile["nodes"][num][1] = end_point[1];
    JsonStructure::jsonFile["nodes"][num][2] = end_point[2];
}


void JsonStructure::setFlags(int index, int value){
    JsonStructure::jsonFile["flags"][index] = value;
}

void JsonStructure::setTime(double t){
    JsonStructure::jsonFile["time"] = t;
}

std::string JsonStructure::jsonToString(){
    std::string value = JsonStructure::jsonFile.dump();
    return value;
}

nlohmann::json JsonStructure::stringToJson(char *s){
    return (json::parse(s));
}
#include "JsonStructure.h"
#include<stdio.h>
#include<iostream>
#include<string>



using json = nlohmann::json;

void JsonStructure::setup(){
    JsonStructure::jsonFile = {
        {"rest_cables_lengths", 
            {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}
        },
        {"nodes",
            {{0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0} }
        },
        {"nodes_velocities",
            {{0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0}, {0.0, 0.0, 0.0} }
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

void JsonStructure::setNode(int num, btVector3 node){
    JsonStructure::jsonFile["nodes"][num][0] = node[0];
    JsonStructure::jsonFile["nodes"][num][1] = node[1];
    JsonStructure::jsonFile["nodes"][num][2] = node[2];
}

void JsonStructure::setNodeVelocity(int num, btVector3 node_velocity){
    JsonStructure::jsonFile["nodes_velocities"][num][0] = node_velocity[0];
    JsonStructure::jsonFile["nodes_velocities"][num][1] = node_velocity[1];
    JsonStructure::jsonFile["nodes_velocities"][num][2] = node_velocity[2];
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
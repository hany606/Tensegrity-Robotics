// The C++ Standard Library
#include "ROS_Bridge.h"
#include <iostream>

#include "nlohmann/json.hpp"
#include <fstream>

using jsonf = nlohmann::json;
// #include "ros/ros.h"
// #include "std_msgs/String.h"

ROS_Bridge::ROS_Bridge(){
    ROS_Bridge::fileName = "data.json";
    ROS_Bridge::jsonFile = {
        {"Controllers", 
            {0,0,0,0,0,0}
        }
    };
}

ROS_Bridge::ROS_Bridge(jsonf customJSON){
    ROS_Bridge::jsonFile = customJSON;
}

void ROS_Bridge::setController(int num, double val){
    ROS_Bridge::jsonFile["Controllers"][num] = val;
    ROS_Bridge::saveJSON();
}

void ROS_Bridge::saveJSON(){
    std::ofstream file(fileName);
    file << ROS_Bridge::jsonFile; 
}
void ROS_Bridge::saveJSON(jsonf j){
    std::ofstream file(fileName);
    file << j; 
}

void ROS_Bridge::test1234(){
    static int tmp = 0;
    if(tmp == 0){
        ROS_Bridge::saveJSON();
        tmp = 1;
  
    // std::cout<<"Create ROS node\n";

    // ros::init(argc,argv,"NAME");
    // ros::NodeHandle node_obj;
    // ros::Publisher number_publisher = node_obj.advertise<std_msgs::Int32>("/numbers",10);
    // ros::Rate loop_rate(10);
    }
    // if(ros::ok)
    // {
    //     std::cout<<"ROS is established\n";
    // }
}
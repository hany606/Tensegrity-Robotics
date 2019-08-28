#ifndef ROS_Brdige_G
#define ROS_Brdige_G
#include "nlohmann/json.hpp"

class ROS_Bridge
{
    public:
    ROS_Bridge();
    ROS_Bridge(nlohmann::json customJSON);
    void setController(int num, double val);
    void test1234();
    
    private:
    nlohmann::json jsonFile;
    char* fileName;
    void saveJSON();
    void saveJSON(nlohmann::json j);

};

#endif
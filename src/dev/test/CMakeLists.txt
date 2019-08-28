link_directories(${LIB_DIR})
link_libraries(tgcreator
                util
                sensors
                core    
                controllers
                terrain 
                tgOpenGLSupport
)
# find_package(roscpp REQUIRED)
# find_package(std_msgs REQUIRED)

set(JSON_BuildTests OFF CACHE INTERNAL "")

add_subdirectory(json)
include_directories(/json/include/nlohmann)


# include_directories(/opt/ros/melodic/include)
# link_directories(/opt/ros/melodic/lib)



add_executable(AppsixBarsModel2
    sixBarsModel.cpp
    AppsixBarsModel.cpp
    LengthController.cpp
    ROS_Bridge.cpp
    TCP.cpp
    JSON_Structure.cpp
)
# target_link_libraries(AppsixBarsModel2 roscpp rostime rosconsole)
# target_link_libraries(AppsixBarsModel2 jsoncpp)

target_link_libraries(AppsixBarsModel2 PRIVATE nlohmann_json::nlohmann_json)
link_directories(${LIB_DIR})

link_libraries(tgcreator
                util
                sensors
                core
                terrain 
                tgOpenGLSupport)



add_executable(AppTwiceCubeGymModel
    TwiceCubeGymModel.cpp
    AppTwiceCubeGymModel.cpp
    SimpleController.cpp
    TCP.cpp
    JsonStructure.cpp
) 


FIND_PACKAGE(Boost COMPONENTS program_options REQUIRED)
INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIRS})

target_link_libraries(AppTwiceCubeGymModel PRIVATE nlohmann_json::nlohmann_json)
target_link_libraries(AppTwiceCubeGymModel ${Boost_LIBRARIES})
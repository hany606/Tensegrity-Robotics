link_directories(${LIB_DIR})

link_libraries(tgcreator
                util
                sensors
                core
                terrain 
                tgOpenGLSupport)



add_executable(AppTwiceCubeModel
    TwiceCubeModel.cpp
    AppTwiceCubeModel.cpp
    SimpleController.cpp
) 


FIND_PACKAGE(Boost COMPONENTS program_options REQUIRED)
INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIRS})

target_link_libraries(AppTwiceCubeModel ${Boost_LIBRARIES})

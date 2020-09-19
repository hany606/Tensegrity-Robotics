link_directories(${LIB_DIR})

link_libraries(tgcreator
                util
                sensors
                core
                terrain 
                tgOpenGLSupport)



add_executable(AppSimpleModel
    SimpleModel.cpp
    AppSimpleModel.cpp
    SimpleController.cpp
) 


FIND_PACKAGE(Boost COMPONENTS program_options REQUIRED)
INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIRS})

target_link_libraries(AppSimpleModel ${Boost_LIBRARIES})

link_directories(${LIB_DIR})

find_package(nlohmann_json REQUIRED)


link_libraries(tgcreator
                util
                sensors
                core
                terrain 
                tgOpenGLSupport)
                
add_executable(AppLegzModel
    legzModel.cpp
    AppLegzModel.cpp
    LengthController.cpp
    TCP.cpp
    JSON_Structure.cpp
) 


target_link_libraries(AppLegzModel PRIVATE nlohmann_json::nlohmann_json)

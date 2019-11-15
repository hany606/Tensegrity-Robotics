link_directories(${LIB_DIR})

link_libraries(tgcreator
                util
                sensors
                core
                terrain 
                tgOpenGLSupport)

add_executable(AppJumperModel
    JumperModel.cpp
    AppJumperModel.cpp
    LengthController.cpp
    TCP.cpp
    JSON_Structure.cpp
) 


target_link_libraries(AppJumperModel PRIVATE nlohmann_json::nlohmann_json)
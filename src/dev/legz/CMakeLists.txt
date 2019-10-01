link_directories(${LIB_DIR})

link_libraries(tgcreator
                util
                sensors
                core
                terrain 
                tgOpenGLSupport)

set(JSON_BuildTests OFF CACHE INTERNAL "")
add_subdirectory(json)
include_directories(/json/include/nlohmann)



add_executable(AppLegzModel
    legzModel.cpp
    AppLegzModel.cpp
    LengthController.cpp
    TCP.cpp
    JSON_Structure.cpp
) 


target_link_libraries(AppLegzModel PRIVATE nlohmann_json::nlohmann_json)
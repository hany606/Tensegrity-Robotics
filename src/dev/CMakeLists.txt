Project(Dev)
set(JSON_BuildTests OFF CACHE INTERNAL "")

add_subdirectory(json)
include_directories(/json/include/nlohmann)

# Add additional dev directories here.
subdirs(
	sixBars	#at least one file in order no to give error in building
	#test
	#json_build
	#legz
	jumper
	#boxCube
	twiceCube
)

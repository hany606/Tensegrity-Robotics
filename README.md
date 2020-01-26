# Tensegrity-Robotics

This repository for my works in the Tensegrity Robotics. It is extension for the work that done in [my university's internship Summer19](https://github.com/hany606/Tensegrity-Robot-IU-Internship19). The work of the simulator is from [NTRTsim](https://github.com/NASA-Tensegrity-Robotics-Toolkit/NTRTsim).

There is a google doc who contain a lot of data related to the project that I have collected during my internship: [Link](https://docs.google.com/document/d/19-lCDq4gPtaQ6hCJNI77qi1bIzHJGaliu4Yrh53H7hs/edit?usp=sharing)

This work is not an individual, this work is part from a research work in robotics lab at Innopolis University.

Mainly, this work will concentrate on using RL to control the movements of the tensegrity structure using NTRTsim for now.

## Active Projects:
1. Tensegrity Leg:
It is in [src/dev/legz](https://github.com/hany606/Tensegrity-Robotics/tree/master/src/dev/legz)


## How to start working with the repository?:
  1. Clone the repo:
	  ```bash
	  git clone https://github.com/hany606/Tensegrity-Robot-IU-Internship19.git
	  ```
  2. Go to the folder:
	 ```bash
	 cd Tensegrity-Robotics
	    ```
	  
 3. Running the setup.sh
	 ```bash
	 ./setup.sh
	 ```
	If you have any problems or issues check the original documentation of installing the simulator: [Link](https://raw.githubusercontent.com/NASA-Tensegrity-Robotics-Toolkit/NTRTsim/master/INSTALL).
	
	If the setup.sh has failed, try first to run it again. (It worked for me)

4. Test the simulator environment
	 a. Run build.sh
    ```bash
    ./bin/build.sh
	```
	b. Run an Example
	```bash
	./build/examples/3_prism/AppPrismModel
	```
	The simulator should be appeared now.

Note: step 5 is not needed any more as the library is installed and build from source, no need to install it into the system
5. Install [nlohmann-json library](https://github.com/nlohmann/json). 

You can install it by linuxbrew, but you need to install first from [here](https://docs.brew.sh/Homebrew-on-Linux).

Sometimes there are errors regarding this library, hence, you can comment [this line](https://github.com/hany606/Tensegrity-Robotics/blob/7ced260c976b223864f59208bfcef89499cf10e8/src/dev/CMakeLists.txt#L7) and ensure to delete the folder of json_build in the directory of build.

6. To Open any stimulation for a structure, you should build the codes then run it from build directory
	```bash
	./bin/build.sh
	cd build/dev
	cd Model_name
	./App_Name_Model
	```
7. To run the openAI gym custom environment and test it. You need first to export the directory folder, then you can run the test for the environment or just install the gym_tensegrity library as it is described in this [README](https://github.com/hany606/Tensegrity-Robotics/blob/master/src/dev/gym-tensegrity/README.md)
	```bash
	export TENSEGRITY_HOME="absolute/path/to/the/root/folder"
	```
	```bash
	cd src/dev/legz/gym-leg/gym_leg/envs/
	python3 jumper_test.py
	```

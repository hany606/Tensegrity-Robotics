# Tensegrity-Robotics

This repository is for the Tensegrity Robotics works.
The work of the simulator is from [NTRTsim](https://github.com/NASA-Tensegrity-Robotics-Toolkit/NTRTsim).


This work is not an individual, this work is part from a research work in the robotics lab at Innopolis University.

Mainly, this work will concentrate on using Reinforcement Learning methods to control the movements of the tensegrity structure using NTRTsim as a simulator for now.

## Publications:
* [Learning Stabilizing Control Policies for a Tensegrity Hopper with Augmented Random Search](https://www.researchgate.net/publication/340475125_Learning_Stabilizing_Control_Policies_for_a_Tensegrity_Hopper_with_Augmented_Random_Search)	[[Code](https://github.com/hany606/Tensegrity-Robotics/tree/Learning-Stabilizing-Control-Policies-for-a-Tensegrity-Hopper-with-Augmented-Random-Search-paper)]

## Active Projects:
1. Tensegrity Jumper:
It is in [src/dev/jumper](https://github.com/hany606/Tensegrity-Robotics/tree/master/src/dev/jumper)


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
	
	If the setup.sh has failed, try first to run it again. (It worked for me in the third time)

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
7. To use RL algorithms a custom environment has been created in the same format of OpenAI gym environments to be able to be used with the libraries that conforms with OpenAI Gym. To run the environment and test it. You need first to export the directory folder, then you can run the test for the environment or just install the gym_tensegrity library as it is described in this [README](https://github.com/hany606/Tensegrity-Robotics/blob/master/src/dev/gym-tensegrity/README.md)

	put this into .bashrc or run it every time
	```bash
	export TENSEGRITY_HOME="absolute/path/to/the/root/folder"
	```

	```bash
	cd src/dev/legz/gym-leg/gym_leg/envs/
	python3 jumper_test.py
	```

## Use it with Docker:

There is a Dockerfile inside docker directory that can be used, it is by default use the headless-server branch to be used with headless servers.

## Running in Headless mode (without xserver display):

This step can be done only when you are in the headless_server branch because the files are configured to run without the extra terminal for the debugging. It is based on using Xvfb tool.

```bash
 git checkout headless_server
```

Example how to use it:

```bash
 xvfb-run -a python3 jumper_test.py
```

Or to specify the server number

```bash
 xvfb-run --server-num=10 python3 jumper_test.py
```

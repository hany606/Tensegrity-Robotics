# Tensegrity_Robotics
This repository for my works in the Tensegrity Robotics. It is extension for the work that done in [my university's internship Summer19](https://github.com/hany606/Tensegrity-Robot-IU-Internship19). The work of the simulator is from [NTRTsim](https://github.com/NASA-Tensegrity-Robotics-Toolkit/NTRTsim).

There is a google doc who contain a lot of data related to the project that I have collected during my internship: [Link](https://docs.google.com/document/d/19-lCDq4gPtaQ6hCJNI77qi1bIzHJGaliu4Yrh53H7hs/edit?usp=sharing)


## How to start?:
  1. Clone the repo:
	  ```bash
	  git clone https://github.com/hany606/Tensegrity-Robot-IU-Internship19.git
	  ```
  2. Go to the folder:
	 ```bash
	 cd Tensegrity-Robot-IU-Internship
	    ```
	  
 3. Running the setup.sh
	 ```bash
	 ./setup.sh
	 ```
	If you have any problems or issues check the original documentation of installing the simulator: [Link](https://raw.githubusercontent.com/NASA-Tensegrity-Robotics-Toolkit/NTRTsim/master/INSTALL).
	
	If the setup.sh has failed, try first to run it again. (It worked for me)

4. Test the environment
	 a. Run build.sh
    ```bash
    ./bin/build.sh
	```
	b. Run an Example
	```bash
	./build/examples/3_prism/AppPrismModel
	```
	The simulator should be appeared now.
5. Go to the main branch of my project
	```bash
	git checkout develop
	```
6. To Open any stimulation for a structure, you should build the codes then run it from build directory
	```bash
	./bin/build.sh
	cd build/dev
	cd Model_name
	./App_Name_Model
	```

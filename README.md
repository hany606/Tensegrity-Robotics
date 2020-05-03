
# Tensegrity-Robotics: Learning-Stabilizing-Control-Policies-for-a-Tensegrity-Hopper-with-Augmented-Random-Search-paper 

## Introduction

This repository is for the implementation of "[Learning Stabilizing Control Policies for a Tensegrity Hopper with Augmented Random Search Paper](https://arxiv.org/abs/2004.02641)"

This repository includes parts of the source code of the Tensegrity simulator is part of [NASA NTRTsim](https://github.com/NASA-Tensegrity-Robotics-Toolkit/NTRTsim), source codes for training and evaluation scripts that were used in the paper, and the gym environment for the tensegrity structure that is used in the paper.
  

This work concentrates on the using of Augmented Random Search to learn a stabilizing control policy for a Tensegrity Hopper. 

* The used RL algorithm which is Augmented Random Search (ARS) is the implementation from [Ray/RLlib](https://docs.ray.io/en/latest/rllib.html)

* The used simulator for the tensegrity structure is [NTRTsim from NASA](https://github.com/NASA-Tensegrity-Robotics-Toolkit/NTRTsim)

This work is a part of the research that is being done in the Robotics Center at Innopolis University.



## Table of contents

*  [Dependencies](#dependencies)

*  [Installation](#installation)

*  [Folders structure](#folders-structure)

*  [Parameters](#parameters)

*  [Train it!](#train-it)

*  [Evaluate it!](evaluate-it)

*  [Pretrained Agents](#pretrained-agents)

*  [Results](#results)

*  [Citation](#citation)

*  [Contact for Issues](#contact-for-issues)

*  [References](#references)

## Dependencies

  

* NTRTsim and its dependencies: [here](https://github.com/NASA-Tensegrity-Robotics-Toolkit/NTRTsim/blob/master/INSTALL)

* Python3, Pip3

*  [Open AI Gym python library](https://github.com/openai/gym)

*  [Ray/RLlib](https://ray.readthedocs.io/en/latest/rllib.html) and its dependency ([Tensorflow](https://www.tensorflow.org/))

<!-- *  [Tensorflow](https://www.tensorflow.org/) for RLlib -->

* Git

  

## Installation

A. Through installing the specific packages and the libraries:
1. Clone the repository and checkout to the paper branch:

	```bash

	git clone --branch Learning-Stabilizing-Control-Policies-for-a-Tensegrity-Hopper-with-Augmented-Random-Search-paper https://github.com/hany606/Tensegrity-Robot-IU-Internship19.git

	```

2. Go to the repository's directory:

	```bash

	cd Tensegrity-Robotics

	```

3. Install the dependencies:
	
	3.1 Install NTRTsim dependencies
	```bash
	sudo apt-get install g++ libglib2.0-dev curl freeglut3 freeglut3-dev cmake build-essential unzip g++-4.8 python python3-pip
	```

	3.2 Install gym
	```bash
	pip3 install gym
	```

	3.3 Install Ray/RLlib
	```bash
	pip3 install ray[rllib]
	pip3 install ray[debug]
	```

4. Running the setup.sh to install NTRTsim

	```bash
	./setup.sh
	```

	If some problems appeared for using NTRTsim related to g++, check [this](https://github.com/NASA-Tensegrity-Robotics-Toolkit/NTRTsim/blob/1a671cca257632200197d369b5382ca490dbd6f2/INSTALL#L62)

	If the setup.sh has failed, try first to run it again. (Usually in the third time it works)

5. Test the simulator environment

	a. Run build.sh to build the executable files for the structures

	```bash
	./bin/build.sh
	```

	b. Run an example to test the simulator

	```bash
	./build/examples/3_prism/AppPrismModel
	```

7. Prepare the environment

	a. Put the following into .bashrc or run it every time to define the home directory for the repository directory

	```bash
	export TENSEGRITY_HOME="absolute/path/to/the/root/folder"
	```

	For example:
	```bash
	export TENSEGRITY_HOME="/home/Tensegrity-Robotics"
	```

	b. To make the command of building the structure faster and easier, put the following into .bashrc to create an alias for the command which is responsible to build the structures executable files:

	```bash
	alias tensegrityBuild="absolute/path/to/the/bin/folder/build.sh"
	```

	For example:
	```bash
	alias tensegrityBuild="/home/Tensegrity-Robotics/bin/build.sh'
	```

8. Install the custom gym environment for Tensegrity

```bash
./bin/setup_gym_env.sh
```

Note: instead of running step 4 and step 8, it is possible just to run:

```bash
./bin/setup_helper.sh
```

B. Using the Docker image for this environment:

```bash
docker pull hany606/tensegrity_headless_server:v0.3
```

Note: the current docker image works with the headless_server branch which is under development for other experiments, headless_server branch is related to training on servers without GUI.

To work with the docker image that works with the current branch (Paper's branch): it is in "docker" directory

```bash
docker build -t tensegrity_img docker/.
```

Note: to run scripts in headless mode (with xserver display/GUI), it is possible to use Xvfb tool
  
Example of how to use it:

```bash
xvfb-run -a python3 src/dev/gym-tensegrity/gym_tensegrity/envs/jumper_test.py
```

Or to specify the server number

```bash
xvfb-run --server-num=10 python3 src/dev/gym-tensegrity/gym_tensegrity/envs/jumper_test.py
```

## Folders' structure

- bin (NTRTsim): includes the utilities to setup the NTRTsim

- conf (NTRTsim): includes the configuration files that related to the NTRTsim

- build (NTRTsim): includes the executable files for the models after building it using NTRTsim scripts

- env (NTRTsim): includes the libraries that are installed for NTRTsim

- resources (NTRTsim): includes the sources for the libraries for NTRTsim

- src (NTRTsim): includes the source codes for the tensegrity structures and the source codes for the paper

	a. dev: includes the source codes for the paper, gym environment, and the used tensegrity structure.

	* gym-tensegrity: includes the gym environment inside gym_tensegrity directory

	* learning_scripts: includes the scripts for training and evaluation for this paper
	
	b. examples (NTRTsim): includes examples for testing the simulator

	c. other (NTRTsim): related to the simulator

## Parameters

Parameters are split into two parts, a part which is related to the parameters for the tensegrity structure and the other part which is related to the ARS parameters and parameters for the gym_tensegrity environment

a. Tensegrity Hopper/Jumper Structure (In dev/jumper/JumperModel.cpp)

* Density (5kg/cm^3)
* Rod Radius for leg rod and the square side rod (0.20cm)
* Stiffness (3000.0kg/sec^2)
* Damping (30.0kg/sec)
* Pretension (12000.0kg*cm/sec^2)
* Leg Rod length (10.0cm)
* Square Side Rod (10.0cm) 
* Max tension (30000kg*cm/sec^2)
* Target Velocity for the actuators (30 cm/sec)
  
b. gym_tensegrity parameters

* Observation: Endpoints of rods, Velocities of the rods' endpoints, and Cables' rest lengths
* Actions: Continuos control in the rest length of the cables
* Reward: +1 each time step the structure stays alive without termination
* Termination: The angle between the leg link and the ground should stay in the interval of [-20, 20] degrees and the angle between the frame link and the ground should stay in the interval of [-40, 40] degrees
* Starting configurations: Starting from above the ground with height 100cm

c. Augmented Random Search Algorithm parameters

* [Full description for the parameters](https://docs.ray.io/en/latest/rllib-algorithms.html#augmented-random-search-ars), the used parameters are written in the training script

## Train it!

Inside "src/dev/gym-tensegrity/learning_scripts/rllib/training_scripts/", there is the script which has been used for training

```bash
python3 training.py
```

This is the successful training script that has been used to get out this paper's results.

## Evaluate it!

Inside "src/dev/gym-tensegrity/learning_scripts/rllib", there is the script which has been used for evaluating the trained model

```bash
python3 evaluate.py --agent-path=<path-to-trained-agent> --checkpoint-num=xx
```

--agent-path: is the path to the trained agent

-- checkpoint-num: is the number of the checkpoint to restore the agent in that checkpoint

Example:
```bash
python3 evaluate.py --agent-path=trained_agents/train_025_rep_act1_restL/ARS_jumper_29224120_2020-01-21_19-35-20j61sj43o/ --checkpoint-num=605
```

Or for different models checkpoints and different configuration files
```bash
python3 evaluate.py --evaluation-file=<path-to-trained-agent-training-checkpoint-xx> --agent-config-file=<path-to-config-file-for-trained-agent.json>
```

--evaluation-file: is the path to the checkpoint for the trained agent that will be used to restore the trained model to be evaluated

--agent-config-file: is the path to the json file which includes all the configurations and parameters to the trained agent

Example:
```bash
python3 evaluate.py --evaluation-file=trained_agents/train_025_rep_act1_restL/ARS_jumper_29224120_2020-01-21_19-35-20j61sj43o/checkpoint_60/checkpoint-60 --agent-config-file=trained_agents/train_025_rep_act1_restL/ARS_jumper_29224120_2020-01-21_19-35-20j61sj43o/params.json
```
  
## Pretrained Agents

Inside "src/dev/gym-tensegrity/learning_scripts/rllib/trained_agents", there is the successful agent that has been trained with the checkpoints, tfevents file, the parameters for the training and the progress log

- train_025_rep_act1_restL/ARS_jumper_29224120_2020-01-21_19-35-20j61sj43o: The configuration of the gym_tensegrity and the parameters for ARS are included in params.json

## Results

TODO: Add results or just from the paper

## Citation

TODO: https://arxiv.org/pdf/2004.02641.pdf (@inproceedings/@conference ??)

## Contact for Issues

Hany Hamed: h.hamed.elanwar@gmail.com / h.hamed@innopolis.university

Vlad Kurenkov: v.kurenkov@innopolis.ru

## References

* [NASA Tensegrity Robotics Toolkit Simulator (NTRTsim)](https://github.com/NASA-Tensegrity-Robotics-Toolkit/NTRTsim)

* [Ray/RLlib](https://docs.ray.io/en/latest/rllib.html)

* [ML Code Completeness Checklist](https://medium.com/paperswithcode/ml-code-completeness-checklist-e9127b168501)

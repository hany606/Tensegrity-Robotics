# Train 9
	
	- Describtion: v1.4.1.0 from the training Changing the parameters not like train3 (v1.0.1.0)

	- Parameters is described inside the experiment folder -> "params.json"
		Changes from train3:
			a. "noise_stdev": 0.04    instead of 0.02
			b. "sgd_stepsize": 0.03 instead of 0.01

	- Notes:
		1. The training didn't finish as the same errors appeared in train1 and train2 for the execeeding in the action_space limits
		2. Before the error the model trained for 23 iterations for total time 15.85 minutes
		3. The reward were much less than other trainings the maximum was 372.19 and this was the first one and then starts to decrease until it reached 66.66 and starts to increase in the last iteration to 102.54 then it crashed.
		
		
	- TODO:
		* Understand the behaviour of the library to generate this problem, maybe from our environment (but we define the action_space and the library should get the limits from the action_space), this error maybe because the algorithm is based on random search and reached to the limits for the change.
		* Test with different paramters for the defined timesteps (500,000)

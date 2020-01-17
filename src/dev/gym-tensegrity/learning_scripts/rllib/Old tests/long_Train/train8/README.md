# Train 8
	
	- Describtion: v1.3.1.0 from the training Changing the parameters not like train3 (v1.0.1.0)

	- Parameters is described inside the experiment folder -> "params.json"
		Changes from train3:
			a. "eval_prob": 0.03    instead of 0.09
			b. "num_rollouts": 32   instead of 30
			c. "rollouts_used": 15  instead of 30
			d. "sgd_stepsize": 0.07 instead of 0.01

	- Notes:
		1. The training didn't finish as the same errors appeared in train1 and train2 for the execeeding in the action_space limits
		2. There was 3 successfull iterations, however, the first one was nan for the episode_reward_mean and episode_reward_len. but the other two were too low rewards.
		
		
	- TODO:
		* Understand the behaviour of the library to generate this problem, maybe from our environment (but we define the action_space and the library should get the limits from the action_space), this error maybe because the algorithm is based on random search and reached to the limits for the change.
		* Test with different paramters for the defined timesteps (500,000)

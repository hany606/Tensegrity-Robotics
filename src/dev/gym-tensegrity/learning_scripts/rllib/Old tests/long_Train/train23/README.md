# Train 23
	
	- Describtion: v4.3.1.0 from the training (1,000,000 timesteps, 10 workers)
		Observation_space: rest_length
		Hyper-parameters have been changed:
			- num_rollouts: 50 instead of 30
			- sgd_stepsize: 0.03 instead of 0.01
			- eval_prob: 0.5 instead of 0.09

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. It gave an error due to the limits of the action space, after 211,410/1,000,000 timesteps with 28 iteration
		2. It started as usual for increasing then reach the maximum then settle near that, however, the rewards has rapidly increased in the last 6 iterations as it reached 1947 -> 1777 which means that it wsa successfully do some jumps.
	
	- TODO:
		* Try to repeat the same experiment
		* Increase the limits of the action_space

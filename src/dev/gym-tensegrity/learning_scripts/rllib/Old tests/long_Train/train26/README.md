# Train 26
	
	- Describtion: v4.6.1.0 from the training (1,000,000 timesteps, 10 workers)
		Observation_space: rest_length
		Hyper-paramters (changes):
			- num_rollouts: 8 instead of 30
			- rollouts_used: 4 instead of 30
			- noise_size: 25000000 instead of 250000000
			- eval_prob: 0.5 instead of 0.09

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. It gave an error due to the limits of the action space, after 218,792/1,000,000 timesteps with 28 iteration
		2. It started as usual for increasing then reach the maximum then settle near that, however, the rewards has rapidly increased in the last 5 iterations as it reached 4099 -> 4027 which means that it wsa successfully do some jumps. It is better of train23
	
	- TODO:
		* Try to repeat the same experiment
		* Increase the limits of the action_space

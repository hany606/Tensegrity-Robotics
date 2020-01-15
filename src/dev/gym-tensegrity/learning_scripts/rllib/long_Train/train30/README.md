# Train 30
	
	- Describtion: v4.6.1.2 from the training (1,000,000 timesteps, 10 workers)	(Repeated train 26)
		Observation_space: rest_length
		Hyper-paramters (changes):
			- num_rollouts: 8 instead of 30
			- rollouts_used: 4 instead of 30
			- noise_size: 25000000 instead of 250000000
			- eval_prob: 0.5 instead of 0.09

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. It gave an error due to the limits of the action space, after 350,607/1,000,000 timesteps with 25 iteration
		2. It was successfull as train26
	- TODO:
		* Try to repeat the same experiment
		* Increase the limits of the action_space

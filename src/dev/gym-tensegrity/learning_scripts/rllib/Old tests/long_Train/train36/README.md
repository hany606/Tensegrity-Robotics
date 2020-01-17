# Train 36
	
	- Describtion: v4.6.2.0 from the training (1,000,000 timesteps, 10 workers)	(Repeated train34)
		Observation_space: rest_length
		Hyper-paramters (changes):
			- num_rollouts: 8 instead of 30
			- rollouts_used: 4 instead of 30
			- noise_size: 25000000 instead of 250000000
			- eval_prob: 0.5 instead of 0.09

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. The same behaviour as train34


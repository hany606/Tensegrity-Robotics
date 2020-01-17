# Train 45
	
	- Describtion: v4.7.1.0 from the training (1,000,000 timesteps, 10 workers) (Repeated trian34 but with observation end_points)
		Observation_space: end_points
		Hyper-paramters (changes):
			- num_rollouts: 8 instead of 30
			- rollouts_used: 4 instead of 30
			- noise_size: 25000000 instead of 250000000
			- eval_prob: 0.5 instead of 0.09

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. It gave an error due to the limits of the action space but after many iterations
		2. It was just decreasing
	

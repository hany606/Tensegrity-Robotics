# Train 25
	
	- Describtion: v4.5.1.0 from the training (1,000,000 timesteps, 10 workers)
		Observation_space: current_length+end_point
		Hyper-paramters (changes):
			- num_rollouts: 8 instead of 30
			- rollouts_used: 4 instead of 30
			- noise_size: 25000000 instead of 250000000
			- eval_prob: 0.5 instead of 0.09

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. It gave error for the action is out of the limits
		2. It was decreasing then started to increase again then in the end decreased again.

# Train 33
	
	- Describtion: v4.3.2.0 from the training (1,000,000 timesteps, 10 workers) (Repeated train33)
		Observation_space: rest_length
		Hyper-parameters have been changed:
			- num_rollouts: 50 instead of 30
			- sgd_stepsize: 0.03 instead of 0.01
			- eval_prob: 0.5 instead of 0.09

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. The same behaviour as train33

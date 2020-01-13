# Train 27
	
	- Describtion: v4.3.1.1 from the training (1,000,000 timesteps, 10 workers) (Repeated trian23)
		Observation_space: rest_length
		Hyper-parameters have been changed:
			- num_rollouts: 50 instead of 30
			- sgd_stepsize: 0.03 instead of 0.01
			- eval_prob: 0.5 instead of 0.09

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. It gave an error due to the limits of the action space, after 238,294/1,000,000 timesteps with 25 iteration
		2. Unfortunately, it wasn't successfull as train23. It started as usual for increasing then reach the maximum then settle near that 300-400
	- TODO:
		* Try to repeat the same experiment
		* Increase the limits of the action_space

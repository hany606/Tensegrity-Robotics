# Train 29
	
	- Describtion: v4.3.1.2 from the training (1,000,000 timesteps, 10 workers) (Repeated trian23)
		Observation_space: rest_length
		Hyper-parameters have been changed:
			- num_rollouts: 50 instead of 30
			- sgd_stepsize: 0.03 instead of 0.01
			- eval_prob: 0.5 instead of 0.09

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. It gave an error due to the limits of the action space, after 570,945/1,000,000 timesteps with 28 iteration
		2. It is started with decreasing then increasing then jump to 1000 then decreasing till 740 but in the last two iterations it reached 80
	- TODO:
		* Try to repeat the same experiment
		* Increase the limits of the action_space

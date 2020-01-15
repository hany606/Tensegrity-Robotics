# Train 33
	
	- Describtion: v4.3.2.0 from the training (1,000,000 timesteps, 10 workers) (Repeated trian23 but after increasing the limits of the action_space)
		Observation_space: rest_length
		Hyper-parameters have been changed:
			- num_rollouts: 50 instead of 30
			- sgd_stepsize: 0.03 instead of 0.01
			- eval_prob: 0.5 instead of 0.09

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. It gave an error due to the limits of the action space, after 320,602/1,000,000 timesteps with 133 iteration
		2. It is started with decreasing then increasing then jump to 1000 then decreasing till 10 which is really bad
		3. Increasing the limits of the action_space increased the number of the iterations but unfortantely the iterations' rewards doesn't converge to increasing case.
	
	- TODO:
		- Understand the reason why this divergence
		- Implement control on the current_length and test.

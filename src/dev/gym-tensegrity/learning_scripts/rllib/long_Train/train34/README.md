# Train 34
	
	- Describtion: v4.6.2.0 from the training (1,000,000 timesteps, 10 workers)	(Repeated train26 but after increasing the limits of the action_space)
		Observation_space: rest_length
		Hyper-paramters (changes):
			- num_rollouts: 8 instead of 30
			- rollouts_used: 4 instead of 30
			- noise_size: 25000000 instead of 250000000
			- eval_prob: 0.5 instead of 0.09

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. It gave an error due to the limits of the action space, after 269,210/1,000,000 timesteps with 374 iteration
		2. It is started with decreasing then increasing then jump to 3000 then decreasing till 7 which is really bad
		3. Increasing the limits of the action_space increased the number of the iterations but unfortantely the iterations' rewards doesn't converge to increasing case.
	
	- TODO:
		- Understand the reason why this divergence
		- Implement control on the current_length and test.



# Train 17
	
	- Describtion: v3.1.1.0 from the training (1,000,000 timesteps, 10 workers)
		Changed the following parameter:
			- noise_size: 25000000 instead of 250000000
			- num_rollouts: 50 instead of 30
			- eval_prob: 0.5 instead of 0.09
	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. Unfortunately,  it started with maximum reward, then the rewards were decreasing, in the middle it start to increase again but then starts to decrease again.
		2. It gave error for the action is out of the limits and it finished 65%.
		3. But with increas in the eval_prob the timing increased.
		4. The rewards started better than train16 with 209 but it ended with worset situation with 58

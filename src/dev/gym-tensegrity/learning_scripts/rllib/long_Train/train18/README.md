# Train 18
	
	- Describtion: v3.2.1.0 from the training (1,000,000 timesteps, 10 workers)
		Changed the following parameter (it is being compared with the train 16's parameters [the initial]):
			- eval_prob: 0.5 instead of 0.09
			- sgd_stepsize: 0.03 instead of 0.01
	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. Unfortunately,  it started with maximum reward, then the rewards were decreasing, in the middle it start to increase again but then starts to decrease again.
		2. It gave error for the action is out of the limits and it finished 65%.
		3. The rewards started better than train17 with 247 but it ended with worset situation with 49

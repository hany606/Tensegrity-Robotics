# Train 21
	
	- Describtion: v4.2.1.0 from the training (1,000,000 timesteps, 10 workers)
		Observation_space: current_length+end_point (the default is end_points starting from v3...)

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. It gave error for the action is out of the limits
		2. The rewards were decreasing in the general trend, it was fluctating up and down in the region of [80-60] but in general it was decreasing.

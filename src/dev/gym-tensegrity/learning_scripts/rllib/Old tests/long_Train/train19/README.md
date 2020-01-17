# Train 19
	
	- Describtion: v4.0.1.0 from the training (1,000,000 timesteps, 10 workers)
		After change add the feature to enable the addition more observation as options for the user.
		There is no changing in the hyper-parameters but I changed the observation space to rest_length as train3 and it is descendants to see if the change in the reward function that make the training worse or not?
		Observation_space: rest_length (the default is end_points starting from v3...

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. The rewards were increasing to the better until it reached 449 but still is not enough

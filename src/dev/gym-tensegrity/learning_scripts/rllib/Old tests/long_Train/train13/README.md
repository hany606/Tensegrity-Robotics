# Train 13
	
	- Describtion: v2.0.1.1 from the training (repeated train 12 and 500,000 timesteps as well)
		After I have added the reduction reward in the termination part but nothing changed in the learning process in general
	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. The problem of the longer iteration is the last appeared again.
		2. There are many nan length for the episode.
		3. After looking again for the episodes, the iterations tha have episode_len_mean = nan is not having real reward it is written just the reward of the previous ones.

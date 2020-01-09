# Train 4
	
	- Describtion: v1.0.1.1 from the training (repeated train 3 and 500,000 timesteps as well)

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. No erros but the number of the timesteps is completed and more it is 1058,609/500,000 and only 54 iteration not 68 like train3 and it was training for 82 minutes not 52 like train3
		2. Only the last iteration was running more than the other by big difference 740496 timesteps = 2299 sec and the rest were in the range of [1000, 10000] 
		3. The flag is True this time for the last iteration which has many differences
		4. Some iterations have episode_reward_mean = nan
		5. Max reward of the mean rewards of the episodes in the iteration = 631.86, the average = 403.115, the minimum = 212.2		
	s- TODO:
		* Run again the experiment
		* Explain the flag and the iteration with episode_len_mean = nan

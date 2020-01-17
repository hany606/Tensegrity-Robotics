# Train 10
	
	- Describtion: v1.0.1.3 from the training (repeated train 3 and 500,000 timesteps as well)
		I repeated this training as repeated version for train3, train4, train5 after the failures of the other modifications of the hyperparameters as I thought that maybe there will be some errors in the environment from changes I made, but it appeared that it is not about the environment.

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. (The same issue as train4) No erros but the number of the timesteps is completed and more it is 1,157,120/500,000 and only 40 iteration not 68 like train3 and it was training for 138.79 minutes not 52 like train3
		2. (The same issue as train4) Only the last iteration was running more than the other by big difference 1005346 timesteps = 6135.04 sec and the rest were in the range of [1000, 10000] timesteps
		3. (The same issue as train4 and train3 too) The flag is True this time for the last iteration which has many differences
		4. (The same issue as train4) Some iterations have episode_reward_mean = nan
		5. Max reward of the mean rewards of the episodes in the iteration = 697.1305, the average = 448.6, the minimum = 231.63		
		6. The rewards started with big value then decreased then back to increase again in the end.

	s- TODO:
		* Explain the flag and the iterations with episode_len_mean = nan
		* Understand why the last iteration its flag is true
		* Test with the same parameters for defined long timesteps

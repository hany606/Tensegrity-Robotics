# Train 6
	
	- Describtion: v1.0.2.0 from the training (repeated train 3 but longer for 1,000,000 timesteps)

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		2. (The same issue as train4) Only the last iteration was running more than the other by big difference 1004384 timesteps = 3244.041 sec and the rest were in the range of [1000, 10000] timesteps
		3. (The same issue as train4) The flag is True this time for the last iteration which has many differences
		4. (The same issue as train4) Some iterations have episode_reward_mean = nan
		5. Max reward of the mean rewards of the episodes in the iteration = 641.7562, the average = 477.3705833, the minimum = 304.60452		
		6. 60 Iterations for the 1,000,000 timesteps
		7. The maximum rewards, the average, and the minimum didn't change much fromo (train3,4,5) by having the double time for the training.
	- TODO:
		* Explain the flag and the iterations with episode_len_mean = nan -> Unknown behaviour until now
		* Test with different paramters for the defined timesteps (500,000)

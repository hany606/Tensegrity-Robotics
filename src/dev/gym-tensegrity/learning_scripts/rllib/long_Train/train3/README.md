# Train 3
	
	- Describtion: v1.0.1.0 from the training (500,000 timesteps as train1 and train2)
		The change:
			- Change the reward functions to have survival reward not proportional with the time and only count the reward when the model reach the ground after the falling

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:

		1. The Experiment finished successfully not like the previous ones train1(v0.0.1.0), train2(v0.0.1.1).
			Conclusion: I don't really know the reason why it doesn't crash because of the exceeding the limits of the action space like the previous ones, but I will repeat this training again to find out if it will repeat or not.

		2. It was much faster than the previous ones (they took approxmitly 2.5 hours and they didn't finished) and this took 51 minutes with 68 iteration and each iteration has 30 episodes.
			Conclusion: as the previous experiments were with wrong reward function, they had to open and close fast to get good rewards as part of the experiment which led to long time to open the simulation every time as the iteration have specific length and the number of times to open the simulator was more in the train1 and train2.

		3. The mean length of the episodes is now proprtional with the mean reward, but still there are some episodes have mean of length equal to nan.
		
		4. Some iterations have episode_reward_mean = nan		
		
		5. Max reward of the mean rewards of the episodes in the iteration = 661.0762, the average = 496.675, the minimum = 192.91734
		
		6. The rewards were increasing to 648 then up and down in good reward range [620, 661]
		

	s- TODO:
		* Explain (N.3)

# Train 2
	
	- Describtion: v0.0.1.1 from the training (Rerun the experiment "Train1" v.0.0.1.1)

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:

		1. (same as "Train1") The experiment did not finish due to error in the generated action as it is out of limits as it is described inside the experiment folder -> "error.txt"

		2. The done flag is always for all the episodes is false
			Conclusion: The done flag is not updated when the episode is terminated by the termination criteria. (internal from the library)

		3. (same as "Train1") Some episodes have "nan" in the "episode_len_mean".
		
		4. The early episodes with high negative rewards are the longest "episode_len_mean"
			Conclusion: the reward function count the rewards while droping from the air, thus the rewards is high positive quantity when there is no change in cables and finish the episode as fast as possibl, and the reward is less negative quantity when the angle is changed a little bit and then terminate the episode and here is getting more rewards.
			The assumed behaviour of learning, the model discover that changing the lengths of the cables in the begining of the episode return less rewards (high negative quantity) and it learns to not change the angle much and before landing terminate the episode by making the angle more than the threshold, then the episode terminates.
			
		5. "time_this_iter_s" and "timesteps_this_iter" are not correlating with each other, they should be proportionally increasing or decreasing together, but this is not the case. If I understand the meaning of them correctly.


	- TODO:
		* Why the library generates an action is not in the limits of the action space? (N.1)
		* Why some episodes have len_mean = nan? (N.3)

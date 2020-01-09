# Train 1
	
	- Describtion: v0.0.1.0 from the training.

	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:

		1. The experiment did not finish due to error in the generated action as it is out of limits as it is described inside the experiment folder -> "error.txt"

		2. The done flag is always for all the episodes is false:
			if it is indeed false, this means:
				a. The termination criteria is not working proberly. (but it has been tested and working with no problems)
				b. Or the done flag is not updated when the episode is terminated by the termination criteria. (internal from the library)

		3. Some episodes have "nan" in the "episode_len_mean".
		
		4. The early episodes with high negative rewards are the longest "episode_len_mean"

		5. "time_this_iter_s" and "timesteps_this_iter" are not correlating with each other, they should be proportionally increasing or decreasing together, but this is not the case. If I understand the meaning of them correctly.

	- TODO:
		* Why the library generates an action is not in the limits of the action space? (N.1)
		* Explain (N.5).
		* Why some episodes have len_mean = nan? (N.3)
		* Understand the progress summary more!

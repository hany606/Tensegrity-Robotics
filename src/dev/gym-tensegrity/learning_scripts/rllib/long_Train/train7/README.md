# Train 7

	- Describtion: v1.1.1.0 from the training Changing the parameters not like train3 (v1.0.1.0)

	- Parameters is described inside the experiment folder -> "params.json"
		The only change in the noise stddev from 0.02 to 0.5

	- Notes:
		1. The training didn't finish as the same errors appeared in train1 and train2 for the execeeding in the action_space limits
		2. This time there was no successfull iteration this error happened before finishing the first iteration unlike the train1, train2 that have some number of successfull iterations then the error of exceeding the limits of the action_space
		
	- TODO:
		* Understand the behaviour of the library to generate this problem, maybe from our environment (but we define the action_space and the library should get the limits from the action_space), this error maybe because the algorithm is based on random search and reached to the limits for the change.
		* Test with different paramters for the defined timesteps (500,000)

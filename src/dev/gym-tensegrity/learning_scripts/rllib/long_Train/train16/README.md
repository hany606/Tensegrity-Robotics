# Train 16
	
	- Describtion: v3.0.2.0 from the training (Repeated train15 but instead of 500,000 it is 1,000,000 and with 10 workers after fixing the parallelization)
		train15 took ~= 80 minutes, this gave an error but finished 70% in 25 minutes
	- Parameters is described inside the experiment folder -> "params.json"

	- Notes:
		1. Unfortunately,  it started with maximum reward, then the rewards were decreasing.
		2. It gave error for the action is out of the limits but finished 70%

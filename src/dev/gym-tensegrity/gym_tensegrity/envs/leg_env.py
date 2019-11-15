"""leg_env.py: Create the gym custom environment of tensegrity leg"""
__author__ = "Hany Hamed"
__credits__ = ["Hany Hamed", "Prof. Sergie Savin"]
__version__ = "3.0.0"
__email__ = "h.hamed.elanwar@gmail.com / h.hamed@innopolis.university"
__status__ = "Testing"

# ----------------------------------------------------------------------------------------
# Problems that undetermined: [TODO]
# 1). A small action (dl=0.1) give multiple sequence of observation.
#       - [Done] Solution 1: Give the last observation.        [The implemented one]
#       - Solution 2: Give all the sequence of observation.
# 2). Action space is too big and we need to reforumlate it.    
#       - [Done] Solution  : Descirbed in the comments above the corressponding part.
# 3). Should we add got stuck for reward and observation or not????
# 4). close and reset not working properly, they destroy the port number
#       - Make text file with the place of the app of the simulator that every time, both of them read the number and simulator increase the number and this is the number of the port
# 5). We need to remove the upper rods in the holding box as they resist the rods sometimes
#       we will need to change any number of 19 in the whole system
# 6). Add some colors to the model of the world in the simulator
# 7). TODO easy: add stuck flag to the sent json from the simulator
# 8). easy TODO: change the unmodifable "immutable" objects to tuple instead of list because of the concept.
#
# 9). [Done] should be easy TODO [Done] I had to write here the LegModel as it is not installed and copied with the LegEnv
# 10). [Done] change the name of the gym to gym-tensegrity and gym_tensegrity but the env is leg as it is
# 11). TODO [Done]: Change the testing functions to the new action_space and observation_space modifications
# 12). TODO [Done]: Implement new observation_space that will work with stable_baselines
# 13). TODO :add the enabled actuators
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# Modifications from previous version:
# 1). Less number of observations: cable_lengths and end_effector position
# 2). Efficient reward function
# 3). More goals
# ----------------------------------------------------------------------------------------






# This file will contain all the information about the agent and the environment starting from the rendering of the GUI to the rewards,... etc.
import os
import time
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import sys
import scipy.spatial as ss
import signal
from math import floor,log2
from random import randint
import logging
from tqdm import tqdm

# logger = logging.getLogger(__name__)

import numpy as np
import math
from gym_tensegrity.envs.leg_model import LegModel

sim_exec = '/home/hany/repos/Work/IU/Tensegrity/Tensegrity-Robotics/src/dev/legz/python_communication_test/helper.sh'


class LegEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, host_name='localhost', port_num=10037, sim_exec=sim_exec,  dl=0.1):
        super(LegEnv, self).__init__()
        # Agent self variables
        self.goal = self._generateGoal()
        self.max_time = 200
        self.max_cable_length = 100
        self.min_coordinate_point = -500
        self.max_coordinate_point = 500
        self.dl = dl
        self.initial_volume = 12464.22707673338 # By testing
        self.collapsed_volume = 10500
        
        # self.enabled_actuators_list = [] # TODO: for now it will take the first (enabled_actuators_num) as enabled
        # self.enabled_actuators_num =  10   # TODO: in future it will be the length of the list


        # Initial configuration for the leg
        # TODO [Done]:
        #   -setup the leg; initialization, communication, start, and set the variables
        #   -Set the initial goal
        # Creation of the environment and pass the initial configuration
        # TODO: [Done]
        self.env = LegModel(host_name=host_name, port_num=port_num, sim_exec=sim_exec, dl=dl)
        self.env.startSimulator()


        # Example: self.env = Viewer(goal=self.goal)

        # Put the details of the action and observation spaces
        # TODO: [Done]
        #   - action_space  [Done]
        #   - observation_space [Done]
        # Solution 1 for action_space: put the dimension for all permutation that can be happen
        # n_actions = 3**60  #180 #TODO [Done]: this is not the correct action_space, it should be 3^60 to get all the possible combination for the cables trit; for each controller (bit but has 3 values)
        # n_actions = 2**(1+self.env.controllers_num)
        # n_actions = 2**(1+self.enabled_actuators_num)
        # self.action_space = spaces.Discrete(n_actions)  # 180 discrete actions = 3 (+/0/-) for each actuator (60)
        n_actions = 2**(floor(log2(self.env.controllers_num))+1)     # bits that represent the binary number for the index of the controller and an extra bit for the action 0 = decrease, 1 = increase
        self.action_space = spaces.Discrete(n_actions)
        #  Solution 2 for action_space:
        # self.action_space = spaces.MultiDiscrete([3 for i in range(self.env.controllers_num)])
        # TODO: Take into consideration the static cables and rods that are made to make the structure rigid
        #           they should be exculeded from the construction
        # Observations:
        #   - The dimensions is specified above and their min. and max. values
        #   1- Time
        #   2- Cables' lengths
        #   3- Endpoints of rods (include the end_effector)
        # self.observation_space = spaces.Tuple((
        #                         spaces.Box(low=0, high=self.max_time, shape=(1,), dtype=np.float16),
        #                         spaces.Box(low=0, high=self.max_cable_length, shape=(self.env.controllers_num,), dtype=np.float16),
        #                         spaces.Box(low=self.min_coordinate_point, high=self.max_coordinate_point, shape=(self.env.rods_num,3), dtype=np.float16)))
        # self.observation_space = spaces.Box(0, self.max_time, dtype=np.float32)

        # low = np.array([0])
        low = np.empty((1,0))
        low = np.append(low, np.zeros(self.env.controllers_num))
        low = np.append(low, np.full((1,1*3), self.min_coordinate_point))

        # high = np.array([self.max_time])
        high = np.empty((1,0))
        high = np.append(high, np.full((1,self.env.controllers_num), self.max_cable_length))
        high = np.append(high, np.full((1,1*3), self.max_coordinate_point))
 
        self.observation_space = spaces.Box(low= low, high= high, dtype=np.float32)
        
        # wrong as we have array of array in the end points(array) and cable lengths, it will need modification
        # low = np.array([
        #     0,
        #     0,
        #     self.min_coordinate_point])
        
        # high = np.array([
        #     self.max_time,
        #     self.max_cable_length,
        #     self.max_coordinate_point])

        # self.observation_space = spaces.Box(low, high, dtype=np.float32)

    def __del__(self):
        self.env.closeSimulator()
            
    # TODO: for now it is static goal
    #           for next is to implement a random goal and validate that it is reachable and in the working space of the end_effector
    # TODO [Done]: add a reachable static goal
    def _generateGoal(self):
        # goals_list = [[-4.90788472695319, 30.659340405658163, 20.34403515302529], [2.97824165453316, 31.33049026107478, 17.861001290043923], [1.4136693755786798, 31.499813150034896, 16.606912752880433]
        #              ,[0.4645273520267196, 31.496780841999787, 17.45188464368201], [1.2149685162614747, 31.468973724514743, 17.53062204869115], [2.250587954426667, 31.374870786715434, 17.694322530240672], [2.590934811462036, 31.344966748265506, 17.07491102530864], [1.9977469804168453, 31.40289128535907, 16.819529930489157], [2.1668521460857275, 31.39766588647915, 16.638145190778037]
        #              ,[1.4660883200259156, 31.46322853200669, 17.641054296127002], [3.471017736355414, 31.271620327895555, 17.559974005719603], [3.328242357679702, 31.321375314882886, 17.232646820364778]
        #              ,[0.08018639051563137, 31.50174457589494, 17.311991683859787], [2.2558169016417233, 31.373286258928225, 17.378835618686978], [1.7791511869136034, 31.33638921726763, 16.64860218335101]
        #              ]
        goals_list = [[2.97824165453316, 31.33049026107478, 17.861001290043923], [1.4136693755786798, 31.499813150034896, 16.606912752880433]
                ,[1.2149685162614747, 31.468973724514743, 17.53062204869115], [2.250587954426667, 31.374870786715434, 17.694322530240672], [2.590934811462036, 31.344966748265506, 17.07491102530864], [1.9977469804168453, 31.40289128535907, 16.819529930489157], [2.1668521460857275, 31.39766588647915, 16.638145190778037]
                ,[3.471017736355414, 31.271620327895555, 17.559974005719603], [3.328242357679702, 31.321375314882886, 17.232646820364778]
                ,[2.2558169016417233, 31.373286258928225, 17.378835618686978], [1.7791511869136034, 31.33638921726763, 16.64860218335101]
                ,[-0.24820994322445333, 31.46403608819641, 16.484511021079662], [1.153962970071699, 31.47863168091707, 16.448772054282166], [2.311731091168423, 31.441481673058604, 17.104274187674278], [1.1939904118684408, 31.501890344632237, 16.53664005922137], [7.071610490590869, 30.03270532495126, 20.17138229086633], [6.627329737305608, 30.088565900954148, 19.98992483653202], [1.7907500169631358, 31.396294439638154, 16.984882565083534], [1.4313399675059526, 31.402756297639236, 16.138577674559553], [2.17528462169328, 31.465917114576172, 16.606455338224407], [1.7840903763800056, 31.498419797748454, 16.125512168208964], [7.206571227410114, 30.007713451522307, 19.93930439215521], [7.065678333602399, 30.004320585789564, 19.596821526799637], [-0.5024839003555412, 31.47168621635042, 17.80669299054103], [-1.4752215842908063, 31.423473430925405, 17.151014920898728], [2.471509287004101, 31.370221112017806, 17.08222371571102], [2.5001591927530282, 31.340267531671916, 16.349782716335316], [2.933624315044942, 31.321837656124927, 16.971696926285976], [2.0749073407423824, 31.386172286098272, 16.261357193285207], [1.4826408481792046, 31.468626441417307, 17.500187461476827], [1.6737504371850425, 31.45432028465872, 17.10024041347118], [1.2506907893870054, 31.48640890161839, 17.02470710590071], [0.42826657314035477, 31.495990990208654, 16.704516212889818], [2.751325239108734, 31.356810890434183, 17.070873527508162], [3.155985828159218, 31.29246224665677, 16.0443838197099], [1.9289185711384202, 31.45436154113823, 17.33650280835189], [2.4264072671423675, 31.425766435143295, 17.124946408928615], [2.1152917672760627, 31.380012727715627, 17.251143740309995], [1.2481359600830984, 31.483869049421482, 17.14072077164593], [3.1155994888166116, 31.24121386972577, 17.416203222683944], [2.924265906096255, 31.270773276698726, 16.711808720848833], [2.7502353108441477, 31.306481790092924, 16.706809904619753], [2.6084352399551745, 31.330839092114743, 16.031343007945548], [1.4037911489798478, 31.501259357069756, 17.307320045767845], [2.2401160732772842, 31.42455884910961, 16.698387248718355], [2.30293815648432, 31.375000447261606, 17.929025292138824], [1.6253998379873953, 31.425555926436864, 17.613639152275613], [3.4285039515212983, 31.256959798740176, 17.45407359476367], [2.2845739670272485, 31.37067297006818, 16.701579686618988], [3.1993294116046753, 31.319387986424665, 17.342112384747654], [1.5511635649716284, 31.49972756513146, 16.870180391561245], [-1.9561490041383185, 31.38561104359016, 16.634179050936723], [0.5926256058290323, 31.49964253673539, 16.92229438415746], [3.2570234194145966, 31.2750548957464, 17.37458458081856], [3.2792385176328196, 31.28091365042832, 16.82447114533511], [3.4583606326494016, 30.69354021197401, 17.90053860771577], [3.087037891064045, 30.816550261386432, 17.167312080805505], [2.1202126983321055, 31.38434535785115, 17.59291882978781], [1.5674371058047822, 31.443160183690424, 16.97518701973333], [1.8114101138196204, 31.390806944630967, 17.355326610166358], [1.0957098827884104, 31.42680532951126, 16.552681560719844], [2.474947817531458, 31.39706832382849, 17.205994772316625], [2.9440314402906345, 31.3194091557066, 16.938315259403584], [1.8747255184460658, 31.366641899113958, 16.34194196182542], [0.8962461380395066, 31.451864007281117, 16.447071784937997], [1.7208303679839068, 31.48679975665229, 16.90837108285275], [1.3179925341902123, 31.498956971820668, 16.221434695416807], [2.9660017894944732, 31.297884987022734, 17.562370921216974], [1.8507165553437503, 31.476154500303494, 16.876006137136304], [3.092788211486754, 31.313444186950413, 17.19079116593975], [2.56201207115347, 31.34570161473792, 17.163632690093564], [2.288417700848502, 31.437654315344016, 17.291094935583853], [2.314177963903535, 31.397953581663835, 16.68855122038505], [2.423830090245007, 31.377652438504615, 16.919599500327838], [1.741460885750657, 31.372694347705163, 15.904134674085487], [4.651048673075907, 30.890591393398736, 17.43950575695186], [4.3924183687073866, 30.938651866211757, 16.50827304146944], [3.617322991937656, 31.277255613367196, 17.51688063942475], [2.815201458065683, 31.349182741123087, 16.994004107714414], [-0.10141249150571174, 31.492542230668704, 17.098660873072113], [0.5009021633238261, 31.497893657899066, 16.288959590674136], [3.414747498768025, 31.208131096782463, 16.83989871283273], [3.0430224748304333, 31.237675505641384, 16.50667362348721], [3.3320063448039883, 31.2014308367424, 16.955633129666346], [2.1564548088416555, 31.316963861230334, 16.29530376923983], [-1.3574900242248429, 31.399768054916745, 16.725762237630214], [0.8323208140305336, 31.500714444242178, 16.7645608083383], [0.8031476584433492, 31.484273785341955, 17.74034380530544], [1.126559825755508, 31.49908612342452, 17.20474801301854], [1.6421502716418865, 31.487305583231148, 17.398775512840835], [1.0765258321189515, 31.500085160403636, 16.77351759614331], [0.5860334197730219, 31.49645123625529, 17.659076585630505], [0.9791361955140583, 31.49118825374842, 17.33835490395335], [2.7120482168623097, 31.385701898485298, 17.26763007283541], [1.987781048480385, 31.42634768533432, 17.28284170490482], [3.189840807791917, 31.30316807725167, 17.264321625392814], [3.4123232760575526, 31.24690932265125, 16.99995905094378], [3.3516223884977454, 31.298998701681214, 17.695872886145295], [1.3785638971149448, 31.49970628374629, 16.76880629252987], [2.829044755889323, 31.310989425104523, 17.379322109363944], [2.5541248610309766, 31.323946221372488, 16.878050149956234], [0.8894032203535279, 31.494787694545998, 17.59118565245162], [1.1396604362429996, 31.484817910375455, 17.200338183976992], [6.308463704372718, 30.30124384940487, 20.10282689272334], [5.184565640227199, 30.558590148116714, 20.092102693192636], [2.7226209636987804, 31.24918086883475, 17.34518431704796], [2.019913893275798, 31.332748962355673, 16.942241219425004], [5.7289384129711225, 30.428964925434734, 13.7356351862254], [5.362843385855543, 30.48004082762812, 13.508484643549496], [2.0463388174848243, 31.44858996785382, 17.28857686946192], [1.1913663599586446, 31.49233780359464, 16.706535390400912]]

        # return (4.252820907910812, 11.42265959555328, -3.1326669704587604)  # Reachable point by the cms of the end-effector rod when the 2nd controller is decreased to 17.1468
        # return (-4.071894028029348, 30.865273129264445, 14.268032968387198)
        random_index = randint(0,len(goals_list)-1)
        return goals_list[random_index]    # Reachable point by the cms of the end-effector rod when the 2nd controller is increased by 50*dl

    def step(self, action):
        """
        Parameters
        ----------
        action :

        Returns
        -------
        observation, reward, episode_over(done), info : tuple
            observation (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        # TODO [Done]: change the controller simulator to read and take the action then write the data of the observations
        #           reverse the order of TCP to read the observation of the corresponding action not the previouse one
        self._takeAction(action)
        observation = self._getObservation()
        reward = self._getReward(observation)
        done = self._isDone()
        return observation, reward, done, {}

    # Actions [0,180):
    #   - 3 possible actions for each controller
    #   0+(3*index) -> -1 -> decrease by dl
    #   1+(3*index) ->  0 -> stay the same
    #   2+(3*index) -> +1 -> increase by dl
    def _takeAction(self, action):
        # pass  
        # # Solution 2: Working but not with stable_baseline 
        # # [Feature not implemented yet in their library to have tuple of actions in the action space]
        # # More details about their problem: https://github.com/hill-a/stable-baselines/issues/133
        # # TODO [Done]: put the scheme of the actions for the leg [Done]
        # # TODO [Done]: test !!!
        # # TODO [Done]: chage it according to the new scheme
        # for i in range(self.env.controllers_num):
        #     value = (action[i]-1)*self.dl
        #     self.env.actions_json["Controllers_val"][i] = value
        
        # # if it was zero means that it will be decreased by dl, if it was 1 will be the same, if it was 2 it will be increased
        # self.env.step()
        # # TODO [Done]: wait until the done_flag is set [Done from the side of the simulator]
        
        # Solution 1: Under testing
        # MSB - LSB
        # Each controller has 2 bits:
        #   if the bits 00 = 0 it will mean decrease by dl
        #   if the bits 01 = 1 it will mean stay the same
        #   if the bits 10 = 2 it will mean increase by dl
        #   if the bits 11 = 3 it will mean increase by dl  ? Redundacy in the actions (wasting) Will it make problems in the learning process?
        # for i in range(0, 2*self.env.controllers_num, 2):
        #     value = (1 if (2**i & action) > 0 else 0) + (2 if (2**(i+1) & action) > 0 else 0)
        #     value = min(value, 2) - 1
        #     self.env.actions_json["Controllers_val"][i] = value**self.dl
        # for i in range(self.enabled_actuators_num//2):
        #     box_start_index = i*2
        #     value = (1 if (2**box_start_index & action) > 0 else 0) + (2 if (2**(box_start_index+1) & action) > 0 else 0) + (4 if (2**(box_start_index+2) & action) > 0 else 0)
        #     # print(value, box_start_index)
        #     if (value == 0):
        #         self.env.actions_json["Controllers_val"][box_start_index] = 1
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = 0
        #     elif (value == 1):
        #         self.env.actions_json["Controllers_val"][box_start_index] = -1
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = 0
        #     elif (value == 2):
        #         self.env.actions_json["Controllers_val"][box_start_index] = 0
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = 1
        #     elif (value == 3):
        #         self.env.actions_json["Controllers_val"][box_start_index] = 1
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = 1
        #     elif (value == 4):
        #         self.env.actions_json["Controllers_val"][box_start_index] = -1
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = 1
        #     elif (value == 5):
        #         self.env.actions_json["Controllers_val"][box_start_index] = 0
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = -1
        #     elif (value == 6):
        #         self.env.actions_json["Controllers_val"][box_start_index] = 1
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = -1
        #     elif (value == 7):
        #         self.env.actions_json["Controllers_val"][box_start_index] = -1
        #         self.env.actions_json["Controllers_val"][box_start_index+1] = -1
        #     self.env.actions_json["Controllers_val"][box_start_index] *= self.dl
        #     self.env.actions_json["Controllers_val"][box_start_index+1] *= self.dl
        # self.env.step()
        bits_num = floor(log2(self.env.controllers_num))+1
        value_sign = (1 if ((2**bits_num) & action) > 0 else -1)    # if sign_bit is 0 = decrease, 1 = increase
        value = value_sign*self.dl
        # print(self.env.controllers_num)
        controller_index = min(self.env.controllers_num-1, action - (2**bits_num if value_sign == 1 else 0))
        # TODO: Don't know if it is necessary or not. Maybe here we can set all the controllers to zero and delete the last line in the method
        # print("Controllers_index {:} :::{:}, Controller_value: {:}".format(controller_index, action, value))
        
        self.env.actions_json["Controllers_val"][controller_index] = value
        self.env.step()
        self.env.actions_json["Controllers_val"][controller_index] = 0    # IF we comment that, this will enable the environment to operate simultanously actuators
        

    # Observations:
    #   - The dimensions is specified above and their min. and max. values
    #   1- Time
    #   2- Cables' lengths
    #   3- Endpoints of rods (include the end_effector)
    # TODO [Done]: conform the return with the new boundries shapes
    def _getObservation(self):
        # TODO[Done]: add the time passed in the observation as it can be used to calculate the reward
        # print(self.env.getTime())
        # observation = np.array(self.env.getTime())
        observation = np.empty((1,0))
        # print(observation)
        observation = np.append(observation, self.env.getCablesLengths())
        
        # end_points = self.env.getEndPoints()
        # end_points_flatten = []
        # # print("--------------")
        # # print(end_points)
        # for end_point_2 in end_points:
        #     for end_point in end_point_2:
        #         for pos in end_point:
        #             end_points_flatten.append(pos)

        # observation = np.append(observation, end_points_flatten)
        observation = np.append(observation, self.env.getEndEffector())
        # observation = [self.env.getTime(), self.env.getCablesLengths(), self.env.getEndPoints()]
        return np.array(observation)

    def _getReward(self, observation):
        # TODO [Done]:Set the reward criteria, which will depend on:
        #   - Euclidian distance between the end-effector and the target_point
        #   - The stability of the structure -> depends on the minimum volume of the structure when collapse
        #   - The time

        # Example:
        # end_effector = self.env.get_end_effector()
        # distance = math.sqrt((end_effector[0] - self.goal['x']) ** 2 + (end_effector[1] - self.goal['y']) ** 2)
        # print(distance)
        # if not(self.env.get_end_effector()[0] == self.goal['x'] and self.env.get_end_effector()[1] == self.goal['y']):
        # eps = 60
        # if distance < eps:
        #     return 100
        # return -max(int(distance / 100), 1)

        # return -0.1*self._getDistancetoGoal()-0.01*self.env.getTime()
        done_reward = 0
        if self._isDone():
            done_reward = 100
        distance = self._getDistancetoGoal()
        print("|| Error_Distance: {:} ||".format(distance))
        return -0.1*self._getDistancetoGoal()+ done_reward

    def _isDone(self):
        # TODO [Done]:
        #  The criteria for finish will be either
        #       - it collapsed or not
        #       - Reached the goal or near to it

        # Example:
        # end_effector = self.env.get_end_effector()
        # distance = math.sqrt((end_effector[0] - self.goal['x']) ** 2 + (end_effector[1] - self.goal['y']) ** 2)
        # # if not(self.env.get_end_effector()[0] == self.goal['x'] and self.env.get_end_effector()[1] == self.goal['y']):
        # eps = 60
        # if distance < eps:
        #     return 1

        # eps = 0.1
        eps = 0.8
        distance = self._getDistancetoGoal()
        
        # TODO [Done]: Implement either if it collapsed criteria
        collapsed = self._isCollapsed(self.env.getEndPoints())
        # print("Collapsed: ???: {:}".format(collapsed))
        if(distance <= eps or collapsed == True):
            return True
        return False

    def _getDistancetoGoal(self):
        end_effector = self.env.getEndEffector()
        MSE = 0
        for i in range(3):
            MSE += (end_effector[i] - self.goal[i])**2 
        distance = math.sqrt(MSE)
        return distance

    # TODO [Done]: Implement it
    # By calculating the volume and comparing with the volume that it is known when it collapsed
    #   or under specific threshold
    def _isCollapsed(self, points_raw):
        points = []
        for i in range(len(points_raw)):
            points.append(points_raw[i][0])
            points.append(points_raw[i][1])

        hull = ss.ConvexHull(points)
        # print("Volume: {:}".format(hull.volume))
        # Initial Volume by testing: 12464.22707673338
        eps = 500
        if(hull.volume - self.collapsed_volume <= eps):
            return True
        return False
    
    # TODO [Done]: Problem mentioned in the header
    def reset(self):
        # TODO [Done]:
        # Reset the state of the environment to an initial state, and the self vars to the initial values
        self.goal = self._generateGoal()
        # Reset the environment and the simulator
        self.env.reset()
        # get the observations after the resetting of the environment
        return self._getObservation()

    def render(self, mode='human'):
        # TODO:
        # Example:
        self.env.render()

    # TODO [Done]: Problem mentioned in the header
    def close(self):
        self.env.closeSimulator()
        # sys.exit(0)

def main():
    def print_observation(obs):
        print("Observations {:}".format(obs))
    env = LegEnv()
    action = 5+64
    init_obs ,_,_,_=env.step(action)
    print(env.env.actions_json)
    # print("")
    input("-> check point: WAIT for INPUT !!!!")
    for _ in range(50):
        observation, reward, done, _= env.step(action)
        print_observation(observation)
        print("Done:???:{:}".format(done))
    print(env.env.getEndEffector())
    # env.reset()
    # time.sleep(5)
    # env.close()
    # # print("")
    input("-> check point: WAIT for INPUT !!!!")
    for i in range(1000):
        action = env.action_space.sample()
        print("--------------- ({:}) ---------------".format(i))
        print("######\nAction: {:}\n######".format(action))
        observation, reward, done, _= env.step(action)
        print_observation(observation)
        # if(observation[0] > env.max_time):
        #     break
    action = 0
    final_obs ,_,_,_=env.step(action)
    print(env.env.actions_json)
    print(env.env.sim_json)
    input("-> check point: WAIT for INPUT !!!!")
    while(1):
        observation, reward, done, _= env.step(action)
        print_observation(observation)
        # print(env.env.getEndEffector())
        print("Done:???:{:}".format(done))

def generateGoal():
    def print_observation(obs):
        print("Observations {:}".format(obs))
    goals = []
    env = LegEnv()
    # action = 5+64
    for i in tqdm(range(50)):
        action = randint(0,127)
        # print("Action: {:}".format(action))
        init_obs ,_,_,_=env.step(action)
        # print(env.env.actions_json)
        # print("")
        # input("-> check point: WAIT for INPUT !!!!")
        for _ in tqdm(range(50)):
            observation, reward, done, _= env.step(action)
            # print_observation(observation)
            # print("Done:???:{:}".format(done))
        # print(env.env.getEndEffector())
        # goals.append(env.env.getEndEffector())
        # input("-> check point: WAIT for INPUT !!!!")
        for i in tqdm(range(1,1001)):
            action = env.action_space.sample()
            # print("--------------- ({:}) ---------------".format(i))
            # print("######\nAction: {:}\n######".format(action))
            observation, reward, done, _= env.step(action)
            # print_observation(observation)
            if(i % 500 == 0):
                # print("Add in the goals")
                # print(env.env.getEndEffector())
                goals.append(env.env.getEndEffector())

        env.reset()
    print(goals)



if __name__ == "__main__":
    generateGoal()

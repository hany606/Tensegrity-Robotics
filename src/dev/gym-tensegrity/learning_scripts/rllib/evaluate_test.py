# This code is being adapted from: https://github.com/ray-project/ray/blob/master/rllib/train.py
import argparse
import yaml
import json
from ray.tune.config_parser import make_parser
import gym
import gym_tensegrity
import ray
from ray import tune
import ray.rllib.agents.ars as ars
from ray.tune.logger import pretty_print



EXAMPLE_USAGE = """
Usage example via RLlib CLI:
    ./train.py -
"""
class Printer:
    def __init__(self,debug=1):
        self.debug_flag = debug

    def all(self, returns, num_episdoes=None):
        if(self.debug_flag):
            if(returns["observation"] is not None):
                self.observation(returns["observation"])
            if(returns["action"] is not None):
                self.action(returns["action"])
            if(returns["done"] is not None):
                self.done(returns["done"])
            if(returns["reward"] is not None):
                self.reward(returns["reward"])
            if(returns["history"] is not None):
                self.history(returns["history"])
            if(returns["mean"] is not None):
                self.mean(returns["mean"], num_episodes=num_episdoes)
    
    def observation(self, observation):
        if(self.debug_flag):
            print("Observations:")
            for obs in range(observation):
                print("{:}".format(obs),end="\t")
    
    def action(self, action):
        if(self.debug_flag):
            print("Actions:")
            for act in range(action):
                print("{:}".format(act),end="\t")
    
    def reward(self, reward):
        if(self.debug_flag):
            print("Reward: {:}".format(reward))

    def done(self, done):
        if(self.debug_flag):
            print("Termination: {:}".format(done))

    def history(self, history):
        if(self.debug_flag):
            print("History for {:} episodes:".format(len(history)))
            rewards = 0
            for i in range(len(history)):
                rewards += history[i]
                print("#Episode {:} -> {:}".format(i+1, history[i]),end="\n")
            self.mean(rewards/len(history))

    def mean(self, mean, num_episodes=None):
        if(self.debug_flag):
            print("The mean for the rewards for {:} episodes is {:}".format(num_episodes, mean))

class Evaluater:
    def __init__(self):
        self.printer = Printer()
        self.env_config = {}
        self.agent_config = {}
        self.evaluate_config = {}

    def create_parser(self, parser_creator=None):
        parser = make_parser(
            parser_creator=parser_creator,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Evaluate a trained RL agent.",
            epilog=EXAMPLE_USAGE)

        parser.add_argument(
            "--random-agent",
            default=False,
            type=bool,
            help="Evaluate and test an agent with random policy")

        parser.add_argument(
            "--evaluation-file",
            default=None,
            type=str,
            help="Path to the object file of the trained model." 
            "The file should be in the following format: checkpoint_<NUM>/checkpoint-<NUM>")

        parser.add_argument(
            "--agent-config-file",
            default=None,
            type=str,
            help="Path to the json configuration file of the trained model." 
            "The file should be in the following format: __.json")

        parser.add_argument(
            "--observation-space-type",
            default=["end_points", "end_points_velocities"],
            type=list,
            help="Set the observation space type to be one of those: [end_points, rest_length, current_length, end_points_velocities] or any option from them together in a form of a list")

        parser.add_argument(
            "--controller-type",
            default="rest_length_mod",
            type=str,
            help="Set the controller type to be one of those: [rest_length, current_length, rest_length_mod, current_length_mod]")
        
        parser.add_argument(
            "--num-episodes",
            default="10",
            type=int,
            help="Set the number of the episodes for the evaluation and running the model on")

        parser.add_argument(
            "-f",
            "--config-file",
            default=None,
            type=str,
            help="If specified, use config options from this file. Note that this "
            "overrides any trial-specific options set via flags above.")

        return parser


    def create_environment(self, env_config):
        import gym_tensegrity
        return gym.make('gym_tensegrity:jumper-v0', config=self.env_config)
        

    def run_episode(self, env, agent):
        observation = env.reset()
        self.printer.observation(observation)
        cumulative_reward = 0
        done  = False
        while not done:
            action = agent.compute_action(observation)
            #action = env.action_space.sample()
            observation, reward, done, _ = env.step(action)
            self.printer.observation(observation)
            self.printer.reward(reward)
            self.printer.action(action)
            self.printer.done(done)
            cumulative_reward += reward

        return cumulative_reward


    def evaluate(self, evaluate_config, agent_config):
        config = ars.DEFAULT_CONFIG.copy()
        for keys in config.keys():
            config[keys] = agent_config[keys]
        trained_agent = ars.ARSTrainer(config=config, env="jumper")
        env = self.create_environment("")
        cumulative_reward = 0
        history = []
        for _ in range(evaluate_config["num_episodes"]):
            reward = self.run_episode(env, trained_agent)
            history.append(reward)
            cumulative_reward += reward
 
        self.printer.history(history)
        self.printer.mean(cumulative_reward/evaluate_config["num_episdoes"])

    def run(self, args, parser):
        if args.config_file:
            with open(args.config_file) as f:
                self.evaluate_config = yaml.safe_load(f)
        else:
            self.evaluate_config = {
                "random_agent": args.random_agent,
                "evaluation_file": args.evaluation_dir,
                "agent-config-file": args.agent_config_file,
                "observation_space_type": args.evaluation_space_type,
                "controller_type": args.controller_type,
                "config_file": args.config_file,
                "num_episodes": args.num_episodes,
            }
        self.env_config = {"observation": self.evaluate_config["observation_space_type"], "control_type": self.evaluate_config["controller_type"]}
        tune.register_env("jumper", self.create_environment)
        ray.init()
        with open(self.evaluate_config["agent-config-file"]) as json_file:
            self.agent_config = json.load(json_file)
        self.evaluate(self.evaluate_config, self.agent_config)

if __name__ == "__main__":
    evaluate = Evaluater()
    parser = evaluate.create_parser()
    args = parser.parse_args()
    evaluate.run(args, parser)
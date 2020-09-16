import os
from jinja2 import Environment, FileSystemLoader
import yaml
import re

class taichi_converter():
	def __init__(self, file_path):
		DIR_PATH = os.path.dirname(os.path.realpath(__file__))
		env = Environment(loader=FileSystemLoader(DIR_PATH))
		template = env.get_template(file_path)
		c = template.render() ## user: {{name}} in yaml, and pass it in render
		config_vals = yaml.load(c)
		
		self.units_config = config_vals["units_config"]
		self.variables = config_vals["variables"]
		self.rods_config = config_vals["rods_config"]
		self.cables_config = config_vals["cables_config"]
		self.nodes = config_vals["nodes"]
		self.rods = config_vals["rods"]
		self.cables = config_vals["cables"]

		self._evaluate_variables()
		self._evaluate_nodes()

	def _evaluate_variables(self):
		for v in self.variables.keys():
			splitted = re.split('(\W)', str(self.variables[v]))
			for w in range(len(splitted)):
				if(splitted[w] in self.variables.keys()):
					splitted[w] = str(self.variables[splitted[w]])
			new_var = "".join(splitted)
			new_var = eval(new_var)
			self.variables[v] = new_var

	def _evaluate_nodes(self):
		for i in range(len(self.nodes)):
			for p in range(len(self.nodes[i]["pos"])):
				splitted_pos = re.split('(\W)', self.nodes[i]["pos"][p])
				for w in range(len(splitted_pos)):
					if(splitted_pos[w] in self.variables.keys()):
						splitted_pos[w] = str(self.variables[splitted_pos[w]])
				new_pos = "".join(splitted_pos)
				new_pos = eval(new_pos)
				self.nodes[i]["pos"][p] = new_pos


	def get_nodes_list(self):
		# return list of dictionaries that will have the same keys for the arguments of the classes
		pass

	def get_rods_list(self):
		pass

	def get_cables_list(self):
		pass


if __name__ == "__main__":
	tconv = taichi_converter("yaml_test.yaml")
	print(tconv.nodes)
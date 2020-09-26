import os
from jinja2 import Environment, FileSystemLoader, Template
import yaml
import re
from math import sqrt
import argparse
import os
import sys
class TensegrityFomratConverter():
	def __init__(self, file_path):
		DIR_PATH = os.path.dirname(os.path.realpath(__file__))
		env = Environment(loader=FileSystemLoader(DIR_PATH))
		template = env.get_template(file_path)
		c = template.render() ## user: {{name}} in yaml, and pass it in render
		config_vals = yaml.load(c)
		
		self.units_config = config_vals["units_config"]
		self.constants = config_vals["constants"]
		self.rods_config = config_vals["rods_config"]
		self.cables_config = config_vals["cables_config"]
		self.nodes = config_vals["nodes"]
		self.rods = config_vals["rods"]
		self.cables = config_vals["cables"]

		self._evaluate_configs()
		self._evaluate_constants()
		self._evaluate_nodes()
		self._evaluate_cables()



	def _evaluate_configs(self):
		self._config_name_to_idx = {"rod":{}, "cable":{}}
		for i, rc in enumerate(self.rods_config):
			self._config_name_to_idx["rod"][rc["name"]] = i

		for i, cc in enumerate(self.cables_config):
			self._config_name_to_idx["cable"][cc["name"]] = i

	def _evaluate_constants(self):
		for i,v in enumerate(self.constants.keys()):
			splitted = re.split(r'(\W)', str(self.constants[v]))
			for w in range(len(splitted)):
				if(splitted[w] in self.constants.keys()):
					splitted[w] = str(self.constants[splitted[w]])
			new_var = "".join(splitted)
			new_var = eval(new_var)
			self.constants[v] = new_var

	def _evaluate_nodes(self):
		for i in range(len(self.nodes)):
			for p in range(len(self.nodes[i]["pos"])):
				splitted_pos = re.split(r'(\W)', str(self.nodes[i]["pos"][p]))
				for w in range(len(splitted_pos)):
					if(splitted_pos[w] in self.constants.keys()):
						splitted_pos[w] = str(self.constants[splitted_pos[w]])
				new_pos = "".join(splitted_pos)
				new_pos = eval(new_pos)
				self.nodes[i]["pos"][p] = new_pos

	def _evaluate_cables(self):
		for i in range(len(self.cables)):
			splitted_length = re.split(r'(\W)', str(self.cables[i]["length"]))
			for w in range(len(splitted_length)):
				if(splitted_length[w] in self.constants.keys()):
					splitted_length[w] = str(self.constants[splitted_length[w]])
			new_length = "".join(splitted_length)
			new_length = eval(new_length)
			self.cables[i]["length"] = new_length

		for i in range(len(self.cables)):
			splitted_node1 = re.split(r'(\W)', str(self.cables[i]["node1"]))
			for w in range(len(splitted_node1)):
				if(splitted_node1[w] in self.constants.keys()):
					splitted_node1[w] = str(self.constants[splitted_node1[w]])
			new_node1 = "".join(splitted_node1)
			new_node1 = eval(new_node1)
			self.cables[i]["node1"] = new_node1

		for i in range(len(self.cables)):
			splitted_node2 = re.split(r'(\W)', str(self.cables[i]["node2"]))
			for w in range(len(splitted_node2)):
				if(splitted_node2[w] in self.constants.keys()):
					splitted_node2[w] = str(self.constants[splitted_node2[w]])
			new_node2 = "".join(splitted_node2)
			new_node2 = eval(new_node2)
			self.cables[i]["node2"] = new_node2



	def get_nodes_list(self):
		# return list of dictionaries that will have the same keys for the arguments of the classes
		pass

	def get_rods_list(self):
		pass

	def get_cables_list(self):
		pass

	def ntrtsim_converter(self, name="Simple", path="./", template_path="./templates"):
		def render_template_save(template_path, template_values, save_path):
			with open(template_path) as reader:
				template = Template(reader.read())
			rendered_template = template.render(template_values)
			with open(save_path, "+w") as writer:
				writer.write(rendered_template)
		
		def _generate_config_vars():
			output = ""
			nl = "\n\t\t"
			for c in self.rods_config:
				config_name = c["name"]
				output += f'double {config_name}_radius;{nl}double {config_name}_density;{nl}'
			for c in self.cables_config:
				config_name = c["name"]
				output += f'double {config_name}_stiffness;{nl}double {config_name}_damping;{nl}double {config_name}_pretension;{nl}double {config_name}_maxTension;{nl}double {config_name}_targetVelocity;{nl}'
			return output

		def _generate_config_values():
			output = ""
			nl = "\n\t\t"
			for c in self.rods_config:
				output += f'{c["radius"]},{nl}{c["density"]},{nl}'
			for c in self.cables_config:
				output += f'{c["stiffness"]},{nl}{c["damping"]},{nl}{c["pretension"]},{nl}{c["maxTension"]},{nl}{c["targetVelocity"]},{nl}'
			return output

		def _generate_add_nodes():
			output = ""
			nl = "\n\t"
			for n in self.nodes:
				pos = n["pos"]
				# y z x
				output += f's.addNode({pos[1]}, {pos[2]}, {pos[0]});{nl}'
			return output

		def _generate_add_rods():
			output = ""
			nl = "\n\t"
			for r in self.rods:
				output += f's.addPair({r["node1"]}, {r["node2"]}, "{r["config"]}");{nl}'
			return output

		def _generate_add_cables():
			output = ""
			nl = "\n\t"
			for c in self.cables:
				output += f's.addPair({c["node1"]}, {c["node2"]}, "{c["config"]}_muscle");{nl}'
			return output
		
		def _generate_config_objs():
			output = ""
			nl = "\n\t"
			for c in self.rods_config:
				config_name = c["name"]
				output += f'const tgRod::Config {config_name}_config({c["radius"]}, {c["density"]});{nl}'
				output += f'spec.addBuilder("{config_name}", new tgRodInfo({config_name}_config));{nl}'

			for c in self.cables_config:
				config_name = c["name"]
				output += f'const tgBasicActuator::Config {config_name}_muscle_config({c["stiffness"]}, {c["damping"]}, {c["pretension"]}, 0, {c["maxTension"]}, {c["targetVelocity"]});{nl}'
				output += f'spec.addBuilder("{config_name}_muscle", new tgBasicActuatorInfo({config_name}_muscle_config));{nl}'
			return output
			
		def _generate_rods_constraints():
			output = ""
			nl = "\n\t"
			for i,r in enumerate(self.rods):
				if(r["actuation"] == 0):
					output += f"rods[{i}]->getPRigidBody()->setCollisionFlags(rods[{i}]->getPRigidBody()->getCollisionFlags() | btCollisionObject::CF_STATIC_OBJECT);{nl}"
				elif(r["actuation"] == 1):
					output += f"rods[{i}]->getPRigidBody()->setCollisionFlags(rods[{i}]->getPRigidBody()->getCollisionFlags() | btCollisionObject::CF_NO_CONTACT_RESPONSE);{nl}"
			return output

		def _generate_endpoints_mapping():
			endpoints = [[] for i in range(len(self.nodes))]
			for i,c in enumerate(self.cables):
				endpoints[c["node1"]].append([i,0])
				endpoints[c["node2"]].append([i,1])

			output = f"int nodes_num = {len(self.nodes)};\n"
			output += f"int endpoints_mapping [{len(self.nodes)}][2] = " + "{"
			for p in endpoints:
				if(len(p) > 0):
					cable_index, endpoint_index = p[0]
					output += "{" + str(cable_index) + ", " +  str(endpoint_index) + "}, "
				else:
					output += "{-1, -1}, "
			output = output[:-2] + "};"
			return output

		if(path[-1] != "/"):
			path = path + "/"

		if(template_path[-1] != "/"):
			template_path = template_path + "/"
		
		name = name[0].upper() + name[1:]


		template_values_model_h = {"ModelName": name,
						   		   "NumRods": len(self.rods),
						   		   "NumCables": len(self.cables)}
		template_values_model_cpp = {
							"ModelName": name,
							"ConfigurationVars": _generate_config_vars(),
							"ConfigurationValues": _generate_config_values(),
							"AddNodes": _generate_add_nodes(),
							"AddRods": _generate_add_rods(),
							"AddCables": _generate_add_cables(),
							"ConfigurationObjects": _generate_config_objs(),
						  }
		template_values_app = {"ModelName": name, "AddRodsConstraints": _generate_rods_constraints()}

		render_template_save(template_path=f"{template_path}model_templateh.txt", template_values=template_values_model_h, save_path=path+name+"Model.h")
		render_template_save(template_path=f"{template_path}model_templatecpp.txt", template_values=template_values_model_cpp, save_path=path+name+"Model.cpp")
		render_template_save(template_path=f"{template_path}simple_controller_templateh.txt",template_values= {"ModelName": name}, save_path=path+"SimpleController.h")
		render_template_save(template_path=f"{template_path}simple_controller_templatecpp.txt",template_values= {"ModelName": name, "EndPointsMapping": _generate_endpoints_mapping()}, save_path=path+"SimpleController.cpp")
		render_template_save(template_path=f"{template_path}app_template.txt", template_values=template_values_app, save_path=path+f"App{name}Model.cpp")
		render_template_save(template_path=f"{template_path}cmake_lists_template.txt", template_values= {"ModelName": name}, save_path=path+"CMakeLists.txt")

		

	def taichi_converter(self, Node, Rod, Spring):
		nodes = []
		rods = []
		springs = []

		for n in self.nodes:
			pos = n["pos"]
			nodes.append(Node(x=pos[0], y=pos[1], z=pos[2], act=n["actuation"]))

		for r in self.rods:
			rods.append(Rod(a=r["node1"], b=r["node2"], stiffness=self.rods_config[self._config_name_to_idx["rod"][r["config"]]]["stiffness"]))

		for c in self.cables:
			# In order not to have an extra parameter in the yaml file
			# pos1 = c["node1"]
			# pos2 = c["node2"]
			# original_length = sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 + (pos1[2]-pos2[2])**2)
			# length = (original_length) + (self.cables_config[self._config_name_to_idx["cable"][c["config"]]]["pretension"]/self.cables_config[self._config_name_to_idx(c["config"])]["stiffness"])
			springs.append(Spring(a=c["node1"], b=c["node2"], length=c["length"], stiffness=self.cables_config[self._config_name_to_idx["cable"][c["config"]]]["stiffness"]))
			
		return nodes, rods, springs

if __name__ == "__main__":
	arg_parser = argparse.ArgumentParser(description='List the content of a folder')

	# Add the arguments
	arg_parser.add_argument('-p',
							'--path',
							type=str,
							default="./",
							help='the path to folder to store the project')

	arg_parser.add_argument('-n',
							'--name',
							type=str,
							default="simple",
							help='Name of the class of the project for the tensegrity strucutre')


	arg_parser.add_argument('-t',
							'--template-path',
							type=str,
							default="./templates",
							help='The path for the templates')
	
	args = arg_parser.parse_args()
	tconv = TensegrityFomratConverter("yaml_test.yaml")
	tconv.ntrtsim_converter(name=args.name, path=args.path, template_path=args.template_path)

	# from pprint import pprint
	# pprint(tconv.nodes)
	# pprint(tconv.rods)
	# pprint(tconv.cables)

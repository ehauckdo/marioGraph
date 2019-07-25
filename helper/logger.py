import logging

def init(obj, method_name):
	class_name = obj.__class__.__name__
	debug_string = "STARTED: object `{}` -> `{}`".format(class_name, method_name)
	logging.debug(debug_string)

def end(obj, method_name):
	class_name = obj.__class__.__name__
	debug_string = "FINISHED: object `{}` -> `{}`".format(class_name, method_name)
	logging.debug(debug_string)

def init_m(module, method_name):
	module = module.split("/")[-1]
	debug_string = "STARTED: module `{}` -> `{}`".format(module, method_name)
	logging.debug(debug_string)

def end_m(module, method_name):
	module = module.split("/")[-1]
	debug_string = "FINISHD: module `{}` -> `{}`".format(module, method_name)
	logging.debug(debug_string)
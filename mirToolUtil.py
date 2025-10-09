import maya.cmds as cmds

def create_object(obj_type: str, name: str = None):

	if not name:
		name = obj_type

	if obj_type == "cube":
		cmds.polyCube(name=name)
	elif obj_type == "cone":
		cmds.polyCone(name=name)
	elif obj_type == "sphere":
		cmds.polySphere(name=name)
	elif obj_type == "torus":
		cmds.polyTorus(name=name)
	else:
		cmds.warning(f"Unknown object type: {obj_type}")

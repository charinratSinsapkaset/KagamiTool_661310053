# mirrorUtil.py
import maya.cmds as cmds
from maya import mel

def mirror(axis="+X"):
	"""ทำงานเหมือน mirrorPlusX(), mirrorMinusX() ฯลฯ"""
	sel = cmds.ls(sl=True, tr=True)
	if not sel:
		cmds.warning("-- INFO -- No object selected! Select the mesh object (Mirror result)!")
		return

	if len(sel) > 1:
		cmds.warning("-- INFO -- Please select only ONE mesh object!")
		return

	obj = sel[0]
	if not cmds.filterExpand(sm=12):
		cmds.warning("-- INFO -- Wrong selection! Select the mesh object (Mirror result)!")
		return

	# map axis to polyMirrorCut direction (1:X, 2:Y, 3:Z)
	axis_map = {"X": 1, "Y": 2, "Z": 3}
	sign = 1 if "+" in axis else -1
	main_axis = axis.replace("+", "").replace("-", "")

	cmds.hyperShade(smn="")
	mats = cmds.ls(sl=True, mat=True)

	cmds.select(obj)
	cmds.polyMirrorCut(axis_map[main_axis], 1, 0.001)
	plane = cmds.ls(sl=True)[0]
	cmds.rename(plane, "K_MirrorCutPlane")

	# rotate cutting plane
	if main_axis == "X" and sign == 1:
		cmds.setAttr(f"{plane}.rotateY", -90)
	elif main_axis == "Y" and sign == 1:
		cmds.setAttr(f"{plane}.rotateZ", -180)
	elif main_axis == "Z" and sign == 1:
		cmds.setAttr(f"{plane}.rotateY", -180)

	# coloring the plane
	leaves = cmds.ls(sl=True, dag=True, leaf=True)
	for each in leaves:
		cmds.setAttr(f"{each}.overrideEnabled", 1)
		cmds.setAttr(f"{each}.overrideRGBColors", 1)
		cmds.setAttr(f"{each}.overrideColorRGB", 0.672, 0.074, 0.074)

	# rename merge node
	hist = cmds.listHistory(pdo=True, f=True)
	for node in hist or []:
		if node.startswith("polyMergeVert"):
			cmds.rename(node, "K_polyMergeVert")

	cmds.hyperShade(assign=mats[0] if mats else "")
	cmds.select(plane)
	cmds.setToolTo("Move")

def rotate(axis="X", angle=15.0, negative=False):
	"""หมุนแกน (Shift+Click)"""
	sel = cmds.ls(sl=True, tr=True)
	if not sel:
		cmds.warning("-- INFO -- No object selected! Select the mesh object (Mirror result)!")
		return

	mult = -1 if negative else 1
	for obj in sel:
		current = cmds.getAttr(f"{obj}.rotate{axis}")
		cmds.setAttr(f"{obj}.rotate{axis}", current + angle * mult)

def clean():
	"""เหมือน mirrorCleanAll()"""
	sel = cmds.ls(sl=True)
	if len(sel) != 1:
		cmds.warning("-- INFO -- Select only ONE mesh object (Mirror result)!")
		return

	if not cmds.filterExpand(sm=12):
		cmds.warning("-- INFO -- Wrong selection! Select the mesh object (Mirror result)!")
		return

	cmds.DeleteHistory()
	cmds.select("K_MirrorCutPlane*")
	connected = cmds.listConnections(d=True)
	if connected:
		cmds.select(connected, add=True)
	cmds.delete()
	try:
		mel.eval("source cleanUpScene.mel; deleteEmptyGroups();")
	except:
		pass

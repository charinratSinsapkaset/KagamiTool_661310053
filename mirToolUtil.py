import maya.cmds as cmds
from maya import mel

def mirror(axis="+X"):
    """Mirror geometry ตามแกนที่เลือก (ใช้ได้กับ Maya 2024–2025)"""
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

    axis_map = {"X": 0, "Y": 1, "Z": 2}
    sign = 1 if "+" in axis else -1
    main_axis = axis.replace("+", "").replace("-", "")

    # duplicate และ mirror object
    mirror_node = cmds.polyDuplicateAndMirror(
        obj,
        axis=axis_map[main_axis],
        mergeMode=1,
        mergeThreshold=0.001,
        flip=sign == -1
    )[0]

    # เปลี่ยนชื่อ node
    cmds.rename(mirror_node, "K_MirrorResult")

    # ทำสีให้ mesh (แดง)
    leaves = cmds.ls(mirror_node, dag=True, leaf=True)
    for each in leaves:
        try:
            cmds.setAttr(f"{each}.overrideEnabled", 1)
            cmds.setAttr(f"{each}.overrideRGBColors", 1)
            cmds.setAttr(f"{each}.overrideColorRGB", 0.672, 0.074, 0.074)
        except:
            pass

    # ย้าย selection และเครื่องมือ
    cmds.select(mirror_node)
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
    """ล้าง mirror node"""
    sel = cmds.ls(sl=True)
    if not sel:
        cmds.warning("-- INFO -- Select something to clean!")
        return

    for obj in sel:
        try:
            cmds.delete(obj, ch=True)  # delete history
        except:
            pass

    try:
        mel.eval("source cleanUpScene.mel; deleteEmptyGroups();")
    except:
        pass

    cmds.warning("-- INFO -- Mirror cleaned successfully!")

import maya.cmds as cmds
import maya.mel as mel


def _mirror_axis(obj, axis_name="+X"):
    """Internal helper for mirroring mesh along given axis."""
    axis_name = axis_name.upper()

    cmds.select(obj)
    mel.eval('polyMirrorCut 1 1 0.001;')

    plane = cmds.ls(selection=True)[0]
    plane = cmds.rename(plane, "MirrorCutPlane")

    # ปรับการหมุนของ plane ตามทิศ
    rotations = {
        "+X": (-90, 0, 0),
        "-X": (90, 0, 0),
        "+Y": (0, 0, 0),
        "-Y": (0, 180, 0),
        "+Z": (0, 90, 0),
        "-Z": (0, -90, 0),
    }

    if axis_name not in rotations:
        cmds.warning("Invalid axis name! Use +X, -X, +Y, -Y, +Z, or -Z")
        return

    rx, ry, rz = rotations[axis_name]
    cmds.setAttr(plane + ".rotateX", rx)
    cmds.setAttr(plane + ".rotateY", ry)
    cmds.setAttr(plane + ".rotateZ", rz)

    # ปรับสี plane
    cmds.setAttr(plane + ".overrideEnabled", 1)
    cmds.setAttr(plane + ".overrideRGBColors", 1)
    cmds.setAttr(plane + ".overrideColorRGB", 0.672, 0.074, 0.074)

    # หา shading group เดิม
    shading_groups = cmds.listConnections(obj, type="shadingEngine") or []
    sg = shading_groups[0] if shading_groups else "initialShadingGroup"

    # บังคับ assign shader เดิมกลับเข้า geometry ปัจจุบัน
    shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
    for s in shapes:
        cmds.sets(s, e=True, forceElement=sg)
        cmds.hyperShade(assign=sg)

    cmds.setToolTo("moveSuperContext")
    print(f"✅ Mirror {axis_name} complete. Material '{sg}' re-applied successfully!")


# --------------------------
# ฟังก์ชันหลักแต่ละแกน
# --------------------------
def mirrorPlusX():
    sel = cmds.ls(selection=True, transforms=True)
    if not sel: return cmds.warning("-- INFO -- No object selected!")
    _mirror_axis(sel[0], "+X")

def mirrorMinusX():
    sel = cmds.ls(selection=True, transforms=True)
    if not sel: return cmds.warning("-- INFO -- No object selected!")
    _mirror_axis(sel[0], "-X")

def mirrorPlusY():
    sel = cmds.ls(selection=True, transforms=True)
    if not sel: return cmds.warning("-- INFO -- No object selected!")
    _mirror_axis(sel[0], "+Y")

def mirrorMinusY():
    sel = cmds.ls(selection=True, transforms=True)
    if not sel: return cmds.warning("-- INFO -- No object selected!")
    _mirror_axis(sel[0], "-Y")

def mirrorPlusZ():
    sel = cmds.ls(selection=True, transforms=True)
    if not sel: return cmds.warning("-- INFO -- No object selected!")
    _mirror_axis(sel[0], "+Z")

def mirrorMinusZ():
    sel = cmds.ls(selection=True, transforms=True)
    if not sel: return cmds.warning("-- INFO -- No object selected!")
    _mirror_axis(sel[0], "-Z")

       

# -------------------------------------------------------------------
# Clean up function
# -------------------------------------------------------------------
def mirrorCleanAll(*_):
    """ลบ history, ลบ MirrorCutPlane ทั้งหมด และใส่ material 'standardSurface1' ให้กับโมเดล"""
    
    sel = cmds.ls(sl=True, tr=True)
    if len(sel) != 1:
        cmds.warning("-- INFO -- Select only ONE mesh object (Mirror result)!")
        return

    obj = sel[0]
    if not cmds.listRelatives(obj, shapes=True):
        cmds.warning("-- INFO -- Wrong selection! Select the mesh object (Mirror result)!")
        return

    # --------------------------
    # 1. ลบ construction history
    # --------------------------
    cmds.delete(obj, ch=True)

    # --------------------------
    # 2. ลบ plane ที่ชื่อ MirrorCutPlane*
    # --------------------------
    for node in cmds.ls("MirrorCutPlane*", type="transform"):
        cmds.delete(node)

    # --------------------------
    # 3. ใส่ material standardSurface1
    # --------------------------
    if not cmds.objExists("standardSurface1"):
        cmds.warning("-- INFO -- 'standardSurface1' not found in scene! Creating new one.")
        mat = cmds.shadingNode("standardSurface", asShader=True, name="standardSurface1")
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="standardSurface1SG")
        cmds.connectAttr(mat + ".outColor", sg + ".surfaceShader", f=True)
    else:
        # หา shading group ของ material เดิม
        sg_list = cmds.listConnections("standardSurface1", type="shadingEngine") or []
        if sg_list:
            sg = sg_list[0]
        else:
            sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="standardSurface1SG")
            cmds.connectAttr("standardSurface1.outColor", sg + ".surfaceShader", f=True)

    # Apply material ให้โมเดล
    shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
    for s in shapes:
        cmds.sets(s, e=True, forceElement=sg)

    print("✅ Mirror cleanup complete & assigned 'standardSurface1' successfully!")
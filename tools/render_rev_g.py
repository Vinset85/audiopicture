#!/usr/bin/env python3
"""Studio renders of the Rev.G frame. Run with Blender, not system Python:

    blender --background --python tools/render_rev_g.py
"""
from __future__ import annotations
import json
import math
import os
import sys

import bpy
from mathutils import Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CAD = os.path.join(ROOT, "mechanical", "rev-g", "cad")
OUT = os.path.join(ROOT, "evidence", "rev-g", "renders")
PARAMS = json.load(open(os.path.join(ROOT, "mechanical", "rev-g", "rev_g_params.json")))
MANIFEST = json.load(open(os.path.join(CAD, "manifest.json")))


def mm(value):
    return value / 1000.0


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras):
        for item in list(block):
            if item.users == 0:
                block.remove(item)


def material(name, color, roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    node = mat.node_tree.nodes.get("Principled BSDF")
    node.inputs["Base Color"].default_value = (*color, 1.0)
    node.inputs["Roughness"].default_value = roughness
    node.inputs["Metallic"].default_value = metallic
    return mat


def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj


def cube(name, size_mm, center_mm, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=tuple(mm(v) for v in center_mm))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = tuple(mm(v) for v in size_mm)
    bpy.ops.object.transform_apply(scale=True)
    return assign(obj, mat)


def cylinder(name, diameter_mm, depth_mm, center_mm, mat):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=mm(diameter_mm / 2),
        depth=mm(depth_mm),
        location=tuple(mm(v) for v in center_mm),
    )
    obj = bpy.context.active_object
    obj.name = name
    return assign(obj, mat)


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def hang(parts):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "hang"
    for obj in parts:
        obj.parent = root
        obj.matrix_parent_inverse = root.matrix_world.inverted()
    root.rotation_euler = (math.radians(90), 0, 0)
    return root


def import_stl(path, name, mat):
    before = set(bpy.data.objects)
    bpy.ops.wm.stl_import(filepath=path)
    imported = [obj for obj in bpy.data.objects if obj not in before]
    obj = imported[0]
    obj.name = name
    obj.scale = (0.001, 0.001, 0.001)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(scale=True)
    return assign(obj, mat)


def cut_positive_x(obj):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.45, 0, 0.015))
    cutter = bpy.context.active_object
    cutter.scale = (0.70, 0.90, 0.08)
    bpy.ops.object.transform_apply(scale=True)
    modifier = obj.modifiers.new("section", "BOOLEAN")
    modifier.operation = "DIFFERENCE"
    modifier.object = cutter
    modifier.solver = "FLOAT"
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.modifier_apply(modifier="section")
    bpy.data.objects.remove(cutter, do_unlink=True)


def build(section=False):
    clear_scene()
    frame_mat = material("frame", (0.02, 0.022, 0.024), 0.55)
    panel_mat = material("panel", (0.55, 0.40, 0.22), 0.7)
    cloth_mat = material("cloth", (0.62, 0.54, 0.42), 0.9)
    motor_mat = material("motor", (0.01, 0.01, 0.012), 0.35)
    pcb_mat = material("pcb", (0.02, 0.16, 0.05), 0.55)
    core_mat = material("core", (0.04, 0.045, 0.05), 0.45)
    amp_mat = material("amp", (0.25, 0.26, 0.28), 0.4, 0.6)
    radar_mat = material("radar", (0.02, 0.02, 0.02), 0.4)

    frame = import_stl(os.path.join(CAD, "AP-G-FRAME.stl"), "frame", frame_mat)
    panel = import_stl(os.path.join(CAD, "AP-G-PANEL.stl"), "panel", panel_mat)
    origin = MANIFEST["panel_origin_mm"]
    pw, ph, pt = PARAMS["panel_mm"]
    lf = PARAMS["exciters"]["lf"]
    wb = PARAMS["exciters"]["wb"]
    lf_c = [
        origin[0] + lf["on_panel_mm_from_lower_left"][0],
        origin[1] + lf["on_panel_mm_from_lower_left"][1],
        origin[2] - lf["depth_mm"] / 2,
    ]
    wb_c = [
        origin[0] + wb["on_panel_mm_from_lower_left"][0],
        origin[1] + wb["on_panel_mm_from_lower_left"][1],
        origin[2] - wb["depth_mm"] / 2,
    ]
    parts = [
        frame,
        panel,
        cylinder("lf", lf["diameter_mm"], lf["depth_mm"], lf_c, motor_mat),
        cube("wb", [wb["footprint_mm"][0], wb["footprint_mm"][1], wb["depth_mm"]], wb_c, motor_mat),
    ]
    hat = PARAMS["electronics"]["hat_mm"]
    core = PARAMS["electronics"]["core_mm"]
    hx, hy = MANIFEST["hat_center_mm"]
    hat_z = 22.5
    parts.append(cube("hat", hat, [hx, hy, hat_z], pcb_mat))
    parts.append(cube("core", core, [hx + hat[0] / 2 + 6 + core[0] / 2, hy, hat_z], core_mat))
    parts.append(cube("amp", [70, 42, 14], [90, hy, 12], amp_mat))
    parts.append(cube("ld2450", [15, 44, 3], [hx, hy, 28.2], radar_mat))
    cloth = cube("cloth", [314, 394, 1.0], [0, 0, 30.5], cloth_mat)
    parts.append(cloth)
    mark_mat = material("touch", (0.45, 0.38, 0.28), 0.85)
    for zone in PARAMS["volume_touch"]["zones"]:
        zw, zh = zone["size_mm"]
        zx, zy = zone["center_mm"]
        parts.append(cube(zone["id"], [zw, zh, 0.3], [zx, zy, 31.0], mark_mat))
    if section:
        cloth.hide_render = True
        for obj in parts:
            if obj is cloth:
                continue
            cut_positive_x(obj)
    hang(parts)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.025, 0))
    wall = bpy.context.active_object
    wall.name = "wall"
    wall.scale = (1.3, 0.02, 1.6)
    bpy.ops.object.transform_apply(scale=True)
    assign(wall, material("wall", (0.95, 0.94, 0.92), 0.85))
    if section:
        wall.hide_render = True
    return {"cloth": cloth, "wall": wall}


def studio():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1200
    scene.render.film_transparent = False
    world = scene.world or bpy.data.worlds.new("world")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.55, 0.56, 0.58, 1)
    bg.inputs["Strength"].default_value = 0.2
    for loc, energy, size in (
        ((0.35, -0.7, 0.45), 80, 0.8),
        ((-0.4, -0.45, 0.1), 25, 0.6),
        ((0.1, 0.55, 0.35), 35, 0.5),
    ):
        bpy.ops.object.light_add(type="AREA", location=loc)
        light = bpy.context.active_object
        light.data.energy = energy
        light.data.size = size
        look_at(light, (0, 0.015, 0))
    bpy.ops.object.camera_add()
    cam = bpy.context.active_object
    scene.camera = cam
    cam.data.lens = 55
    return cam


def shoot(cam, location, target, path, ortho=None):
    cam.location = Vector(location)
    look_at(cam, target)
    if ortho:
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = ortho
    else:
        cam.data.type = "PERSP"
        cam.data.lens = 42
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("wrote", path)


def main():
    os.makedirs(OUT, exist_ok=True)
    target = (0.0, -0.015, 0.0)
    scene = build(section=False)
    cam = studio()
    shoot(cam, (0.16, -0.88, 0.02), target, os.path.join(OUT, "AP-G-front.png"))
    scene["wall"].hide_render = True
    shoot(cam, (-0.12, 0.78, 0.02), (0.0, 0.0, 0.0), os.path.join(OUT, "AP-G-rear.png"))
    shoot(cam, (0.52, -0.48, 0.0), target, os.path.join(OUT, "AP-G-edge.png"))
    build(section=True)
    cam = studio()
    shoot(cam, (0.70, -0.72, 0.06), (0.0, -0.012, 0.0), os.path.join(OUT, "AP-G-section.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

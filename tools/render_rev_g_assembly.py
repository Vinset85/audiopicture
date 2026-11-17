#!/usr/bin/env python3
"""Photoreal cutaway of the Rev.G assembly, cloth omitted.

    blender --background --python tools/render_rev_g_assembly.py
"""
from __future__ import annotations
import math
import os
import sys

import bpy
from mathutils import Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CAD = os.path.join(ROOT, "mechanical", "rev-g", "cad")
OUT = os.path.join(ROOT, "evidence", "rev-g", "renders", "AP-G-assembly.png")


def mm(value):
    return value / 1000.0


def material(name, color, roughness=0.45, metallic=0.0, emission=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    node = mat.node_tree.nodes.get("Principled BSDF")
    node.inputs["Base Color"].default_value = (*color, 1.0)
    node.inputs["Roughness"].default_value = roughness
    node.inputs["Metallic"].default_value = metallic
    if emission and "Emission Color" in node.inputs:
        node.inputs["Emission Color"].default_value = (*color, 1.0)
        node.inputs["Emission Strength"].default_value = emission
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


def cut_rear(obj):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.004))
    cutter = bpy.context.active_object
    cutter.scale = (0.50, 0.60, 0.010)
    bpy.ops.object.transform_apply(scale=True)
    modifier = obj.modifiers.new("open_rear", "BOOLEAN")
    modifier.operation = "DIFFERENCE"
    modifier.object = cutter
    modifier.solver = "FLOAT"
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.modifier_apply(modifier="open_rear")
    bpy.data.objects.remove(cutter, do_unlink=True)


def hang(parts):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "hang"
    for obj in parts:
        obj.parent = root
        obj.matrix_parent_inverse = root.matrix_world.inverted()
    root.rotation_euler = (math.radians(90), 0, 0)
    return root


def build():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    frame_mat = material("frame", (0.015, 0.016, 0.018), 0.42)
    panel_mat = material("panel", (0.62, 0.46, 0.28), 0.62)
    motor_mat = material("motor", (0.02, 0.02, 0.022), 0.28, 0.85)
    pcb_mat = material("pcb", (0.03, 0.22, 0.08), 0.48)
    core_mat = material("core", (0.08, 0.085, 0.09), 0.35, 0.7)
    psu_mat = material("psu", (0.04, 0.04, 0.045), 0.4)
    amp_mat = material("amp", (0.55, 0.56, 0.58), 0.32, 0.85)
    radar_mat = material("radar", (0.01, 0.01, 0.012), 0.35)
    magnet_mat = material("magnet", (0.72, 0.73, 0.75), 0.25, 1.0)
    wire_mat = material("wire", (0.08, 0.05, 0.03), 0.55)
    led_mat = material("led", (0.95, 0.85, 0.55), 0.3, emission=4.0)

    frame = import_stl(os.path.join(CAD, "AP-G-FRAME.stl"), "frame", frame_mat)
    cut_rear(frame)
    parts = [
        frame,
        cube("panel", [292, 278, 8], [0, 47, 24.5], panel_mat),
        cylinder("xt19", 36.3, 14, [-36, -14, 13.5], motor_mat),
        cube("teax", [61.3, 50.8, 19], [40, 108, 11], motor_mat),
        cube("hat", [88, 88, 10], [-108, -147, 6], pcb_mat),
        cube("core", [66, 31, 10], [-25, -147, 6], core_mat),
        cube("radar", [15, 44, 3], [-108, -147, 26.7], radar_mat),
        cube("psu", [69.5, 39, 24], [46.75, -147, 13], psu_mat),
        cube("amp", [60, 80, 16], [115.5, -147, 9], amp_mat),
        cube("pd", [30, 16, 10], [-37, -147, 17], core_mat),
        cube("filter", [28, 16, 8], [110, -147, 22], core_mat),
        cube("mute", [8, 10, 8], [0, -191, 15], psu_mat),
        cube("ttp_l", [16, 11, 3], [-40, -176.5, 14.5], pcb_mat),
        cube("ttp_r", [16, 11, 3], [40, -176.5, 14.5], pcb_mat),
    ]
    for x, y in (
        (-153.25, -150), (153.25, -150), (-153.25, -50), (153.25, -50),
        (-153.25, 50), (153.25, 50), (-153.25, 150), (153.25, 150),
        (-100, -193.25), (-100, 193.25), (0, -193.25), (0, 193.25),
        (100, -193.25), (100, 193.25),
    ):
        parts.append(cylinder(f"mag_{x}_{y}", 8, 2, [x, y, 27.5], magnet_mat))
    for x in (-45, -15, 15, 45):
        parts.append(cylinder(f"led_{x}", 2.8, 5, [x, -192, 20.5], led_mat))
    hang(parts)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    build()
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1200
    scene.render.film_transparent = False
    try:
        scene.view_settings.view_transform = "AgX"
    except TypeError:
        scene.view_settings.view_transform = "Filmic"
    world = scene.world or bpy.data.worlds.new("world")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.16, 0.16, 0.17, 1)
    bg.inputs["Strength"].default_value = 0.4
    for loc, energy, size in (
        ((0.15, 0.55, 0.45), 120, 0.45),
        ((-0.35, 0.25, 0.15), 40, 0.3),
        ((0.4, -0.2, 0.2), 25, 0.25),
    ):
        bpy.ops.object.light_add(type="AREA", location=loc)
        light = bpy.context.active_object
        light.data.energy = energy
        light.data.size = size
        look_at(light, (0.0, -0.01, 0.02))
    bpy.ops.object.camera_add()
    cam = bpy.context.active_object
    scene.camera = cam
    cam.data.lens = 48
    cam.location = Vector((0.46, 0.98, 0.28))
    look_at(cam, (0.0, -0.012, 0.0))
    bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0.2, -0.28))
    floor = bpy.context.active_object
    assign(floor, material("floor", (0.12, 0.12, 0.13), 0.8))
    scene.render.filepath = OUT
    bpy.ops.render.render(write_still=True)
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())

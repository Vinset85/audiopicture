#!/usr/bin/env python3
"""Front render of the finished picture: cloth, printed image, LEDs on.

    blender --background --python tools/render_rev_g_cloth.py
"""
from __future__ import annotations
import math
import os
import sys

import bpy
from mathutils import Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CAD = os.path.join(ROOT, "mechanical", "rev-g", "cad")
PRINT = os.environ.get(
    "AP_CLOTH_PRINT",
    "/Users/cinetyk/.cursor/projects/Users-cinetyk-Library-CloudStorage-Dropbox-Azienda-Cinetyk-Sviluppo-audiopicture/assets/cloth-print.jpg",
)
OUT = os.path.join(ROOT, "evidence", "rev-g", "renders", "AP-G-cloth.png")


def mm(value):
    return value / 1000.0


def material(name, color, roughness=0.45, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    node = mat.node_tree.nodes.get("Principled BSDF")
    node.inputs["Base Color"].default_value = (*color, 1.0)
    node.inputs["Roughness"].default_value = roughness
    node.inputs["Metallic"].default_value = metallic
    return mat


def emission(name, color, strength):
    mat = material(name, color, roughness=0.4)
    node = mat.node_tree.nodes.get("Principled BSDF")
    node.inputs["Emission Color"].default_value = (*color, 1.0)
    node.inputs["Emission Strength"].default_value = strength
    return mat


def cloth_material(path):
    mat = material("cloth", (0.7, 0.65, 0.55), roughness=0.82)
    tree = mat.node_tree
    tex = tree.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(path)
    tex.interpolation = "Smart"
    bump = tree.nodes.new("ShaderNodeTexNoise")
    bump.inputs["Scale"].default_value = 180.0
    bump.inputs["Detail"].default_value = 8.0
    height = tree.nodes.new("ShaderNodeBump")
    height.inputs["Strength"].default_value = 0.08
    bsdf = tree.nodes.get("Principled BSDF")
    tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    tree.links.new(bump.outputs["Fac"], height.inputs["Height"])
    tree.links.new(height.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def import_stl(path, name, mat):
    before = set(bpy.data.objects)
    bpy.ops.wm.stl_import(filepath=path)
    obj = [item for item in bpy.data.objects if item not in before][0]
    obj.name = name
    obj.scale = (0.001, 0.001, 0.001)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(scale=True)
    return assign(obj, mat)


def hang(parts):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
    root = bpy.context.active_object
    for obj in parts:
        obj.parent = root
        obj.matrix_parent_inverse = root.matrix_world.inverted()
    root.rotation_euler = (math.radians(90), 0, 0)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    frame = import_stl(
        os.path.join(CAD, "AP-G-FRAME.stl"),
        "frame",
        material("frame", (0.012, 0.012, 0.014), 0.38),
    )
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, mm(30.05)))
    cloth = bpy.context.active_object
    cloth.name = "cloth"
    cloth.scale = (mm(317), mm(397), 1)
    bpy.ops.object.transform_apply(scale=True)
    assign(cloth, cloth_material(PRINT))
    parts = [frame, cloth]
    lamps = (
        (-45, (1.0, 0.96, 0.88)),
        (-15, (0.25, 0.45, 1.0)),
        (15, (1.0, 0.12, 0.08)),
        (45, (1.0, 0.62, 0.12)),
    )
    for x, color in lamps:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=mm(2.2),
            depth=mm(0.3),
            location=(mm(x), mm(-192), mm(30.2)),
        )
        glow = bpy.context.active_object
        glow.name = f"led_{x}"
        assign(glow, emission(f"ledmat_{x}", color, 6.0))
        parts.append(glow)
    hang(parts)

    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 64
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1400
    scene.render.resolution_y = 1600
    try:
        scene.view_settings.view_transform = "AgX"
    except TypeError:
        scene.view_settings.view_transform = "Filmic"
    scene.view_settings.exposure = -0.85
    world = scene.world or bpy.data.worlds.new("world")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.72, 0.70, 0.66, 1)
    bg.inputs["Strength"].default_value = 0.15

    bpy.ops.mesh.primitive_plane_add(size=3.2, location=(0, 0.02, 0), rotation=(math.radians(90), 0, 0))
    assign(bpy.context.active_object, material("wall", (0.86, 0.84, 0.80), 0.9))

    for loc, energy, size in (
        ((-0.7, -1.1, 0.7), 90, 0.8),
        ((0.8, -0.6, 0.2), 28, 0.5),
        ((0.0, -0.4, -0.6), 10, 0.4),
    ):
        bpy.ops.object.light_add(type="AREA", location=loc)
        light = bpy.context.active_object
        light.data.energy = energy
        light.data.size = size
        look_at(light, (0.0, -0.02, 0.0))

    bpy.ops.object.camera_add()
    cam = bpy.context.active_object
    scene.camera = cam
    cam.data.lens = 55
    cam.location = Vector((-0.16, -1.05, 0.04))
    look_at(cam, (0.0, -0.02, 0.0))
    scene.render.filepath = OUT
    bpy.ops.render.render(write_still=True)
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())

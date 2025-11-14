#!/usr/bin/env python3
"""
Blender script to import and render stacked PCB boards.
This script is designed to be called by KiBot's blender_export output.

Usage:
    blender --background --python stack_boards_render.py -- \
        --control-board path/to/control-board.pcb3d \
        --main-board path/to/main-board.pcb3d \
        --output path/to/output.png \
        --spacing 15.0
"""

import bpy
import sys
import argparse
from pathlib import Path


def parse_args():
    """Parse command line arguments after '--' separator.

    Board arguments are parsed sequentially: --board specifies a new board,
    and subsequent --board-offset, --board-shift-x, --board-shift-y apply to that board
    until the next --board argument.
    """
    # Find the '--' separator that Blender uses
    try:
        argv = sys.argv[sys.argv.index("--") + 1:]
    except ValueError:
        argv = []

    # Parse boards manually for sequential grouping
    boards = []
    current_board = None
    i = 0

    while i < len(argv):
        arg = argv[i]

        if arg == "--board":
            # Start a new board
            if current_board:
                boards.append(current_board)
            current_board = {
                'path': argv[i + 1],
                'offset': 0.0,
                'shift_x': 0.0,
                'shift_y': 0.0
            }
            i += 2
        elif arg == "--board-offset" and current_board:
            current_board['offset'] = float(argv[i + 1])
            i += 2
        elif arg == "--board-shift-x" and current_board:
            current_board['shift_x'] = float(argv[i + 1])
            i += 2
        elif arg == "--board-shift-y" and current_board:
            current_board['shift_y'] = float(argv[i + 1])
            i += 2
        else:
            # Not a board-related argument, stop processing
            break

    # Add the last board
    if current_board:
        boards.append(current_board)

    # Parse remaining arguments with argparse
    remaining_argv = argv[i:]

    parser = argparse.ArgumentParser(description="Render PCB boards in Blender (single or stacked)")
    parser.add_argument("--output", required=True, help="Output image path")
    parser.add_argument("--scale-factor", type=float, default=0.001, help="Scale factor for imported models (default: 0.001)")
    parser.add_argument("--samples", type=int, default=100, help="Number of render samples")
    parser.add_argument("--resolution-x", type=int, default=1920, help="Output width")
    parser.add_argument("--resolution-y", type=int, default=1080, help="Output height")
    parser.add_argument("--camera-view", type=str, default="angle", choices=["angle", "front", "top", "side", "bottom", "perspective"], help="Camera view")
    parser.add_argument("--orthographic", action="store_true", help="Use orthographic projection")
    parser.add_argument("--animate", action="store_true", help="Create rotating animation")
    parser.add_argument("--frames", type=int, default=120, help="Animation frames")
    parser.add_argument("--fps", type=int, default=30, help="Animation FPS")
    parser.add_argument("--background-color", type=str, default="#66667F", help="Background color as hex")
    parser.add_argument("--background-gradient-top", type=str, default=None, help="Top gradient color")
    parser.add_argument("--background-gradient-bottom", type=str, default=None, help="Bottom gradient color")
    parser.add_argument("--transparent-background", action="store_true", help="Transparent background")
    parser.add_argument("--auto-crop", action="store_true", help="Auto-crop output")
    parser.add_argument("--camera-distance-multiplier", type=float, default=1.0, help="Camera distance multiplier")

    args = parser.parse_args(remaining_argv)

    # Add boards to args
    if not boards:
        parser.error("At least one --board must be specified")

    args.board = [b['path'] for b in boards]
    args.board_offset = [b['offset'] for b in boards]
    args.board_shift_x = [b['shift_x'] for b in boards]
    args.board_shift_y = [b['shift_y'] for b in boards]

    return args


def clear_scene():
    """Remove all objects from the scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


def get_scene_bounds():
    """Calculate bounding box of all mesh objects in the scene."""
    from mathutils import Vector

    coords = []
    z_values = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and obj.data and hasattr(obj.data, 'vertices'):
            # Get world-space coordinates of all vertices
            for vert in obj.data.vertices:
                world_co = obj.matrix_world @ vert.co
                coords.append(world_co)
                z_values.append(world_co.z)

    if coords:
        min_coords = Vector((min(v.x for v in coords), min(v.y for v in coords), min(v.z for v in coords)))
        max_coords = Vector((max(v.x for v in coords), max(v.y for v in coords), max(v.z for v in coords)))
        center = (min_coords + max_coords) / 2
        size = max_coords - min_coords

        # Debug ranges
        if z_values:
            x_values = [v.x for v in coords]
            y_values = [v.y for v in coords]
            print(f"  X range: {min(x_values):.2f} to {max(x_values):.2f}")
            print(f"  Y range: {min(y_values):.2f} to {max(y_values):.2f}")
            print(f"  Z range: {min(z_values):.2f} to {max(z_values):.2f}")

        return min_coords, max_coords, center, size

    return None, None, Vector((0, 0, 0)), Vector((0, 0, 0))


def setup_border_render(camera, scene, padding_percent=5, is_animation=False):
    """Configure border rendering to crop to scene bounds with padding.

    Args:
        camera: The camera object
        scene: The scene object
        padding_percent: Percentage of padding to add around the boards (default: 5%)
        is_animation: If True, add extra horizontal padding to account for rotation
    """
    from bpy_extras.object_utils import world_to_camera_view

    # Get all mesh objects
    mesh_objects = [obj for obj in scene.objects if obj.type == 'MESH']
    if not mesh_objects:
        return

    # Calculate 2D bounding box in camera view
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')

    for obj in mesh_objects:
        for vert in obj.data.vertices:
            world_co = obj.matrix_world @ vert.co
            # Convert to camera view (returns Vector with x, y in 0-1 range, z is depth)
            cam_co = world_to_camera_view(scene, camera, world_co)

            min_x = min(min_x, cam_co.x)
            max_x = max(max_x, cam_co.x)
            min_y = min(min_y, cam_co.y)
            max_y = max(max_y, cam_co.y)

    # Add padding
    width = max_x - min_x
    height = max_y - min_y

    # For animations, add extra horizontal padding to account for rotation
    # The boards will extend further horizontally as they rotate
    if is_animation:
        # Add approximately 40% extra horizontal padding for full rotation coverage
        padding_x = width * ((padding_percent + 40) / 100.0)
        padding_y = height * (padding_percent / 100.0)
    else:
        padding_x = width * (padding_percent / 100.0)
        padding_y = height * (padding_percent / 100.0)

    min_x = max(0.0, min_x - padding_x)
    max_x = min(1.0, max_x + padding_x)
    min_y = max(0.0, min_y - padding_y)
    max_y = min(1.0, max_y + padding_y)

    # Calculate actual pixel dimensions to ensure they're even (required for video encoding)
    width = int((max_x - min_x) * scene.render.resolution_x)
    height = int((max_y - min_y) * scene.render.resolution_y)

    # Round to nearest even number
    if width % 2 != 0:
        width = width + 1 if width < scene.render.resolution_x else width - 1
    if height % 2 != 0:
        height = height + 1 if height < scene.render.resolution_y else height - 1

    # Convert back to normalized coordinates
    max_x = min_x + (width / scene.render.resolution_x)
    max_y = min_y + (height / scene.render.resolution_y)

    # Clamp to valid range
    max_x = min(1.0, max_x)
    max_y = min(1.0, max_y)

    # Set border render
    scene.render.use_border = True
    scene.render.use_crop_to_border = True
    scene.render.border_min_x = min_x
    scene.render.border_max_x = max_x
    scene.render.border_min_y = min_y
    scene.render.border_max_y = max_y

    print(f"  Auto-crop enabled: X[{min_x:.3f}-{max_x:.3f}] Y[{min_y:.3f}-{max_y:.3f}] ({width}x{height})")


def setup_camera(scene_center=None, scene_size=None, angle_x=45, angle_z=-45, view_type="angle", distance_multiplier=1.0):
    """Set up camera position - always at fixed angled view looking at scene center.

    The camera is always positioned at a 45° angled view. Different board orientations
    are achieved by rotating the board, then the camera re-centers on the new position.
    """
    from mathutils import Vector
    import math

    # If no scene bounds provided, use defaults
    if scene_center is None:
        scene_center = Vector((0, 0, 0))
    if scene_size is None:
        scene_size = Vector((100, 100, 20))

    # Calculate camera distance based on XY scene size only
    max_xy = max(scene_size.x, scene_size.y)
    distance = max_xy * 2.5 * distance_multiplier

    # Camera is always at the same angle - 45° elevation, -45° azimuth
    angle_x_rad = math.radians(45)
    angle_z_rad = math.radians(-45)

    cam_x = distance * math.cos(angle_z_rad)
    cam_y = -distance * math.sin(angle_z_rad)
    cam_z = distance * 0.5

    camera_location = scene_center + Vector((cam_x, cam_y, cam_z))

    bpy.ops.object.camera_add(location=camera_location)
    camera = bpy.context.object

    # Point camera at scene center
    direction = scene_center - camera_location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()

    bpy.context.scene.camera = camera

    # Return board rotation for the requested view
    # Camera is at 45° angle (front-right, elevated). Rotate board to show desired face.
    # Note: Boards are initially rotated 180° around Z-axis after import
    # Camera position: azimuth=-45° (from +Y toward +X), elevation=45° (above XY plane)
    # To face camera: rotate board so its face normal aligns with camera direction
    board_rotation = None
    if view_type == "top":
        # Camera view direction: points down at -45° elevation and comes from -45° azimuth
        # Board normal starts at +Z (pointing up). Need to tilt it toward camera.
        # First rotate 45° around X to tilt top edge forward (toward camera's elevation angle)
        # Then rotate 135° around Z (180° base flip - 45° azimuth adjustment)
        board_rotation = (math.radians(65), 0, math.radians(135))
    elif view_type == "bottom":
        # This shows the bottom face with proper orientation
        board_rotation = (math.radians(295), math.radians(180), math.radians(135))
    elif view_type == "front":
        board_rotation = (math.radians(26.5), math.radians(0), math.radians(315))  # Tilt X, keep Z
    elif view_type == "side":
        board_rotation = (0, math.radians(26.5), math.radians(225))  # Rotate Y, keep Z
    else:  # angle/perspective
        board_rotation = (0, 0, math.radians(180))  # Keep initial Z rotation

    return camera, board_rotation


def setup_orthographic_camera(camera, scene_size):
    """Convert camera to orthographic projection and set scale."""
    camera.data.type = 'ORTHO'
    # Set orthographic scale based on scene size
    max_dimension = max(scene_size.x, scene_size.y, scene_size.z)
    camera.data.ortho_scale = max_dimension * 3.0  # Scale to fit scene


def set_pcb_color(pcb_obj, hex_color):
    """Set the PCB substrate/solder mask color for pcb2blender materials."""
    # Convert hex color to RGB (0-1 range)
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0

    print(f"  Setting PCB color to #{hex_color}")
    print(f"  Note: To properly set black PCB color, configure KiCad board stackup with black solder mask")
    print(f"  Attempting runtime color override (may have limited effect)...")

    # The pcb2blender material system is complex with custom groups
    # For now, just note that the color should be set in KiCad's stackup
    # We'll skip the runtime modification since it's not reliably working
    return


def setup_lighting(scene_center, scene_size, transparent_background=False):
    """Set up professional 3-point lighting for PCB renders using area lights.

    Standard 3-point lighting setup:
    - Key light: Main light source (brightest, from upper front-left)
    - Fill light: Softer light to fill shadows (from front-right, less intense)
    - Rim/Back light: Separates subject from background (from behind/above)

    Args:
        scene_center: Center point of the scene (Vector)
        scene_size: Size of the scene (Vector with x, y, z dimensions)
        transparent_background: If True, use brighter lighting
    """
    import math
    from mathutils import Vector

    # Scale based on scene size
    max_dimension = max(scene_size.x, scene_size.y)

    # Simple energy values - easy to adjust
    # Moody lighting: Low key, minimal fill, subtle rim
    # Higher contrast ratio (Key:Fill:Rim = 1.0 : 0.2 : 0.5)
    key_energy = 1.0 if not transparent_background else 4.0
    fill_energy = 0.2 if not transparent_background else 0.8
    rim_energy = 0.5 if not transparent_background else 2.0

    # Area light size - scale with scene
    light_size = max_dimension * 0.5

    print(f"  Lighting setup: Key={key_energy}W, Fill={fill_energy}W, Rim={rim_energy}W")

    # Key Light - main light source (45° from camera axis, elevated 45°)
    # Position: front-left, elevated
    key_distance = max_dimension * 2.0
    key_angle = 45  # degrees from front
    key_height = max_dimension * 1.5

    key_x = scene_center.x - key_distance * math.cos(math.radians(key_angle))
    key_y = scene_center.y + key_distance * math.sin(math.radians(key_angle))

    bpy.ops.object.light_add(type='AREA', location=(key_x, key_y, scene_center.z + key_height))
    key_light = bpy.context.object
    key_light.data.energy = key_energy
    key_light.data.size = light_size
    key_light.data.shape = 'SQUARE'
    key_light.name = "Key_Light"

    # Point the light at the scene center
    direction = scene_center - key_light.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    key_light.rotation_euler = rot_quat.to_euler()

    print(f"  Key Light (AREA): energy={key_energy}W, size={light_size:.3f}, pos=({key_x:.3f}, {key_y:.3f}, {scene_center.z + key_height:.3f})")

    # Fill Light - softer light to fill in shadows (opposite side from key)
    # Position: front-right, lower elevation than key
    fill_distance = max_dimension * 2.0
    fill_angle = -30  # degrees from front (opposite side)
    fill_height = max_dimension * 1.0  # Lower than key

    fill_x = scene_center.x - fill_distance * math.cos(math.radians(fill_angle))
    fill_y = scene_center.y + fill_distance * math.sin(math.radians(fill_angle))

    bpy.ops.object.light_add(type='AREA', location=(fill_x, fill_y, scene_center.z + fill_height))
    fill_light = bpy.context.object
    fill_light.data.energy = fill_energy
    fill_light.data.size = light_size * 1.2  # Slightly larger for softer shadows
    fill_light.data.shape = 'SQUARE'
    fill_light.name = "Fill_Light"

    # Point the light at the scene center
    direction = scene_center - fill_light.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    fill_light.rotation_euler = rot_quat.to_euler()

    print(f"  Fill Light (AREA): energy={fill_energy}W, size={light_size * 1.2:.3f}, pos=({fill_x:.3f}, {fill_y:.3f}, {scene_center.z + fill_height:.3f})")

    # Rim/Back Light - separates subject from background
    # Position: behind and above, creates edge lighting
    rim_distance = max_dimension * 1.8
    rim_angle = 180  # degrees (behind the subject)
    rim_height = max_dimension * 1.5  # High and behind

    rim_x = scene_center.x - rim_distance * math.cos(math.radians(rim_angle))
    rim_y = scene_center.y + rim_distance * math.sin(math.radians(rim_angle))

    bpy.ops.object.light_add(type='AREA', location=(rim_x, rim_y, scene_center.z + rim_height))
    rim_light = bpy.context.object
    rim_light.data.energy = rim_energy
    rim_light.data.size = light_size * 0.8  # Smaller for more focused rim
    rim_light.data.shape = 'SQUARE'
    rim_light.name = "Rim_Light"

    # Point the light at the scene center
    direction = scene_center - rim_light.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    rim_light.rotation_euler = rot_quat.to_euler()

    print(f"  Rim Light (AREA): energy={rim_energy}W, size={light_size * 0.8:.3f}, pos=({rim_x:.3f}, {rim_y:.3f}, {scene_center.z + rim_height:.3f})")


def enable_pcb2blender_addon():
    """Enable the pcb2blender addon if not already enabled."""
    import addon_utils
    import traceback

    print("Enabling pcb2blender addon...")
    try:
        mod = addon_utils.enable('pcb2blender', default_set=True, persistent=False)
        if mod is None:
            print("ERROR: Failed to enable pcb2blender addon - addon not found")
            sys.exit(1)

        if hasattr(bpy.ops, 'pcb2blender') and hasattr(bpy.ops.pcb2blender, 'import_pcb3d'):
            print("pcb2blender addon enabled successfully")
        else:
            print("ERROR: pcb2blender addon loaded but import_pcb3d operator not available")
            sys.exit(1)

    except Exception as e:
        print(f"ERROR: Failed to enable pcb2blender addon:")
        print(f"  {type(e).__name__}: {e}")
        traceback.print_exc()
        sys.exit(1)


def import_pcb3d(filepath, z_offset=0):
    """Import PCB3D file and position it at given Z offset."""
    try:
        # Import PCB3D file
        bpy.ops.pcb2blender.import_pcb3d(filepath=str(filepath))

        # Get the imported objects (typically just the top-level PCB parent)
        imported = bpy.context.selected_objects

        # Only move the top-level objects, not children
        # Children (components) maintain their relative position to the parent
        for obj in imported:
            obj.location.z += z_offset

        # Force Blender to update transforms
        bpy.context.view_layer.update()

        print(f"  Moved {len(imported)} top-level objects by Z+{z_offset}mm")

        return imported
    except AttributeError:
        print("ERROR: pcb2blender addon not found or not enabled.")
        sys.exit(1)


def setup_render_settings(scene, args):
    """Configure render settings."""
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = args.samples
    scene.render.resolution_x = args.resolution_x
    scene.render.resolution_y = args.resolution_y
    scene.render.resolution_percentage = 100
    scene.render.filepath = args.output

    if args.animate:
        # Animation settings
        scene.render.image_settings.file_format = 'FFMPEG'
        scene.render.ffmpeg.format = 'MPEG4'
        scene.render.ffmpeg.codec = 'H264'
        scene.render.ffmpeg.constant_rate_factor = 'HIGH'
        scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
        scene.frame_start = 1
        scene.frame_end = args.frames
        scene.render.fps = args.fps
    else:
        # Still image
        scene.render.image_settings.file_format = 'PNG'

    # Enable denoising for cleaner output
    scene.cycles.use_denoising = True

    # Set background - transparent, gradient, or solid color
    if args.transparent_background:
        # Enable transparent background
        scene.render.film_transparent = True
        # Set world to transparent (no background shader needed)
        scene.world.use_nodes = True
        world_nodes = scene.world.node_tree.nodes
        world_links = scene.world.node_tree.links

        # Clear existing nodes
        for node in world_nodes:
            world_nodes.remove(node)

        # Create output node with no background
        output_node = world_nodes.new(type='ShaderNodeOutputWorld')
        output_node.location = (300, 0)
    else:
        # Opaque background
        scene.render.film_transparent = False
        scene.world.use_nodes = True
        world_nodes = scene.world.node_tree.nodes
        world_links = scene.world.node_tree.links

        # Clear existing nodes
        for node in world_nodes:
            world_nodes.remove(node)

        # Create output node
        output_node = world_nodes.new(type='ShaderNodeOutputWorld')
        output_node.location = (300, 0)

    if not args.transparent_background and args.background_gradient_top and args.background_gradient_bottom:
        # Create gradient background
        # Convert hex colors to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

        top_color = hex_to_rgb(args.background_gradient_top) + (1.0,)
        bottom_color = hex_to_rgb(args.background_gradient_bottom) + (1.0,)

        # Use Sky texture for vertical gradient
        tex_coord = world_nodes.new(type='ShaderNodeTexCoord')
        tex_coord.location = (-800, 0)

        # Mapping node to control gradient direction
        mapping = world_nodes.new(type='ShaderNodeMapping')
        mapping.location = (-600, 0)
        # Rotate 90 degrees around X to make gradient vertical
        mapping.inputs['Rotation'].default_value = (1.5708, 0, 0)  # 90 degrees in radians
        world_links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])

        # Gradient texture
        gradient = world_nodes.new(type='ShaderNodeTexGradient')
        gradient.location = (-400, 0)
        gradient.gradient_type = 'LINEAR'
        world_links.new(mapping.outputs['Vector'], gradient.inputs['Vector'])

        # Color ramp for gradient colors
        color_ramp = world_nodes.new(type='ShaderNodeValToRGB')
        color_ramp.location = (-200, 0)
        color_ramp.color_ramp.elements[0].color = bottom_color
        color_ramp.color_ramp.elements[1].color = top_color
        world_links.new(gradient.outputs['Fac'], color_ramp.inputs['Fac'])

        # Background shader
        bg_shader = world_nodes.new(type='ShaderNodeBackground')
        bg_shader.location = (0, 0)
        # Dark background with NO ambient lighting - only 3-point lights illuminate
        bg_shader.inputs['Strength'].default_value = 0.0  # No ambient light
        world_links.new(color_ramp.outputs['Color'], bg_shader.inputs['Color'])

        # Connect to output
        world_links.new(bg_shader.outputs['Background'], output_node.inputs['Surface'])
    elif not args.transparent_background:
        # Solid color background
        bg_shader = world_nodes.new(type='ShaderNodeBackground')
        bg_shader.location = (0, 0)
        # Convert hex color to RGB
        hex_color = args.background_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
        bg_shader.inputs['Color'].default_value = (r, g, b, 1.0)
        # Subtle ambient lighting - adds soft fill without washing out the 3-point lights
        bg_shader.inputs['Strength'].default_value = 0.2

        # Connect to output
        world_links.new(bg_shader.outputs['Background'], output_node.inputs['Surface'])


def setup_animation(scene, pcb_objects, scene_center, args):
    """Set up rotation animation by rotating the board stack around Y-axis using a parent empty."""
    import math
    import bpy
    from mathutils import Euler

    # Create an empty at the scene center to act as parent/pivot
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=scene_center)
    pivot = bpy.context.active_object
    pivot.name = "RotationPivot"

    # Parent all PCB objects to the pivot
    for obj in pcb_objects:
        obj.parent = pivot
        # Keep the transform - objects stay in place visually but are now relative to pivot
        obj.matrix_parent_inverse = pivot.matrix_world.inverted()

    # Animate the pivot rotation around Y-axis
    for frame in range(1, args.frames + 1):
        # Calculate rotation angle for this frame (full 360° rotation)
        angle = (frame - 1) / args.frames * 2 * math.pi

        # Set pivot rotation
        pivot.rotation_euler.y = angle

        # Insert keyframe for pivot
        pivot.keyframe_insert(data_path="rotation_euler", index=1, frame=frame)


def main():
    """Main execution function."""
    args = parse_args()

    print(f"Rendering PCB boards:")
    for i, board_path in enumerate(args.board):
        print(f"  Board {i+1}: {board_path}")
        print(f"    Z-offset: {args.board_offset[i]}mm")
        if args.board_shift_x[i] != 0 or args.board_shift_y[i] != 0:
            print(f"    XY-shift: ({args.board_shift_x[i]}, {args.board_shift_y[i]})mm")
    print(f"  Output: {args.output}")

    # Enable pcb2blender addon
    enable_pcb2blender_addon()

    # Clear default scene
    clear_scene()

    # Import all boards with their offsets
    pcb_objects = []
    for i, board_path in enumerate(args.board):
        scaled_offset = args.board_offset[i] * args.scale_factor
        print(f"\nImporting board {i+1} (Z-offset: {args.board_offset[i]}mm real = {scaled_offset:.3f}mm scene)...")
        before_count = len(bpy.context.scene.objects)
        board_objs = import_pcb3d(board_path, z_offset=scaled_offset)
        after_count = len(bpy.context.scene.objects)
        print(f"  Scene grew from {before_count} to {after_count} objects ({after_count - before_count} added)")

    # Find PCB objects and apply transformations
    import math

    # First pass: collect all PCB objects and match them to boards
    board_pcb_map = {}  # Maps board index to PCB object
    for obj in bpy.context.scene.objects:
        if 'PCB_' in obj.name:
            pcb_objects.append(obj)

            # Find which board this is
            for i, board_path in enumerate(args.board):
                board_name = Path(board_path).stem
                if board_name in obj.name:
                    board_pcb_map[i] = obj
                    # Rotate 180° around Z-axis for better viewing angle
                    obj.rotation_euler.z = math.radians(180)
                    break

    print(f"  Rotated all boards 180° around Z-axis")
    bpy.context.view_layer.update()

    # Second pass: align Y positions to first board, then apply XY shifts
    if len(board_pcb_map) > 1:
        # Use first board as reference for Y alignment
        first_pcb = board_pcb_map[0]
        reference_y = first_pcb.location.y
        print(f"\nAligning boards to first board's Y position: {reference_y:.4f}")

        for i in range(1, len(args.board)):
            if i in board_pcb_map:
                pcb = board_pcb_map[i]
                old_y = pcb.location.y
                # First align Y to reference
                pcb.location.y = reference_y
                print(f"  Board {i+1} Y: {old_y:.4f} -> {reference_y:.4f} (delta: {reference_y - old_y:.4f})")

                # Then apply any XY shifts
                if args.board_shift_x[i] != 0 or args.board_shift_y[i] != 0:
                    scaled_shift_x = args.board_shift_x[i] * args.scale_factor
                    scaled_shift_y = args.board_shift_y[i] * args.scale_factor
                    pcb.location.x += scaled_shift_x
                    pcb.location.y += scaled_shift_y
                    print(f"  Applied XY shift: ({args.board_shift_x[i]}, {args.board_shift_y[i]})mm")

    bpy.context.view_layer.update()

    # Check what's in the scene
    all_objects = list(bpy.context.scene.objects)
    print(f"\nTotal objects in scene: {len(all_objects)}")

    # Find and report the PCB board objects specifically
    print("\nLooking for PCB board objects...")
    for obj in all_objects:
        if 'PCB_' in obj.name or 'board' in obj.name.lower():
            print(f"  {obj.name}: location={obj.location}, type={obj.type}")
            if obj.type == 'MESH' and obj.data:
                # Calculate this object's bounds
                if hasattr(obj.data, 'vertices') and len(obj.data.vertices) > 0:
                    from mathutils import Vector
                    verts = [obj.matrix_world @ v.co for v in obj.data.vertices]
                    min_z = min(v.z for v in verts)
                    max_z = max(v.z for v in verts)
                    print(f"    Mesh Z range: {min_z:.2f} to {max_z:.2f}")

    # Calculate scene bounds
    print("\nCalculating scene bounds...")
    min_coords, max_coords, scene_center, scene_size = get_scene_bounds()

    print(f"  Center: ({scene_center.x:.1f}, {scene_center.y:.1f}, {scene_center.z:.1f})")
    print(f"  Size: ({scene_size.x:.1f}, {scene_size.y:.1f}, {scene_size.z:.1f})")

    # Set up scene
    # For animation, default to top view; otherwise use specified view
    camera_view = "top" if args.animate and args.camera_view == "angle" else args.camera_view
    projection_type = "orthographic" if args.orthographic else "perspective"
    print(f"Setting up camera ({camera_view} view, {projection_type}) and lights...")

    # Apply board rotation FIRST to achieve different views
    camera, board_rotation = setup_camera(scene_center, scene_size, view_type=camera_view, distance_multiplier=args.camera_distance_multiplier)

    if board_rotation:
        print(f"  Applying board rotation for {camera_view} view...")
        for obj in pcb_objects:
            obj.rotation_euler = board_rotation
        bpy.context.view_layer.update()

        # Recalculate scene bounds after rotation
        print(f"  Recalculating scene bounds after rotation...")
        min_coords, max_coords, scene_center, scene_size = get_scene_bounds()

        # Re-center camera on the rotated board
        print(f"  Re-centering camera on rotated board...")
        from mathutils import Vector
        import math
        max_xy = max(scene_size.x, scene_size.y)
        distance = max_xy * 2.5 * args.camera_distance_multiplier

        angle_x_rad = math.radians(45)
        angle_z_rad = math.radians(-45)

        cam_x = distance * math.cos(angle_z_rad)
        cam_y = -distance * math.sin(angle_z_rad)
        cam_z = distance * 0.5

        camera.location = scene_center + Vector((cam_x, cam_y, cam_z))

        # Re-point camera at new scene center
        direction = scene_center - camera.location
        rot_quat = direction.to_track_quat('-Z', 'Y')
        camera.rotation_euler = rot_quat.to_euler()

    if args.orthographic:
        setup_orthographic_camera(camera, scene_size)

    print(f"  Camera location: {camera.location}")

    setup_lighting(scene_center, scene_size, transparent_background=args.transparent_background)

    # Configure render settings
    scene = bpy.context.scene
    setup_render_settings(scene, args)

    # Enable auto-crop if requested
    if args.auto_crop:
        print(f"\nConfiguring auto-crop...")
        setup_border_render(camera, scene, is_animation=args.animate)

    # Set up animation if requested
    if args.animate:
        print(f"\nSetting up animation ({args.frames} frames at {args.fps} fps)...")
        # pcb_objects list already populated from board imports above
        # Keep boards stationary, camera will orbit around them
        # No need to reset rotation - boards stay in place

        setup_animation(scene, pcb_objects, scene_center, args)
        print(f"  Animation keyframes created (camera orbiting around center)")

        # Render animation
        print(f"Rendering animation with {args.samples} samples at {args.resolution_x}x{args.resolution_y}...")
        bpy.ops.render.render(animation=True)
        print(f"✓ Animation complete: {args.output}")
    else:
        # Render still image
        print(f"Rendering with {args.samples} samples at {args.resolution_x}x{args.resolution_y}...")
        bpy.ops.render.render(write_still=True)
        print(f"✓ Render complete: {args.output}")


if __name__ == "__main__":
    main()

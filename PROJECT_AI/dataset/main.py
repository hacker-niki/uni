import bpy
import os
import random
import math

# ##### НАСТРОЙКИ (с относительными путями) #####
# Эти пути НЕ нужно менять, если вы следуете структуре папок.

# Количество образцов для генерации
NUM_SAMPLES = 20

# Относительный путь к папке для сохранения результатов
# '//' означает "папка, где сохранен этот .blend файл"
OUTPUT_PATH = "//dataset/"

# Относительный путь к папке с текстурами
TEXTURES_PATH = "//textures/"

# Разрешение изображений
RENDER_WIDTH = 512
RENDER_HEIGHT = 512

# ID для маски
BOX_PASS_INDEX = 1
# ##### КОНЕЦ НАСТРОЕК #####


# --- Функции-помощники ---

def clear_scene():
    """ Удаляет все объекты, материалы и данные из сцены """
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    # Очистка "сиротских" данных
    for block in bpy.data.meshes:
        if block.users == 0: bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0: bpy.data.materials.remove(block)
    for block in bpy.data.textures:
        if block.users == 0: bpy.data.textures.remove(block)
    for block in bpy.data.images:
        if block.users == 0: bpy.data.images.remove(block)


def setup_render_settings():
    """ Настраивает движок рендеринга и разрешение """
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    # Для ускорения можно уменьшить количество сэмплов
    scene.cycles.samples = 64 
    scene.render.image_settings.file_format = 'PNG'
    scene.render.resolution_x = RENDER_WIDTH
    scene.render.resolution_y = RENDER_HEIGHT
    scene.render.resolution_percentage = 100
    bpy.context.view_layer.use_pass_object_index = True


def create_gift_box():
    """ Создает коробку случайного размера и назначает ей pass_index """
    scale_x = random.uniform(0.2, 0.8)
    scale_y = random.uniform(0.2, 0.8)
    scale_z = random.uniform(0.1, 0.5)
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, scale_z))
    box = bpy.context.active_object
    box.scale = (scale_x, scale_y, scale_z)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    box.pass_index = BOX_PASS_INDEX
    bpy.ops.object.shade_smooth()
    bevel = box.modifiers.new(name='Bevel', type='BEVEL')
    bevel.width = 0.01
    bevel.segments = 3
    return box

def apply_random_texture(obj, textures_dir_relative):
    """ Применяет случайную текстуру из папки к объекту """
    # Преобразуем относительный путь Blender в абсолютный путь, понятный Python
    abs_textures_path = bpy.path.abspath(textures_dir_relative)
    
    if not os.path.exists(abs_textures_path):
        print(f"Предупреждение: папка с текстурами не найдена по пути: {abs_textures_path}")
        return

    try:
        texture_files = [f for f in os.listdir(abs_textures_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not texture_files:
            print(f"Предупреждение: не найдено текстур в папке {abs_textures_path}")
            return

        chosen_texture = random.choice(texture_files)
        # Используем относительный путь для загрузчика Blender
        texture_path = os.path.join(textures_dir_relative, chosen_texture)
        
        mat = bpy.data.materials.new(name="BoxMaterial")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get('Principled BSDF')
        tex_image_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
        
        tex_image_node.image = bpy.data.images.load(texture_path)
        mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image_node.outputs['Color'])
        obj.data.materials.append(mat)
    except Exception as e:
        print(f"Ошибка при применении текстуры: {e}")


def setup_lighting_and_camera():
    """ Устанавливает случайное освещение и положение камеры """
    bpy.ops.object.camera_add()
    camera = bpy.context.active_object
    bpy.context.scene.camera = camera
    target_obj = next((obj for obj in bpy.data.objects if obj.type == 'MESH'), None)
    if not target_obj: return

    track_constraint = camera.constraints.new(type='TRACK_TO')
    track_constraint.target = target_obj
    track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    track_constraint.up_axis = 'UP_Y'
    
    radius = random.uniform(2.0, 4.0)
    theta = random.uniform(math.pi/4, 3*math.pi/4)
    phi = random.uniform(0, 2 * math.pi)
    
    camera.location.x = radius * math.sin(theta) * math.cos(phi)
    camera.location.y = radius * math.sin(theta) * math.sin(phi)
    camera.location.z = radius * math.cos(theta)

    bpy.ops.object.light_add(type='SUN', location=(0, 0, 5))
    light = bpy.context.active_object
    light.data.energy = random.uniform(1.5, 4.0)
    light.rotation_euler.x = math.radians(random.uniform(20, 70))
    light.rotation_euler.y = math.radians(random.uniform(-45, 45))


def setup_compositor_nodes(sample_name):
    """ Настраивает ноды композитора для сохранения всех нужных выходов """
    scene = bpy.context.scene
    scene.use_nodes = True
    tree = scene.node_tree
    for node in tree.nodes: tree.nodes.remove(node)
        
    render_layers = tree.nodes.new('CompositorNodeRLayers')
    
    # Выходные ноды теперь используют относительные пути
    rgb_output_node = tree.nodes.new('CompositorNodeFileOutput')
    rgb_output_node.base_path = os.path.join(OUTPUT_PATH, "images")
    rgb_output_node.file_slots[0].path = f"{sample_name}_"
    
    depth_output_node = tree.nodes.new('CompositorNodeFileOutput')
    depth_output_node.base_path = os.path.join(OUTPUT_PATH, "depth")
    depth_output_node.file_slots[0].path = f"{sample_name}_"
    depth_output_node.format.file_format = 'OPEN_EXR'
    
    mask_output_node = tree.nodes.new('CompositorNodeFileOutput')
    mask_output_node.base_path = os.path.join(OUTPUT_PATH, "masks")
    mask_output_node.file_slots[0].path = f"{sample_name}_"
    mask_output_node.format.color_mode = 'BW'
    
    id_mask_node = tree.nodes.new('CompositorNodeIDMask')
    id_mask_node.index = BOX_PASS_INDEX

    tree.links.new(render_layers.outputs['Image'], rgb_output_node.inputs[0])
    tree.links.new(render_layers.outputs['Depth'], depth_output_node.inputs[0])
    tree.links.new(render_layers.outputs['IndexOB'], id_mask_node.inputs[0])
    tree.links.new(id_mask_node.outputs[0], mask_output_node.inputs[0])


# --- Главный цикл генерации ---

def main():
    """ Основная функция для запуска генерации датасета """
    # ПРОВЕРКА: убеждаемся, что файл сохранен, иначе относительные пути не сработают
    if not bpy.data.is_saved:
        print("\nОШИБКА: Пожалуйста, сохраните .blend файл перед запуском скрипта.")
        print("Относительные пути (//) работают только для сохраненных файлов.\n")
        return

    setup_render_settings()
    
    for i in range(NUM_SAMPLES):
        sample_name = f"sample_{i:04d}"
        print(f"--- Генерируется образец {i+1}/{NUM_SAMPLES}: {sample_name} ---")
        clear_scene()
        box = create_gift_box()
        apply_random_texture(box, TEXTURES_PATH)
        setup_lighting_and_camera()
        setup_compositor_nodes(sample_name)
        bpy.ops.render.render(write_still=True)
        
    print("--- Генерация датасета завершена! ---")
    print(f"Результаты сохранены в папку: {bpy.path.abspath(OUTPUT_PATH)}")


# Запуск главной функции
if __name__ == "__main__":
    main()

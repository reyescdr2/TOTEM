import os
import json
import uuid
import zipfile
import io
from PIL import Image

# --- PROTOCOLO DE COMPILACIÓN SOBERANA v55.0 (Absolute Sound Overdrive) ---
# Compilador recalibrado para blindar la audibilidad y la iconografía industrial.

def create_mcpack(name, desc, icon_bytes, frames, audio_bytes=None):
    """
    Consolidación de Activos v55.0.
    1. Iconografía Industrial: Incrustación de pack_icon.png.
    2. Sound Overdrive: Inyecta múltiples disparadores para asegurar que el sonido se escuche.
    3. Ultra-Resolución: Mapeo de texturas a 256x256.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        # 1. MANIFEST (Identidad v2.0.0)
        manifest = {
            "format_version": 2,
            "header": {
                "name": name,
                "description": desc,
                "uuid": str(uuid.uuid4()),
                "version": [2, 0, 0],
                "min_engine_version": [1, 20, 0]
            },
            "modules": [{"type": "resources", "uuid": str(uuid.uuid4()), "version": [2, 0, 0]}]
        }
        zip_file.writestr("manifest.json", json.dumps(manifest, indent=4))
        
        # 2. ICONO (Identidad del Pack)
        if not icon_bytes:
            fallback = os.path.join(os.getcwd(), "CDRLOGO.png")
            if os.path.exists(fallback):
                try:
                    with open(fallback, "rb") as f:
                        icon_bytes = f.read()
                except: pass
        if icon_bytes:
            zip_file.writestr("pack_icon.png", icon_bytes)
            
        # 3. TEXTURAS (High-Fidelity)
        for i, frame in enumerate(frames):
            frame_256 = frame.resize((256, 256), Image.Resampling.LANCZOS)
            frame_256.info.clear() 
            f_bytes = io.BytesIO()
            frame_256.save(f_bytes, format="PNG")
            zip_file.writestr(f"textures/item/item{i+1}.png", f_bytes.getvalue())
            
        # Flipbook 2D
        strip = Image.new("RGBA", (256, 256 * len(frames)))
        for i, frame in enumerate(frames):
            strip.paste(frame.resize((256, 256)), (0, i * 256))
        s_bytes = io.BytesIO()
        strip.save(s_bytes, format="PNG")
        zip_file.writestr("textures/items/totem.png", s_bytes.getvalue())

        zip_file.writestr("item_texture.json", json.dumps({
            "resource_pack_name": "totem",
            "texture_data": {"totem": {"textures": "textures/items/totem"}}
        }, indent=4))
        
        zip_file.writestr("textures/flipbook_textures.json", json.dumps([
            {
                "flipbook_texture": "textures/items/totem",
                "atlas_tile": "totem",
                "frames": list(range(len(frames))),
                "ticks_per_frame": 2
            }
        ], indent=4))
        
        # 4. GEOMETRÍA (vm.geo.json)
        geometry = {
            "format_version": "1.16.0",
            "minecraft:geometry": [
                {
                    "description": {
                        "identifier": "geometry.vm",
                        "texture_width": 256,
                        "texture_height": 256,
                        "visible_bounds_width": 15,
                        "visible_bounds_height": 5,
                        "visible_bounds_offset": [0, 0.5, 0]
                    },
                    "bones": [
                        {
                            "name": "leftitem",
                            "pivot": [0, 0, 0],
                            "cubes": [
                                {
                                    "origin": [2 + (j*0.01), 0, 0],
                                    "size": [0, 2, 2],
                                    "uv": {
                                        "north": {"uv": [11, 11], "uv_size": [2, 2]},
                                        "east": {"uv": [256, 256], "uv_size": [-1, -1]},
                                        "south": {"uv": [9, 11], "uv_size": [2, 2]},
                                        "west": {"uv": [0, 0], "uv_size": [256, 256]},
                                        "up": {"uv": [20, 12], "uv_size": [-2, -12]},
                                        "down": {"uv": [22, 12], "uv_size": [-2, -12]}
                                    }
                                } for j in range(11)
                            ]
                        }
                    ]
                }
            ]
        }
        zip_file.writestr("models/entity/vm.geo.json", json.dumps(geometry, indent=4))
        
        # 5. ANIMACIONES (Scale Boost)
        animation = {
            "format_version": "1.10.0",
            "animations": {
                "animation.leftblock.first_person_wield": {
                    "loop": True,
                    "bones": {
                        "leftitem": {
                            "rotation": ["c.is_first_person ? -15.0 : 100.0", "c.is_first_person ? 30.0 : 20.0", "c.is_first_person ? 4.0 : 80.0"],
                            "position": ["c.is_first_person ? -23.0 : -6.2", "c.is_first_person ? 7.0 : 7.0", "c.is_first_person ? 11.0 : 4.0"],
                            "scale": ["c.is_first_person ? 3.3 : 5", "c.is_first_person ? 3.3 : 5", "c.is_first_person ? 3.3 : 5"]
                        }
                    }
                }
            }
        }
        zip_file.writestr("animations/vleftblock.animation.json", json.dumps(animation, indent=4))

        # 6. RENDER CONTROLLER
        rc = {
            "format_version": "1.10",
            "render_controllers": {
                "controller.render.item_animation_totem": {
                    "arrays": {
                        "textures": {"array.item_frames": [f"texture.item_frame_{i+1}" for i in range(len(frames))]}
                    },
                    "geometry": "Geometry.default",
                    "materials": [{"*": "variable.is_enchanted ? material.enchanted : material.default"}],
                    "textures": [
                        f"temp.life_time = query.life_time * 10.0; return array.item_frames[math.mod(temp.life_time, {len(frames)})];",
                        "texture.enchanted"
                    ]
                }
            }
        }
        zip_file.writestr("render_controllers/item_animation.render_controllers.json", json.dumps(rc, indent=4))

        # 7. ATTACHABLE
        attach = {
            "format_version": "1.10.0",
            "minecraft:attachable": {
                "description": {
                    "identifier": "minecraft:totem_of_undying",
                    "materials": {"default": "entity_alphatest", "enchanted": "entity_alphatest_glint"},
                    "textures": {**{f"item_frame_{i+1}": f"textures/item/item{i+1}" for i in range(len(frames))}, "enchanted": "textures/misc/enchanted_item_glint"},
                    "geometry": {"default": "geometry.vm"},
                    "animations": {"wield": "animation.leftblock.first_person_wield"},
                    "scripts": {"animate": ["wield"]},
                    "render_controllers": ["controller.render.item_animation_totem"]
                }
            }
        }
        zip_file.writestr("attachables/totem.json", json.dumps(attach, indent=4))

        # 8. AUDIO OVERDRIVE (Multi-Trigger Infallible)
        if audio_bytes:
            # 1. El archivo físico absoluto
            zip_file.writestr("sounds/random/totem.ogg", audio_bytes)
            
            # 2. DEFINICIÓN DE SONIDOS (Multi-disparo)
            # Cubrimos TODOS los identificadores posibles para asegurar la activación.
            sound_defs = {
                "format_version": "1.20.0",
                "sound_definitions": {
                    "random.totem": {
                        "category": "player",
                        "sounds": [
                            {
                                "name": "sounds/random/totem",
                                "volume": 2.0,
                                "pitch": 1.0,
                                "load_on_low_memory": True
                            }
                        ]
                    },
                    "item.totem.use": {
                        "category": "player",
                        "sounds": ["sounds/random/totem"]
                    }
                }
            }
            # INSERCIÓN REDUNDANTE (Double-Binding)
            json_str = json.dumps(sound_defs, indent=4)
            zip_file.writestr("sounds/sound_definitions.json", json_str) # Prioridad 1
            zip_file.writestr("sound_definitions.json", json_str)        # Prioridad 2

    return zip_buffer.getvalue()

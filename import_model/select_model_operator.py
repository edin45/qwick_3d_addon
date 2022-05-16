import bpy
import os
import json
import urllib.request
import requests
import math

class WM_OT_download_model(bpy.types.Operator):
    """"""
    bl_label = "model download"
    bl_idname = "wm.download_model"
    
#    def __init__(self, model_name):
#        self.model_name = model_name
    
    def execute(self, context):
        print('download')
        f = urllib.request.urlopen("http://localhost/models/get_model_index.php?license=62815c6be654d")
        f.read()
        return {'FINISHED'}

class WM_OT_select_model(bpy.types.Operator):
    """"""
    bl_label = "Qwick3d Asset Browser"
    bl_idname = "wm.select_model"
    
    model_search : bpy.props.StringProperty(name = "Search",default="")
#    preset_enum : bpy.props.EnumProperty(
#        name = "",
#        description = "abc",
#        items=[
#            ('1','a','a1'),
#            ('2','b','b2'),
#            ('3','c','c3'),
#        ]
#    )

    @classmethod
    def poll(cls,context):
        obj = context.object
        if obj is not None:
            if obj.mode == "OBJECT":
                return True
        return False
    
    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self,context,event):
        #,width=1280
        return context.window_manager.invoke_props_dialog(self,width=800)
    
    def draw(self,context):
        layout = self.layout
        # layout.prop(self, "preset_enum")
        layout.prop(self, "model_search")
        
        # This tells Blender to draw the my_previews window manager object
        # (Which is our preview)
        # print(models)
        index = 0
        columns = 4
        for i in range(0,int(math.ceil(len(models) / columns))):
            print(f"loop_1: {i}")
            row = layout.row()
            # len(models) - index, min
            for x in range(index,(index + columns)):
                if index > len(models) - 1:
                    break
                print(f"loop_2: {x}")
                column = row.column()
                img = preview_collections["thumbnail_previews"][models[index]['model_name'] + '.jpg']
                # row.template_icon_view(context.scene, "my_thumbnails")
                
                button_name = f"Download {models[index]['display_name']}"
                column.template_icon(icon_value=img.icon_id,scale=10)
                column.operator("wm.download_model", text = button_name)
                index+=1
            
        # Just a way to access which one is selected
        #row = layout.row()
        #row.label(text="You selected: " + bpy.context.scene.my_thumbnails)

preview_collections = {}
models = []

asset_location = "/home/edin/blender/assets/"
preview_location = "/home/edin/blender/previews/"

def generate_previews(images_location):
    # We are accessing all of the information that we generated in the register function below
    pcoll = preview_collections["thumbnail_previews_prep"]
    image_location = images_location
    VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg')
        
    index = 0
    # Generate the thumbnails
    for i, image in enumerate(os.listdir(image_location)):
        if image.endswith(VALID_EXTENSIONS):
            filepath = os.path.join(image_location, image)
            thumb = pcoll.load(f"{image}", filepath, 'IMAGE')
            index+=1
    return pcoll

def get_models(keyword):
    if not os.path.exists(preview_location):
        os.mkdir(preview_location)
        
    f = urllib.request.urlopen("http://localhost/backend/get_model_index.php?license=62815c6be654d")
    in_json = json.loads(f.read())
    result = in_json['models']
    
    for i in in_json['models']:
        print(i['display_name'])
        response = requests.get(f"http://localhost/backend/previews/{i['model_name']}.jpg")
        open(os.path.join(preview_location, i['model_name'] + ".jpg"), "wb").write(response.content)
    # print(in_json['models'][0]['display_name'])
    return result

addon_keymaps = []
def register():
    global models
    # Get the models from the webiste, fill in the previews
    
    models = get_models("")
    print(f"models: {models}")
    
    pcoll = bpy.utils.previews.new()
    
    # This line needs to be uncommented if you install as an addon
    images_location = preview_location
    
    # This line is for running as a script. Make sure images are in a folder called images in the same
    # location as the Blender file. Comment out if you install as an addon
    #pcoll.images_location = bpy.path.abspath('//images')
    
    # Enable access to our preview collection outside of this function
    preview_collections["thumbnail_previews_prep"] = pcoll
    preview_collections["thumbnail_previews"] = generate_previews(images_location)
    
    bpy.utils.register_class(WM_OT_select_model)
    bpy.utils.register_class(WM_OT_download_model)
    
    # This is an EnumProperty to hold all of the images
    # You really can save it anywhere in bpy.types.*  Just make sure the location makes sense
    #bpy.types.Scene.my_thumbnails = bpy.props.EnumProperty(
    #    items=generate_previews(),
    #)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(WM_OT_select_model.bl_idname, 'K', 'PRESS', ctrl=False, shift=False)
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(WM_OT_select_model)
    bpy.utils.unregister_class(WM_OT_download_model)
    bpy.utils.previews.remove()
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()



if __name__ == "__main__":
    register()
    
    bpy.ops.wm.select_model('INVOKE_DEFAULT')
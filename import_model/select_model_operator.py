import bpy
import os
import json
import urllib.request
import requests
import math

license = "62815c6be654d";

class DonwloadInfoPropertyGroup(bpy.types.PropertyGroup):
    res : bpy.props.EnumProperty(
        name = "res",
        description = "abc",
        items=[
            ('1k','1K','1k'),
            ('2k','2K','2k'),
            ('4k','4K','4k'),
        ],
        default='4k'
    )

class WM_OT_download_model(bpy.types.Operator):
    """"""
    bl_label = "model download"
    bl_idname = "wm.download_model"
    
    model_name : bpy.props.StringProperty(  # bl 2.80 use testint: bpy.props
        name="model_name",
        description="",
        default="",
        )
    
#    def __init__(self, model_name):
#        self.model_name = model_name
    
    def execute(self, context):
        props = context.scene.DonwloadInfoPropertyGroup
        print('download')
        f = urllib.request.urlopen(f"http://localhost/backend/download_model.php?license={license}&model_name={self.model_name}&preferred_resolution={props.res}")
        download_url = "http://localhost/backend" + f.read().decode("utf-8")
        print(download_url)
        response = requests.get(download_url)
        
        result_folder = os.path.join(asset_location, self.model_name + "_" + props.res + ".blend")
        open(result_folder, "wb").write(response.content)
        
        print(result_folder)
        
        bpy.ops.wm.append(
            filepath=os.path.join(result_folder, 'Object', self.model_name),
            directory=os.path.join(result_folder, 'Object'),
            filename=self.model_name
        )
        
        return {'FINISHED'}

class WM_OT_select_model(bpy.types.Operator):
    """"""
    bl_label = "Qwick3d Asset Browser"
    bl_idname = "wm.select_model"
    
    model_search : bpy.props.StringProperty(name = "Search",default="")
#    res : bpy.props.EnumProperty(
#        name = "resolution",
#        description = "abc",
#        items=[
#            ('1','1K','1k'),
#            ('2','2K','2k'),
#            ('3','4K','4k'),
#        ],
#        default='3'
#    )

    @classmethod
    def poll(cls,context):
#        obj = context.object
#        if obj is not None:
#            if obj.mode == "OBJECT":
#                return True
        return True
    
    def execute(self, context):
        print('execute')
        return {'FINISHED'}
    
    def invoke(self,context,event):
        #,width=1280
        return context.window_manager.invoke_props_dialog(self,width=800)
    
    def draw(self,context):
        layout = self.layout
        props = context.scene.DonwloadInfoPropertyGroup
        layout.prop(props, "res")
#        layout.prop(self, "res")
        layout.prop(self, "model_search")
        
        
        
        # This tells Blender to draw the my_previews window manager object
        # (Which is our preview)
        # print(models)
        index = 0
        columns = 4
        for i in range(0,int(math.ceil(len(models) / columns))):
            row = layout.row()
            # len(models) - index, min
            for x in range(index,(index + columns)):
                if index > len(models) - 1:
                    break
                column = row.column()
                img = preview_collections["thumbnail_previews"][models[index]['model_name'] + '.jpg']
                # row.template_icon_view(context.scene, "my_thumbnails")
                
                button_name = f"Download {models[index]['display_name']}"
                column.template_icon(icon_value=img.icon_id,scale=10)
                column.operator("wm.download_model", text = f"{button_name}").model_name = models[index]['model_name']
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
        
    f = urllib.request.urlopen(f"http://localhost/backend/get_model_index.php?license={license}")
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
    bpy.utils.register_class(DonwloadInfoPropertyGroup)
    
    bpy.types.Scene.DonwloadInfoPropertyGroup = bpy.props.PointerProperty(
            type=DonwloadInfoPropertyGroup)
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
    bpy.utils.unregister_class(DonwloadInfoPropertyGroup)
    del bpy.types.Scene.DonwloadInfoPropertyGroup
    
    bpy.utils.previews.remove()
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()



if __name__ == "__main__":
    register()
    
    bpy.ops.wm.select_model('INVOKE_DEFAULT')
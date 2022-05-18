import bpy
import os
import json
import urllib.request
import requests
import math
import qwick3d_importer

class WM_OT_select_model(bpy.types.Operator):
    """"""
    bl_label = "Qwick3d Asset Browser"
    bl_idname = "wm.select_model"

    def __init__(self):
        qwick3d_importer.setup()

    
    model_search : bpy.props.StringProperty(name = "Search (Press enter to search)",default="",options={'TEXTEDIT_UPDATE'})
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

    # for pagination
    start = 0
    end = 10

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
        qwick3d_importer.setup()
        return context.window_manager.invoke_props_dialog(self,width=800)
    
    def draw(self,context):

        print('draw')

        #ToDo: Implement model search

        #qwick3d_importer.models = qwick3d_importer.get_models(self.model_search)
        qwick3d_importer.fill_disp_models(self.start,self.end,self.model_search)

        # global qwick3d_importer.models

        # qwick3d_importer.models = qwick3d_importer.get_models("")
        # print(f"models: {qwick3d_importer.models}")

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
        print(qwick3d_importer.disp_models)
        for i in range(0,int(math.ceil(len(qwick3d_importer.disp_models) / columns))):
            row = layout.row()
            # len(models) - index, min
            for x in range(index,(index + columns)):
                if index > len(qwick3d_importer.disp_models) - 1:
                    break
                column = row.column()
                img = qwick3d_importer.preview_collections["thumbnail_previews"][qwick3d_importer.disp_models[index]['model_name'] + '.jpg']
                # row.template_icon_view(context.scene, "my_thumbnails")
                
                button_name = f"Download {qwick3d_importer.disp_models[index]['display_name']}"
                column.template_icon(icon_value=img.icon_id,scale=10)
                column.operator("wm.download_model", text = f"{button_name}").model_name = qwick3d_importer.disp_models[index]['model_name']
                index+=1
import bpy
import os
import json
import urllib.request
import requests
import math
import qwick3d_importer

class WM_OT_select_model(bpy.types.Operator):
    """"""
    bl_label = "Qwick3d Asset Browser, (Downloads work in the background so you can close this alert anytime)"
    bl_idname = "wm.select_model"

    last_updated_search_query = ""
    # def __init__(self):
        # qwick3d_importer.setup()

    @classmethod
    def poll(cls,context):
        return True
    
    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self,context,event):
        #,width=1280
        qwick3d_importer.setup()
        return context.window_manager.invoke_props_dialog(self,width=800)

    def check(self, context):
        props = context.scene.DonwloadInfoPropertyGroup
        if props.update_ui == True or props.model_search != self.last_updated_search_query:
            self.last_updated_search_query = props.model_search
            props.update_ui = False
            return True
        return False
    
    def draw(self,context):

        props = context.scene.DonwloadInfoPropertyGroup

        qwick3d_importer.fill_disp_models(props.start,props.end,props.model_search)

        # global qwick3d_importer.models

        # qwick3d_importer.models = qwick3d_importer.get_models("")
        # print(f"models: {qwick3d_importer.models}")

        layout = self.layout
        
        layout.prop(props, "res")

        layout.prop(props, "model_search")
        
        index = 0

        # How many models for every row
        columns = 4

        # Iterate over models and show them
        for i in range(0,int(math.ceil(len(qwick3d_importer.disp_models) / columns))):
            
            row = layout.row()
            
            for x in range(index,(index + columns)):
                if index > len(qwick3d_importer.disp_models) - 1:
                    break
                column = row.column()
                img = qwick3d_importer.preview_collections["thumbnail_previews"][qwick3d_importer.disp_models[index]['model_name'] + '.jpg']
                
                button_name = f"Download {qwick3d_importer.disp_models[index]['display_name']}"
                column.template_icon(icon_value=img.icon_id,scale=10)
                column.operator("wm.download_model", text = f"{button_name}").model_name = qwick3d_importer.disp_models[index]['model_name']
                index+=1
        
        # Pagination
        pagination_row = layout.row()
        pagination_row.operator("wm.previous_page",text="Previous Page")
        pagination_row.operator("wm.next_page",text="Next Page")

class WM_OT_previous_page(bpy.types.Operator):
    """"""
    bl_label = "Previous Page"
    bl_idname = "wm.previous_page"

    def execute(self, context):
        props = context.scene.DonwloadInfoPropertyGroup

        if props.start > 0:
            props.start = props.start - props.page_step_size
            props.end = props.end - props.page_step_size

        # qwick3d_importer.fill_disp_models(props.start,props.end,props.model_search)

        props.update_ui = True

        return {'FINISHED'}

class WM_OT_next_page(bpy.types.Operator):
    """"""
    bl_label = "Next Page"
    bl_idname = "wm.next_page"

    def execute(self, context):
        props = context.scene.DonwloadInfoPropertyGroup

        if props.end < len(qwick3d_importer.temp_search_array):
            props.start = props.start + props.page_step_size
            props.end = props.end + props.page_step_size

        # qwick3d_importer.fill_disp_models(props.start,props.end,props.model_search)

        props.update_ui = True

        return {'FINISHED'}
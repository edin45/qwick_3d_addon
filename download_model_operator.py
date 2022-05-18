import bpy
import urllib
import os
import qwick3d_importer
import _thread
import time

class WM_OT_download_model(bpy.types.Operator):
    """"""
    bl_label = "The Model is downloading, You can now close the alerts, The model will Auto-Import once the download is done."
    bl_idname = "wm.download_model"
    
    model_name : bpy.props.StringProperty(  # bl 2.80 use testint: bpy.props
        name="model_name",
        description="",
        default="",
        )
    
#    def __init__(self, model_name):
#        self.model_name = model_name

    def execute(self, context):
        override = bpy.context.copy()
        _thread.start_new_thread( download_model, (self.model_name,override) )
        return {'FINISHED'}

def download_model(model_name,override):
    props = bpy.context.scene.DonwloadInfoPropertyGroup
        
    f = urllib.request.urlopen(f"http://localhost/backend/download_model.php?license={qwick3d_importer.license}&model_name={model_name}&preferred_resolution={props.res}")
    download_url = "http://localhost/backend" + f.read().decode("utf-8")
    print(download_url)
    response = qwick3d_importer.requests.get(download_url)
        
    result_folder = os.path.join(qwick3d_importer.asset_location, model_name + "_" + props.res + ".blend")
    open(result_folder, "wb").write(response.content)
        
    bpy.ops.wm.append(
        override,
        filepath=os.path.join(result_folder, 'Object', model_name),
        directory=os.path.join(result_folder, 'Object'),
        filename=model_name
    )
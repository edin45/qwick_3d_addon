import bpy
import urllib
import os
import qwick3d_importer

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
        f = urllib.request.urlopen(f"http://localhost/backend/download_model.php?license={qwick3d_importer.license}&model_name={self.model_name}&preferred_resolution={props.res}")
        download_url = "http://localhost/backend" + f.read().decode("utf-8")
        print(download_url)
        response = qwick3d_importer.requests.get(download_url)
        
        result_folder = os.path.join(qwick3d_importer.asset_location, self.model_name + "_" + props.res + ".blend")
        open(result_folder, "wb").write(response.content)
        
        print(result_folder)
        
        bpy.ops.wm.append(
            filepath=os.path.join(result_folder, 'Object', self.model_name),
            directory=os.path.join(result_folder, 'Object'),
            filename=self.model_name
        )
        
        return {'FINISHED'}
import bpy
import urllib
import os
import qwick3d_importer
#import threading
from multiprocessing import Process, Queue
import time
import platform

class WM_OT_download_model(bpy.types.Operator):
    """Will download the Asset"""
    bl_label = "The Model is downloading, You can now close the alerts, The model will Auto-Import once the download is done."
    bl_idname = "wm.download_model"
    
    model_name : bpy.props.StringProperty(  # bl 2.80 use testint: bpy.props
        name="model_name",
        description="",
        default="",
        )
    _updating = False
    _download_done = False
    _timer = None

    
#    def __init__(self, model_name):
#        self.model_name = model_name

    def modal(self, context, event):
        
        if event.type == 'TIMER' and not self._updating:
            
            self._updating = True
            self.download_model(self.model_name)
            #self._updating = False
        if self._download_done:
            self.cancel(context)

        return {'PASS_THROUGH'}
    
    def execute(self, context):
        if qwick3d_importer.license == '' and bpy.context.scene.DonwloadInfoPropertyGroup.res != '1k':
            self.report({'INFO'}, "Free users can't download higher Resolutions than 1k will download 1k")
        context.window_manager.modal_handler_add(self)
        self._updating = False
        self._timer = context.window_manager.event_timer_add(0.5, window=context.window)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
    
        return {'CANCELLED'}

    def download_model(self,model_name):
        props = bpy.context.scene.DonwloadInfoPropertyGroup
            
        try:
            f = urllib.request.urlopen(f"http://localhost/backend/download_model.php?license={qwick3d_importer.license}&model_name={model_name}&preferred_resolution={props.res}")
            download_url = "http://localhost/backend" + f.read().decode("utf-8")
            print(download_url)
            response = qwick3d_importer.requests.get(download_url)

            #qwick3d_importer.asset_location + ("" if qwick3d_importer.asset_location[-1] == "/" or qwick3d_importer.asset_location[-1] == "\\" else ("/" if platform.system() == "Linux" else "\\")) + model_name + "_" + props.res + ".blend"
            result_folder = os.path.join(qwick3d_importer.asset_location, model_name + "_" + props.res + ".blend")
            open(result_folder, "wb").write(response.content)
                
            bpy.ops.wm.append(
                #override,
                filepath=os.path.join(result_folder, 'Object', model_name + "_" + props.res),
                directory=os.path.join(result_folder, 'Object'),
                filename=model_name + "_" + props.res
            )
            self._download_done = True
        except:
            print("exception")

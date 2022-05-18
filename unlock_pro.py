import bpy
import webbrowser

class WM_OT_unlock_pro(bpy.types.Operator):
    """"""
    bl_label = 'unlock pro'
    bl_idname = "wm.unlock_pro"

    def execute(self, context):
        webbrowser.open('https://qwick3d.com/unlock')
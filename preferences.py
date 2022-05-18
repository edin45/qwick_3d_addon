from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty
import bpy

class Qwick3dAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    previews_path: StringProperty(
        name="Preview Path (Required)",
        subtype='FILE_PATH',
    )
    asset_path: StringProperty(
        name="Asset Path, If it's the same as Asset browser assets will show up there (Required)",
        subtype='FILE_PATH',
    )
    license: StringProperty(
        name="License (Not Required)",
        default=""
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Qwick3d Preferences")
        layout.prop(self, "previews_path")
        layout.prop(self, "asset_path")
        layout.prop(self, "license")


# class OBJECT_OT_addon_prefs_qwick_3d(Operator):
#     """Display example preferences"""
#     bl_idname = "object.addon_prefs_qwick_3d"
#     bl_label = "Add-on Preferences Example"
#     bl_options = {'REGISTER', 'UNDO'}

#     def execute(self, context):
#         preferences = context.preferences
#         addon_prefs = preferences.addons[__name__].preferences

#         info = ("Path: %s, Number: %d, Boolean %r" %
#                 (addon_prefs.filepath, addon_prefs.number, addon_prefs.boolean))

#         self.report({'INFO'}, info)
#         print(info)

#         return {'FINISHED'}
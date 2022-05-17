# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "qwick3d_importer",
    "author" : "Edin Spiegel",
    "description" : "Importer for the Qwick3d asset library",
    "blender": (3, 0, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Import-Export",
}

import bpy
import os
import urllib
import json
import requests

from . select_model_operator import WM_OT_select_model
from . download_model_operator import WM_OT_download_model
from . download_info_property import DonwloadInfoPropertyGroup

classes = (WM_OT_select_model,WM_OT_download_model,DonwloadInfoPropertyGroup)

addon_keymaps = []
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

def register():

    global models

    models = get_models("")
    print(f"models: {models}")
    
    pcoll = bpy.utils.previews.new()
    images_location = preview_location
    preview_collections["thumbnail_previews_prep"] = pcoll
    preview_collections["thumbnail_previews"] = generate_previews(images_location)

    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.DonwloadInfoPropertyGroup = bpy.props.PointerProperty(
            type=DonwloadInfoPropertyGroup)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(WM_OT_select_model.bl_idname, 'K', 'PRESS', ctrl=False, shift=False)
        addon_keymaps.append((km, kmi))

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
        
    del bpy.types.Scene.DonwloadInfoPropertyGroup

    # remove previews
    bpy.utils.previews.remove()

    # Remove custom shortcuts
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()

import bpy
from bpy.props import *
from bpy.types import Menu, Operator, Panel, UIList, AddonPreferences
from bpy.app.handlers import persistent
import os
from os.path import basename, dirname, join
import shutil
import requests

class ARImporterAddonPreferences(AddonPreferences):

    bl_idname = basename(dirname(__file__))  # directory name containing this file

    ip_address = StringProperty(
            name="IP Address",
            )

    ar_root = StringProperty(
            name="Storage root",
            subtype='FILE_PATH',
            )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "ip_address")
        layout.prop(self, "ar_root")

# -------------------------------------------------------------------------------
# UI PANEL - Extra Image List
# -------------------------------------------------------------------------------
class ARImporter_PT_ImagePreview(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "AR Importer"
    bl_label = "Import"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("arimporter.latest", text="Import Latest")


class ARImportLatest(Operator):
    bl_idname = "arimporter.latest"
    bl_label = "Latest"
    bl_description = "AR Import Latest"

    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[basename(dirname(__file__))].preferences
        root_url = "http://%s/" % addon_prefs.ip_address

        print("Importing latest " + addon_prefs.ip_address)
        resp = requests.get(root_url + "shots").json()
        latest = resp[0]
        print(latest)
        local_shot_dir = join(addon_prefs.ar_root, latest["uuid"])

        file_types = ["_pointcloud_z.ply", ".mov", "_scene.fbx"]
        try:
            # Create target Directory
            os.mkdir(local_shot_dir)
        except FileExistsError:
            print("Directory ", local_shot_dir, " already exists")

        for file_type in file_types:
            remote_url  = root_url + "content/shots/%s/shot-%s%s" % (latest["uuid"], latest["uuid"], file_type)
            file_basename = basename(remote_url)
            local_file = join(local_shot_dir, file_basename)
            r = requests.get(remote_url, allow_redirects=True)
            open(local_file, 'wb').write(r.content)

        return {'FINISHED'}



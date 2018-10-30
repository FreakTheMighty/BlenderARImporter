
import bpy
from bpy.props import *
from bpy.types import Menu, Operator, Panel, UIList, AddonPreferences
from bpy.app.handlers import persistent
from os.path import basename, dirname

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
        print(user_preferences.addons.keys())
        addon_prefs = user_preferences.addons[basename(dirname(__file__))].preferences
        print("Importing latest " + addon_prefs.ip_address)
        return {'FINISHED'}



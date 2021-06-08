bl_info = {
    "name": "Tool Collection (ToolBox)",
    "author": "ZoZo Zoe",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View 3D > Tool Shelf > Tool Collection",
    "description": "A collection of simple but handy tools",
    "warning": "",
    "wiki_url": "",
    "category": "Tools",
}


import bpy
from bpy.types import (
    Operator,
    AddonPreferences,
    Panel,
    PropertyGroup,
)
from bpy.props import(StringProperty)

#----------------------------------------------
#               ToolBox Properties
#----------------------------------------------

class ToolBoxPropertyGroup(bpy.types.PropertyGroup):
    Armature: bpy.props.PointerProperty(type=bpy.types.Object)
    Mesh: bpy.props.PointerProperty(type=bpy.types.Object)





#----------------------------------------------
#               Main Panel
#----------------------------------------------

class ToolboxMainMenu(bpy.types.Panel):
    bl_label = "Tool Box"
    bl_idname = "SCENE_PT_main_menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool Collection"
    bl_option = {'REGISTER', 'UNDO'}
    
    def draw(self, context):
        layout = self.layout
        

    
#---------------------------------------------- Shapekey tools ----------------------------------------------        

#----------------------------------------------
#               Shapekey tools
#----------------------------------------------

class ShapekeyTools(bpy.types.Panel):
    bl_label = "Shapekey Tools"
    bl_idname = "SCENE_PT_shapekey_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool Collection"
    bl_parent_id= 'SCENE_PT_main_menu'
    bl_option = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        box = layout.box()
        col = box.column(align=True)
        row = layout.row()
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.5
        row.label(text="Select verts in shapekey")
        row.operator("object.shapekeyop", icon='VERTEXSEL')
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.5
        row.label(text="Remove verts from all shapekeys")
        row.operator("object.returnshapeop", icon='SHAPEKEY_DATA')

#----------------------------------------------
#               Select shapekey
#----------------------------------------------
	
class OBJECT_OT_shapekeyOp(Operator):
    bl_label = "Select shapekey verts"
    bl_idname = "object.shapekeyop"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool Collection"
    bl_option = {'REGISTER', 'UNDO'}
    

    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'MESH'

    
    def execute(self, context):
        
        tolerance = 1e-5
        obj = bpy.context.object
        shape_keys = obj.data.shape_keys.key_blocks
        current_selected = obj.active_shape_key_index
        sk1_data = shape_keys[current_selected].data
        skb_data = shape_keys['Basis'].data
        
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.object.mode_set(mode="OBJECT")
        
        for i, (x, y) in enumerate(zip(sk1_data, skb_data)):
            if (x.co - y.co).length > tolerance:
                obj.data.vertices[i].select = True
        bpy.ops.object.mode_set(mode="EDIT")
        
        return {"FINISHED"}
 
#----------------------------------------------
#               Select vert shapekey
#----------------------------------------------       

class OBJECT_OT_returnshapeOp(Operator):
    bl_label = "Return verts to shapekey"
    bl_idname = "object.returnshapeop"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool Collection"
    bl_option = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'MESH'
    
    def draw(self, context):
        layout = self.layout    
        layout.label(text="WARNING: This process will take a")
        layout.label(text="long time and blender will freeze")
        layout.label(text="Depending on the amount of shapekeys and")
        layout.label(text="hardware allow blender to take up to 5 min")
        
    def execute(self, context):
        
        o = bpy.context.view_layer.objects.active
        s = o.data.shape_keys.key_blocks.keys()
        
        if "Basis" in s:
            s.remove('Basis')
        
        for i in s:
            index = o.data.shape_keys.key_blocks.find(i)
            bpy.context.object.active_shape_key_index = index
            bpy.ops.mesh.blend_from_shape(shape='Basis', add=False)
            
        return {"FINISHED"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


#---------------------------------------------- Weightpaint Tools ----------------------------------------------

#----------------------------------------------
#               Weightpaint tools
#----------------------------------------------

class WeightpaintingTools(bpy.types.Panel):
    bl_label = "Weightpaint Tools"
    bl_idname = "SCENE_PT_weightpaint_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool Collection"
    bl_parent_id= 'SCENE_PT_main_menu'
    bl_option = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        box = layout.box()
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.5
        row.label(text="Transfer weights mesh to mesh")
        row.operator("object.transweight", icon='MOD_VERTEX_WEIGHT')
        
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.5
        row.label(text="Transfer weights from bone")
        row.operator("object.transweightsingle", icon='BONE_DATA')

#----------------------------------------------
#               Transfer Weights
#----------------------------------------------       

class OBJECT_OT_transweights(Operator):
    bl_label = "Transfer Weights"
    bl_idname = "object.transweight"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool Collection"
    bl_option = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'MESH'
 
        
    def execute(self, context):
        bpy.ops.object.mode_set(mode='WEIGHT_PAINT', toggle=False)
        bpy.ops.object.data_transfer(use_reverse_transfer=True, data_type='VGROUP_WEIGHTS', layers_select_src='NAME', layers_select_dst='ALL')
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        return {"FINISHED"}

#----------------------------------------------
#               Transfer Weights Single
#----------------------------------------------       

class OBJECT_OT_transweightsSingle(Operator):
    bl_label = "Transfer Weights Single"
    bl_idname = "object.transweightsingle"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool Collection"
    bl_option = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'MESH'
 
    def execute(self, context):

        bpy.ops.object.data_transfer(use_reverse_transfer=True, data_type='VGROUP_WEIGHTS',  vert_mapping='NEAREST', layers_select_src='NAME', layers_select_dst='BONE_SELECT', mix_mode='REPLACE')


        return {"FINISHED"}


#---------------------------------------------- Mesh tools ----------------------------------------------

#----------------------------------------------
#               Mesh Tools
#----------------------------------------------

class MeshMenu(bpy.types.Panel):
    bl_label = "Mesh Tools"
    bl_idname = "SCENE_PT_mesh_menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool Collection"
    bl_parent_id= 'SCENE_PT_main_menu'
    bl_option = {'REGISTER', 'UNDO', 'DEFAULT_CLOSED'}
    
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        box = layout.box()
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.5
        row.label(text="Object Shading:")

        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.5
        row.operator("object.shade_smooth")
        row.operator("object.shade_flat")

        row = layout.row()
        box = layout.box()
        col = box.column(align=True)
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.5
        row.label(text="Delete non existing vetex groups:")

        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.5
        row.label(text="Update object:")
        row.operator("object.selarmature", icon='MESH_DATA')
        row.operator("object.selmesh", icon='SHAPEKEY_DATA')

        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.5
        row.operator("object.remvertgroups", icon='OUTLINER_DATA_MESH')

#----------------------------------------------
#               Update Material
#----------------------------------------------
    
class OBJECT_OT_SelectArmatureOp(Operator):
    bl_label = "Armature"
    bl_idname = "object.selarmature"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool Collection Beta"
    bl_option = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'ARMATURE'

    def execute(self, context):
        
        ob = bpy.context.object
        bpy.context.scene.ToolBox.Armature = ob
        return {"FINISHED"}

#----------------------------------------------
#               Update Vertex
#----------------------------------------------
    
class OBJECT_OT_SelectMeshOp(Operator):
    bl_label = "Mesh"
    bl_idname = "object.selmesh"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool Collection Beta"
    bl_option = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'MESH'
    
    def execute(self, context):
        
        ob = bpy.context.object
        bpy.context.scene.ToolBox.Mesh = ob
        return {"FINISHED"}
    
    
#----------------------------------------------
#               Remove Vertex Groups
#----------------------------------------------
    
class OBJECT_OT_RemoveVertexGroupsOp(Operator):
    bl_label = "Remove Vertex Groups"
    bl_idname = "object.remvertgroups"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool Collection Beta"
    bl_option = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.context.scene.ToolBox.Armature and bpy.context.scene.ToolBox.Mesh
    
    def execute(self, context):
        Arma = bpy.context.scene.ToolBox.Armature
        Mesh = bpy.context.scene.ToolBox.Mesh
        VertexKeys = Mesh.vertex_groups.keys()
        BoneKeys = Arma.data.bones.keys()
        
        for key in VertexKeys:
            print("checking " + key)
            if not key in BoneKeys:
                
                RemoveVertexGroup = Mesh.vertex_groups.get(key)

                Mesh.vertex_groups.remove(RemoveVertexGroup)
                print("removed " + key)
                

        bpy.context.scene.ToolBox.property_unset('Armature')
        bpy.context.scene.ToolBox.property_unset('Mesh')
        
        return {"FINISHED"}

#----------------------------------------------
#               Registering panel
#----------------------------------------------

classes = (
    ToolBoxPropertyGroup,
    ToolboxMainMenu,
    MeshMenu,
    ShapekeyTools,
    WeightpaintingTools,
    OBJECT_OT_shapekeyOp,
    OBJECT_OT_returnshapeOp,
    OBJECT_OT_transweights,
    OBJECT_OT_transweightsSingle,
    OBJECT_OT_RemoveVertexGroupsOp,
    OBJECT_OT_SelectMeshOp,
    OBJECT_OT_SelectArmatureOp,
)
    


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.ToolBox = bpy.props.PointerProperty(type=ToolBoxPropertyGroup)
        
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)    

if __name__ == "__main__":
    register()
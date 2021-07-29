bl_info = {
    "name": "Tool Collection (ToolBox)",
    "author": "ZoZo Zoe",
    "version": (2, 0),
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

class ToolBoxMeshGroup(bpy.types.PropertyGroup):
    Armature: bpy.props.PointerProperty(type=bpy.types.Object)
    Mesh: bpy.props.PointerProperty(type=bpy.types.Object)
    
class ToolBoxWeightpaintGroup(bpy.types.PropertyGroup):
    Armature: bpy.props.PointerProperty(type=bpy.types.Object)
    Mesh: bpy.props.PointerProperty(type=bpy.types.Object)
    SecondMesh: bpy.props.PointerProperty(type=bpy.types.Object)
    Bone: bpy.props.StringProperty()





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
        row.scale_y = 1
        row.label(text="Update object:")
        row.operator("object.isselweightbone", text="", icon='SELECT_SET')
        row.operator("object.isselweightmesh", text="", icon='SELECT_SET')
        row.operator("object.isselweightsecmesh", text="", icon='SELECT_SET')
        
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1
        row.label(text="")
        row.operator("object.selweightbone", text="", icon='BONE_DATA')
        row.operator("object.selweightmesh", text="", icon='SHAPEKEY_DATA')
        row.operator("object.selweightsecmesh", text="", icon='SHAPEKEY_DATA')
        
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.5
        row.label(text="Transfer weights from:")
        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.5
        row.operator("object.transweight",text="Mesh", icon='MOD_VERTEX_WEIGHT')
        row.operator("object.transweightsingle",text="Bone", icon='BONE_DATA')
        


#----------------------------------------------
#               Transfer Weights
#----------------------------------------------       

class OBJECT_OT_transweights(Operator):
    bl_label = "Transfer Weights"
    bl_idname = "object.transweight"
    bl_option = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return bpy.context.scene.ToolBoxWeight.Mesh and bpy.context.scene.ToolBoxWeight.SecondMesh
 
        
    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.ToolBoxWeight.Mesh.select_set(True)
        bpy.context.scene.ToolBoxWeight.SecondMesh.select = True
        
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
    bl_option = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return bpy.context.scene.ToolBoxWeight.Mesh and bpy.context.scene.ToolBoxWeight.SecondMesh
 
    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = bpy.context.scene.ToolBoxWeight.Armature
        bpy.context.scene.ToolBoxWeight.Armature.select = True
                
        bpy.ops.object.mode_set(mode='POSE', toggle=False)
                
        for i in bpy.context.selected_pose_bones:
            bpy.context.object.data.bones[i.name].select = False

        bpy.context.object.data.bones[bpy.context.scene.ToolBoxWeight.Bone].select = True

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        bpy.context.scene.ToolBoxWeight.Mesh.select_set(True)
        bpy.context.scene.ToolBoxWeight.SecondMesh.select = True
        bpy.context.view_layer.objects.active = bpy.context.scene.ToolBoxWeight.SecondMesh
        bpy.ops.object.mode_set(mode='WEIGHT_PAINT', toggle=False)

        bpy.ops.object.data_transfer(use_reverse_transfer=True, data_type='VGROUP_WEIGHTS',  layers_select_src='NAME', layers_select_dst='BONE_SELECT', mix_mode='REPLACE')
        
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')


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
        row.scale_y = 1
        row.label(text="Selector:")
        row.operator("object.isselmesharmature", text="", icon='SELECT_SET')
        row.operator("object.isselmeshmesh", text="", icon='SELECT_SET')

        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1
        row.label(text="")
        row.operator("object.selmesharmature", text="", icon='MESH_DATA')
        row.operator("object.selmeshmesh", text="", icon='SHAPEKEY_DATA')

        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.5
        row.operator("object.remvertgroups", icon='OUTLINER_DATA_MESH')
    
    
#----------------------------------------------
#               Remove Vertex Groups
#----------------------------------------------
    
class OBJECT_OT_RemoveVertexGroupsOp(Operator):
    bl_label = "Remove Vertex Groups"
    bl_idname = "object.remvertgroups"
    bl_option = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.context.scene.ToolBoxMesh.Armature and bpy.context.scene.ToolBoxMesh.Mesh
    
    def execute(self, context):
        Arma = bpy.context.scene.ToolBox.Armature
        Mesh = bpy.context.scene.ToolBoxMesh
        VertexKeys = Mesh.vertex_groups.keys()
        BoneKeys = Arma.data.bones.keys()
        
        for key in VertexKeys:
            print("checking " + key)
            if not key in BoneKeys:
                
                RemoveVertexGroup = Mesh.vertex_groups.get(key)

                Mesh.vertex_groups.remove(RemoveVertexGroup)
                print("removed " + key)
                
        
        return {"FINISHED"}




#---------------------------------------------- Selection updates ----------------------------------------------

#---------------------------------------------- Mesh ----------------------------------------------     
#----------------------------------------------
#               Update Armature
#----------------------------------------------
    
class OBJECT_OT_SelectMeshArmatureOp(Operator):
    bl_label = "Select Armature"
    bl_idname = "object.selmesharmature"
    bl_option = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'ARMATURE'

    def execute(self, context):
        
        ob = bpy.context.object
        bpy.context.scene.ToolBoxMesh.Armature = ob
        return {"FINISHED"}
    

class OBJECT_OT_ISSelectMeshArmatureOp(Operator):
    bl_label = "Select Armature"
    bl_idname = "object.isselmesharmature"
    bl_option = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.context.scene.ToolBoxMesh.Armature

    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.ToolBoxMesh.Armature.select_set(True)
        
        return {"FINISHED"}
       

#----------------------------------------------
#               Update Mesh
#----------------------------------------------
    
class OBJECT_OT_SelectMeshOp(Operator):
    bl_label = "Select Mesh"
    bl_idname = "object.selmeshmesh"
    bl_option = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'MESH'
    
    def execute(self, context):
        
        ob = bpy.context.object
        bpy.context.scene.ToolBoxMesh.Mesh = ob
        return {"FINISHED"}
 
    
class OBJECT_OT_ISSelectMeshOp(Operator):
    bl_label = "Select Mesh"
    bl_idname = "object.isselmeshmesh"
    bl_option = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return bpy.context.scene.ToolBoxMesh.Mesh

    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.ToolBoxMesh.Mesh.select_set(True)
        
        return {"FINISHED"}


#---------------------------------------------- Weights ----------------------------------------------  
#----------------------------------------------
#               Update Mesh
#----------------------------------------------
    
class OBJECT_OT_SelectWeightMeshOp(Operator):
    bl_label = "Source Mesh"
    bl_idname = "object.selweightmesh"
    bl_option = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'MESH'
    
    def execute(self, context):
        
        ob = bpy.context.object
        bpy.context.scene.ToolBoxWeight.Mesh = ob
        return {"FINISHED"}
 
    
class OBJECT_OT_ISMeshWeightSelectMeshOp(Operator):
    bl_label = "Select Source Mesh"
    bl_idname = "object.isselweightmesh"
    bl_option = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return bpy.context.scene.ToolBoxWeight.Mesh

    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.ToolBoxWeight.Mesh.select_set(True)
        
        return {"FINISHED"}
    
#----------------------------------------------
#               Secondary Mesh
#----------------------------------------------
    
class OBJECT_OT_SelectWeightSecondMeshOp(Operator):
    bl_label = "Destination Mesh"
    bl_idname = "object.selweightsecmesh"
    bl_option = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'MESH'
    
    def execute(self, context):
        
        ob = bpy.context.object
        bpy.context.scene.ToolBoxWeight.SecondMesh = ob
        return {"FINISHED"}
    

class OBJECT_OT_ISSelectWeightSecondMeshOp(Operator):
    bl_label = "Select Destination Mesh"
    bl_idname = "object.isselweightsecmesh"
    bl_option = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.context.scene.ToolBoxWeight.SecondMesh

    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.ToolBoxWeight.SecondMesh.select_set(True)
        
        return {"FINISHED"}
    
    
#----------------------------------------------
#               Select Bone
#----------------------------------------------
    
class OBJECT_OT_SelectWeightBoneOp(Operator):
    bl_label = "Select Bone"
    bl_idname = "object.selweightbone"
    bl_option = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object.select_get() and context.object.type == 'ARMATURE' and bpy.context.object.mode == 'EDIT' or bpy.context.object.mode == 'POSE'
    
    def execute(self, context):
        
        if bpy.context.object.mode == 'EDIT':
            if len(bpy.context.selected_bones) !=0:
                bpy.context.scene.ToolBoxWeight.Armature = bpy.context.object
                bpy.context.scene.ToolBoxWeight.Bone = bpy.context.selected_bones[0].name
            else:
                self.report({"WARNING"}, "No bone was selected, please select one")
                
            if len(bpy.context.selected_bones) > 1:
                self.report({"INFO"}, "Multiple bones selected. The first bone was selected: " + bpy.context.scene.ToolBoxWeight.Bone)
            
        if bpy.context.object.mode == 'POSE':
            if len(bpy.context.selected_pose_bones) != 0:
                bpy.context.scene.ToolBoxWeight.Armature = bpy.context.object
                bpy.context.scene.ToolBoxWeight.Bone = bpy.context.selected_pose_bones[0].name
            else:    
                self.report({"WARNING"}, "No bone was selected, please select one")
                
            if len(bpy.context.selected_pose_bones) > 1:
                self.report({"INFO"}, "Multiple bones selected. The first bone was selected: " + bpy.context.scene.ToolBoxWeight.Bone)
            
        return {"FINISHED"}
    

class OBJECT_OT_ISSelectWeightBoneOp(Operator):
    bl_label = "Select Bone"
    bl_idname = "object.isselweightbone"
    bl_option = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.context.scene.ToolBoxWeight.Bone

    def execute(self, context):
        
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = bpy.context.scene.ToolBoxWeight.Armature
        bpy.context.scene.ToolBoxWeight.Armature.select = True
        
        bpy.ops.object.mode_set(mode='POSE', toggle=False)
        
        for i in bpy.context.selected_pose_bones:
            bpy.context.object.data.bones[i.name].select = False

        bpy.context.object.data.bones[bpy.context.scene.ToolBoxWeight.Bone].select = True
        
        return {"FINISHED"}  
    

#----------------------------------------------
#               Registering panel
#----------------------------------------------

classes = (
    ToolBoxMeshGroup,
    ToolBoxWeightpaintGroup,
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
    OBJECT_OT_ISSelectMeshOp,
    OBJECT_OT_SelectMeshArmatureOp,
    OBJECT_OT_ISSelectMeshArmatureOp,
    OBJECT_OT_SelectWeightMeshOp,
    OBJECT_OT_ISMeshWeightSelectMeshOp,
    OBJECT_OT_SelectWeightSecondMeshOp,
    OBJECT_OT_ISSelectWeightSecondMeshOp,
    OBJECT_OT_SelectWeightBoneOp,
    OBJECT_OT_ISSelectWeightBoneOp,
)
    


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.ToolBoxMesh = bpy.props.PointerProperty(type=ToolBoxMeshGroup)
    bpy.types.Scene.ToolBoxWeight = bpy.props.PointerProperty(type=ToolBoxWeightpaintGroup)
        
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)    

if __name__ == "__main__":
    register()
import bpy
from bpy.props import FloatProperty, EnumProperty

bl_info = {
    "name": "VertexAttrConverter",
    "author": "nekome",
    "version": (0, 0),
    "blender": (2, 82, 0),
    "location": "3Dビューポート > オブジェクト",
    "description": "頂点ウェイトを頂点カラーに変換するアドオン",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "https://github.com/nekomehako/VertexAttrConverter",
    "tracker_url": "https://github.com/nekomehako/VertexAttrConverter",
    "category": "Object"
}

#Make vertex group incluede all vertices and vertex color by the name of "outliine"
def vertices_attr_add(name ='outline'):
    obj = bpy.context.object
    obj.vertex_groups.new(name = name)

def verticesInitialize(name ='outline'):
    obj = bpy.context.object
    msh = obj.data
    obj.vertex_groups[name].add(range(len(msh.vertices)), 0.5, 'ADD')

def data_modifier_add(name = 'outline'):
    mod = bpy.context.object.modifiers.new(name=name, type="SOLIDIFY")

def modifierInitialize(slotIndex, name = 'outline'):
    mod = bpy.context.object.modifiers['outline']
    mod.vertex_group = name
    mod.thickness = -0.1
    mod.use_rim = False
    mod.use_flip_normals = True
    mod.material_offset = slotIndex


def  data_material_add(name = 'outline'):
    mtl = bpy.data.materials.new(name = name)
    mtl.diffuse_color = [0.0]*4
    return mtl

def  materialInitilaize(x):
    if 'outline' in bpy.context.object.material_slots:
        for idx, x in enumerate(bpy.context.object.material_slots): 
            if x.name == 'outline':
                break
        return idx
    else:
        bpy.ops.object.material_slot_add()
        bpy.context.object.active_material = x
        return bpy.context.object.active_material_index


#Convert vertex group wheight into vertex color
def VertexWeightToVertexColor(x):
    obj = bpy.context.object
    for idx, vc in enumerate(obj.data.vertex_colors['outline'].data):
        vc.color = [0]*4
        if x == "R":
            vc.color[0]= obj.vertex_groups["outline"].weight(idx)
        elif x == "G":
            vc.color[1]= obj.vertex_groups["outline"].weight(idx)
        elif x == "B":
            vc.color[2]= obj.vertex_groups["outline"].weight(idx)
        elif x == "a":
            vc.color[3]= obj.vertex_groups["outline"].weight(idx)




class Objects_OT_Initialize(bpy.types.Operator):
    bl_idname = "object.vertices_initialize"
    bl_label = "initialize"
    bl_description = "場を整えます/nMake vertex group incluede all vertices and vertex color by the name of 'outliine'"
    bl_options = {'REGISTER', 'UNDO'}

    # メニューを実行したときに呼ばれる関数
    def execute(self, context):
        name = 'outline'
        obj = bpy.context.object
        if name in bpy.data.materials:
            slotidx = materialInitilaize(bpy.data.materials[name])
        else:
            slotidx = materialInitilaize(data_material_add())
        if name in obj.vertex_groups:
            print("a")
            verticesInitialize()
        else:
            print("b")
            vertices_attr_add()
            verticesInitialize()
        if name in obj.modifiers:
            modifierInitialize(slotidx)
        else:
            data_modifier_add(name)
            modifierInitialize(slotidx)

        if not name in obj.data.vertex_colors:
            obj.data.vertex_colors.new(name = name)
        print("環境を整えました")
        return {'FINISHED'}

class Vertex_OT_ConvertWheightIntoColor(bpy.types.Operator):
    bl_idname = "object.convert_vertex_wheight_into_vertexcolor"
    bl_label = "convert"
    bl_description = "頂点ウェイトを頂点カラーに代入します/nConvert vertex group wheight into vertex color"
    bl_options = {'REGISTER', 'UNDO'}

    RGBa = EnumProperty(
        name="RGBa",
        description="コンバート先を設定します",
        default="R",
        items=[
            ("R", "R", "R値にウェイト値をコンバートします"),
            ("G", "G", "G値にウェイト値をコンバートします"),
            ("B", "B", "B値にウェイト値をコンバートします"),
            ("a", "a", "a値にウェイト値をコンバートします")
        ]
    )

    # メニューを実行したときに呼ばれる関数
    def execute(self, context):
        VertexWeightToVertexColor(self.RGBa)
        print("頂点カラーに変換しました")

        return {'FINISHED'}

# サブメニュー
class Vertex_MT_Converter(bpy.types.Menu):

    bl_idname = "Vertex_MT_Converter"
    bl_label = "頂点ウェイトと頂点カラー"
    bl_description = "頂点ウェイトと頂点カラー間で値のやり取りをします"

    def draw(self, context):
        self.layout.operator(Objects_OT_Initialize.bl_idname)
        self.layout.operator(Vertex_OT_ConvertWheightIntoColor.bl_idname)
        
def menu_fn(self, context):
    self.layout.separator()
    self.layout.menu(Vertex_MT_Converter.bl_idname)

# Blenderに登録するクラス
classes = [
    Vertex_MT_Converter,
    Objects_OT_Initialize,
    Vertex_OT_ConvertWheightIntoColor,
]

# アドオン有効化時の処理
def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_object.append(menu_fn)
    print("頂点ウェイトを頂点カラーに変換するアドオン有効化されました。")


# アドオン無効化時の処理
def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_fn)
    for c in classes:
        bpy.utils.unregister_class(c)
    print("頂点ウェイトを頂点カラーに変換するアドオンが無効化されました。")


# メイン処理
if __name__ == "__main__":
    register()
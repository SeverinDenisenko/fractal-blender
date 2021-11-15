import bpy
from math import pi
from mathutils import Vector, Euler

# Make iteration and return list of childs
def iteration(SCALE, TRANLATE, ROTATE, obj):
    arr = []
    for i in range(len(obj.data.vertices)):
        tmp = obj.copy()
        tmp.data = obj.data.copy()
        bpy.context.collection.objects.link(tmp)
        
        # Applying transform
        tmp.location = obj.matrix_world @ obj.data.vertices[i].co + Vector((obj.location.x * SCALE[0], obj.location.y * SCALE[1], obj.location.z * SCALE[2]))
        tmp.scale = (tmp.scale.x * SCALE[0], 
                        tmp.scale.y * SCALE[1], 
                        tmp.scale.z * SCALE[2])
        tmp.rotation_euler = Euler((obj.rotation_euler.x + ROTATE[0],
                                    obj.rotation_euler.y + ROTATE[1],
                                    obj.rotation_euler.y + ROTATE[2]), 'XYZ')
        
        arr.append(tmp)
    return arr


# Making wireframe
def modify(objects, thickness):
    for object in objects:
        bpy.context.view_layer.objects.active = object
        
        object.modifiers.new("wireframe", type='WIREFRAME')
        object.modifiers["wireframe"].show_in_editmode = True
        object.modifiers["wireframe"].thickness = thickness
        
        bpy.ops.object.modifier_apply(modifier="wireframe")
    

# Making it one object for optimisation
def combine(objects):
    bpy.context.active_object.select_set(state=True)
    bpy.ops.object.join()
    

# Repeat iteration N times. Return all childs
def iterate(SCALE, TRANLATE, ROTATE, N, obj):
    all = []
    array1 = [obj]
    array2 = []
    
    while N > 0:
        for object in array1:
            array2 = array2 + iteration(SCALE, TRANLATE, ROTATE, object)
            
        all = all + array2
        array1 = array2
        array2 = []
        
        N = N - 1
    
    return all


# Main function
def main():
    SCALE = (0.5, 0.5, 0.5)
    TRANLATE = (0, 0, 0)
    ROTATE = (0, 0, 0)
    
    N = 4
    thickness = 0.2
    
    object = bpy.context.active_object
    all = iterate(SCALE, TRANLATE, ROTATE, N, object)
    
    # TODO: fix this
    #modify(all, thickness)
    #modify([object], thickness)
    combine(all)
    

if __name__ == "__main__":
    main()


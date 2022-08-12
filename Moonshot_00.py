import bpy
from json import load
from math import pi
from mathutils import Vector

# removing the Object Plane 
bpy.data.objects['Plane'].select_set(True)
bpy.ops.object.delete()

# reading Json
Data_01=open(r"C:\Users\HP\Desktop\blender_python\Data_set.json")
dict_json=load(Data_01)
velocity=dict_json["velocities"]

# set up new Camera
c=bpy.data.cameras.new('Drone_Cam')
c1=bpy.data.objects.new('Drone_Cam',c)
c1.location=(0,0,-0.5)
c1.rotation_euler=(0,pi/2,pi/2)
bpy.context.scene.collection.objects.link(c1)

 # temp variable for Local Gimmbal roll   
c=0

crv = bpy.data.curves.new('crv', 'CURVE')
crv.dimensions = '3D'
coords_list=[[0,0,0]]
for i in range(3):
    coords_list+=[[velocity[i]["X-val"],velocity[i]["Y-val"],velocity[i]["Z-val"]]]
# make a new spline in that curve
spline = crv.splines.new(type='NURBS')
# a spline point for each point
spline.points.add(len(coords_list)-1) # theres already one point by default

# assign the point coordinates to the spline points
for p, new_co in zip(spline.points, coords_list):
    p.co = (new_co + [1.0]) # (add nurbs weight)

# make a new object with the curve
obj = bpy.data.objects.new('object_name', crv)
bpy.context.scene.collection.objects.link(obj)

def movement(fra_me):
    # linear motion in X direction(Both Camera and Drone)
   bpy.data.objects['Drone'].location[0] +=velocity[fra_me]["X-val"]
   bpy.data.objects['Drone_Cam'].location[0] +=velocity[fra_me]["X-val"]
   bpy.data.objects['Drone'].keyframe_insert(data_path='location',frame=100*fra_me)
   bpy.data.objects['Drone_Cam'].keyframe_insert(data_path='location',frame=100*fra_me)
   
    # linear motion in Y direction(Both Camera and Drone)
   bpy.data.objects['Drone'].location[1] +=velocity[fra_me]["Y-val"]
   bpy.data.objects['Drone_Cam'].location[1] +=velocity[fra_me]["Y-val"]
   bpy.data.objects['Drone'].keyframe_insert(data_path='location',frame=100*fra_me)
   bpy.data.objects['Drone_Cam'].keyframe_insert(data_path='location',frame=100*fra_me)
   
    # linear motion in Z direction(Both Camera and Drone)
   bpy.data.objects['Drone'].location[2] +=velocity[fra_me]["Z-val"]
   bpy.data.objects['Drone_Cam'].location[2] +=velocity[fra_me]["Z-val"]
   bpy.data.objects['Drone'].keyframe_insert(data_path='location',frame=100*fra_me)
   bpy.data.objects['Drone_Cam'].keyframe_insert(data_path='location',frame=100*fra_me)
   
    # Circular motion in X direction(Both Camera and Drone)
   bpy.data.objects['Drone'].rotation_euler[0] =(velocity[fra_me]["Roll"])*pi/180
   bpy.data.objects['Drone_Cam'].rotation_euler[0] =((velocity[fra_me]["Roll"])*pi/180)+(pi/2)
   bpy.data.objects['Drone'].keyframe_insert(data_path='rotation_euler',frame=100*fra_me)
   bpy.data.objects['Drone_Cam'].keyframe_insert(data_path='rotation_euler',frame=100*fra_me)
#    
    # Circular motion in Y direction(Both Camera and Drone)
   bpy.data.objects['Drone'].rotation_euler[1] =(velocity[fra_me]["Yaw"])*pi/180
   bpy.data.objects['Drone_Cam'].rotation_euler[1] =((velocity[fra_me]["Yaw"])*pi/180) 
   bpy.data.objects['Drone'].keyframe_insert(data_path='rotation_euler',frame=100*fra_me)
   bpy.data.objects['Drone_Cam'].keyframe_insert(data_path='rotation_euler',frame=100*fra_me)
    
    # Circular motion in Z direction(Both Camera and Drone)
   bpy.data.objects['Drone'].rotation_euler[2] =(velocity[fra_me]["Pitch"])*pi/180
   bpy.data.objects['Drone_Cam'].rotation_euler[2] =(velocity[fra_me]["Pitch"])*pi/180
   bpy.data.objects['Drone'].keyframe_insert(data_path='rotation_euler',frame=100*fra_me)
   bpy.data.objects['Drone_Cam'].keyframe_insert(data_path='rotation_euler',frame=100*fra_me)
    
    # Initiating The Gimbal Roll in Blender
   bpy.context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'
   bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'

    # conditional Requirement of Gimbal Roll
   if ((velocity[fra_me]["Gimbleroll"])*pi/180)>(pi/2) :
        c=pi/2
   elif ((velocity[fra_me]["Gimbleroll"])*pi/180)<((-1)*pi/2):
        c=(-1)*pi/2
   else:
        c=((velocity[fra_me]["Gimbleroll"])*pi/180)

    #Activating the Camera for Gimbal roll
   bpy.data.objects['Drone_Cam'].select_set(True)

   #Actvating LocalGimbal Rotation
   bpy.data.objects['Drone_Cam'].rotation_euler[1] =c
   bpy.data.objects['Drone_Cam'].keyframe_insert(data_path='rotation_euler',frame=100*fra_me)


    # Conditional requirement of Dolly Roll
   if ((velocity[fra_me]["Planar_roll"])*pi/180) > (pi/2) :
        c=pi/2
   elif ((velocity[fra_me]["Planar_roll"])*pi/180) < 0:
        c=0
   else:
        c=((velocity[fra_me]["Planar_roll"])*pi/180)

    
    # Actvating Local DOLLY Rotation
   bpy.data.objects['Drone_Cam'].rotation_euler[2] =c
   bpy.data.objects['Drone_Cam'].keyframe_insert(data_path='rotation_euler',frame=100*fra_me)
    
    # Reset the Global Rotations again for next steps
   bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
   bpy.context.scene.transform_orientation_slots[0].type = 'GLOBAL'
    
for i in range(3):
    movement(i)
bpy.ops.screen.animation_play()
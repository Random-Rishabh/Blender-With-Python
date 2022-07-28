#importing blender toolkit and json
import bpy
from json import load

#initailizations
original_json=open(r"C:\Users\HP\Desktop\blender_python\Drome.json")
dict_json=load(original_json)
list_actions=list(dict_json.keys())
n=len(list(dict_json.keys()))

#selecting an existing camera Variable
cam=bpy.data.collections[0].objects[2]

##markFrames -- mark the frames accoording to parameters defined in json file
def markFrames(i):
    bpy.ops.screen.animation_play()             #start animation
    if list_actions[i]=='X_velocity':
        cam.location[0]=int(dict_json[list_actions[i]])
        cam.keyframe_insert(data_path="location",frame=(i+1)*24)
        print("x")
    if list_actions[i]=='Y_velocity':
        cam.location[1]=int(dict_json[list_actions[i]])
        cam.keyframe_insert(data_path="location",frame=(i+1)*24)
        print("y")
    if list_actions[i]=='Z_velocity':
        cam.location[2]=int(dict_json[list_actions[i]])
        cam.keyframe_insert(data_path="location",frame=(i+1)*24)
        print("z")
    if list_actions[i]=='pitch':
        cam.rotation_euler[0]=float(dict_json[list_actions[i]])
        cam.keyframe_insert(data_path="rotation_euler",frame=(i+1)*24)
        print("p")
    if list_actions[i]=='yaw':
        cam.rotation_euler[1]=float(dict_json[list_actions[i]])
        cam.keyframe_insert(data_path="rotation_euler",frame=(i+1)*24)
        print("y")
    if list_actions[i]=='roll':
        cam.rotation_euler[2]=float(dict_json[list_actions[i]])
        cam.keyframe_insert(data_path="rotation_euler",frame=(i+1)*24)
        print("r")

#To create animation
for i in range(n):
    markFrames(i)

from arena import *

from threading import Thread

# class DemoObject(object):
#     def __init__(self):
#         self.pos = Position(0,0,0)
#         self.rot = Rotation(0,0,0)
#         self.obj = Box(object_id="my_box", position=Position(0,4,-2), scale=Scale(2,2,2))

# setup library
scene = Scene(host="arenaxr.org", scene="mini_demo")

# make a box
box = Box(object_id="my_box", position=Position(0,4,-2), scale=Scale(2,2,2))
sword = GLTF(
        object_id="sword",
        position=(0,3,0),
        scale=(0.5,0.5,0.5),
        url="store/users/joeym/sword.glb",
    )

ramen = GLTF(
        object_id="ramen",
        position=(0,1,0),
        scale=(10,10,10),
        url="store/users/joeym/Ramen.gltf",
    )

# ball = Sphere(object_id="ball", position=Position(0,4,0), scale=Scale(2,2,2))

# demo_objects = [sword, ball]

@scene.run_once
def main():
    global scene
    global sword
    global ramen
    # add the box
    
    current_sel = 0
    scene.add_object(ramen)

    # Slider0 = 0
    # Slider1 = 0
    # Slider2 = 0
    
    # while True:
    #     val = input("Enter Value: ")
    #     vals_list = val.split()
    #     if vals_list[0] == "A":
    #         num = int(vals_list[1])
    #         Slider0 = num
    #     if vals_list[0] == "B":
    #         num = int(vals_list[1])
    #         Slider1 = num
    #     if vals_list[0] == "C":
    #         num = int(vals_list[1])
    #         Slider2 = num
        
        # if vals_list[0] == "Choose":
        #     sel = int(vals_list[1])
        #     if sel == 0:
        #         scene.delete_object(ball)
        #         scene.add_object(sword)
        #     else:
        #         scene.delete_object(sword)
        #         scene.add_object(ball)

        
        # current_obj.update_attributes(rotation=Rotation(Slider0, Slider1, Slider2))
        # scene.update_object(current_obj)


# x = 0
# @scene.run_forever(interval_ms=500)
# def periodic():
#     global x    # non allocated variables need to be global
#     box.update_attributes(position=Position(x,3,0))
#     scene.update_object(box)
#     x += 0.1

# start tasks

# def keyboard_inputs():
    # Slider0 = 0
    # Slider1 = 0
    # Slider2 = 0
    # y = 0
    # global scene
    # global sword
    # while True:
    #     val = input("Enter Value: ")
    #     vals_list = val.split()
    #     if vals_list[0] == "A":
    #         num = int(vals_list[1])
    #         Slider0 = num
    #     if vals_list[0] == "B":
    #         num = int(vals_list[1])
    #         Slider1 = num
    #     if vals_list[0] == "C":
    #         num = int(vals_list[1])
    #         Slider2 = num
        
    #     if vals_list[0] == "Choose":
    #         sel = int(vals_list[1])
        
    #     sword.update_attributes(rotation=Rotation(Slider0, Slider1, Slider2))
    #     scene.update_object(sword)


# t1 = Thread(target=keyboard_inputs)
# t1.start()
scene.run_tasks()
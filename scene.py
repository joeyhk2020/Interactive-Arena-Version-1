import serial
from time import sleep
from arena import *
from threading import Thread
import ast

scene = Scene(host="arenaxr.org", scene="mini_demo")

scale_factors = [0.8, 1.2, 0.4, 0.4]

box = Box(object_id="box", 
          position=Position(0,0,0), 
          scale=Scale(0.001,0.001,0.001),
          persist=True)
parrot = GLTF(object_id="parrot", 
                position=Position(0,0,0), 
                scale=Scale(0.001,0.001,0.001),
                url="store/users/johnchoi/PolyCam/PolyCam_Parrot_Photogrammetry.glb",
                persist=True)
xr_logo = GLTF(
        object_id="xr-logo",
        position=(0,-0.1,0),
        scale=(0.001,0.001,0.001),
        url="store/users/wiselab/models/XR-logo.glb",
        persist=True)
shine = GLTF(
        object_id="shine",
        position=(0,0,0),
        scale=(0.001,0.001,0.001),
        url="store/users/joeym/Shine.gltf",
        persist=True)
keys = []

keys_clicked = []

mouse_keys_down = [0] * 16

for i in range(16):
    name = "key" + str(i)
    x = i%4
    y = i//4
    xpos = 0.3 + (x*0.08)
    zpos = 0 + (0.08*y)
    ypos = 0

    pos = Position(xpos, ypos, zpos)
    sca = Scale(0.04,0.04,0.04)
    col = Color(50,50,50)
    key = Box(object_id=name, position=pos, scale=sca, color=col, persist=True)
    keys.append(key)


interactives = [box, parrot, xr_logo, shine]

obj_sel = 0
obj_sel_prev = 0

@scene.run_once
def main():
    global box

    for key in keys:
        scene.update_object(key, click_listener=True, evt_handler=mouse_handler)

    scene.add_objects([box, parrot, xr_logo, shine])
    scene.add_objects(keys)


def update_keys(keypad_keys_down):
    global keys
    global mouse_keys_down
    # if (type(keypad_keys_down) is not list) and 1:
    #     return

    
    for i in range(16):
        if (i in keypad_keys_down) or (mouse_keys_down[i] > 0):
            div = i//4
            if div == 0:
                keys[i].update_attributes(color = Color(200,0,0))
            elif div == 1:
                keys[i].update_attributes(color = Color(0,200,0))
            elif div == 2:
                keys[i].update_attributes(color = Color(0,0,200))
            else:
                keys[i].update_attributes(color = Color(200,200,0))
        else:
            keys[i].update_attributes(color = Color(50,50,50))
    
    scene.update_objects(keys)

def update_scene(data_arr):
    global scene
    global interactives
    global obj_sel
    global obj_sel_prev
    print(obj_sel)


    val0 = 0
    val1 = 0
    keypad_keys_down = []
    try:
        val0 = float(data_arr[0][2:])
        val1 = float(data_arr[1])
        keypad_keys_down = ast.literal_eval(data_arr[2][:-1])

        if val0 > 3.35 or val1 > 3.35:
            return
    except:
        return

    # print(val0, val1)
    try:
        for i in range(len(interactives)):
            if i in keypad_keys_down:
                obj_sel = i
    except:
        pass


    if obj_sel_prev != obj_sel:
        obj_sel_prev = obj_sel
        for i in range(len(interactives)):
            if i != obj_sel:
                interactives[i].update_attributes(scale=Scale(0.001,0.001,0.001))
                scene.update_object(interactives[i])
    
    update_keys(keypad_keys_down)


    ob = interactives[obj_sel]
    roty = val0 * 360/3.3
    obj_scale = (val1 * 0.15/3.3 + 0.15) * scale_factors[obj_sel]

    ob.update_attributes(rotation=Rotation(0,roty,0), scale=Scale(obj_scale,obj_scale,obj_scale))
    scene.update_object(ob)

def mouse_handler(scene, evt, msg):
    global mouse_keys_down
    if evt.type == "mousedown":
        name = msg["object_id"]
        try:
            num = int(name[3:])
            mouse_keys_down[num] += 1
        except:
            pass
        # print(mouse_keys_down)
    elif evt.type == "mouseup":
        name = msg["object_id"]
        try:
            num = int(name[3:])
            mouse_keys_down[num] -= 1
        except:
            pass

def get_mouse_keys_down():
    global mouse_keys_down
    down = []
    for i in range(16):
        if mouse_keys_down[i] > 0:
            val = ""
            if i < 9:
                val = "0" + str(i)
            else:
                val = str(i)

            down.append(val)
    return down

def t():
    global box
    ser = serial.Serial("/dev/ttyS0", 9600)
    ser.write("START".encode('utf-8'))
    while True:
        rd = ser.read()
        sleep(0.08)
        dl = ser.inWaiting()
        rd += ser.read(dl)
        data_arr = str(rd).split(":")
        update_scene(data_arr)
        ser.write(str(get_mouse_keys_down()).encode('utf-8'))

        


t1 = Thread(target=t)
t1.start()
scene.run_tasks()
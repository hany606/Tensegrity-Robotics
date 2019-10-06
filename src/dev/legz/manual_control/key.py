# This code is for manual control for the tensegrity structure especially the leg design

from pynput.keyboard import Key, Listener, KeyCode
import time

import numpy as np
import os
import tempfile
import pprint
from scipy.spatial.transform import Rotation


global controller_num
global controller_state

controller_state = [0 for i in range(10)]

yaw_ax = 0
throttle_ax = 0
forward_ax = 0
right_ax = 0

def on_press(key):
    global state, yaw_ax, throttle_ax, forward_ax, right_ax
    global client
    # print('{0} pressed'.format(
    #     key))
    step = 0.1
    if key == Key.up:
        forward_ax += step
        if forward_ax > 1:
            forward_ax = 1
    if key == Key.down:
        forward_ax -= step
        if forward_ax < -1:
            forward_ax = -1
    if key == Key.left:
        right_ax -= step
        if right_ax < -1:
            right_ax = -1
    if key == Key.right:
        right_ax += step
        if right_ax > 1:
            right_ax = 1

    if key == KeyCode.from_char('w'):
        throttle_ax += step
        if throttle_ax > 1:
            throttle_ax = 1
    if key == KeyCode.from_char('s'):
        throttle_ax -= step
        if throttle_ax < -1:
            throttle_ax = -1
    if key == KeyCode.from_char('d'):
        yaw_ax += step
        if yaw_ax > 1:
            yaw_ax = 1
    if key == KeyCode.from_char('a'):
        yaw_ax -= step
        if yaw_ax < -1:
            yaw_ax = -1

    if key == Key.space:
        yaw_ax = 0
        throttle_ax = 0
        forward_ax = 0
        right_ax = 0


def on_release(key):
    # print('{0} release'.format(
    #     key))
    if key == Key.esc:
        # Stop listener
        return False


# connect to the AirSim simulator
client = airsim.MultirotorClient(ip = "10.90.130.117")
client.simLoadLevel("ZhangJiaJie_Medium")
#client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl()
client.arm()

state = client.getMultirotorState()
if state.landed_state == airsim.LandedState.Landed:
    client.takeoffAsync(timeout_sec = 5).join()

# Collect events
listener = Listener(
        on_press=on_press,
        on_release=on_release)

listener.start()

while True:
    dx = forward_ax
    dy = right_ax
    dz = throttle_ax
    dyaw = yaw_ax

    print(f"throttle {throttle_ax:.1f}, yaw {yaw_ax:.1f}, forward {forward_ax:.1f}, right {right_ax:.1f}")

    state = client.getMultirotorState()
    qt = state.kinematics_estimated.orientation

    q1 = Rotation.from_quat( qt.to_numpy_array() )
    rot = q1.apply([20*dx, 20*dy, -10*dz])

    yaw_ctr = airsim.YawMode(is_rate=True, yaw_or_rate = dyaw * 200)
    client.moveByVelocityAsync(rot[0], rot[1], rot[2], 0.1, yaw_mode=yaw_ctr)


    dec = 0.3
    forward_ax -= dec * forward_ax
    right_ax -= dec * right_ax
    throttle_ax -= dec * throttle_ax
    yaw_ax -= dec * yaw_ax
    
    time.sleep(0.1)

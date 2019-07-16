# -*- encoding:utf8 -*-
import time
import numpy as np
import cv2
import json
import time
import traceback
from time import sleep
from threading import Thread
import pyrealsense as pyrs
from pyrealsense.constants import rs_option
from libled.util.led_draw_util import *
import zmq
import libled.util.logger as logger
from libled.util.zmq_util import *
import sys

context = zmq.Context()
socket = context.socket(zmq.PUB)

target = "tcp://*:5501"
socket.bind(target)
logger.i("ZMQ PUB Socket Start: " + target)

dev = None

# FRAME_WIDTH = 16
# FRAME_HEIGHT = 32
FRAME_WIDTH = 15
FRAME_HEIGHT = 50

try:
    pyrs.start()
    dev = pyrs.Device()
    logger.i("initialize realsense is successfull.")
    dev.apply_ivcam_preset(0)
    dev.set_device_option(rs_option.RS_OPTION_F200_LASER_POWER, 15.0)
    while True:

        # [r,g,b,深度] の形式に変換する

        dev.wait_for_frames()

        c = dev.color
        c = cv2.cvtColor(c, cv2.COLOR_RGB2BGR)

        d = dev.depth / 256.0

        scale = max(FRAME_HEIGHT/640.0, FRAME_WIDTH/480.0)

        # カラーのサイズ変換
        scaledc = get_scled_rgb_image(c, scale, scale)
        framec = resize2(scaledc, (FRAME_WIDTH, FRAME_HEIGHT),
                         (-4, 0), [[0]*4])

        # 深度のサイズ変換
        d = cv2.applyColorMap(d.astype(np.uint8), cv2.COLORMAP_BONE)
        scaledd = get_scled_rgb_image(d, scale, scale)
        framed = resize2(scaledd, (FRAME_WIDTH, FRAME_HEIGHT),
                         (-4, 0), [[0]*4])

        # 深度を最後に添付する
        frame = np.hstack(
            (framec.reshape(FRAME_WIDTH*FRAME_HEIGHT, 3), framed[:, :, 0].reshape(FRAME_WIDTH*FRAME_HEIGHT, 1)))

        frame = frame.reshape(FRAME_WIDTH, FRAME_HEIGHT, 4)

        send_array(socket, frame)
except:
    logger.e("initialize realsense failed.:" + str(sys.exc_info()[0]))
    logger.e(traceback.format_exc())

finally:
    if dev is not None:
        dev.stop()
    # pyrs.stop()
    if socket is not None:
        socket.close()
    if context is not None:
        context.term()

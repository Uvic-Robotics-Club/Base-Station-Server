import cv2 as cv
import numpy as np
from settings import Settings
import socket
from state import State
import struct
from time import sleep

settings = Settings()
state = State()

MAX_DGRAM = 2**16
BLANK_IMAGE_HEIGHT = 300
BLANK_IMAGE_WIDTH = 300

class VideoServer():
    '''
    This class is responsible for listening for video frames being sent
    from the rover to the base station.
    '''
    # This stores the jpg binary data of the most recently received frame from the rover.
    video_frame_front_camera = None

    # Blank image used as placeholder when video frame does not exist. It is an image
    # of 3 bars (blue, green, red).
    blank_image_array = np.zeros((BLANK_IMAGE_HEIGHT, BLANK_IMAGE_WIDTH, 3), np.uint8)
    blank_image_array[:,0:BLANK_IMAGE_WIDTH//3] = (255,0,0)      # (B, G, R)
    blank_image_array[:,BLANK_IMAGE_WIDTH//3:2*(BLANK_IMAGE_WIDTH//3)] = (0,255,0)
    blank_image_array[:,2*(BLANK_IMAGE_WIDTH//3):BLANK_IMAGE_WIDTH] = (0,0,255)
    blank_image = cv.imencode('.jpg', blank_image_array)[1].tostring()

    def __init__(self):
        self.setup_socket()

    def setup_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('0.0.0.0', settings.get_setting('port_base_station_udp_video')))
        self.dump_buffer()
        self.listen()

    def listen(self):
        '''
        As long as there is an active connection, listen for video
        frames from the rover and process.
        '''
        process_frame = False
        data = b''

        i=0
        while state.get_attribute('connection_established'):
            seg, addr = self.s.recvfrom(MAX_DGRAM)

            if struct.unpack("B", seg[0:1])[0] > 0:
                data += seg[1:]
            else:
                # Ensures that we do not process part of an image
                # when we first start the server. 
                if not process_frame:
                    process_frame = True
                    data = b''
                    continue

                data += seg[1:]
                # Update latest video frame in state
                VideoServer.video_frame_front_camera = data
                data = b''
                i+=1

        cv.destroyAllWindows()
        self.s.close()

    @staticmethod
    def get_latest_frame():
        if VideoServer.video_frame_front_camera is not None:
            return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + VideoServer.video_frame_front_camera + b'\r\n\r\n'
        
        # If no video frames have been received yet, then display a "blank" image as a placeholder. We sleep for a 
        # duration such that streaming responses are not overhwelmed.
        sleep(0.1)
        return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + VideoServer.blank_image + b'\r\n\r\n'

    def dump_buffer(self):
        while True:
            seg, addr = self.s.recvfrom(MAX_DGRAM)
            if struct.unpack("B", seg[0:1])[0] == 1:
                print('finished emptying buffer.')
                break
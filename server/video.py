import cv2 as cv
import numpy as np
from settings import Settings
import socket
from state import State
import struct

settings = Settings()
state = State()

MAX_DGRAM = 2**16

class VideoServer():
    '''
    This class is responsible for listening for video frames being sent
    from the rover to the base station.
    '''

    def __init__(self):
        self.setup_socket()

    def setup_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('127.0.0.1', settings.get_setting('port_base_station_udp_video')))
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
                state.set_attribute('rover_video_frame_latest', data)

                #img = cv.imdecode(np.fromstring(data, dtype=np.uint8), cv.IMREAD_COLOR)
                #cv.imwrite('/home/anton/Desktop/frame_{}.jpg'.format(i), img)
                data = b''
                i+=1

        cv.destroyAllWindows()
        self.s.close()

    @staticmethod
    def get_latest_frame():
        return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + state.get_attribute('rover_video_frame_latest') + b'\r\n\r\n'
        #return state.get_attribute('rover_video_frame_latest')

    def dump_buffer(self):
        while True:
            seg, addr = self.s.recvfrom(MAX_DGRAM)
            if struct.unpack("B", seg[0:1])[0] == 1:
                print('finished emptying buffer.')
                break
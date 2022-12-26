# First import the library
import pyrealsense2 as rs
import time
import signal

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
config.enable_stream(rs.stream.accel)
config.enable_stream(rs.stream.gyro)
config.enable_record_to_file('test.bag')

class GracefulKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
    
    def exit_gracefully(self, *args):
        self.kill_now = True

video_length = 30 #video length in seconds
killer = GracefulKiller()
while True:
    config.enable_record_to_file('rs_'+str(round(time.time()))+'.bag') #Writes epoch into file name
    pipeline.start(config)
    start = time.time()
    while time.time()-start < video_length:
        pipeline.wait_for_frames().keep()
        if killer.kill_now: #Gracefully ends script on shutdown to prevent file corruption
            print("Stopping gracefully")
            pipeline.stop()
            time.sleep(7)
            quit()
    pipeline.stop()
        


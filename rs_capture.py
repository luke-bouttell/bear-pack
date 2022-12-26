# First import the library
import pyrealsense2 as rs
import time
from graceful_killer import GracefulKiller

def rs_capture():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
    config.enable_stream(rs.stream.accel)
    config.enable_stream(rs.stream.gyro)

    killer = GracefulKiller()

    video_length = 30 #video length in seconds
    while True:
        config.enable_record_to_file('rs_'+str(round(time.time()))+'.bag') #Writes epoch into file name
        pipeline.start(config)
        start = time.time()
        while time.time()-start < video_length:
            pipeline.wait_for_frames().keep()
            if killer.kill_now: #Gracefully ends script on shutdown to prevent file corruption
                print("rs_capture: stopping gracefully")
                pipeline.stop()
                time.sleep(10)
                print("rs_capture: stopped gracefully")
                quit()
        pipeline.stop()
        print("File recorded")

if __name__ == '__main__':
    rs_capture()
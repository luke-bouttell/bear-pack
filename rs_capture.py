# First import the library
import pyrealsense2 as rs
import time

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
config.enable_record_to_file('test.bag')
num = 0
while True:
    try:
        config.enable_record_to_file('rs_'+str(round(time.time()))+'.bag')
        pipeline.start(config)
        start = time.time()
        while time.time()-start < 20:
            pipeline.wait_for_frames().keep()

    finally:
        pipeline.stop()
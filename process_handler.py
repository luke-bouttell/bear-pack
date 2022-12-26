from multiprocessing import Process
import time
from graceful_killer import GracefulKiller

from rosbag_rollover import rosbag_rollover
from rs_capture import rs_capture

rosbag_check_timer = 30

#if __name__ == '__main__':
killer = GracefulKiller()

rs_capture_proc = Process(target=rs_capture,args=())
rs_capture_proc.start()

rosbag_rollover_proc = Process(target=rosbag_rollover,args=(10000000000,))

start = time.time()
while True:
    if time.time()-start > rosbag_check_timer:
        rosbag_rollover_proc.start()
        start = time.time()

    if killer.kill_now: #Gracefully ends script on shutdown to prevent file corruption
            rs_capture_proc.terminate()
            try:
                rosbag_rollover_proc.terminate()
            except:
                print("process_handler: rosbag_rollover_process not running at interrupt")
            print("process_handler: stopped gracefully")
            quit()


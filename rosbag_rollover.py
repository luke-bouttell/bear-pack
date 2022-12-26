import os.path
import os
import glob

from graceful_killer import GracefulKiller

def rosbag_rollover(volume_limit):
    while True:
        killer = GracefulKiller()

        path = '*.bag'
        bag_total_size = 0
        oldest_file_time = 100000000000

        files = glob.glob(path)
        print("Found files: ", files)

        for file in files:
            print(file, ": ", os.path.getctime(file))
            if (os.path.getmtime(file)<oldest_file_time):
                oldest_file= file
                oldest_file_time = os.path.getmtime(file)
                print("found older file")
            bag_total_size += os.path.getsize(file)
        
        print("Bag total size: ", bag_total_size)
        if (bag_total_size > volume_limit):
            os.remove(oldest_file)
            print("deleting file: " , oldest_file)
        else:
            print("Volume size acceptable")
            break

        if killer.kill_now: #Gracefully ends script on shutdown to prevent file corruption
                print("rosbag_rollover: stopping gracefully")
                quit()
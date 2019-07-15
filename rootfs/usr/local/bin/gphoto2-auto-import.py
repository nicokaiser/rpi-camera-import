#!/usr/bin/env python3

from __future__ import print_function

from datetime import datetime
import os
import sys
import time
import shutil
#import blinkt

import gphoto2 as gp

PICTURES_DIR = os.getenv('PICTURES_DIR', os.getcwd())

#blinkt.set_clear_on_exit()
#blinkt.set_brightness(0.1)
#c = 0

def get_all_files(camera, folder='/'):
    print('Listing files in %s' % (folder))
    gp_list = gp.check_result(gp.gp_camera_folder_list_files(camera, folder))
    for name, value in gp_list:
        blinkt.set_pixel(c % blinkt.NUM_PIXELS, 0, 0, 0)
        #c = c + 1
        #blinkt.set_pixel(c % blinkt.NUM_PIXELS, 31, 31, 31)
        #blinkt.show()
        info = gp.check_result(gp.gp_camera_file_get_info(camera, folder, name))
        timestamp = datetime.fromtimestamp(info.file.mtime)
        dest_dir = os.path.join(PICTURES_DIR, timestamp.strftime('%Y-%m-%d/'))
        dest = os.path.join(dest_dir, name)
        if os.path.isfile(dest):
            if (info.file.size and info.file.size == os.path.getsize(dest)):
                #print('Skipping existing file %s' % (dest))
                continue
            print('Warning: existing file %s has different size, overwriting.' % (dest))

        try:
            camera_file = gp.check_result(gp.gp_camera_file_get(
                camera, folder, name, gp.GP_FILE_TYPE_NORMAL))
            print('Downloading file %s' % (name))
            if not os.path.isdir(dest_dir):
                os.makedirs(dest_dir)            
            gp.check_result(gp.gp_file_save(camera_file, dest))
        except gp.GPhoto2Error as e:
            if e.code != -6: # Ignore "Unsupported operation"
                raise

    gp_list = gp.check_result(gp.gp_camera_folder_list_folders(camera, folder))
    for name, value in gp_list:
        get_all_files(camera, os.path.join(folder, name))


if __name__ == '__main__':
    if not os.path.isdir(PICTURES_DIR):
        os.makedirs(PICTURES_DIR)

    try:
        camera = gp.check_result(gp.gp_camera_new())
        time.sleep(1)
        gp.check_result(gp.gp_camera_init(camera))
        get_all_files(camera)
        gp.check_result(gp.gp_camera_exit(camera))
    except gp.GPhoto2Error as e:
        print('Error: %s (%d)' % (e.string, e.code), file=sys.stderr)
EOF

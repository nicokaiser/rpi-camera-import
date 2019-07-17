#!/usr/bin/python3

# Copyright (C) 2014-19  Jim Easterbrook  jim@jim-easterbrook.me.uk
# Copyright (C) 2019     Nico Kaiser      nico@kaiser.me
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
import os
import sys
import time
import blinkt

import gphoto2 as gp

PHOTO_DIR = os.path.expanduser('~/Pictures')

def get_target_dir(timestamp):
    return os.path.join(PHOTO_DIR, timestamp.strftime('%Y-%m-%d/'))

def list_computer_files():
    result = []
    for root, dirs, files in os.walk(os.path.expanduser(PHOTO_DIR)):
        for name in files:
            result.append(os.path.join(root, name))
    return result

def list_camera_files(camera, path='/'):
    result = []
    # get files
    gp_list = gp.check_result(
        gp.gp_camera_folder_list_files(camera, path))
    for name, value in gp_list:
        result.append(os.path.join(path, name))
    # read folders
    folders = []
    gp_list = gp.check_result(
        gp.gp_camera_folder_list_folders(camera, path))
    for name, value in gp_list:
        folders.append(name)
    # recurse over subfolders
    for name in folders:
        result.extend(list_camera_files(camera, os.path.join(path, name)))
    return result

def get_camera_file_info(camera, path):
    folder, name = os.path.split(path)
    return gp.check_result(
        gp.gp_camera_file_get_info(camera, folder, name))

def main():
    blinkt.set_clear_on_exit()
    blinkt.set_brightness(0.1)
    computer_files = list_computer_files()
    camera = gp.check_result(gp.gp_camera_new())
    time.sleep(0.5)
    gp.check_result(gp.gp_camera_init(camera))
    print('Getting list of files from camera...')
    camera_files = list_camera_files(camera)
    if not camera_files:
        print('No files found')
        gp.check_result(gp.gp_camera_exit(camera))
        return 0
    print('Copying files...')
    for idx, path in enumerate(camera_files):
        blinkt.set_pixel((idx - 1) % blinkt.NUM_PIXELS, 0, 0, 0)
        blinkt.set_pixel(idx % blinkt.NUM_PIXELS, 31, 31, 31)
        blinkt.show()
        info = get_camera_file_info(camera, path)
        timestamp = datetime.fromtimestamp(info.file.mtime)
        folder, name = os.path.split(path)
        dest_dir = get_target_dir(timestamp)
        dest = os.path.join(dest_dir, name)
        if dest in computer_files:
            if (info.file.size and info.file.size == os.path.getsize(dest)):
                continue
        print('%s -> %s' % (path, dest_dir))
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        camera_file = gp.check_result(gp.gp_camera_file_get(
            camera, folder, name, gp.GP_FILE_TYPE_NORMAL))
        gp.check_result(gp.gp_file_save(camera_file, dest))
    gp.check_result(gp.gp_camera_exit(camera))
    return 0

if __name__ == '__main__':
    sys.exit(main())

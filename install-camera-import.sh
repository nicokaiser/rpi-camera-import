#!/bin/sh

apt install -y --no-install-recommends python3-gphoto2 python3-blinkt python3-psutil lockfile-progs exfat-fuse

cp -a rootfs/* /

dpkg -i /usr/local/src/usbmount_0.0.24_all.deb

systemctl daemon-reload
systemctl enable blinkt-clear.service
systemctl enable blinkt-disk-usage.service

#!/bin/bash -e

if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi

apt install -y --no-install-recommends python3-gphoto2 python3-blinkt python3-psutil lockfile-progs exfat-fuse
dpkg -i /usr/local/src/usbmount_0.0.24_all.deb

cp -a rootfs/* /

systemctl daemon-reload
systemctl enable blinkt-clear.service
systemctl enable blinkt-disk-usage.service

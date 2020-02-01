#!/bin/bash -e

if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi

apt update
apt upgrade -y

apt install -y --no-install-recommends python3-gphoto2 python3-blinkt python3-psutil lockfile-progs exfat-fuse
cp -a rootfs/* /
dpkg -i --force-confold /usr/local/src/usbmount_0.0.24_all.deb

# python3-blinkt Timing fix, see https://github.com/pimoroni/blinkt/pull/73
sed -i.backup -e 's/time.sleep(0.0000005)/time.sleep(0)/' /usr/lib/python3/dist-packages/blinkt.py

systemctl daemon-reload
systemctl enable blinkt-clear.service
systemctl enable --now blinkt-disk-usage.service

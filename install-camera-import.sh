#!/bin/sh

apt install -y --no-install-recommends python3-gphoto2 python3-blinkt python3-psutil

cp -a rootfs/* /

systemctl daemon-reload
#systemctl enable blinkt-clear.service
#systemctl enable blinkt-disk-usage.service

# Raspberry Pi Camera Import

These instructions transform a Raspberry Pi to an automatic headless photo import device for digital cameras.

## Features

When a digital camera is plugged in the USB port, all new photos are copied to the Pi's SD card automatically. Use a reasonably large SD card and build a headless photo backup device.

The files are stored in the home directory and ordered by file date (usually the capture date):

`/home/pi/Pictures/Sony_ILCE-7_xxxxxxxx/2018-02-13/DSC01234.arw`

This way, the chance of duplicates is reduced (see "Restrictions").

## Requirements

- Raspberry Pi (B+, 2, 3, Zero, Zero W) with a free USB port
- Raspbian Stretch Lite (tested with version 2017-11-29)
- Digital Camera with PTP [supported by gphoto2](http://gphoto.org/proj/libgphoto2/support.php)

## Installation

All commands must be run as root, so become root first with

```
sudo su -
```

### Upgrade packages and install gphoto2 library

```
apt update
apt upgrade -y
apt install -y --no-install-recommends libgphoto2-6 libgphoto2-port12 \ 
    libgphoto2-dev python3-dev python3-wheel python3-pip python3-setuptools

pip3 install gphoto2

rpi-update
```

### Camera Import udev script

This script is executed as systemd service every time a PTP device is plugged in. All new files are imported, duplicate filenames are skipped.

```
cp usr/local/bin/gphoto2-auto-import.py /usr/local/bin
cp etc/systemd/system/gphoto2-auto-import@.service /etc/systemd/system
cp etc/udev/rules.d/70-gphoto2-auto-import.rules /etc/udev/rules.d
```

### Read-only mode

This puts the Raspbian filesystem into read-only mode and only remounts it to read-write when a camera is connected. So you can just pull the power plug when copying is done.

```
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/read-only-fs.sh
bash read-only-fs.sh

apt remove -y triggerhappy
systemctl disable apt-daily-upgrade.service
systemctl disable apt-daily-upgrade.timer
```

## Limitations

- This only works with cameras supported by gphoto2 and with PTP mode (not USB mass storage mode).
- There could theoretically be filename duplicates. That usually is, when more than 10.000 photos are taken with the same camera on the same day.
- For some cameras, udev cannot determine a serial number. E.g. the folder for any Canon EOS 400D is always `Canon_Inc._Canon_Digital_Camera`. This may only be a problem when importing from more than one camera.

## Optional Components

### Wi-Fi Access Point

Make the Raspberry Pi open a Wi-Fi Access Point, so you can connect to it with your mobile phone (any SSH client) and check the files that were imported.

```
apt install -y --no-install-recommends hostapd

echo "interface wlan0" >> /etc/dhcpcd.conf
echo "static ip_address=192.168.4.1/24" >> /etc/dhcpcd.conf

cp etc/hostapd/hostapd.conf /etc/hostapd
cp etc/default/hostapd /etc/default
```

### Announce SSH service via Bonjour

To find the device's IP address, you can make it announce via Avahi (Bonjour). SSH clients like Prompt or Termius (iOS) can find the device in the same network:

```
cp /usr/share/doc/avahi-daemon/examples/ssh.service /etc/avahi/services/ssh.service
```

### Disable Bluetooth and Audio

Since no Bluetooth and Audio support is needed, these can be disabled:

```
systemctl disable bluetooth.service
systemctl disable hciuart.service

echo "dtparam=audio=off" >> /boot/config.txt
echo "dtoverplay=pi3-disable-bt" >> /boot/config.txt
```

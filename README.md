# Raspberry Pi Camera Import

These instructions transform a Raspberry Pi to an automatic headless photo import device for digital cameras and SD card readers.

![Raspberry Pi Camera Import](preview.jpg)

## Features

When a digital camera or and SD card reader is plugged in the USB port, all new photos are copied to the Pi's SD card automatically. Use a reasonably large SD card and build a headless photo backup device.

The files are stored in the home directory and ordered by file date (usually the capture date):

`/home/pi/Pictures/2018-02-13/DSC01234.arw`

This way, the risk of duplicates is reduced (see "Restrictions").

## Requirements

- Raspberry Pi with a free USB port
- Raspbian Buster Lite (tested with version September 2019)
- USB SD card reader or digital camera with PTP or USB mass storage support
- Optional: Piromoni Blinkt! for graphical status display

## Installation

```
sudo apt update -y
sudo apt upgrade -y
sudo apt install -y --no-install-recommends git

git clone https://github.com/nicokaiser/rpi-camera-import.git
cd rpi-camera-import

sudo ./install-camera-import.sh
```

### Read-only mode

This puts the Raspbian filesystem into read-only mode and only remounts it to read-write when files are copied. So you can just pull the power plug when copying is done.

```
sudo ./enable-read-only.sh
```

## Limitations

- Only works with cameras that support USB mass storage mode or are supported by gphoto2 with PTP mode.
- There could theoretically be filename duplicates. That usually is, when more than 10.000 photos are taken on the same day, or when backing up multiple cameras.
- When using an USB card reader, you need to unplug and replug the card reader when changing cards.

## Optional Components

### Pimoroni Blinkt!

[Blinkt!](https://github.com/pimoroni/blinkt) is a pHAT stacking header for Raspberry Pi with 8 RGB LEDs. If it is installed, it is used for a simple status display:

- When idle, disk usage is displayed with red/green LEDs
- While copying, the progress is displayed [see video](https://www.youtube.com/watch?v=rcr646JgzJ4).

### Wi-Fi Access Point

Make the Raspberry Pi open a Wi-Fi Access Point, so you can connect to it with your mobile phone (any SSH client) and check the files that were imported.

This `wpa_supplicant.conf` configuration tries to connect to `Your Home Network` first and if that fails, creates an own network called `Camera Import` with passphrase `raspberry`:

```
country=DE
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
ap_scan=1

network={
    ssid="Your Home Network"
    psk="yoursecretpassphrase"
    key_mgmt=WPA-PSK
}

network={
    ssid="Camera Import"
    mode=2
    frequency=2432
    key_mgmt=WPA-PSK
    psk="raspberry"
}
```

### Announce SSH service via Bonjour

To find the device's IP address, you can make it announce via Avahi (Bonjour). SSH clients like Prompt or Termius (iOS) can find the device in the same network:

```
sudo cp /usr/share/doc/avahi-daemon/examples/ssh.service /etc/avahi/services/ssh.service
```

### Activate Samba access

If you would like to access the imported pictures via SMB, you can install `samba` with a minimal configuration (please change the default password `raspberry`):

```
sudo ./install-samba.sh
```

(This is currently untested and may collide with the read-only filesystem)

### Disable Bluetooth and Audio

Since no Bluetooth and Audio support is needed, these can be disabled:

```
systemctl disable bluetooth.service
systemctl disable hciuart.service

echo "dtparam=audio=off" >> /boot/config.txt
echo "dtoverplay=pi3-disable-bt" >> /boot/config.txt
```

## References

- [libgphoto2: camera access and control library](https://github.com/gphoto/libgphoto2)
- [python-gphoto2: Python interface to libgphoto2](https://github.com/jim-easterbrook/python-gphoto2)
- [usbmount](https://github.com/rbrito/usbmount)

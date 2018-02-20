#!/bin/sh

# Install Samba for SMB access to imported Pictures

apt install -y --no-install-recommends samba
cat <<'EOF' > /etc/samba/smb.conf
[global]
    netbios name = Camera Import
    server string = Camera Import
    workgroup = WORKGROUP
    security = user
    map to guest = Never
    local master = no
    preferred master = no
    dns proxy = no
    syslog only = yes
    syslog = 1
    server role = standalone server
    passdb backend = smbpasswd:/etc/samba/smbpasswd
    obey pam restrictions = yes
    private dir = /var/lib/samba

[Pictures]
    comment = Pictures Folder
    path = /home/pi/Pictures
    guest ok = no
    browseable = yes
    valid users = pi
    read only = no
EOF

cat <<'EOF' | smbpasswd -a pi -s
raspberry
raspberry
EOF

echo "tmpfs /var/lib/samba tmpfs nodev,nosuid 0 0" >> /etc/fstab

#!/bin/bash

MOUNT_POINT="/mnt/<your folder here>"  
DEVICE="UUID=XXXXXXXXXXXXXXXX"  #  <-- Replace with your actual device UUID --> check with 'lsblk -f'

# Check if the mount point exists; 
if [[ ! -d "$MOUNT_POINT" ]]; then
    echo "Error: Mount point $MOUNT_POINT does not exist. Please create it first."
    exit 1
fi

# Check if the device is already mounted
if mountpoint -q "$MOUNT_POINT"; then
    echo "The partition is already mounted at $MOUNT_POINT."
else
    echo "Mounting $DEVICE to $MOUNT_POINT..."

    # Filesystem type detection
    FS_TYPE=$(lsblk -no FSTYPE "$DEVICE")

    if [[ "$FS_TYPE" == "ntfs" ]] || [[ "$FS_TYPE" == "exfat" ]]; then
      sudo mount -t "$FS_TYPE" -o uid="$(id -u)",gid="$(id -g)",umask=022 "$DEVICE" "$MOUNT_POINT"
    else
      sudo mount "$DEVICE" "$MOUNT_POINT"
    fi  

    if [[ $? -eq 0 ]]; then
        echo "Successfully mounted $DEVICE at $MOUNT_POINT."
    else
        echo "Failed to mount $DEVICE. Check the device path or permissions."
    fi
fi

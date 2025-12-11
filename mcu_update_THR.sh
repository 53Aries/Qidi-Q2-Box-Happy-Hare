#!/bin/bash

VERSION=1.3
RESET_CMD=73 # 0x73 -> 115
KLIPPER_BIN="/home/mks/klipper_THR.bin"
KLIPPER_MCU="/dev/ttyS4"
BOOTLOADER_MCU="/dev/ttyS4"

echo "Start mcu_update_THR.sh, version: $VERSION"

if [ $# -ge 1 ]
then
	KLIPPER_BIN=$1
	echo "KLIPPER_BIN: $KLIPPER_BIN"
fi
if [ $# -ge 2 ]
then
	KLIPPER_MCU=$2
	echo "KLIPPER_MCU: $KLIPPER_MCU"
fi
if [ $# -ge 3 ]
then
	BOOTLOADER_MCU=$3
	echo "BOOTLOADER_MCU: $BOOTLOADER_MCU"
fi
if [ $# -ge 4 ]
then
	RESET_CMD=$4
fi

if [ -f $KLIPPER_BIN ]
then
	# reset & wait success
	# /home/mks/serial_com $KLIPPER_MCU --cmd=$RESET_CMD
	if [ -e $KLIPPER_MCU ] # softlink
	then
		# get dict
		/home/mks/serial_com_dict $KLIPPER_MCU
		/home/mks/zlib_decompress
		msgid=$(/home/mks/json_reader dict.json | awk -F': ' '{print $2}')
		if [ $msgid -le 0 ]
		then
			msgid=$((128+$msgid))
		fi
		RESET_CMD=$msgid
		echo "Get $KLIPPER_MCU 's dict, reset commond id = $msgid."
	fi

	# No need to check klipper mode 
	/home/mks/serial_com $KLIPPER_MCU --cmd=$RESET_CMD
	sleep 2

	if [ -e $BOOTLOADER_MCU ]
	then
		# update
		/home/mks/hid-flash $KLIPPER_BIN $BOOTLOADER_MCU

		cmd=$?
		if [ $cmd -eq 0 ]
		then
			result=0
		else
			echo "ERROR: hid-flash failed($cmd)..."
			result=$((3+$cmd))
		fi
	else
		echo "ERROR: no ACM-CDC device..."
		result=2
	fi

	exit $result
else
	echo "ERROR: no firmware..."
	exit 1
fi

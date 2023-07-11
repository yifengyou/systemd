# udev规则定义


## 基础

* udev规则是一些定义在以.rules为扩展名的文件中的指令，用于控制udev如何管理设备文件和设备事件。
* udev规则可以根据设备的属性，如内核名称，子系统，驱动，序列号等，来匹配设备，并为设备分配名称，权限，符号链接等。
* udev规则还可以调用外部程序来执行一些操作或获取一些信息。
* udev规则文件通常存放在/usr/lib/udev/rules.d或/etc/udev/rules.d目录下，文件名以数字开头，表示规则的执行顺序。
* udev规则文件的执行顺序是从小到大，即数字越小的规则文件越先执行，数字相同的规则文件按照字母顺序执行.
* 每个规则文件由多行组成，每行代表一个规则。每个规则由多个键值对组成，用逗号分隔。键值对分为匹配键和赋值键。匹配键用来判断规则是否应用于设备，赋值键用来指定规则的效果。一些常用的匹配键和赋值键如下：

| 键         | 类别   | 作用                                                                                           |
| ---------- | ------ | ---------------------------------------------------------------------------------------------- |
| ACTION     | 匹配键 | 匹配设备事件的类型，如add, remove, change等。                                                  |
| KERNEL     | 匹配键 | 匹配设备的子系统名称，如block, usb, input等                                                    |
| SUBSYSTEM  | 匹配键 | 匹配设备的子系统名称，如block, usb, input等                                                    |
| DRIVER     | 匹配键 | 匹配设备的驱动名称，如usbhid, ide-disk等。                                                     |
| BUS        | 匹配键 | 匹配设备的总线名称，如usb, pci等                                                               |
| ID         | 匹配键 | 匹配设备在devpath中的识别号，如1-1.2, 0000:00:1d.0等                                           |
| ATTR{file} | 匹配键 | 匹配设备在sysfs中的属性文件的内容，如ATTR{vendor}==“Logitech”                                  |
| ENV{key}   | 匹配键 | 匹配一个环境变量的值，如ENV{ID_FS_TYPE}==“vfat”                                                |
| PROGRAM    | 匹配键 | 执行一个外部程序，并根据其返回值判断是否匹配，如PROGRAM==“/sbin/blkid -o value -s TYPE %N”     |
| RESULT     | 匹配键 | 匹配最近一次PROGRAM调用的返回字符串，如RESULT==“ext4”。                                        |
| ENV{key}   | 匹配键 | 匹配一个环境变量的值，如ENV{ID_FS_TYPE}==“vfat”                                                |
| NAME       | **赋值键** | 指定设备节点的名称，如NAME=“mydisk”。                                                          |
| SYMLINK    | **赋值键** | 指定设备节点的符号链接，可以有多个，用空格分隔，如SYMLINK+=“disk1 disk2”。                     |
| OWNER      | **赋值键** | 指定设备节点的所有者，可以是用户名或用户ID，如OWNER="root"或OWNER=“0”。                        |
| GROUP      | **赋值键** | 指定设备节点的所属组，可以是组名或组ID，如GROUP="disk"或GROUP=“6”。                            |
| MODE       | **赋值键** | 指定设备节点的权限，用八进制表示，如MODE=“0660”。                                              |
| RUN        | **赋值键** | 指定执行一个外部程序或脚本，可以有多个，用空格分隔，如RUN+=“/sbin/hdparm -q -m16 /dev/$kernel” |


* udev规则是挨个执行的，即当一个设备事件发生时，udev会按照规则文件的顺序和规则的顺序，逐一匹配和执行规则。如果一个规则匹配成功，那么udev会执行该规则的赋值键，并继续执行后面的规则，直到遇到一个GOTO或者OPTIONS last_rule的赋值键，或者所有的规则都执行完毕
* udev规则的匹配键和赋值键是用来定义规则的条件和动作的两类键。
 - **匹配键**用来判断设备的属性是否符合规则的要求，例如设备的内核名、子系统、驱动、事件类型等。
 - **赋值键**用来指定规则的执行结果，例如设备节点的名称、权限、所有者、符号链接等。
 - 匹配键和赋值键之间用逗号分隔，一条规则可以有多个匹配键和赋值键。


## udev规则用例

简单的udev规则：

```
# This rule assigns a fixed name to a USB mouse
ACTION=="add", SUBSYSTEM=="input", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="c52f", NAME="usbmouse"
```

规则：当添加一个输入子系统的设备时，如果它的厂商ID是046d，产品ID是c52f（这是一个罗技无线鼠标的标识），那么就为它分配一个名字叫usbmouse，并在/dev下创建一个设备文件。这样就可以保证这个鼠标总是有一个固定的名字，而不会受到插入顺序或其他因素的影响。

```
ACTION=="add", KERNEL=="sda", RUN+="/bin/raw /dev/raw/raw1 %N"
```
规则：当添加一个设备，并且设备的内核名是sda时，执行/bin/raw /dev/raw/raw1 %N这个命令。其中，ACTION和KERNEL是匹配键，RUN是赋值键，%N是一个替换操作符，表示设备节点的名称。



## 最佳素材

udev默认规则，是最好的学习素材

```
[root@rocky8 ~]# rpm -ql systemd-udev |grep "\.rules"
/etc/udev/rules.d
/usr/lib/udev/rules.d
/usr/lib/udev/rules.d/40-elevator.rules
/usr/lib/udev/rules.d/40-redhat.rules
/usr/lib/udev/rules.d/50-udev-default.rules
/usr/lib/udev/rules.d/60-alias-kmsg.rules
/usr/lib/udev/rules.d/60-block.rules
/usr/lib/udev/rules.d/60-cdrom_id.rules
/usr/lib/udev/rules.d/60-drm.rules
/usr/lib/udev/rules.d/60-evdev.rules
/usr/lib/udev/rules.d/60-fido-id.rules
/usr/lib/udev/rules.d/60-input-id.rules
/usr/lib/udev/rules.d/60-persistent-alsa.rules
/usr/lib/udev/rules.d/60-persistent-input.rules
/usr/lib/udev/rules.d/60-persistent-storage-tape.rules
/usr/lib/udev/rules.d/60-persistent-storage.rules
/usr/lib/udev/rules.d/60-persistent-v4l.rules
/usr/lib/udev/rules.d/60-sensor.rules
/usr/lib/udev/rules.d/60-serial.rules
/usr/lib/udev/rules.d/64-btrfs.rules
/usr/lib/udev/rules.d/70-joystick.rules
/usr/lib/udev/rules.d/70-mouse.rules
/usr/lib/udev/rules.d/70-power-switch.rules
/usr/lib/udev/rules.d/70-touchpad.rules
/usr/lib/udev/rules.d/70-uaccess.rules
/usr/lib/udev/rules.d/71-seat.rules
/usr/lib/udev/rules.d/73-idrac.rules
/usr/lib/udev/rules.d/73-seat-late.rules
/usr/lib/udev/rules.d/75-net-description.rules
/usr/lib/udev/rules.d/75-probe_mtd.rules
/usr/lib/udev/rules.d/78-sound-card.rules
/usr/lib/udev/rules.d/80-drivers.rules
/usr/lib/udev/rules.d/80-net-setup-link.rules
/usr/lib/udev/rules.d/90-vconsole.rules
/usr/lib/udev/rules.d/99-systemd.rules
```

```
# rpm -ql systemd-udev  |grep rules |xargs -i cat {}

# We aren't adding devices skip the elevator check
ACTION!="add", GOTO="sched_out"

SUBSYSTEM!="block", GOTO="sched_out"
ENV{DEVTYPE}!="disk", GOTO="sched_out"

# Technically, dm-multipath can be configured to use an I/O scheduler.
# However, there are races between the 'add' uevent and the linking in
# of the queue/scheduler sysfs file.  For now, just skip dm- devices.
KERNEL=="dm-*|md*", GOTO="sched_out"

# Skip bio-based devices, which don't support an I/O scheduler.
ATTR{queue/scheduler}=="none", GOTO="sched_out"

# If elevator= is specified on the kernel command line, change the
# scheduler to the one specified.
IMPORT{cmdline}="elevator"
ENV{elevator}!="", ATTR{queue/scheduler}="$env{elevator}"

LABEL="sched_out"# do not edit this file, it will be overwritten on update

# CPU hotadd request
SUBSYSTEM=="cpu", ACTION=="add", TEST=="online", ATTR{online}=="0", ATTR{online}="1"

# Memory hotadd request
SUBSYSTEM!="memory", GOTO="memory_hotplug_end"
ACTION!="add", GOTO="memory_hotplug_end"
CONST{arch}=="s390*", GOTO="memory_hotplug_end"
CONST{arch}=="ppc64*", GOTO="memory_hotplug_end"

ENV{.state}="online"
CONST{virt}=="none", ENV{.state}="online_movable"
ATTR{state}=="offline", ATTR{state}="$env{.state}"

LABEL="memory_hotplug_end"

# reload sysctl.conf / sysctl.conf.d settings when the bridge module is loaded
ACTION=="add", SUBSYSTEM=="module", KERNEL=="bridge", RUN+="/usr/lib/systemd/systemd-sysctl --prefix=/proc/sys/net/bridge"

# load SCSI generic (sg) driver
SUBSYSTEM=="scsi", ENV{DEVTYPE}=="scsi_device", TEST!="[module/sg]", RUN+="/sbin/modprobe -bv sg"
SUBSYSTEM=="scsi", ENV{DEVTYPE}=="scsi_target", TEST!="[module/sg]", RUN+="/sbin/modprobe -bv sg"

# Rule for prandom character device node permissions
KERNEL=="prandom", MODE="0644"

# Rules for creating the ID_PATH for SCSI devices based on the CCW bus
# using the form: ccw-<BUS_ID>-zfcp-<WWPN>:<LUN>
#
ACTION=="remove", GOTO="zfcp_scsi_device_end"

#
# Set environment variable "ID_ZFCP_BUS" to "1" if the devices
# (both disk and partition) are SCSI devices based on FCP devices
#
KERNEL=="sd*", SUBSYSTEMS=="ccw", DRIVERS=="zfcp", ENV{.ID_ZFCP_BUS}="1"

# For SCSI disks
KERNEL=="sd*[!0-9]", SUBSYSTEMS=="scsi", ENV{.ID_ZFCP_BUS}=="1", ENV{DEVTYPE}=="disk", SYMLINK+="disk/by-path/ccw-$attr{hba_id}-zfcp-$attr{wwpn}:$attr{fcp_lun}"


# For partitions on a SCSI disk
KERNEL=="sd*[0-9]", SUBSYSTEMS=="scsi", ENV{.ID_ZFCP_BUS}=="1", ENV{DEVTYPE}=="partition", SYMLINK+="disk/by-path/ccw-$attr{hba_id}-zfcp-$attr{wwpn}:$attr{fcp_lun}-part%n"

LABEL="zfcp_scsi_device_end"
# do not edit this file, it will be overwritten on update

# run a command on remove events
ACTION=="remove", ENV{REMOVE_CMD}!="", RUN+="$env{REMOVE_CMD}"
ACTION=="remove", GOTO="default_end"

SUBSYSTEM=="virtio-ports", KERNEL=="vport*", ATTR{name}=="?*", SYMLINK+="virtio-ports/$attr{name}"

# select "system RTC" or just use the first one
SUBSYSTEM=="rtc", ATTR{hctosys}=="1", SYMLINK+="rtc"
SUBSYSTEM=="rtc", KERNEL=="rtc0", SYMLINK+="rtc", OPTIONS+="link_priority=-100"

SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", IMPORT{builtin}="usb_id", IMPORT{builtin}="hwdb --subsystem=usb"
ENV{MODALIAS}!="", IMPORT{builtin}="hwdb --subsystem=$env{SUBSYSTEM}"

ACTION!="add", GOTO="default_end"

SUBSYSTEM=="tty", KERNEL=="ptmx", GROUP="tty", MODE="0666"
SUBSYSTEM=="tty", KERNEL=="tty", GROUP="tty", MODE="0666"
SUBSYSTEM=="tty", KERNEL=="tty[0-9]*", GROUP="tty", MODE="0620"
SUBSYSTEM=="tty", KERNEL=="sclp_line[0-9]*", GROUP="tty", MODE="0620"
SUBSYSTEM=="tty", KERNEL=="ttysclp[0-9]*", GROUP="tty", MODE="0620"
SUBSYSTEM=="tty", KERNEL=="3270/tty[0-9]*", GROUP="tty", MODE="0620"
SUBSYSTEM=="vc", KERNEL=="vcs*|vcsa*", GROUP="tty"
KERNEL=="tty[A-Z]*[0-9]|ttymxc[0-9]*|pppox[0-9]*|ircomm[0-9]*|noz[0-9]*|rfcomm[0-9]*", GROUP="dialout"

SUBSYSTEM=="mem", KERNEL=="mem|kmem|port", GROUP="kmem", MODE="0640"

SUBSYSTEM=="input", GROUP="input"
SUBSYSTEM=="input", KERNEL=="js[0-9]*", MODE="0664"

SUBSYSTEM=="video4linux", GROUP="video"
SUBSYSTEM=="graphics", GROUP="video"
SUBSYSTEM=="drm", KERNEL!="renderD*", GROUP="video"
SUBSYSTEM=="dvb", GROUP="video"
SUBSYSTEM=="media", GROUP="video"
SUBSYSTEM=="cec", GROUP="video"

SUBSYSTEM=="drm", KERNEL=="renderD*", GROUP="render", MODE="0666"
SUBSYSTEM=="kfd", GROUP="render", MODE="0666"

SUBSYSTEM=="sound", GROUP="audio", \
  OPTIONS+="static_node=snd/seq", OPTIONS+="static_node=snd/timer"

SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", MODE="0664"

SUBSYSTEM=="firewire", ATTR{units}=="*0x00a02d:0x00010*", GROUP="video"
SUBSYSTEM=="firewire", ATTR{units}=="*0x00b09d:0x00010*", GROUP="video"
SUBSYSTEM=="firewire", ATTR{units}=="*0x00a02d:0x010001*", GROUP="video"
SUBSYSTEM=="firewire", ATTR{units}=="*0x00a02d:0x014001*", GROUP="video"

KERNEL=="parport[0-9]*", GROUP="lp"
SUBSYSTEM=="printer", KERNEL=="lp*", GROUP="lp"
SUBSYSTEM=="ppdev", GROUP="lp"
KERNEL=="lp[0-9]*", GROUP="lp"
KERNEL=="irlpt[0-9]*", GROUP="lp"
SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ENV{ID_USB_INTERFACES}=="*:0701??:*", GROUP="lp"

SUBSYSTEM=="block", GROUP="disk"
SUBSYSTEM=="block", KERNEL=="sr[0-9]*", GROUP="cdrom"
SUBSYSTEM=="scsi_generic", SUBSYSTEMS=="scsi", ATTRS{type}=="4|5", GROUP="cdrom"
KERNEL=="sch[0-9]*", GROUP="cdrom"
KERNEL=="pktcdvd[0-9]*", GROUP="cdrom"
KERNEL=="pktcdvd", GROUP="cdrom"

SUBSYSTEM=="scsi_generic|scsi_tape", SUBSYSTEMS=="scsi", ATTRS{type}=="1|8", GROUP="tape"
SUBSYSTEM=="scsi_generic", SUBSYSTEMS=="scsi", ATTRS{type}=="0", GROUP="disk"
KERNEL=="qft[0-9]*|nqft[0-9]*|zqft[0-9]*|nzqft[0-9]*|rawqft[0-9]*|nrawqft[0-9]*", GROUP="disk"
KERNEL=="loop-control", GROUP="disk", OPTIONS+="static_node=loop-control"
KERNEL=="btrfs-control", GROUP="disk"
KERNEL=="rawctl", GROUP="disk"
SUBSYSTEM=="raw", KERNEL=="raw[0-9]*", GROUP="disk"
SUBSYSTEM=="aoe", GROUP="disk", MODE="0220"
SUBSYSTEM=="aoe", KERNEL=="err", MODE="0440"

KERNEL=="rfkill", MODE="0664"
KERNEL=="tun", MODE="0666", OPTIONS+="static_node=net/tun"

KERNEL=="fuse", MODE="0666", OPTIONS+="static_node=fuse"

# The static_node is required on s390x and ppc (they are using MODULE_ALIAS)
KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"

SUBSYSTEM=="ptp", ATTR{clock_name}=="KVM virtual PTP", SYMLINK += "ptp_kvm"

SUBSYSTEM=="ptp", ATTR{clock_name}=="hyperv", SYMLINK += "ptp_hyperv"

LABEL="default_end"
SUBSYSTEM!="block", GOTO="log_end"
KERNEL=="loop*|ram*", GOTO="log_end"
ACTION=="remove", GOTO="log_end"
ENV{DM_UDEV_DISABLE_OTHER_RULES_FLAG}=="1", GOTO="log_end"
ENV{DM_UDEV_DISABLE_DISK_RULES_FLAG}=="1", GOTO="log_end"

IMPORT{cmdline}="udev.alias"
ENV{udev.alias}=="1", RUN+="/bin/sh -c 'echo udev-alias: $name \($links\) > /dev/kmsg'"

LABEL="log_end"
# do not edit this file, it will be overwritten on update

# enable in-kernel media-presence polling
ACTION=="add", SUBSYSTEM=="module", KERNEL=="block", ATTR{parameters/events_dfl_poll_msecs}=="0", \
  ATTR{parameters/events_dfl_poll_msecs}="2000"

# forward scsi device event to corresponding block device
ACTION=="change", SUBSYSTEM=="scsi", ENV{DEVTYPE}=="scsi_device", TEST=="block", ATTR{block/*/uevent}="change"

# watch metadata changes, caused by tools closing the device node which was opened for writing
ACTION!="remove", SUBSYSTEM=="block", KERNEL=="loop*|nvme*|sd*|vd*|xvd*|pmem*|mmcblk*|dasd*", OPTIONS+="watch"
# do not edit this file, it will be overwritten on update

ACTION=="remove", GOTO="cdrom_end"
SUBSYSTEM!="block", GOTO="cdrom_end"
KERNEL!="sr[0-9]*|vdisk*|xvd*", GOTO="cdrom_end"
ENV{DEVTYPE}!="disk", GOTO="cdrom_end"

# unconditionally tag device as CDROM
KERNEL=="sr[0-9]*", ENV{ID_CDROM}="1"

# stop automatically any mount units bound to the device if the media eject
# button is pressed.
ENV{ID_CDROM}=="1", ENV{SYSTEMD_MOUNT_DEVICE_BOUND}="1"

# media eject button pressed
ENV{DISK_EJECT_REQUEST}=="?*", RUN+="cdrom_id --eject-media $devnode", GOTO="cdrom_end"

# import device and media properties and lock tray to
# enable the receiving of media eject button events
IMPORT{program}="cdrom_id --lock-media $devnode"

# ejecting a CD does not remove the device node, so mark the systemd device
# unit as inactive while there is no medium; this automatically cleans up of
# stale mounts after ejecting
ENV{DISK_MEDIA_CHANGE}=="?*", ENV{ID_CDROM_MEDIA}!="?*", ENV{SYSTEMD_READY}="0"

KERNEL=="sr0", SYMLINK+="cdrom", OPTIONS+="link_priority=-100"

LABEL="cdrom_end"
# do not edit this file, it will be overwritten on update

ACTION!="remove", SUBSYSTEM=="drm", SUBSYSTEMS=="pci|usb|platform", IMPORT{builtin}="path_id"

# by-path
ENV{ID_PATH}=="?*", KERNEL=="card*", SYMLINK+="dri/by-path/$env{ID_PATH}-card"
ENV{ID_PATH}=="?*", KERNEL=="controlD*", SYMLINK+="dri/by-path/$env{ID_PATH}-control"
ENV{ID_PATH}=="?*", KERNEL=="renderD*", SYMLINK+="dri/by-path/$env{ID_PATH}-render"
# do not edit this file, it will be overwritten on update

ACTION=="remove", GOTO="evdev_end"
KERNEL!="event*", GOTO="evdev_end"

# skip later rules when we find something for this input device
IMPORT{builtin}="hwdb --subsystem=input --lookup-prefix=evdev:", \
  RUN{builtin}+="keyboard", GOTO="evdev_end"

# AT keyboard matching by the machine's DMI data
DRIVERS=="atkbd", \
  IMPORT{builtin}="hwdb 'evdev:atkbd:$attr{[dmi/id]modalias}'", \
  RUN{builtin}+="keyboard", GOTO="evdev_end"

# device matching the input device name + properties + the machine's DMI data
KERNELS=="input*", IMPORT{builtin}="hwdb 'evdev:name:$attr{name}:phys:$attr{phys}:ev:$attr{capabilities/ev}:$attr{[dmi/id]modalias}'", \
  RUN{builtin}+="keyboard", GOTO="evdev_end"

# device matching the input device name and the machine's DMI data
KERNELS=="input*", IMPORT{builtin}="hwdb 'evdev:name:$attr{name}:$attr{[dmi/id]modalias}'", \
  RUN{builtin}+="keyboard", GOTO="evdev_end"

LABEL="evdev_end"
# do not edit this file, it will be overwritten on update

ACTION=="remove", GOTO="fido_id_end"

SUBSYSTEM=="hidraw", IMPORT{program}="fido_id"

LABEL="fido_id_end"
# do not edit this file, it will be overwritten on update

ACTION=="remove", GOTO="id_input_end"

SUBSYSTEM=="input", ENV{ID_INPUT}=="", IMPORT{builtin}="input_id"
SUBSYSTEM=="input", IMPORT{builtin}="hwdb --subsystem=input --lookup-prefix=id-input:modalias:"

LABEL="id_input_end"
# do not edit this file, it will be overwritten on update

ACTION=="remove", GOTO="persistent_alsa_end"
SUBSYSTEM!="sound", GOTO="persistent_alsa_end"
KERNEL!="controlC[0-9]*", GOTO="persistent_alsa_end"

SUBSYSTEMS=="usb", ENV{ID_MODEL}=="", IMPORT{builtin}="usb_id"
ENV{ID_SERIAL}=="?*", ENV{ID_USB_INTERFACE_NUM}=="?*", SYMLINK+="snd/by-id/$env{ID_BUS}-$env{ID_SERIAL}-$env{ID_USB_INTERFACE_NUM}"
ENV{ID_SERIAL}=="?*", ENV{ID_USB_INTERFACE_NUM}=="", SYMLINK+="snd/by-id/$env{ID_BUS}-$env{ID_SERIAL}"

IMPORT{builtin}="path_id"
ENV{ID_PATH}=="?*", SYMLINK+="snd/by-path/$env{ID_PATH}"

LABEL="persistent_alsa_end"
# do not edit this file, it will be overwritten on update

ACTION=="remove", GOTO="persistent_input_end"
SUBSYSTEM!="input", GOTO="persistent_input_end"
SUBSYSTEMS=="bluetooth", ENV{ID_BUS}="bluetooth", GOTO="persistent_input_end"
# Bluetooth devices don't always have the bluetooth subsystem
ATTRS{id/bustype}=="0005", ENV{ID_BUS}="bluetooth", GOTO="persistent_input_end"
SUBSYSTEMS=="rmi4", ENV{ID_BUS}="rmi"
SUBSYSTEMS=="serio", ENV{ID_BUS}="i8042"

SUBSYSTEMS=="usb", ENV{ID_BUS}=="", IMPORT{builtin}="usb_id"

# determine class name for persistent symlinks
ENV{ID_INPUT_KEYBOARD}=="?*", ENV{.INPUT_CLASS}="kbd"
ENV{ID_INPUT_MOUSE}=="?*", ENV{.INPUT_CLASS}="mouse"
ENV{ID_INPUT_TOUCHPAD}=="?*", ENV{.INPUT_CLASS}="mouse"
ENV{ID_INPUT_TABLET}=="?*", ENV{.INPUT_CLASS}="mouse"
ENV{ID_INPUT_JOYSTICK}=="?*", ENV{.INPUT_CLASS}="joystick"
DRIVERS=="pcspkr", ENV{.INPUT_CLASS}="spkr"
ATTRS{name}=="*dvb*|*DVB*|* IR *", ENV{.INPUT_CLASS}="ir"

# fill empty serial number
ENV{.INPUT_CLASS}=="?*", ENV{ID_SERIAL}=="", ENV{ID_SERIAL}="noserial"

# by-id links
KERNEL=="mouse*|js*", ENV{ID_BUS}=="?*", ENV{.INPUT_CLASS}=="?*", ATTRS{bInterfaceNumber}=="|00", SYMLINK+="input/by-id/$env{ID_BUS}-$env{ID_SERIAL}-$env{.INPUT_CLASS}"
KERNEL=="mouse*|js*", ENV{ID_BUS}=="?*", ENV{.INPUT_CLASS}=="?*", ATTRS{bInterfaceNumber}=="?*", ATTRS{bInterfaceNumber}!="00", SYMLINK+="input/by-id/$env{ID_BUS}-$env{ID_SERIAL}-if$attr{bInterfaceNumber}-$env{.INPUT_CLASS}"
KERNEL=="event*", ENV{ID_BUS}=="?*", ENV{.INPUT_CLASS}=="?*", ATTRS{bInterfaceNumber}=="|00", SYMLINK+="input/by-id/$env{ID_BUS}-$env{ID_SERIAL}-event-$env{.INPUT_CLASS}"
KERNEL=="event*", ENV{ID_BUS}=="?*", ENV{.INPUT_CLASS}=="?*", ATTRS{bInterfaceNumber}=="?*", ATTRS{bInterfaceNumber}!="00", SYMLINK+="input/by-id/$env{ID_BUS}-$env{ID_SERIAL}-if$attr{bInterfaceNumber}-event-$env{.INPUT_CLASS}"
# allow empty class for USB devices, by appending the interface number
SUBSYSTEMS=="usb", ENV{ID_BUS}=="?*", KERNEL=="event*", ENV{.INPUT_CLASS}=="", ATTRS{bInterfaceNumber}=="?*", \
  SYMLINK+="input/by-id/$env{ID_BUS}-$env{ID_SERIAL}-event-if$attr{bInterfaceNumber}"

# by-path
SUBSYSTEMS=="pci|usb|platform|acpi", IMPORT{builtin}="path_id"
ENV{ID_PATH}=="?*", KERNEL=="mouse*|js*", ENV{.INPUT_CLASS}=="?*", SYMLINK+="input/by-path/$env{ID_PATH}-$env{.INPUT_CLASS}"
ENV{ID_PATH}=="?*", KERNEL=="event*", ENV{.INPUT_CLASS}=="?*", SYMLINK+="input/by-path/$env{ID_PATH}-event-$env{.INPUT_CLASS}"
# allow empty class for platform and usb devices; platform supports only a single interface that way
SUBSYSTEMS=="usb|platform", ENV{ID_PATH}=="?*", KERNEL=="event*", ENV{.INPUT_CLASS}=="", \
  SYMLINK+="input/by-path/$env{ID_PATH}-event"

LABEL="persistent_input_end"
# do not edit this file, it will be overwritten on update

# persistent storage links: /dev/tape/{by-id,by-path}

ACTION=="remove", GOTO="persistent_storage_tape_end"
ENV{UDEV_DISABLE_PERSISTENT_STORAGE_RULES_FLAG}=="1", GOTO="persistent_storage_tape_end"

# type 8 devices are "Medium Changers"
SUBSYSTEM=="scsi_generic", SUBSYSTEMS=="scsi", ATTRS{type}=="8", IMPORT{program}="scsi_id --sg-version=3 --export --whitelisted -d $devnode", \
  SYMLINK+="tape/by-id/scsi-$env{ID_SERIAL}"

SUBSYSTEM=="scsi_generic", SUBSYSTEMS=="scsi", ATTRS{type}=="8", IMPORT{builtin}="path_id", \
  SYMLINK+="tape/by-path/$env{ID_PATH}-changer"

SUBSYSTEM!="scsi_tape", GOTO="persistent_storage_tape_end"

KERNEL=="st*[0-9]|nst*[0-9]", ATTRS{ieee1394_id}=="?*", ENV{ID_SERIAL}="$attr{ieee1394_id}", ENV{ID_BUS}="ieee1394"
KERNEL=="st*[0-9]|nst*[0-9]", ENV{ID_SERIAL}!="?*", SUBSYSTEMS=="usb", IMPORT{builtin}="usb_id"
KERNEL=="st*[0-9]|nst*[0-9]", ENV{ID_SERIAL}!="?*", SUBSYSTEMS=="scsi", KERNELS=="[0-9]*:*[0-9]", ENV{.BSG_DEV}="$root/bsg/$id"
KERNEL=="st*[0-9]|nst*[0-9]", ENV{ID_SERIAL}!="?*", IMPORT{program}="scsi_id --whitelisted --export --device=$env{.BSG_DEV}", ENV{ID_BUS}="scsi"
KERNEL=="st*[0-9]",  ENV{ID_SERIAL}=="?*", SYMLINK+="tape/by-id/$env{ID_BUS}-$env{ID_SERIAL}"
KERNEL=="nst*[0-9]", ENV{ID_SERIAL}=="?*", SYMLINK+="tape/by-id/$env{ID_BUS}-$env{ID_SERIAL}-nst"

# by-path (parent device path)
KERNEL=="st*[0-9]|nst*[0-9]", IMPORT{builtin}="path_id"
KERNEL=="st*[0-9]", ENV{ID_PATH}=="?*", SYMLINK+="tape/by-path/$env{ID_PATH}"
KERNEL=="nst*[0-9]", ENV{ID_PATH}=="?*", SYMLINK+="tape/by-path/$env{ID_PATH}-nst"

LABEL="persistent_storage_tape_end"
# do not edit this file, it will be overwritten on update

# persistent storage links: /dev/disk/{by-id,by-uuid,by-label,by-path}
# scheme based on "Linux persistent device names", 2004, Hannes Reinecke <hare@suse.de>

ACTION=="remove", GOTO="persistent_storage_end"
ENV{UDEV_DISABLE_PERSISTENT_STORAGE_RULES_FLAG}=="1", GOTO="persistent_storage_end"

SUBSYSTEM!="block", GOTO="persistent_storage_end"
KERNEL!="loop*|mmcblk*[0-9]|msblk*[0-9]|mspblk*[0-9]|nvme*|sd*|sr*|vd*|xvd*|bcache*|cciss*|dasd*|ubd*|scm*|pmem*|nbd*", GOTO="persistent_storage_end"

# ignore partitions that span the entire disk
TEST=="whole_disk", GOTO="persistent_storage_end"

# for partitions import parent information
ENV{DEVTYPE}=="partition", IMPORT{parent}="ID_*"

# NVMe
KERNEL=="nvme*[0-9]n*[0-9]", ATTR{wwid}=="?*", SYMLINK+="disk/by-id/nvme-$attr{wwid}"
KERNEL=="nvme*[0-9]n*[0-9]p*[0-9]", ENV{DEVTYPE}=="partition", ATTRS{wwid}=="?*", SYMLINK+="disk/by-id/nvme-$attr{wwid}-part%n"

KERNEL=="nvme*[0-9]n*[0-9]", ENV{DEVTYPE}=="disk", ATTRS{serial}=="?*", ENV{ID_SERIAL_SHORT}="$attr{serial}"
KERNEL=="nvme*[0-9]n*[0-9]", ENV{DEVTYPE}=="disk", ATTRS{wwid}=="?*", ENV{ID_WWN}="$attr{wwid}"
KERNEL=="nvme*[0-9]n*[0-9]", ENV{DEVTYPE}=="disk", ATTRS{model}=="?*", ENV{ID_MODEL}="$attr{model}"
KERNEL=="nvme*[0-9]n*[0-9]", ENV{DEVTYPE}=="disk", ENV{ID_MODEL}=="?*", ENV{ID_SERIAL_SHORT}=="?*", \
  ENV{ID_SERIAL}="$env{ID_MODEL}_$env{ID_SERIAL_SHORT}", SYMLINK+="disk/by-id/nvme-$env{ID_SERIAL}"

KERNEL=="nvme*[0-9]n*[0-9]p*[0-9]", ENV{DEVTYPE}=="partition", ATTRS{serial}=="?*", ENV{ID_SERIAL_SHORT}="$attr{serial}"
KERNEL=="nvme*[0-9]n*[0-9]p*[0-9]", ENV{DEVTYPE}=="partition", ATTRS{model}=="?*", ENV{ID_MODEL}="$attr{model}"
KERNEL=="nvme*[0-9]n*[0-9]p*[0-9]", ENV{DEVTYPE}=="partition", ENV{ID_MODEL}=="?*", ENV{ID_SERIAL_SHORT}=="?*", \
  ENV{ID_SERIAL}="$env{ID_MODEL}_$env{ID_SERIAL_SHORT}", SYMLINK+="disk/by-id/nvme-$env{ID_SERIAL}-part%n"

# virtio-blk
KERNEL=="vd*[!0-9]", ATTRS{serial}=="?*", ENV{ID_SERIAL}="$attr{serial}", SYMLINK+="disk/by-id/virtio-$env{ID_SERIAL}"
KERNEL=="vd*[0-9]", ATTRS{serial}=="?*", ENV{ID_SERIAL}="$attr{serial}", SYMLINK+="disk/by-id/virtio-$env{ID_SERIAL}-part%n"

# ATA
KERNEL=="sd*[!0-9]|sr*", ENV{ID_SERIAL}!="?*", SUBSYSTEMS=="scsi", ATTRS{vendor}=="ATA", IMPORT{program}="ata_id --export $devnode"

# ATAPI devices (SPC-3 or later)
KERNEL=="sd*[!0-9]|sr*", ENV{ID_SERIAL}!="?*", SUBSYSTEMS=="scsi", ATTRS{type}=="5", ATTRS{scsi_level}=="[6-9]*", IMPORT{program}="ata_id --export $devnode"

# Run ata_id on non-removable USB Mass Storage (SATA/PATA disks in enclosures)
KERNEL=="sd*[!0-9]|sr*", ENV{ID_SERIAL}!="?*", ATTR{removable}=="0", SUBSYSTEMS=="usb", IMPORT{program}="ata_id --export $devnode"

# Fall back usb_id for USB devices
KERNEL=="sd*[!0-9]|sr*", ENV{ID_SERIAL}!="?*", SUBSYSTEMS=="usb", IMPORT{builtin}="usb_id"

# SCSI devices
KERNEL=="sd*[!0-9]|sr*", ENV{ID_SERIAL}!="?*", IMPORT{program}="scsi_id --export --whitelisted -d $devnode", ENV{ID_BUS}="scsi"
KERNEL=="cciss*", ENV{DEVTYPE}=="disk", ENV{ID_SERIAL}!="?*", IMPORT{program}="scsi_id --export --whitelisted -d $devnode", ENV{ID_BUS}="cciss"
KERNEL=="sd*|sr*|cciss*", ENV{DEVTYPE}=="disk", ENV{ID_SERIAL}=="?*", SYMLINK+="disk/by-id/$env{ID_BUS}-$env{ID_SERIAL}"
KERNEL=="sd*|cciss*", ENV{DEVTYPE}=="partition", ENV{ID_SERIAL}=="?*", SYMLINK+="disk/by-id/$env{ID_BUS}-$env{ID_SERIAL}-part%n"

# FireWire
KERNEL=="sd*[!0-9]|sr*", ATTRS{ieee1394_id}=="?*", SYMLINK+="disk/by-id/ieee1394-$attr{ieee1394_id}"
KERNEL=="sd*[0-9]", ATTRS{ieee1394_id}=="?*", SYMLINK+="disk/by-id/ieee1394-$attr{ieee1394_id}-part%n"

# MMC
KERNEL=="mmcblk[0-9]", SUBSYSTEMS=="mmc", ATTRS{name}=="?*", ATTRS{serial}=="?*", \
  ENV{ID_NAME}="$attr{name}", ENV{ID_SERIAL}="$attr{serial}", SYMLINK+="disk/by-id/mmc-$env{ID_NAME}_$env{ID_SERIAL}"
KERNEL=="mmcblk[0-9]p[0-9]*", ENV{ID_NAME}=="?*", ENV{ID_SERIAL}=="?*", SYMLINK+="disk/by-id/mmc-$env{ID_NAME}_$env{ID_SERIAL}-part%n"

# UBI-MTD
SUBSYSTEM=="ubi", KERNEL=="ubi*_*", ATTRS{mtd_num}=="*", SYMLINK+="ubi_mtd%s{mtd_num}_%s{name}"

# Memstick
KERNEL=="msblk[0-9]|mspblk[0-9]", SUBSYSTEMS=="memstick", ATTRS{name}=="?*", ATTRS{serial}=="?*", \
  ENV{ID_NAME}="$attr{name}", ENV{ID_SERIAL}="$attr{serial}", SYMLINK+="disk/by-id/memstick-$env{ID_NAME}_$env{ID_SERIAL}"
KERNEL=="msblk[0-9]p[0-9]|mspblk[0-9]p[0-9]", ENV{ID_NAME}=="?*", ENV{ID_SERIAL}=="?*", SYMLINK+="disk/by-id/memstick-$env{ID_NAME}_$env{ID_SERIAL}-part%n"

# by-path
ENV{DEVTYPE}=="disk", DEVPATH!="*/virtual/*", IMPORT{builtin}="path_id"
KERNEL=="mmcblk[0-9]boot[0-9]", ENV{DEVTYPE}=="disk", ENV{ID_PATH}=="?*", SYMLINK+="disk/by-path/$env{ID_PATH}-boot%n"
KERNEL!="mmcblk[0-9]boot[0-9]", ENV{DEVTYPE}=="disk", ENV{ID_PATH}=="?*", SYMLINK+="disk/by-path/$env{ID_PATH}"
ENV{DEVTYPE}=="partition", ENV{ID_PATH}=="?*", SYMLINK+="disk/by-path/$env{ID_PATH}-part%n"

# legacy virtio-pci by-path links (deprecated)
KERNEL=="vd*[!0-9]", ENV{ID_PATH}=="pci-*", SYMLINK+="disk/by-path/virtio-$env{ID_PATH}"
KERNEL=="vd*[0-9]", ENV{ID_PATH}=="pci-*", SYMLINK+="disk/by-path/virtio-$env{ID_PATH}-part%n"

# probe filesystem metadata of optical drives which have a media inserted
KERNEL=="sr*", ENV{DISK_EJECT_REQUEST}!="?*", ENV{ID_CDROM_MEDIA_TRACK_COUNT_DATA}=="?*", ENV{ID_CDROM_MEDIA_SESSION_LAST_OFFSET}=="?*", \
  IMPORT{builtin}="blkid --offset=$env{ID_CDROM_MEDIA_SESSION_LAST_OFFSET}"
# single-session CDs do not have ID_CDROM_MEDIA_SESSION_LAST_OFFSET
KERNEL=="sr*", ENV{DISK_EJECT_REQUEST}!="?*", ENV{ID_CDROM_MEDIA_TRACK_COUNT_DATA}=="?*", ENV{ID_CDROM_MEDIA_SESSION_LAST_OFFSET}=="", \
  IMPORT{builtin}="blkid --noraid"

# probe filesystem metadata of disks
KERNEL!="sr*", IMPORT{builtin}="blkid"

# by-label/by-uuid links (filesystem metadata)
ENV{ID_FS_USAGE}=="filesystem|other|crypto", ENV{ID_FS_UUID_ENC}=="?*", SYMLINK+="disk/by-uuid/$env{ID_FS_UUID_ENC}"
ENV{ID_FS_USAGE}=="filesystem|other|crypto", ENV{ID_FS_LABEL_ENC}=="?*", SYMLINK+="disk/by-label/$env{ID_FS_LABEL_ENC}"

# by-id (World Wide Name)
ENV{DEVTYPE}=="disk", ENV{ID_WWN_WITH_EXTENSION}=="?*", SYMLINK+="disk/by-id/wwn-$env{ID_WWN_WITH_EXTENSION}"
ENV{DEVTYPE}=="partition", ENV{ID_WWN_WITH_EXTENSION}=="?*", SYMLINK+="disk/by-id/wwn-$env{ID_WWN_WITH_EXTENSION}-part%n"

# by-partlabel/by-partuuid links (partition metadata)
ENV{ID_PART_ENTRY_UUID}=="?*", SYMLINK+="disk/by-partuuid/$env{ID_PART_ENTRY_UUID}"
ENV{ID_PART_ENTRY_SCHEME}=="gpt", ENV{ID_PART_ENTRY_NAME}=="?*", SYMLINK+="disk/by-partlabel/$env{ID_PART_ENTRY_NAME}"

LABEL="persistent_storage_end"
# do not edit this file, it will be overwritten on update

ACTION=="remove", GOTO="persistent_v4l_end"
SUBSYSTEM!="video4linux", GOTO="persistent_v4l_end"
ENV{MAJOR}=="", GOTO="persistent_v4l_end"

IMPORT{program}="v4l_id $devnode"

SUBSYSTEMS=="usb", IMPORT{builtin}="usb_id"
KERNEL=="video*", ENV{ID_SERIAL}=="?*", SYMLINK+="v4l/by-id/$env{ID_BUS}-$env{ID_SERIAL}-video-index$attr{index}"

# check for valid "index" number
TEST!="index", GOTO="persistent_v4l_end"
ATTR{index}!="?*", GOTO="persistent_v4l_end"

IMPORT{builtin}="path_id"
ENV{ID_PATH}=="?*", KERNEL=="video*|vbi*", SYMLINK+="v4l/by-path/$env{ID_PATH}-video-index$attr{index}"
ENV{ID_PATH}=="?*", KERNEL=="audio*", SYMLINK+="v4l/by-path/$env{ID_PATH}-audio-index$attr{index}"

LABEL="persistent_v4l_end"
# do not edit this file, it will be overwritten on update

ACTION=="remove", GOTO="sensor_end"

# device matching the sensor's name and the machine's DMI data for IIO devices
SUBSYSTEM=="iio", KERNEL=="iio*", SUBSYSTEMS=="usb|i2c", \
  IMPORT{builtin}="hwdb 'sensor:modalias:$attr{modalias}:$attr{[dmi/id]modalias}'", \
  GOTO="sensor_end"

SUBSYSTEM=="input", ENV{ID_INPUT_ACCELEROMETER}=="1", SUBSYSTEMS=="acpi", \
  IMPORT{builtin}="hwdb 'sensor:modalias:acpi:$attr{hid}:$attr{[dmi/id]modalias}'", \
  GOTO="sensor_end"

SUBSYSTEM=="input", ENV{ID_INPUT_ACCELEROMETER}=="1", SUBSYSTEMS=="platform", \
  IMPORT{builtin}="hwdb 'sensor:modalias:platform:$id:$attr{[dmi/id]modalias}'", \
  GOTO="sensor_end"

LABEL="sensor_end"
# do not edit this file, it will be overwritten on update

ACTION=="remove", GOTO="serial_end"
SUBSYSTEM!="tty", GOTO="serial_end"

SUBSYSTEMS=="pci", ENV{ID_BUS}="pci", ENV{ID_VENDOR_ID}="$attr{vendor}", ENV{ID_MODEL_ID}="$attr{device}"
SUBSYSTEMS=="pci", IMPORT{builtin}="hwdb --subsystem=pci"
SUBSYSTEMS=="usb", IMPORT{builtin}="usb_id", IMPORT{builtin}="hwdb --subsystem=usb"

# /dev/serial/by-path/, /dev/serial/by-id/ for USB devices
KERNEL!="ttyUSB[0-9]*|ttyACM[0-9]*", GOTO="serial_end"

SUBSYSTEMS=="usb-serial", ENV{.ID_PORT}="$attr{port_number}"

IMPORT{builtin}="path_id"
ENV{ID_PATH}=="?*", ENV{.ID_PORT}=="", SYMLINK+="serial/by-path/$env{ID_PATH}"
ENV{ID_PATH}=="?*", ENV{.ID_PORT}=="?*", SYMLINK+="serial/by-path/$env{ID_PATH}-port$env{.ID_PORT}"

IMPORT{builtin}="usb_id"
ENV{ID_SERIAL}=="", GOTO="serial_end"
SUBSYSTEMS=="usb", ENV{ID_USB_INTERFACE_NUM}="$attr{bInterfaceNumber}"
ENV{ID_USB_INTERFACE_NUM}=="", GOTO="serial_end"
ENV{.ID_PORT}=="", SYMLINK+="serial/by-id/$env{ID_BUS}-$env{ID_SERIAL}-if$env{ID_USB_INTERFACE_NUM}"
ENV{.ID_PORT}=="?*", SYMLINK+="serial/by-id/$env{ID_BUS}-$env{ID_SERIAL}-if$env{ID_USB_INTERFACE_NUM}-port$env{.ID_PORT}"

LABEL="serial_end"
# do not edit this file, it will be overwritten on update

SUBSYSTEM!="block", GOTO="btrfs_end"
ACTION=="remove", GOTO="btrfs_end"
ENV{ID_FS_TYPE}!="btrfs", GOTO="btrfs_end"
ENV{SYSTEMD_READY}=="0", GOTO="btrfs_end"

# let the kernel know about this btrfs filesystem, and check if it is complete
IMPORT{builtin}="btrfs ready $devnode"

# mark the device as not ready to be used by the system
ENV{ID_BTRFS_READY}=="0", ENV{SYSTEMD_READY}="0"

# reconsider pending devices in case when multidevice volume awaits
ENV{ID_BTRFS_READY}=="1", RUN+="/usr/bin/udevadm trigger -s block -p ID_BTRFS_READY=0"

LABEL="btrfs_end"
# do not edit this file, it will be overwritten on update

ACTION=="remove", GOTO="joystick_end"
ENV{ID_INPUT_JOYSTICK}=="", GOTO="joystick_end"
KERNEL!="event*", GOTO="joystick_end"

# joystick:<bustype>:v<vid>p<pid>:name:<name>:*
KERNELS=="input*", ENV{ID_BUS}!="", \
        IMPORT{builtin}="hwdb 'joystick:$env{ID_BUS}:v$attr{id/vendor}p$attr{id/product}:name:$attr{name}:'", \
        GOTO="joystick_end"

LABEL="joystick_end"
# do not edit this file, it will be overwritten on update

ACTION=="remove", GOTO="mouse_end"
KERNEL!="event*", GOTO="mouse_end"
ENV{ID_INPUT_MOUSE}=="", GOTO="mouse_end"

# mouse:<subsystem>:v<vid>p<pid>:name:<name>:*
KERNELS=="input*", ENV{ID_BUS}=="usb", \
        IMPORT{builtin}="hwdb 'mouse:$env{ID_BUS}:v$attr{id/vendor}p$attr{id/product}:name:$attr{name}:'", \
        GOTO="mouse_end"
KERNELS=="input*", ENV{ID_BUS}=="bluetooth", \
        IMPORT{builtin}="hwdb 'mouse:$env{ID_BUS}:v$attr{id/vendor}p$attr{id/product}:name:$attr{name}:'", \
        GOTO="mouse_end"
DRIVERS=="psmouse", SUBSYSTEMS=="serio", \
        IMPORT{builtin}="hwdb 'mouse:ps2::name:$attr{device/name}:'", \
        GOTO="mouse_end"

LABEL="mouse_end"
#  SPDX-License-Identifier: LGPL-2.1+
#
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.

ACTION=="remove", GOTO="power_switch_end"

SUBSYSTEM=="input", KERNEL=="event*", ENV{ID_INPUT_SWITCH}=="1", TAG+="power-switch"
SUBSYSTEM=="input", KERNEL=="event*", ENV{ID_INPUT_KEY}=="1", TAG+="power-switch"

LABEL="power_switch_end"
# do not edit this file, it will be overwritten on update

ACTION=="remove", GOTO="touchpad_end"
ENV{ID_INPUT}=="", GOTO="touchpad_end"
ENV{ID_INPUT_TOUCHPAD}=="", GOTO="touchpad_end"
KERNEL!="event*", GOTO="touchpad_end"

# touchpad:<subsystem>:v<vid>p<pid>:name:<name>:*
KERNELS=="input*", ENV{ID_BUS}!="", \
        IMPORT{builtin}="hwdb 'touchpad:$env{ID_BUS}:v$attr{id/vendor}p$attr{id/product}:name:$attr{name}:'", \
        GOTO="touchpad_end"

LABEL="touchpad_end"
#  SPDX-License-Identifier: LGPL-2.1+
#
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.

ACTION=="remove", GOTO="uaccess_end"
ENV{MAJOR}=="", GOTO="uaccess_end"

# PTP/MTP protocol devices, cameras, portable media players
SUBSYSTEM=="usb", ENV{ID_USB_INTERFACES}=="*:060101:*", TAG+="uaccess"

# Digicams with proprietary protocol
ENV{ID_GPHOTO2}=="?*", TAG+="uaccess"

# SCSI and USB scanners
ENV{libsane_matched}=="yes", TAG+="uaccess"

# HPLIP devices (necessary for ink level check and HP tool maintenance)
ENV{ID_HPLIP}=="1", TAG+="uaccess"

# optical drives
SUBSYSTEM=="block", ENV{ID_CDROM}=="1", TAG+="uaccess"
SUBSYSTEM=="scsi_generic", SUBSYSTEMS=="scsi", ATTRS{type}=="4|5", TAG+="uaccess"

# Sound devices
SUBSYSTEM=="sound", TAG+="uaccess", \
  OPTIONS+="static_node=snd/timer", OPTIONS+="static_node=snd/seq"

# ffado is an userspace driver for firewire sound cards
SUBSYSTEM=="firewire", ENV{ID_FFADO}=="1", TAG+="uaccess"

# Webcams, frame grabber, TV cards
SUBSYSTEM=="video4linux", TAG+="uaccess"
SUBSYSTEM=="dvb", TAG+="uaccess"

# IIDC devices: industrial cameras and some webcams
SUBSYSTEM=="firewire", ATTR{units}=="*0x00a02d:0x00010*",  TAG+="uaccess"
SUBSYSTEM=="firewire", ATTR{units}=="*0x00b09d:0x00010*",  TAG+="uaccess"
# AV/C devices: camcorders, set-top boxes, TV sets, audio devices, and more
SUBSYSTEM=="firewire", ATTR{units}=="*0x00a02d:0x010001*", TAG+="uaccess"
SUBSYSTEM=="firewire", ATTR{units}=="*0x00a02d:0x014001*", TAG+="uaccess"

# DRI video devices
SUBSYSTEM=="drm", KERNEL=="card*", TAG+="uaccess"

# smart-card readers
ENV{ID_SMARTCARD_READER}=="?*", TAG+="uaccess"

# (USB) authentication devices
ENV{ID_SECURITY_TOKEN}=="?*", TAG+="uaccess"

# PDA devices
ENV{ID_PDA}=="?*", TAG+="uaccess"

# Programmable remote control
ENV{ID_REMOTE_CONTROL}=="1", TAG+="uaccess"

# joysticks
SUBSYSTEM=="input", ENV{ID_INPUT_JOYSTICK}=="?*", TAG+="uaccess"

# color measurement devices
ENV{COLOR_MEASUREMENT_DEVICE}=="?*", TAG+="uaccess"

# DDC/CI device, usually high-end monitors such as the DreamColor
ENV{DDC_DEVICE}=="?*", TAG+="uaccess"

# media player raw devices (for user-mode drivers, Android SDK, etc.)
SUBSYSTEM=="usb", ENV{ID_MEDIA_PLAYER}=="?*", TAG+="uaccess"

# software-defined radio communication devices
ENV{ID_SOFTWARE_RADIO}=="?*", TAG+="uaccess"

# 3D printers, CNC machines, laser cutters, 3D scanners, etc.
ENV{ID_MAKER_TOOL}=="?*", TAG+="uaccess"

LABEL="uaccess_end"
#  SPDX-License-Identifier: LGPL-2.1+
#
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.

ACTION=="remove", GOTO="seat_end"

TAG=="uaccess", SUBSYSTEM!="sound", TAG+="seat"
SUBSYSTEM=="sound", KERNEL=="card*", TAG+="seat"
SUBSYSTEM=="input", KERNEL=="input*", TAG+="seat"
SUBSYSTEM=="graphics", KERNEL=="fb[0-9]*", TAG+="seat", TAG+="master-of-seat"
SUBSYSTEM=="drm", KERNEL=="card[0-9]*", TAG+="seat", TAG+="master-of-seat"
SUBSYSTEM=="usb", ATTR{bDeviceClass}=="09", TAG+="seat"

# 'Plugable' USB hub, sound, network, graphics adapter
SUBSYSTEM=="usb", ATTR{idVendor}=="2230", ATTR{idProduct}=="000[13]", ENV{ID_AUTOSEAT}="1"

# qemu (version 2.4+) has a PCI-PCI bridge (-device pci-bridge-seat) to group
# devices belonging to one seat. See:
#     http://git.qemu.org/?p=qemu.git;a=blob;f=docs/multiseat.txt
SUBSYSTEM=="pci", ATTR{vendor}=="0x1b36", ATTR{device}=="0x000a", TAG+="seat", ENV{ID_AUTOSEAT}="1"

# Mimo 720, with integrated USB hub, displaylink graphics, and e2i
# touchscreen. This device carries no proper VID/PID in the USB hub,
# but it does carry good ID data in the graphics component, hence we
# check it from the parent. There's a bit of a race here however,
# given that the child devices might not exist yet at the time this
# rule is executed. To work around this we'll trigger the parent from
# the child if we notice that the parent wasn't recognized yet.

# Match parent
SUBSYSTEM=="usb", ATTR{idVendor}=="058f", ATTR{idProduct}=="6254", \
                  ATTR{%k.2/idVendor}=="17e9", ATTR{%k.2/idProduct}=="401a", ATTR{%k.2/product}=="mimo inc", \
                  ENV{ID_AUTOSEAT}="1", ENV{ID_AVOID_LOOP}="1"

# Match child, look for parent's ID_AVOID_LOOP
SUBSYSTEM=="usb", ATTR{idVendor}=="17e9", ATTR{idProduct}=="401a", ATTR{product}=="mimo inc", \
                  ATTR{../idVendor}=="058f", ATTR{../idProduct}=="6254", \
                  IMPORT{parent}="ID_AVOID_LOOP"

# Match child, retrigger parent
SUBSYSTEM=="usb", ATTR{idVendor}=="17e9", ATTR{idProduct}=="401a", ATTR{product}=="mimo inc", \
                  ATTR{../idVendor}=="058f", ATTR{../idProduct}=="6254", \
                  ENV{ID_AVOID_LOOP}=="", \
                  RUN+="/usr/bin/udevadm trigger --parent-match=%p/.."

TAG=="seat", ENV{ID_PATH}=="", IMPORT{builtin}="path_id"
TAG=="seat", ENV{ID_FOR_SEAT}=="", ENV{ID_PATH_TAG}!="", ENV{ID_FOR_SEAT}="$env{SUBSYSTEM}-$env{ID_PATH_TAG}"

SUBSYSTEM=="input", ATTR{name}=="Wiebetech LLC Wiebetech", RUN+="/usr/bin/loginctl lock-sessions"

LABEL="seat_end"
# do not edit this file, it will be overwritten on update

# On Dell PowerEdge systems, the iDRAC7 and later support a USB Virtual NIC
# with terminates in the iDRAC. Help identify this with 'idrac'

ACTION=="add", SUBSYSTEM=="net", SUBSYSTEMS=="usb", ATTRS{idVendor}=="413c", ATTRS{idProduct}=="a102", NAME="idrac"
#  SPDX-License-Identifier: LGPL-2.1+
#
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.

ACTION=="remove", GOTO="seat_late_end"

ENV{ID_SEAT}=="", ENV{ID_AUTOSEAT}=="1", ENV{ID_FOR_SEAT}!="", ENV{ID_SEAT}="seat-$env{ID_FOR_SEAT}"
ENV{ID_SEAT}=="", IMPORT{parent}="ID_SEAT"

ENV{ID_SEAT}!="", TAG+="$env{ID_SEAT}"

TAG=="uaccess", ENV{MAJOR}!="", RUN{builtin}+="uaccess"

LABEL="seat_late_end"
# do not edit this file, it will be overwritten on update

ACTION=="remove", GOTO="net_end"
SUBSYSTEM!="net", GOTO="net_end"

IMPORT{builtin}="net_id"

SUBSYSTEMS=="usb", IMPORT{builtin}="usb_id", IMPORT{builtin}="hwdb --subsystem=usb"
SUBSYSTEMS=="usb", GOTO="net_end"

SUBSYSTEMS=="pci", ENV{ID_BUS}="pci", ENV{ID_VENDOR_ID}="$attr{vendor}", ENV{ID_MODEL_ID}="$attr{device}"
SUBSYSTEMS=="pci", IMPORT{builtin}="hwdb --subsystem=pci"

LABEL="net_end"
# do not edit this file, it will be overwritten on update

ACTION!="add", GOTO="mtd_probe_end"

KERNEL=="mtd*ro", IMPORT{program}="mtd_probe $devnode"

LABEL="mtd_probe_end"
# do not edit this file, it will be overwritten on update

SUBSYSTEM!="sound", GOTO="sound_end"

ACTION=="add|change", KERNEL=="controlC*", ATTR{../uevent}="change"
ACTION!="change", GOTO="sound_end"

# Ok, we probably need a little explanation here for what the two lines above
# are good for.
#
# The story goes like this: when ALSA registers a new sound card it emits a
# series of 'add' events to userspace, for the main card device and for all the
# child device nodes that belong to it. udev relays those to applications,
# however only maintains the order between father and child, but not between
# the siblings. The control device node creation can be used as synchronization
# point. All other devices that belong to a card are created in the kernel
# before it. However unfortunately due to the fact that siblings are forwarded
# out of order by udev this fact is lost to applications.
#
# OTOH before an application can open a device it needs to make sure that all
# its device nodes are completely created and set up.
#
# As a workaround for this issue we have added the udev rule above which will
# generate a 'change' event on the main card device from the 'add' event of the
# card's control device. Due to the ordering semantics of udev this event will
# only be relayed after all child devices have finished processing properly.
# When an application needs to listen for appearing devices it can hence look
# for 'change' events only, and ignore the actual 'add' events.
#
# When the application is initialized at the same time as a device is plugged
# in it may need to figure out if the 'change' event has already been triggered
# or not for a card. To find that out we store the flag environment variable
# SOUND_INITIALIZED on the device which simply tells us if the card 'change'
# event has already been processed.

KERNEL!="card*", GOTO="sound_end"

ENV{SOUND_INITIALIZED}="1"

IMPORT{builtin}="hwdb"
SUBSYSTEMS=="usb", IMPORT{builtin}="usb_id"
SUBSYSTEMS=="usb", GOTO="skip_pci"

SUBSYSTEMS=="firewire", ATTRS{guid}=="?*", \
  ENV{ID_BUS}="firewire", ENV{ID_SERIAL}="$attr{guid}", ENV{ID_SERIAL_SHORT}="$attr{guid}", \
  ENV{ID_VENDOR_ID}="$attr{vendor}", ENV{ID_MODEL_ID}="$attr{model}", \
  ENV{ID_VENDOR}="$attr{vendor_name}", ENV{ID_MODEL}="$attr{model_name}"
SUBSYSTEMS=="firewire", GOTO="skip_pci"

SUBSYSTEMS=="pci", ENV{ID_BUS}="pci", ENV{ID_VENDOR_ID}="$attr{vendor}", ENV{ID_MODEL_ID}="$attr{device}"
SUBSYSTEMS=="pci", GOTO="skip_pci"

# If we reach here, the device nor any of its parents are USB/PCI/firewire bus devices.
# If we now find a parent that is a platform device, assume that we're working with
# an internal sound card.
SUBSYSTEMS=="platform", ENV{SOUND_FORM_FACTOR}="internal", GOTO="sound_end"

LABEL="skip_pci"

# Define ID_ID if ID_BUS and ID_SERIAL are set. This will work for both
# USB and firewire.
ENV{ID_SERIAL}=="?*", ENV{ID_USB_INTERFACE_NUM}=="?*", ENV{ID_ID}="$env{ID_BUS}-$env{ID_SERIAL}-$env{ID_USB_INTERFACE_NUM}"
ENV{ID_SERIAL}=="?*", ENV{ID_USB_INTERFACE_NUM}=="", ENV{ID_ID}="$env{ID_BUS}-$env{ID_SERIAL}"

IMPORT{builtin}="path_id"

# The values used here for $SOUND_FORM_FACTOR and $SOUND_CLASS should be kept
# in sync with those defined for PulseAudio's src/pulse/proplist.h
# PA_PROP_DEVICE_FORM_FACTOR, PA_PROP_DEVICE_CLASS properties.

# If the first PCM device of this card has the pcm class 'modem', then the card is a modem
ATTR{pcmC%nD0p/pcm_class}=="modem", ENV{SOUND_CLASS}="modem", GOTO="sound_end"

# Identify cards on the internal PCI bus as internal
SUBSYSTEMS=="pci", DEVPATH=="*/0000:00:??.?/sound/*", ENV{SOUND_FORM_FACTOR}="internal", GOTO="sound_end"

# Devices that also support Image/Video interfaces are most likely webcams
SUBSYSTEMS=="usb", ENV{ID_USB_INTERFACES}=="*:0e????:*", ENV{SOUND_FORM_FACTOR}="webcam", GOTO="sound_end"

# Matching on the model strings is a bit ugly, I admit
ENV{ID_MODEL}=="*[Ss]peaker*", ENV{SOUND_FORM_FACTOR}="speaker", GOTO="sound_end"
ENV{ID_MODEL_FROM_DATABASE}=="*[Ss]peaker*", ENV{SOUND_FORM_FACTOR}="speaker", GOTO="sound_end"

ENV{ID_MODEL}=="*[Hh]eadphone*", ENV{SOUND_FORM_FACTOR}="headphone", GOTO="sound_end"
ENV{ID_MODEL_FROM_DATABASE}=="*[Hh]eadphone*", ENV{SOUND_FORM_FACTOR}="headphone", GOTO="sound_end"

ENV{ID_MODEL}=="*[Hh]eadset*", ENV{SOUND_FORM_FACTOR}="headset", GOTO="sound_end"
ENV{ID_MODEL_FROM_DATABASE}=="*[Hh]eadset*", ENV{SOUND_FORM_FACTOR}="headset", GOTO="sound_end"

ENV{ID_MODEL}=="*[Hh]andset*", ENV{SOUND_FORM_FACTOR}="handset", GOTO="sound_end"
ENV{ID_MODEL_FROM_DATABASE}=="*[Hh]andset*", ENV{SOUND_FORM_FACTOR}="handset", GOTO="sound_end"

ENV{ID_MODEL}=="*[Mm]icrophone*", ENV{SOUND_FORM_FACTOR}="microphone", GOTO="sound_end"
ENV{ID_MODEL_FROM_DATABASE}=="*[Mm]icrophone*", ENV{SOUND_FORM_FACTOR}="microphone", GOTO="sound_end"

LABEL="sound_end"
# do not edit this file, it will be overwritten on update

ACTION!="add", GOTO="drivers_end"

ENV{MODALIAS}=="?*", RUN{builtin}+="kmod load $env{MODALIAS}"
SUBSYSTEM=="tifm", ENV{TIFM_CARD_TYPE}=="SD", RUN{builtin}+="kmod load tifm_sd"
SUBSYSTEM=="tifm", ENV{TIFM_CARD_TYPE}=="MS", RUN{builtin}+="kmod load tifm_ms"
SUBSYSTEM=="memstick", RUN{builtin}+="kmod load ms_block mspro_block"
SUBSYSTEM=="i2o", RUN{builtin}+="kmod load i2o_block"
SUBSYSTEM=="module", KERNEL=="parport_pc", RUN{builtin}+="kmod load ppdev"
KERNEL=="mtd*ro", ENV{MTD_FTL}=="smartmedia", RUN{builtin}+="kmod load sm_ftl"

LABEL="drivers_end"
# do not edit this file, it will be overwritten on update

SUBSYSTEM!="net", GOTO="net_setup_link_end"

IMPORT{builtin}="path_id"

ACTION!="add", GOTO="net_setup_link_end"

IMPORT{builtin}="net_setup_link"

NAME=="", ENV{ID_NET_NAME}!="", NAME="$env{ID_NET_NAME}"

LABEL="net_setup_link_end"
#  SPDX-License-Identifier: LGPL-2.1+
#
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.

# Each vtcon keeps its own state of fonts.
#
ACTION=="add", SUBSYSTEM=="vtconsole", KERNEL=="vtcon*", ATTR{name}!="*dummy device", RUN+="/usr/lib/systemd/systemd-vconsole-setup"
#  SPDX-License-Identifier: LGPL-2.1+
#
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.

ACTION=="remove", GOTO="systemd_end"

SUBSYSTEM=="tty", KERNEL=="tty[a-zA-Z]*|hvc*|xvc*|hvsi*|ttysclp*|sclp_line*|3270/tty[0-9]*", TAG+="systemd"
KERNEL=="vport*", TAG+="systemd"

SUBSYSTEM=="ubi", TAG+="systemd"

SUBSYSTEM=="block", TAG+="systemd"
SUBSYSTEM=="block", ACTION=="add", ENV{DM_UDEV_DISABLE_OTHER_RULES_FLAG}=="1", ENV{SYSTEMD_READY}="0"

# Ignore encrypted devices with no identified superblock on it, since
# we are probably still calling mke2fs or mkswap on it.
SUBSYSTEM=="block", ENV{DM_UUID}=="CRYPT-*", ENV{ID_PART_TABLE_TYPE}=="", ENV{ID_FS_USAGE}=="", ENV{SYSTEMD_READY}="0"

# add symlink to GPT root disk
SUBSYSTEM=="block", ENV{ID_PART_GPT_AUTO_ROOT}=="1", ENV{ID_FS_TYPE}!="crypto_LUKS", SYMLINK+="gpt-auto-root"
SUBSYSTEM=="block", ENV{ID_PART_GPT_AUTO_ROOT}=="1", ENV{ID_FS_TYPE}=="crypto_LUKS", SYMLINK+="gpt-auto-root-luks"
SUBSYSTEM=="block", ENV{DM_UUID}=="CRYPT-*", ENV{DM_NAME}=="root", SYMLINK+="gpt-auto-root"

# Ignore raid devices that are not yet assembled and started
SUBSYSTEM=="block", ENV{DEVTYPE}=="disk", KERNEL=="md*", TEST!="md/array_state", ENV{SYSTEMD_READY}="0"
SUBSYSTEM=="block", ENV{DEVTYPE}=="disk", KERNEL=="md*", ATTR{md/array_state}=="|clear|inactive", ENV{SYSTEMD_READY}="0"

# Ignore loop devices that don't have any file attached
SUBSYSTEM=="block", KERNEL=="loop[0-9]*", ENV{DEVTYPE}=="disk", TEST!="loop/backing_file", ENV{SYSTEMD_READY}="0"

# Ignore nbd devices until the PID file exists (which signals a connected device)
SUBSYSTEM=="block", KERNEL=="nbd*", ENV{DEVTYPE}=="disk", TEST!="pid", ENV{SYSTEMD_READY}="0"

# We need a hardware independent way to identify network devices. We
# use the /sys/subsystem/ path for this. Kernel "bus" and "class" names
# should be treated as one namespace, like udev handles it. This is mostly
# just an identification string for systemd, so whether the path actually is
# accessible or not does not matter as long as it is unique and in the
# filesystem namespace.
#
# http://cgit.freedesktop.org/systemd/systemd/tree/src/libudev/libudev-enumerate.c#n955

SUBSYSTEM=="net", KERNEL!="lo", TAG+="systemd", ENV{SYSTEMD_ALIAS}+="/sys/subsystem/net/devices/$name"
SUBSYSTEM=="bluetooth", TAG+="systemd", ENV{SYSTEMD_ALIAS}+="/sys/subsystem/bluetooth/devices/%k"

SUBSYSTEM=="bluetooth", TAG+="systemd", ENV{SYSTEMD_WANTS}+="bluetooth.target"
ENV{ID_SMARTCARD_READER}=="?*", TAG+="systemd", ENV{SYSTEMD_WANTS}+="smartcard.target"
SUBSYSTEM=="sound", KERNEL=="card*", TAG+="systemd", ENV{SYSTEMD_WANTS}+="sound.target"

SUBSYSTEM=="printer", TAG+="systemd", ENV{SYSTEMD_WANTS}+="printer.target"
SUBSYSTEM=="usb", KERNEL=="lp*", TAG+="systemd", ENV{SYSTEMD_WANTS}+="printer.target"
SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ENV{ID_USB_INTERFACES}=="*:0701??:*", TAG+="systemd", ENV{SYSTEMD_WANTS}+="printer.target"

# Apply sysctl variables to network devices (and only to those) as they appear.
ACTION=="add", SUBSYSTEM=="net", KERNEL!="lo", RUN+="/usr/lib/systemd/systemd-sysctl --prefix=/net/ipv4/conf/$name --prefix=/net/ipv4/neigh/$name --prefix=/net/ipv6/conf/$name --prefix=/net/ipv6/neigh/$name"

# Pull in backlight save/restore for all backlight devices and
# keyboard backlights
SUBSYSTEM=="backlight", TAG+="systemd", IMPORT{builtin}="path_id", ENV{SYSTEMD_WANTS}+="systemd-backlight@backlight:$name.service"
SUBSYSTEM=="leds", KERNEL=="*kbd_backlight", TAG+="systemd", IMPORT{builtin}="path_id", ENV{SYSTEMD_WANTS}+="systemd-backlight@leds:$name.service"

# Pull in rfkill save/restore for all rfkill devices
SUBSYSTEM=="rfkill", ENV{SYSTEMD_RFKILL}="1"
SUBSYSTEM=="rfkill", IMPORT{builtin}="path_id"
SUBSYSTEM=="misc", KERNEL=="rfkill", TAG+="systemd", ENV{SYSTEMD_WANTS}+="systemd-rfkill.socket"

# Asynchronously mount file systems implemented by these modules as soon as they are loaded.
SUBSYSTEM=="module", KERNEL=="fuse", TAG+="systemd", ENV{SYSTEMD_WANTS}+="sys-fs-fuse-connections.mount"
SUBSYSTEM=="module", KERNEL=="configfs", TAG+="systemd", ENV{SYSTEMD_WANTS}+="sys-kernel-config.mount"

LABEL="systemd_end"

```



---

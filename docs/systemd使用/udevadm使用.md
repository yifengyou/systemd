<!-- MDTOC maxdepth:6 firsth1:1 numbering:0 flatten:0 bullets:1 updateOnSave:1 -->

- [udevadm使用](#udevadm使用)   
   - [info 用例](#info-用例)   
   - [settle用例](#settle用例)   
   - [control用例](#control用例)   
   - [control monitor用例](#control-monitor用例)   
   - [test用例](#test用例)   
   - [trigger用例](#trigger用例)   

<!-- /MDTOC -->
# udevadm使用

udevadm 是一个用来管理 udev 守护进程的工具，它可以控制 udev 的运行时行为，请求内核事件，管理事件队列，提供简单的调试机制等1。

使用 udevadm 的基本步骤如下：

- 首先，确定要执行的命令和选项，例如 info，trigger，settle，control，monitor 或 test。
- 然后，根据命令的不同，指定一些参数，例如设备名称，设备路径，属性过滤器，事件类型等。
- 最后，查看命令的输出或执行结果，或者使用其他工具来分析或处理输出。

## info 用例


* expected an absolute path in /dev/ or /sys or a unit name

```
udevadm info [OPTIONS] [DEVPATH|FILE]

Query sysfs or the udev database.

  -h --help                   Print this message
  -V --version                Print version of the program
  -q --query=TYPE             Query device information:
       name                     Name of device node
       symlink                  Pointing to node
       path                     sysfs device path
       property                 The device properties
       all                      All values
       指定查询类型，可以是name, path, symlink, property, all等
  -p --path=SYSPATH           sysfs device path used for query or attribute walk
                              查询设备节点或符号链接的信息，例如/dev/sda
  -n --name=NAME              Node or symlink name used for query or attribute walk
                              查询设备路径的信息，例如/block/sda
  -r --root                   Prepend dev directory to path names
  -a --attribute-walk         Print all key matches walking along the chain
                              of parent devices 打印设备和其所有父设备的所有属性，用于编写udev规则
  -d --device-id-of-file=FILE Print major:minor of device containing this file
  -x --export                 Export key/value pairs 以键值对的形式输出设备信息
  -P --export-prefix          Export the key name with a prefix
  -e --export-db              Export the content of the udev database
  -c --cleanup-db             Clean up the udev database
  -w --wait-for-initialization[=SECONDS]
                              Wait for device to be initialized
```

如果要查看一个设备的所有属性信息，可以使用以下命令：

```
# udevadm info /dev/vda
P: /devices/pci0000:00/0000:00:01.3/0000:04:00.0/virtio2/block/vda
N: vda
L: 0
S: disk/by-path/virtio-pci-0000:04:00.0
S: disk/by-path/pci-0000:04:00.0
E: DEVPATH=/devices/pci0000:00/0000:00:01.3/0000:04:00.0/virtio2/block/vda
E: DEVNAME=/dev/vda
E: DEVTYPE=disk
E: MAJOR=253
E: MINOR=0
E: SUBSYSTEM=block
E: USEC_INITIALIZED=4280474
E: ID_PATH=pci-0000:04:00.0
E: ID_PATH_TAG=pci-0000_04_00_0
E: ID_PART_TABLE_UUID=406c278b
E: ID_PART_TABLE_TYPE=dos
E: DEVLINKS=/dev/disk/by-path/virtio-pci-0000:04:00.0 /dev/disk/by-path/pci-0000:04:00.0
E: TAGS=:systemd:


# udevadm info -a -p /sys/block/vda

Udevadm info starts with the device specified by the devpath and then
walks up the chain of parent devices. It prints for every device
found, all possible attributes in the udev rules key format.
A rule to match, can be composed by the attributes of the device
and the attributes from one single parent device.

  looking at device '/devices/pci0000:00/0000:00:01.3/0000:04:00.0/virtio2/block/vda':
    KERNEL=="vda"
    SUBSYSTEM=="block"
    DRIVER==""
    ATTR{serial}==""
    ATTR{size}=="209715200"
    ATTR{ext_range}=="256"
    ATTR{stat}=="   26526      387  1039963     9425   101957    25640  2256479   472055        0   294878   427306        0        0        0        0"
    ATTR{discard_alignment}=="0"
    ATTR{capability}=="50"
    ATTR{removable}=="0"
    ATTR{cache_type}=="write back"
    ATTR{range}=="16"
    ATTR{inflight}=="       0        0"
    ATTR{alignment_offset}=="0"
    ATTR{ro}=="0"
    ATTR{hidden}=="0"
...
```

其中，-a 选项表示打印所有的 sysfs 属性，-p 选项表示指定设备路径。如果是网卡设备，怎么知道路径？

```
# find /sys -name enp1s0
# udevadm info -a -p /sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0/virtio0/net/enp1s0

Udevadm info starts with the device specified by the devpath and then
walks up the chain of parent devices. It prints for every device
found, all possible attributes in the udev rules key format.
A rule to match, can be composed by the attributes of the device
and the attributes from one single parent device.

  looking at device '/devices/pci0000:00/0000:00:01.0/0000:01:00.0/virtio0/net/enp1s0':
    KERNEL=="enp1s0"
    SUBSYSTEM=="net"
    DRIVER==""
    ATTR{flags}=="0x1003"
    ATTR{address}=="52:54:00:7c:15:0d"
    ATTR{ifindex}=="3"
    ATTR{operstate}=="up"
    ATTR{proto_down}=="0"
    ATTR{iflink}=="3"
    ATTR{mtu}=="1500"
    ATTR{dev_port}=="0"
    ATTR{dormant}=="0"
    ATTR{link_mode}=="0"
    ATTR{name_assign_type}=="4"
    ATTR{dev_id}=="0x0"
    ATTR{tx_queue_len}=="1000"
    ATTR{duplex}=="unknown"
    ATTR{carrier_down_count}=="1"
    ATTR{carrier_changes}=="2"
    ATTR{carrier_up_count}=="1"
    ATTR{speed}=="-1"
    ATTR{broadcast}=="ff:ff:ff:ff:ff:ff"
    ATTR{ifalias}==""
    ATTR{type}=="1"
    ATTR{netdev_group}=="0"
    ATTR{carrier}=="1"
    ATTR{gro_flush_timeout}=="0"
    ATTR{addr_len}=="6"
    ATTR{addr_assign_type}=="0"
```

udevadm info命令用于查询设备的属性和层次结构。它可以接受一个设备节点或一个符号链接作为参数，也可以接受一个设备路径。它会从指定的设备开始，沿着父设备链向上遍历，打印出每个设备的所有可能的属性，用于编写udev规则1。

输出内容中，开头的P、N、E、S分别表示：
```
P: 设备路径（devpath），是设备在/sys目录下的相对路径。
N: 设备节点（devname），是设备在/dev目录下的名称。
E: 设备属性（env），是设备的一些特征值，如厂商、型号、序列号、大小等。
S: 软连接设备（soft），代表该设备的软连接
```

每个字段的意义如下：

```
KERNEL: 设备节点的内核名称。
SUBSYSTEM: 设备所属的子系统名称。
DRIVER: 设备使用的驱动名称。
ATTR: 设备或其父设备的属性值，可以用于匹配规则。
KERNELS, SUBSYSTEMS, DRIVERS, ATTRS: 设备的父设备的内核名称、子系统名称、驱动名称和属性值，用于匹配规则时区分同名的属性。
```


## settle用例

如果要等待所有的事件处理完成，可以使用以下命令：
```
udevadm settle
```

这个命令没有参数。

## control用例

如果要修改 udev 守护进程的规则或参数，可以使用以下命令：

```
udevadm control --reload
```
其中，--reload 选项表示重新加载规则文件。

## control monitor用例

如果要监视设备的内核和用户空间事件，可以使用以下命令：
```
udevadm monitor --kernel --property
```
其中，--kernel 选项表示打印内核事件，--property 选项表示打印用户空间事件。

## test用例

如果要测试一个设备的规则匹配和执行过程，可以使用以下命令：

```
udevadm test $(udevadm info -q path -n /dev/sda)
```

其中，$(udevadm info -q path -n /dev/sda) 表示获取设备路径。

```
# udevadm info -q path -n /dev/vda
/devices/pci0000:00/0000:00:08.0/virtio2/block/vda
```

## trigger用例

如果要触发一个设备的添加事件，可以使用以下命令：

```
udevadm trigger --action=add --subsystem-match=block
```
其中，--action=add 选项表示指定事件类型为添加，--subsystem-match=block 选项表示指定子系统类型为块设备。










---

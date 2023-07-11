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

* udevadm settle 是一个用于等待 udevd 处理所有硬件设备的设备创建事件的命令，从而确保所有设备节点都已成功创建，然后再继续。
* 它通常用于在启动脚本中，以避免在 udev 还没有完成设备节点的创建时就执行一些依赖于设备节点的操作。它也可以用于在执行 udevadm trigger 后等待所有的 coldplug 事件处理完毕。

udevadm settle 的一般用法是：
```
udevadm settle [options]
```
其中 options 可以是：
```
-t, --timeout=seconds 设置等待的最大时间，如果超过这个时间，命令就会退出。默认值是 120 秒。
-E, --exit-if-exists=file 如果指定的文件存在，命令就会立即退出，不再等待。
-h, --help 显示帮助信息并退出。
```

udevadm settle 是通过监听 udev 事件队列来确保所有事件都已经执行的。它会在事件队列为空时退出，或者在超过指定的超时时间时退出。它不一定能保证所有的硬件设备都已经被发现，因为**内核是异步地进行硬件检测的，而且某些设备可能需要很长时间才能准备好，或者可能在任何时候被插入或移除**。所以，使用这个命令并不推荐，而应该让服务订阅 udev 事件并对新发现的设备做出相应的反应。

* udevadm settle 常用于系统启动过程中的一些启动脚本，以避免在 udev 还没有完成设备节点的创建时就执行一些依赖于设备节点的操作。它也可以用于在执行 udevadm trigger 后等待所有的 coldplug 事件处理完毕。
* coldplug 事件是指内核在启动时已经检测到了系统的硬件设备，并把硬件设备信息通过 sysfs 内核虚拟文件系统导出，然后由 udev 扫描 sysfs 文件系统，生成热插拔（hotplug）事件，再由 udev 读取这些事件，生成对应的硬件设备文件的过程


udev 对 coldplug 设备的处理逻辑大致如下：

1. udev 在启动时，会遍历 /sys 目录下的所有设备，并读取它们的 uevent 文件，然后向内核发送 "add" 事件，请求内核重新触发这些设备的 uevent。
2. 内核收到 "add" 事件后，会通过 netlink socket 将 uevent 发送给 udevd 守护进程。
udevd 收到 uevent 后，会根据 /usr/lib/udev/rules.d 下的规则文件，匹配设备的属性和事件类型，并. 执行相应的操作，如创建或删除设备节点，运行配置程序，设置权限和所有者等。
3. udevd 处理完一个 uevent 后，会将其从事件队列中移除，并继续处理下一个 uevent。
4. **udevadm settle 命令就是用来等待事件队列为空**，即所有的 coldplug 设备都已经被处理完毕的。

注意：

1. 系统启动的时候会先挂载 /sys，然后才去执行 udev 的逻辑。如果 /sys 没有挂载，那么 udev 就无法正常工作，因为它需要从 /sys 中读取设备的信息和事件。所以，**/sys 是一个必要的前提条件，而不是一个可选的挂载点**。一般来说，/sys 是在内核启动时就自动挂载的，或者在 init 系统中很早就挂载的。如果你使用的是 chroot 环境，那么你需要在 chroot 之前用 --bind 选项把宿主机的 /sys 挂载到 chroot 目录下的 /sys 上。
2. 如何获取事件队列长度。```udevadm info --statistics```(systemd 253 版本中才引入)。

如果要等待所有的事件处理完成，可以使用以下命令：

```
udevadm settle
```

这个命令没有参数。

## control用例

```
udevadm control OPTION

Control the udev daemon.

  -h --help                Show this help
  -V --version             Show package version
  -e --exit                Instruct the daemon to cleanup and exit
  -l --log-priority=LEVEL  Set the udev log level for the daemon
  -s --stop-exec-queue     Do not execute events, queue only
  -S --start-exec-queue    Execute events, flush queue
  -R --reload              Reload rules and databases
  -p --property=KEY=VALUE  Set a global property for all events
  -m --children-max=N      Maximum number of children
  -t --timeout=SECONDS     Maximum time to block for a reply

```



如果要修改 udev 守护进程的规则或参数，可以使用以下命令：

```
udevadm control --reload
udevadm control -R
```
其中，--reload 选项表示重新加载规则文件。

通知后台服务退出，但是可以看到是systemd-udev服务重新拉起，pid发生了变化

```
[root@rocky8 ~]# systemctl status systemd-udevd
● systemd-udevd.service - udev Kernel Device Manager
   Loaded: loaded (/usr/lib/systemd/system/systemd-udevd.service; static; vendor preset: disabled)
   Active: active (running) since Tue 2023-07-11 22:06:02 CST; 1s ago
     Docs: man:systemd-udevd.service(8)
           man:udev(7)
 Main PID: 174258 (systemd-udevd)
   Status: "Processing with 40 children at max"
    Tasks: 1
   Memory: 2.8M
   CGroup: /system.slice/systemd-udevd.service
           └─174258 /usr/lib/systemd/systemd-udevd

Jul 11 22:06:01 rocky8 systemd[1]: Starting udev Kernel Device Manager...
Jul 11 22:06:02 rocky8 systemd[1]: Started udev Kernel Device Manager.
[root@rocky8 ~]# udevadm control -e
[root@rocky8 ~]# systemctl status systemd-udevd
● systemd-udevd.service - udev Kernel Device Manager
   Loaded: loaded (/usr/lib/systemd/system/systemd-udevd.service; static; vendor preset: disabled)
   Active: active (running) since Tue 2023-07-11 22:06:11 CST; 810ms ago
     Docs: man:systemd-udevd.service(8)
           man:udev(7)
 Main PID: 174266 (systemd-udevd)
   Status: "Processing with 40 children at max"
    Tasks: 1
   Memory: 2.6M
   CGroup: /system.slice/systemd-udevd.service
           └─174266 /usr/lib/systemd/systemd-udevd

Jul 11 22:06:11 rocky8 systemd[1]: Starting udev Kernel Device Manager...
Jul 11 22:06:11 rocky8 systemd[1]: Started udev Kernel Device Manager.
[root@rocky8 ~]#

```

在调试udev事件时，使用：
```
udevadm control --log-priority=debug
```

来设置日志级别为debug，然后使用journalctl -f来查看实时日志输出


## control monitor用例

```
udevadm monitor -h
udevadm monitor [OPTIONS]

Listen to kernel and udev events.

  -h --help                                Show this help
  -V --version                             Show package version
  -p --property                            Print the event properties
  -k --kernel                              Print kernel uevents
  -u --udev                                Print udev events
  -s --subsystem-match=SUBSYSTEM[/DEVTYPE] Filter events by subsystem
  -t --tag-match=TAG                       Filter events by tag
```

udevadm monitor的典型用法有：

在分析设备插拔事件时，使用:
```udevadm monitor --kernel --udev```

同时监听内核事件和udev事件，然后比较两者的时间戳和属性，找出可能的问题。


在过滤特定类型的设备事件时，使用:
```
udevadm monitor --subsystem-match=<subsystem>或者–tag-match=<tag>
```
来指定子系统或标签，只输出匹配的事件。

在查看某个设备的属性变化时，使用:
```udevadm monitor --property --sysname-match=<name>```

来指定设备名，并打印事件的属性。

如果要监视设备的内核和用户空间事件，可以使用以下命令：
```
udevadm monitor --kernel --property
```
其中，--kernel 选项表示打印内核事件，--property 选项表示打印用户空间事件。

## test用例

```
# udevadm test --help
calling: test
version 239 (239-74.el8_8.2)
udevadm test [OPTIONS] DEVPATH

Test an event run.

  -h --help                            Show this help
  -V --version                         Show package version
  -a --action=ACTION                   Set action string
  -N --resolve-names=early|late|never  When to resolve names

```


在测试udev规则时，使用:
```
udevadm test devpath来模拟一个udev
```
事件，打印出规则执行的过程和结果，检查是否有错误或者不符合预期的地方。

在指定事件的动作时，使用:
```
udevadm test --action=<action> devpath
```
来设置ACTION变量的值，例如add, remove, change等。

在过滤特定类型的设备事件时，使用:
```
udevadm test --subsystem-match=<subsystem>或者–attr-match=<file[=<value>]>或者–property-match=<key>=<value>
```
来指定子系统，属性或者属性值，只测试匹配的事件。

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

```
# udevadm trigger --help
udevadm trigger [OPTIONS] DEVPATH

Request events from the kernel.

  -h --help                         Show this help
  -V --version                      Show package version
  -v --verbose                      Print the list of devices while running
  -n --dry-run                      Do not actually trigger the events
  -t --type=                        Type of events to trigger
          devices                     sysfs devices (default)
          subsystems                  sysfs subsystems and drivers
  -c --action=ACTION                Event action value, default is "change"
  -s --subsystem-match=SUBSYSTEM    Trigger devices from a matching subsystem
  -S --subsystem-nomatch=SUBSYSTEM  Exclude devices from a matching subsystem
  -a --attr-match=FILE[=VALUE]      Trigger devices with a matching attribute
  -A --attr-nomatch=FILE[=VALUE]    Exclude devices with a matching attribute
  -p --property-match=KEY=VALUE     Trigger devices with a matching property
  -g --tag-match=KEY=VALUE          Trigger devices with a matching property
  -y --sysname-match=NAME           Trigger devices with this /sys path
     --name-match=NAME              Trigger devices with this /dev name
  -b --parent-match=NAME            Trigger devices with that parent device
  -w --settle                       Wait for the triggered events to complete
```

在重放系统冷插拔事件时，使用:

```
udevadm trigger
```

来请求内核发送设备事件，让udev重新处理这些事件。如果停用udev服务，然后热插入一个新的设备，再次启用udev服务，不会自动执行刚刚插入设备的规则。需要手动执行udevadm trigger命令来触发udev重新扫描设备并应用规则。

在指定事件的动作时，使用:
```
udevadm trigger --action=<action>
```
来设置事件的类型，例如add, remove, change等。

在过滤特定类型的设备事件时，使用:
```
udevadm trigger --subsystem-match=<subsystem>或者–attr-match=<file[=<value>]>或者–property-match=<key>=<value>或者–tag-match=<tag>或者–sysname-match=<name>
```

来指定子系统，属性，属性值，标签或者设备名，只触发匹配的事件。


如果要触发一个设备的添加事件，可以使用以下命令：

```
udevadm trigger --action=add --subsystem-match=block
```
其中，--action=add 选项表示指定事件类型为添加，--subsystem-match=block 选项表示指定子系统类型为块设备。


注意：

1. 执行```udevadm trigger -c add /dev/vda```不会对正在使用vda的程序造成影响。这个命令的作用是告诉内核发送热插拔事件给udev，让udev重新扫描设备并应用规则。这个命令只会写入/sys/devices/uevent文件，不会影响设备的数据或状态。但是，如果您的udev规则中有一些会改变设备属性或执行一些外部命令的操作，那么可能会有一些副作用。所以，在执行这个命令之前，先检查udev规则是否有可能对设备造成影响。
2. trigger执行会有风险，最好明确规则和当前对设备的使用情况再执行







---

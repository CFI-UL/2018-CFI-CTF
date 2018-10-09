# UnixDrive

> forensics

Author: [jorkanofaln](https://github.com/jorkanofaln)

A Captured ext2 formatted drive with hidden files


## Writeup

Download the archive in a Kali Linux Virtual Machine and complete the following steps as root:

Extract the archive using the following command: `tar -xvf  UnixDrive.tar.xz`

Install the `libewf` package on kali linux: `apt install ewf-tools`

Open a Terminal and type the following commands:

```shell
mkdir /mnt/E01Drive/

ewfmount unixDrive.E01 /mnt/E01Drive/

cd /mnt/E01Drive/

fdisk -l ewf1

mkdir /mnt/dd

mount -o ro,loop,offset=1048576 ewf1 /mnt/dd/ 

cd /mnt/dd

ls -lah

cd .private

ls -lah

cat .flag.txt 
```

There you have the flag! `FLAG: CFI{Hidden_F1l3s_F0ld3rs_D3c3pt1on}`

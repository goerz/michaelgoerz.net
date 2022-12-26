---
Category: Tech
Tags: mac
Date: 30 Nov 2008
---

# Creating an ISO image on MacOS X

1.  Insert your CD/DVD. Check that MacOS has mounted it in as a Volume (It will appear on the Desktop).

2.  Identify which device the CD/DVD is.

    This is the trickiest part of the whole procedure. First, use `drutil` to get some comprehensive information about your CD/DVD

    ```
    $ drutil status
    Vendor   Product           Rev
    HL-DT-ST DVDRW  GS21N      SA15

    Type: CD-ROM               Name: /dev/disk4
    Sessions: 1                  Tracks: 1
    Overwritable: 00:00:00         blocks:        0 /   0.00MB /   0.00MiB
    Space Free:   00:00:00         blocks:        0 /   0.00MB /   0.00MiB
    Space Used:   30:12:40         blocks:   135940 / 278.41MB / 265.51MiB
    Writability:
    ```

    Note the device name here (`/dev/disk4`) and the "Space Used"
    (265.51MiB). If you do everything right, your iso file should end up with the
    size that you see here.

    `/dev/disk4` may not be the right device yet, however. It may be that
    you have to use a subdevice. Check which device MacOS used for mounting the CD.
    In my example, I got this:

    ```
    $ df -h
    /dev/disk4s1s2      50Mi   50Mi    0Bi   100%    /Volumes/hp LaserJet 1010 Series
    ```

    This CD is pretty special. It contains printer drivers for both Windows and
    Mac, and is split in two parts. Mac OS only mounted the Mac-readable part,
    which is on device `/dev/disk4s1s2`. As you can see, this part is only 50
    MiB, which is less than the 266 MiB that we're expecting. If you check which
    devices actually exist in  `/dev/`, you'll find

    ```
    /dev/disk4
    /dev/disk4s1
    /dev/disk4s1s2
    ```

    The one you have to use here is `/dev/disk4s1`. This one contains the proper
    file system of the whole CD.

    In general, if you see something like `/dev/disk4` in the output of `df -h`,
    that's what you should use. If you see something like `/dev/disk4s1` or
    `/dev/disk4s1s2`, you'll most likely have to go with `/dev/disk4s1.`

3.  Create the ISO file

    ```
    $ cat /dev/disk4s1 > file.iso
    ```

    You may get this error message:

    ```
    cat: /dev/disk4s1: Resource busy
    ```

    If you do, use the following command:

    ```
    $ diskutil unmountDisk /dev/disk4s1
    Disk /dev/disk4s1 unmounted`
    ```

    After that, `cat` should work.

4.  Test the ISO image by mounting the new file (or open with Finder):

    ```
    $ hdiutil attach file.iso
    ```

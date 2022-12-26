---
Date: 2015-07-08 22:49:36
Category: Tech
Tags: bash
---

# Process Pools in Bash

The `xargs` utility allows to easily implement a process pool, where a constant
pool of workers processes a list of jobs in parallel. We use the
following example `worker.sh`:

    #!/bin/bash
    echo "Called worker with args $@"
    sleep 2

The following call will run `worker.sh` 26 times, always keeping 5 processes
running in parallel.

```bash
xargs -L1 -P5 ./worker.sh <<EOF
a 1
b 2
c 3
--extra d 4
e 5
f 6
g 7
h 8
i 9
j 10
k 11
l 12
m 13
n 14
o 15
p 16
q 17
r 18
s 19
t 20
u 21
v 22
w 23
x 24
y 25
z 26
EOF
```

The `-L1` argument ensures that each line below `<<EOF` is taken as one set of
parameters for `worker.sh`. The `-P5` argument results in 5 processes.

An alternative would be to place the lines between `<<EOF` and `EOF` in a file
`args.dat`, and call `<args.dat xargs -L1 -P5 ./worker.sh`

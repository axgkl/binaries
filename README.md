# Binaries for k3s setups

## binenv distris

distributions.patch.yaml for binenv

as taken from my laptops. required to bridge gaps until binenv prs are taken

## Caddy

xcaddy build with loadbalancer lb4 added.


## hetzner-k3s 

Until v2 is released we have this custom build. 

Contains:
- POSIX compliant shell scripts
- Removed waiting for cloud init for autoscaled nodes
- kubectl set to master1 node (in use for cluster creation)

Date: 2024-08-30

https://github.com/vitobotta/hetzner-k3s/pull/396

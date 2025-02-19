# Binaries for k3s setups

An intermediate helper repo, for dev. Purpose: Quickly provide a few download urls for dev installers.

When stuff is working out for me, then proper releaeses are done elsewhere.

Edit 2025-02: Using this repo's gh actions for binenv testing, via github actions, pushing back the **[results](./binenv-tests.md)**.

## Caddy

xcaddy build with loadbalancer lb4 added.


## hetzner-k3s 

Date: 2024-08-30

Until v2 is released we have this custom build. 

Contains:
- POSIX compliant shell scripts
- Removed waiting for cloud init for autoscaled nodes
- kubectl set to master1 node (in use for cluster creation)

https://github.com/vitobotta/hetzner-k3s/pull/396

## binenv distris

Date: 2024-09-10

distributions.patch.yaml for [binenv](https://github.com/devops-works/binenv)

as taken from my laptop. required to bridge gaps until binenv prs are taken


## binenv distri checker

On pushes containing 'binenv-tests' in commit msg, we [test all the entries in the distributions.yaml file of binenv](https://github.com/axgkl/binaries/actions) for:

- downloadability (dl url format might have evolved)
- executability (the files matcher often [finds the wrong file](https://github.com/devops-works/binenv/issues/260#issue-2431278698), just matching on regex match) 

Results are pushed back by gh actions to **[here](./binenv-tests.md)**.

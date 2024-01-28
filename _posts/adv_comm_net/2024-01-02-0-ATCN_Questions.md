---
tags: [Networks, Routing, Questions]
title: "ATCN Exam Questions"
categories: adv-comm-net lecture-notes
math: true
---

## Scaling BGP—Route Reflection

![topology](/assets/images/atcn/ex1_topology.jpg)

### Compute the routes selected by each router, assuming an iBGP full-mesh

| Router | Route |
| ------ | ----- |
| RA     | RA    |
| RB     | RB    |
| RC     | RC    |
| RD     | RB    |
| RE     | RC    |
| RF     | RC    |
| RG     | RB    |
| RH     | RC    |

### Compute the routes selected by each router, assuming that RF acts as the sole route reflector (every other router is a client of RF)

| Router | Route |
| ------ | ----- |
| RA     | RA    |
| RB     | RB    |
| RC     | RC    |
| RD     | RC    |
| RE     | RC    |
| RF     | RC    |
| RG     | RC    |
| RH     | RC    |

There is suboptimal routing in this case, since RD and RG are closer to RB than to RC, but they're forced to go through RC.

### Assuming that we can only have one route reflector and our goal is to minimize suboptimal routing (wrt a full-mesh), is there a better alternative for a route reflector than RF?

No, the others are equal or worse. To minimize suboptimal routing, one should pick a route reflector which selects as best the most preferred route network-wide (if any). RC is the most preferred route network-wide, so any reflector that selects RC as best will minimize suboptimal routing.

### Propose one route reflection topology that guarantees optimal routing and uses the minimum amount of route reflectors possible

We'd need three route reflectors, RA, RB and RC, since there are three routes that need to be reflected and each reflector can only reflect one route.

## Scaling IGPs—Incremental Shortest Path First

![topology](/assets/images/atcn/ex1b_topology.jpg)
> Apply the iSPF algorithm from RA's viewpoint:
{: .prompt-tip}

### assuming the link $(A,C)$ fails

BC now active, EC inactive, substituted by EB

### assuming the link $(A,C)$ increases from $10$ to $20$

EC inactive, substituted by EB

### assuming the link $(A,C)$ decreases from $10$ to $1$

Same links as original tree, except $(A,C)$ is now $1$.

## Scaling IGPs—Hierarchical IGPs

![shutup](/assets/images/atcn/ex1c.jpg)

Compute the forwarding paths to 10.1.{4,5,6,7}/24 from b1, assuming b3 and b4 announces:

### one aggregated prefix $10.1.4.0/22$

All traffic will go through b3, since it has the lowest cost. This is optimal for .4 and .5, but suboptimal for .6 and .7.

### two aggregated prefixes: $10.1.4.0/23$ and $10.1.6.0/23$

Now, .4 and .5 will go through b3, while .6 and .7 will go through b4. This is optimal for all prefixes.

## Scaling IGPs—Traffic Engineering

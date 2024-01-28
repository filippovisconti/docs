---
tags: [Networks, Routing, Prefix-Filtering]
title: Prefix filtering and aggregation
categories: adv-comm-net lecture-notes
math: true
---

## Prefix aggregation and filtering

Maintaining many forwarding entries is problematic for at least three reasons:

| Resource        |   Issue                                                                             |
| ---------------- | -------------------------------------------------------------------------------------- |
| bandwidth        | Installing many entries in a linecard is slow                                          |
| memory           | Routers linecards have limited (and expensive!)<br>memory banks to hold these entriese |
| processing power | It is time-consuming to compute<br>one forwarding entry per destination                |

The key idea behind prefix aggregation/filtering is to leverage the IP addresses hierarchy. A child prefix can be filtered whenever it shares the same output interface as its parent.

We can apply prefix aggregation/filtering either: locally, at the FIB-level, or globally, at the RIB-level ![shutup](/assets/img/ScreenShot%202024-01-03%20at%2022.56.10.png)

One can identify up to four local aggregation/filtering strategies:
![shutup](/assets/img/ScreenShot%202024-01-03%20at%2022.56.48.png)

The first two strategies are simple and preserve strong forwarding consistency.

1. Strong forwarding consistency mandates identical forwarding behaviour—for all packets.
2. The longest-prefix lookup of any destination that appears in the original FIB should return the same next-hop before and after aggregation.

> Any **non**-routable destination by the original FIB should **not** be routable after aggregation. -> Packets that were dropped initially will also be dropped after aggregation

![shutup](/assets/img/ScreenShot%202024-01-03%20at%2022.57.04.png)

> Weak forwarding consistency mandates identical forwarding behaviour—only for routable packets. The longest-prefix lookup of any destination that appears in the original FIB should return the same
> next-hop before and after aggregation.

> **Non**-routable destination by the original FIB _**may**_ become routable after aggregation.

### Optimal Routing Table Constructor (ORTC)

ORTC is an optimal FIB aggregation algorithm: its output has the smallest number of prefixes possible.

ORTC guarantees strong forwarding consistency: it guarantees identical forwarding decisions—for any packet.

ORTC relies upon subnetting and supernetting applied to a binary tree representation of the FIB ![shutup](/assets/img/ScreenShot%202024-01-03%20at%2023.01.34.png)

ORTC performs three consecutive tree traversals, each with a distinct goal

|         | goal             | tree traversal                 |
| ------- | ---------------- | ------------------------------ |
| pass #1 | normalization    | pre-order, from the root down  |
| pass #2 | next-hop ranking | post-order, from the leaves up |
| pass #3 | prefix filtering | pre-order, from the root down  |

The first pass normalizes the tree by fully expanding it, ensuring each node has either zero or two children ![shutup](/assets/img/ScreenShot%202024-01-03%20at%2023.07.38.png)

The second pass calculates the most common next-hops from the bottom up, by merging them according to the following logic

![shutup](/assets/img/ScreenShot%202024-01-03%20at%2023.08.26.png)

Namely, return the common elements if any, otherwise return the union.

![shutup](/assets/img/ScreenShot%202024-01-03%20at%2023.12.12.png)

The third pass moves down the tree, selecting next-hops and eliminating redundant routes. ![shutup](/assets/img/ScreenShot%202024-01-03%20at%2023.12.34.png)

> ORTC is optimal but comes with tradeoffs when it comes to updating the compressed FIB.
{: .prompt-tip}

> ORTC doesn't support update operations to the aggregated FIB. The aggregated FIB must be recomputed upon each update.
{: .prompt-danger}

#### Net result

**Even** if the cost is **linear** in the number of entries, it can still take **hundreds** of ms to update a table.

The **effectiveness** of prefix aggregation **varies** on a per-router basis.

The aggregation **effectiveness** **depends** on:

- **how** prefixes are **distributed** over the next-hops
  - The **fewer** neighbours a router has, the **better** aggregation it may achieve
  - If **all** prefixes **share** the same next-hop, **aggregation** is **maximised**
- how "aggregatable" prefixes are.

Prefix aggregation does not come for free computationally and therefore time-wise, both at the beginning and whenever there is an update.

### DRAGON

DRAGON is distributed route-aggregation technique where routers "think globally, but act locally".

The main result is that by comparing routes for different prefixes, a router can locally compute which routes it can filter and not export while preserving routing and forwarding decisions globally.

When a router filters q, it does not create any forwarding entry for q and does not export q to any neighbor. ![shutup](/assets/img/ScreenShot%202024-01-03%20at%2023.25.41.png)

DRAGON routers propagate more-specific prefixes only in a small vicinity of their origins AS. Packets are forwarded according to increasingly more-specific prefixes as they reach the destination.

![image](/assets/img/2024-01-22-1b-Prefix-filtering-and-aggregation/ScreenShot-2023-09-29-at-23.26.21.png) DRAGON guarantees network-wide routing and/or forwarding consistency post-filtering.
![shutup](/assets/img/ScreenShot%202024-01-03%20at%2023.26.59.png)

All PR nodes filtering is a Nash Equilibrium.

Any node has two incentives to filter q-routes:

- retrieve a better route to forward traffic
- gain space in its routing and forwarding tables

with no node having an unilateral incentive to move away

#### Simple route consistent algorithm

Considering a node u, a child prefix q, its parent prefix p,

> [!Algorithm] If u is not the destination for q and If elected q-route ≥ elected p-route then u filters q-routes

![shutup](/assets/img/ScreenShot%202024-01-03%20at%2023.45.16.png)

DRAGON relies on isotonicity, a property which characterises the combined policies of two neighbours.

> [!Isotonicity] If an AS u prefers one route over another, a neighbouring AS does not have the opposite preference It is required for optimality, not correctness.

DRAGON shows extremely good performance on inferred Internet topologies:

- Between 50% and 80% of the prefixes can be filtered on the vast majority of the nodes
- Convergence time can be reduced as much as 8 times with 73% of the prefixes seeing an improvement
- Good filtering efficiency is quickly reached: 90% of ASes filter prefixes when 100 ASes deploy DRAGON

DRAGON node can automatically introduce aggregation prefix to filter prefixes without parent.

- Node can autonomously announce aggregation prefixes based on local computation and preserving consistency.
- Routing system self-organises itself in case of conflict when more than one node announce the same parent prefix
- Number of aggregation prefixes introduced can be tuned
  - e.g., maximum prefix length or minimum ## covered children

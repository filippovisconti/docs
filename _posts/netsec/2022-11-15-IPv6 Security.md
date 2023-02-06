# IPv6 Security

## Overview

128 bit address space

Typical network sizes:

- /32 per ISP
- /48 per location
- /64 per logical network

Types of addresses:

- Link local
    - fe80::/10 — typically /64
- Global Unique Address
    - globally reachable
    - the “normal” IPv6 address
- Unique Local Address
    - For local deployments
    - Can be NAT’ed to GUA

Nodes assign themselves an IPv6 address, after receiving the prefix from the router through a Router Advertisement (RA), and use **DAD** (duplicate address detection, RFC3484, RFC4429).
Simplified:
▶ "Does anybody have this IPv6 address?"
▶ (no answer)
▶ Great, I take it

<aside>
❗ Easy Denial of Service (DoS) attack: Answer "Yes I have" to every DAD request

</aside>

![Screenshot 2023-01-12 at 16.42.40.png](Screenshot_2023-01-12_at_16.42.40.png)

![Screenshot 2023-01-12 at 16.42.48.png](Screenshot_2023-01-12_at_16.42.48.png)

![Screenshot 2023-01-12 at 16.43.06.png](Screenshot_2023-01-12_at_16.43.06.png)
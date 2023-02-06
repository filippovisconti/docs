# Virtual Private Networks

## Introduction

A VPN creates a **secure channel** between two networks **over an untrusted network**. During the setup phase, the **gateways** (tunnel endpoints) **authenticate** each other and set up encryption keys. After the setup phase has been completed, the communication over the tunnel can begin: **packets are encapsulated** (and usually encrypted and authenticated) at the first gateway and decapsulated at the second. 

## Properties of a VPN tunnel

- Authentication of the source (handshake), data integrity (MACs)
- Secrecy (encryption)
- Replay suppression (sequence numbers)

Not all tunnelling protocols provide encryption and/or authentication (see PPTP).

## Common configurations

- Site-to-Site:
    - provides a secure connection between two physically separated networks;
    - replaces private physical networks and leased lines
- Host-to-Site:
    - remote hosts can securely access resources in a private network, without exposing services to the Internet
- VPN as proxy:
    - users can connect to Internet using the VPN server’s IP address, to circumvent censorship, avoid tracking, spoof location, access locally restricted content.

<aside>
🚫 NB: VPNs do not provide full anonymity (cookies still used, logins, etc…) and the VPN server could monitor and record all of the traffic

</aside>

Generally, VPNs do not provide higher availability (no built-in DDoS protection nor routing attacks).

VPNs can defend against targeted packet filtering (payload is encrypted, all VPN packets would need to be dropped to prevent “unauthorised” communication).

VPNs create virtual network adapters on the host machine, which can then be used like any other network adapters, for either all traffic or only selectively.

## VPN vs TLS

Differently from TLS, VPNs protect all traffic (including e.g.: DNS requests). However, this protection is only available inside the tunnel: TLS comes in handy to protect the communication once packets leave the tunnel. 

Also, a VPN would not authenticate the web server - only the tunnel endpoint. A VPN server, without TLS’s encryption, would be able to read all the traffic in plaintext.

![Screenshot 2023-01-09 at 11.42.56.png](Screenshot_2023-01-09_at_11.42.56.png)

## Cons of using a VPN

- Negative impacts on performance:
    - increased overhead
    - additional cryptographic operations
    - potentially limited bandwidth at VPN server

## VPN vs VLAN

- **VPN**: one virtual network over multiple physical networks.
- **VLAN**: set up multiple isolated virtual networks on a single physical infrastructure.
    - Virtual networks are identified by tags, which are added to Ethernet frames
    - Example protocol: IEEE 802.1Q
    - Often used in cloud-computing environments for isolating communication between VMs

VXLAN (virtual extensible LAN) combines features from both systems.

# IPSec

![Screenshot 2023-01-09 at 12.14.49.png](Screenshot_2023-01-09_at_12.14.49.png)

![Screenshot 2023-01-09 at 12.37.33.png](Screenshot_2023-01-09_at_12.37.33.png)

![Screenshot 2023-01-09 at 12.37.54.png](Screenshot_2023-01-09_at_12.37.54.png)
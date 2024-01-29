---
layout: post
title: "DNS Security"
categories: network-security lecture-notes
tags: network-security lecture-notes DNS security DNSSEC dos reflection attacks
---

# DNS security

## Introduction

DNS is fundamentally insecure. Despite being mission-critical for any online business, this component is often overlooked and forgotten — until something breaks.

![Screenshot 2023-01-11 at 13.56.15.png](/assets/images/DNS/Screenshot_2023-01-11_at_13.56.15.png)

DNS is a globally distributed, loosely coupled, scalable, reliable, and dynamic database. DNS data is maintained locally and retrievable globally.

No single computer has all DNS data.

DNS has no built-in encryption, integrity, nor authentication.

- Why attack DNS?
  - Control DNS resolution of all clients served by name server / resolver
- Why study DNS security?
  - Use DNS to explain attack classes irrespective of protocol
  - Understand security impact of specific features in protocol design or implementation
- What could possibly go wrong?
  - Cache poisoning, replay & amplification, session state, dependencies, org structures, ..

![Screenshot 2023-01-11 at 14.27.17.png](/assets/images/DNS/Screenshot_2023-01-11_at_14.27.17.png)

### Common DNS attacks

| ATTACK                 | DESCRIPTION                                                                                              | IMPACT                                     |
| ---------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| LOCAL HOST NETWORK     | Manipulate DNS entries and conversation on local host or network                                         | Impersonation of services                  |
| CACHE POISONING        | Inject manipulated information into DNS cache of resolver                                                | Impersonation of services                  |
| DNS TUNNELING          | Uses DNS as a covert communication channel to bypass firewalls                                           | Data exfiltration and hidden communication |
| DNS HIJACKING          | Modify DNS record settings (most often at the domain registrar) to point to a rogue DNS server or domain | Impersonation of services                  |
| DISTRIBUTED REFLECTION | Abuse large number of DNS servers to combine reflection and amplification of queries                     | DDoS on victim                             |

## DNS Root Server Security

Every name resolution in the Internet either starts with a query to a root server, or, uses information that was once obtained from a root server. They only resolve the IP addresses for the top-level
name servers (TLD). All other name servers use a hard coded config file to lookup the IP addresses for the root name servers.

### **Key Challenge: Denial of Service Attacks (DOS)**

A sophisticated (D)DoS attack could saturate any system on the Internet. The bandwidth of the root server operators (RSS) is significant, but not immune to DOS attacks

## Cache poisoning

![Screenshot 2023-01-11 at 14.34.27.png](/assets/images/DNS/Screenshot_2023-01-11_at_14.34.27.png)

![Screenshot 2023-01-11 at 14.34.44.png](/assets/images/DNS/Screenshot_2023-01-11_at_14.34.44.png)

### Flawed processing of _****************additional****************_ section

![Screenshot 2023-01-11 at 14.40.40.png](/assets/images/DNS/Screenshot_2023-01-11_at_14.40.40.png)

### Guessing game 1

![Screenshot 2023-01-11 at 14.41.33.png](/assets/images/DNS/Screenshot_2023-01-11_at_14.41.33.png)

### Guessing game 2

![Screenshot 2023-01-11 at 14.43.01.png](/assets/images/DNS/Screenshot_2023-01-11_at_14.43.01.png)

### Cache Poisoning — SADDNS (2020)

<aside>
❗ NOVEL APPROACH: When a DNS server issues a query, its source port effectively becomes open to the public.

</aside>

- Trigger a query on target server
  - OS creates a session awaiting for the response
  - **Ephemeral source port becomes open to public as it has to expect the response**
- Scan port range with UDP to identify open source port:
  - Triggers nothing upon hitting the correct port (as the probe will be accepted by the OS but discarded at the application layer - src ip mismatch)
  - ICMP port unreachable message upon missing it
- Once the source port number is known, the attacker simply injects a large number of spoofed DNS replies brute forcing the txid

![Screenshot 2023-01-11 at 14.50.55.png](/assets/images/DNS/Screenshot_2023-01-11_at_14.50.55.png)

## Compromised Registrar Configuration Attack

Second level domains (SLD) are registered with one of the domain registrars of the TLD.

DNS information is as secure as the Web App, Registration Processes, or the passwords of the registrar and the domain owner.

## Compromised Local Configuration Attack

Manipulate DNS configuration settings on internal network or local host and have target point to attacker’s name server.

![Screenshot 2023-01-11 at 15.12.03.png](/assets/images/DNS/Screenshot_2023-01-11_at_15.12.03.png)

![Screenshot 2023-01-11 at 15.12.29.png](/assets/images/DNS/Screenshot_2023-01-11_at_15.12.29.png)

## DNSSEC, DoH, DoT

Queries can be read by networks, ISPs, or anybody able to monitor. Even if a website uses HTTPS, the DNS query required to navigate to that website is exposed. This lack of privacy has a huge impact
on security and, in some cases, human rights. It becomes easier for governments to censor the Internet and for attackers to stalk users' online behaviour.

**DNSSEC** is a set of security extensions for verifying the identity of DNS root and authoritative nameservers. The root DNS key is provided to the client by the operating system.

It is designed to prevent DNS cache poisoning & other attacks. It does not encrypt communications.

Instead, DNS over TLS or HTTPS (**DoT & DoH**) do encrypt DNS queries.

![Screenshot 2023-01-11 at 15.29.45.png](/assets/images/DNS/Screenshot_2023-01-11_at_15.29.45.png)

![Screenshot 2023-01-11 at 15.31.40.png](/assets/images/DNS/Screenshot_2023-01-11_at_15.31.40.png)

# BGP Security

Insecure ASes use legacy BGP, and secure ASes must accept legacy insecure routes
▪ Problem 1: routing policies can interact in ways that can cause BGP “wedgies”

## Introduction

Border Gateway Protocol (BGP) is a standardised exterior gateway protocol designed to exchange routing and reachability information among autonomous systems (AS) on the Internet. BGP is classified as a path-vector routing protocol, and it makes routing decisions based on paths, network policies, or rule-sets configured by a network administrator.

BGP used for routing within an autonomous system is called Interior Border Gateway Protocol, Internal BGP (iBGP). In contrast, the Internet application of the protocol is called Exterior Border Gateway Protocol, External BGP (eBGP).

### Problems

Since not all traffic is encrypted (see DNS, HTTP), and even encrypted traffic leaks timing information, rerouting attacks are still a threat. Rerouting can cause dropped packages and widespread outages, are hard to notice and impossible to solve without ISP cooperation. 

Rerouting attacks undermine and invalidate other security protocols:

- Used to obtain fake TLS certificates (e.g.: with ACME)
- Used to deanonymize TOR users
- Used to hijack DNS requests
- Used to cause DoS attacks

<aside>
⚠️ BGP does not validate the origin nor the content of advertisements

</aside>

![Screenshot 2023-01-10 at 12.17.52.png](Screenshot_2023-01-10_at_12.17.52.png)

![Screenshot 2023-01-10 at 12.21.27.png](Screenshot_2023-01-10_at_12.21.27.png)

Hijacked traffic can be blackholed (dropped), redirected or intercepted.

## Countermeasures

Ideally, we’d want that:

- only an AS which owns an IP prefix is allowed to announce it — e.g.: by proving it cryptographically
- routing messages are authenticated by all ASes on the path

### RPKI and ROA

The Resource Public Key Infrastructure cryptographically asserts the cryptographic keys of ASes and the AS numbers and IP prefixes they own. Roots of trust are ICANN and the five RIRs (regional internet registries).

RPKI enables the issuance of Route Origination Authorisations. A ROA states which AS is authorised to announce certain IP prefixes. ROAs are signed, distributed and checked ***********out-of-band***********. Checking validity out-of-band allows to make no modification to BGP.

![Screenshot 2023-01-10 at 18.06.10.png](Screenshot_2023-01-10_at_18.06.10.png)

ASes and RIRs create ROAs and upload them to repositories, which are periodically fetched by each AS, which will verify signatures for all entries based on RPKI and store them in trusted local caches.

All BGP routers of an AS periodically fetch a list of ROAs from the local cache, with a ******************secure****************** connection (as the router does not repeat the cryptographic checks (TLS, SSH, IPSec). 

When a BGP update message arrives, the router can check whether a ROA exists and it is consistent with the **first** AS entry of the BGP message.

<aside>
⚠️ Path prepending is still an issue.

![Screenshot 2023-01-10 at 19.11.38.png](Screenshot_2023-01-10_at_19.11.38.png)

</aside>

### BGPsec

The main idea is to secure the AS-PATH attribute in BGP announcements, preventing path prepending and poisoning, by signing received BGP messages to prove that the path was correctly updated. 

![Screenshot 2023-01-10 at 19.25.56.png](Screenshot_2023-01-10_at_19.25.56.png)

Insecure ASes use legacy BGP, and secure ASes must accept legacy insecure routes
Problem 1: routing policies can interact in ways that can cause BGP “wedgies”

Problem 2: protocol downgrade attacks
If operators don’t prioritise security, an attacker can just use legacy BGP to announce bogus routes to BGPsec neighbours.

Problem 3: performance degradation
• Prefix aggregation no longer possible
• Expensive asymmetric cryptography (signature and validation) →Slower convergence
▪ Unless security is the first priority or BGPsec deployment is very large, security benefits from partially deployed BGPsec are meager
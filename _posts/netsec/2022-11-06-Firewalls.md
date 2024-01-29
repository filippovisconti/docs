---
layout: post
title: "Firewalls"
categories: network-security lecture-notes
tags: network-security lecture-notes firewalls ids ips
---

# Firewalls

## Introduction

A firewall is a system used to protect or separate a trusted network from an untrusted network, while allowing authorised communications to pass from one side to the other.

Firewalls enforce an access control policy between two networks Inside / Intranet.

Network firewalls protect different network segments. Host firewalls protect single hosts.

| INGRESS        | Filter incoming traffic from a low security to a high security net |
| -------------- | ------------------------------------------------------------------ |
| EGRESS         | Filter incoming traffic from a high security to a low security net |
| DEFAULT POLICY | Defines what to do when no rule matches (ACCEPT or DENY ALL)       |

## Stateless firewalls

These firewalls examine a packet at the network layer and the decision based on packet header information, such as IP, port, flags.

Pros:

- Application independent
- Good performance and scalability

Cons:

- No state nor application context

## Stateful firewalls

These firewalls keep also track of the state of the network connections and the decision is based on it too.

Pros:

- More powerful rules

Cons:

- State for UDP?
- Possibly inconsistent state between host and firewall
- State explosion → possible DoS attack

## Next Generation Firewalls

These firewalls perform deep packet inspection and take application and protocol state into account for security decision.

Pros:

- Even more powerful rules
- Application and protocol awareness

Cons:

- Needs to support many applications and protocols
- Performance, scalability
- Possibly inconsistent state between host and firewall

## Web Application Firewalls

These firewalls protect web-based applications from malicious requests.

They use request patterns (signatures) to detect SQL injections, XSS, buffer overflow attempts, etc...

They also offer user authentication and session management.

Most often, WAFs are implemented as a reverse proxy to protect public-facing web applications.

### Deployment challenges

Protecting large number of hosts, endpoints and network segments is not trivial.

## Attack techniques

| IP SOURCE SPOOFING | Spoofing the source IP address to bypass filters Works for stateless protocols (e.g. UDP, ineffective for TCP). | | --- | --- | | ARTIFICIAL FRAGMENTATION | Fragment packets to
bypass rules. Without proper reassembly at the firewall the attack gets through. | | VULNERABILITIES | Exploiting vulnerabilities in firewall software / firmware / OS. Exploit vulnerabilities in
target application. | | DENIAL OF SERVICE | Firewall state explosion → defaults to fallback policy. | | TUNNELING/COVERT CHANNELS | Data in ICMP ping packets, or use DNS requests as channel. Attack
through VPN virtual private network. | | PAYLOAD ENCODING | Different encodings or mappings confuse detection |

## Attack detection

| REACTIVE | System can only detect already known attacks | | --- | --- | | PROACTIVE | System can detect known and new, yet unknown attacks

| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | | DETERMINISTIC | System
always performs the same given the same input. The same stimuli always result in same action. Reason for alert is known. | | NON-DETERMINISTIC | System detection is fuzzy (heuristics, machine
learning, sandboxing) and depends on current state of the world. Reason for alert typically not known. |

![Screenshot 2023-01-10 at 22.32.14.png](/assets/images/Firewalls/Screenshot_2023-01-10_at_22.32.14.png)

### Signature-based Detection

Exists in practically all detection and protection technologies and it is by far the fastest and most efficient way of categorising a data artifact. It has a boolean output: known good and known bad.

Pros:

- Low resource requirements
- Fast
- Low false positives

Cons:

- Reactive – threat must be known before
- Frequent update of signatures
- Humans in the loop

### Sandboxing-based Detection

Sandboxing products typically run a samples in a (instrumented) sandbox environment It examines / monitors the runtime behaviour of sample (e.g. malware) and it compares the behaviour against a list
or rules previously developed by the vendor in their lab or it applies machine learning for behaviour classification.

Pros:

- Proactive, can detect unknown threats
- No signature updates required

Cons:

- Resource intensive
- High latency
- Difficult to scale

### Machine Learning

Golden rule: Data you are going to work on needs to come from approximately the same distribution as the data you are training on.

## Types of attacks

![Screenshot 2023-01-10 at 23.23.43.png](/assets/images/Firewalls/Screenshot_2023-01-10_at_23.23.43.png)

![Screenshot 2023-01-10 at 23.25.00.png](/assets/images/Firewalls/Screenshot_2023-01-10_at_23.25.00.png)

"It is better to be roughly right than precisely wrong."

![Screenshot 2023-01-10 at 23.33.45.png](/assets/images/Firewalls/Screenshot_2023-01-10_at_23.33.45.png)

![Screenshot 2023-01-10 at 23.34.08.png](/assets/images/Firewalls/Screenshot_2023-01-10_at_23.34.08.png)

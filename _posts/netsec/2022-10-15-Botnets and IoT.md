---
layout: post
title: "Botnets and IoT"
categories: network-security lecture-notes
tags: network-security lecture-notes bot botnet iot security cnc
---

# Botnets and IoT

## Introduction

Your malware has infected 10k targets .. What do you do now?
Spam or DDoS actions are really stupid - noisy behaviour leads to fast detection & neutralisation of the agent.

Better approaches are:

| Persist and avoid detection | Explore target and steal all valuable information.
Load customised exploitation functionality.
Persist to maximise yield (password intercepts, ..). |
| --- | --- |
| Move to active attacks | An increased chance of detection is now justified to further monetise the target → noisier attacks.
Load customised attack functionality. |
| Throw away agent | Sell/rent infected machines to clueless
idiots to maximise profit |

## Botnets

A bot agent is a malware tool installed on compromised machines.

A botnet is the collection of all bot agents controlled by a bot-master, who is the operator/controller of the botnet.

Command&Control is the botnet management and communication system.

![Screenshot 2023-01-11 at 11.29.04.png](/assets/images/Botnets/Screenshot_2023-01-11_at_11.29.04.png)

This architecture allows efficient, scalable, dynamic, and robust control of millions of machines with low risk of identification of the bot master.

### Challenges

- Send and receive new instructions and malicious capabilities
- Robustly manage 10,000+ globally distributed agents
- Resistant to hijack and shut-down attempts

```mermaid
graph TD
	subgraph INITIALIZE
	  id1(Machine infected, bot agent installed) --> id2(Bot connects to CnC to join botnet)
		style id1 fill:red
		id2 --> id3(Retrieve protection module)
		id3 --> id4(Secure the bot)
	end
	subgraph EXPLOITATION
		direction BT
		id4 --> id5(Listen to CnC await commands)
		id5 --> id6(Download new payload module)
		id6 --> id7(Execute payload Exfiltrate data)
		id7 --> id8(Report result to CnC)
		id8 --> id5
	end
	subgraph TERMINATION
		id7 --> id9(Erase evidence, abandon client)
	end
```

![Screenshot 2023-01-11 at 11.47.58.png](/assets/images/Botnets/Screenshot_2023-01-11_at_11.47.58.png)

![Screenshot 2023-01-11 at 11.51.01.png](/assets/images/Botnets/Screenshot_2023-01-11_at_11.51.01.png)

![Screenshot 2023-01-11 at 11.51.14.png](/assets/images/Botnets/Screenshot_2023-01-11_at_11.51.14.png)

## CnC Infrastructure Localisation

The ability of a bot agent to locate the CnC infrastructure is a critical requirement for maintaining control of the entire botnet. A bot agent that cannot connect to the control infrastructure cannot be controlled. 

The bot has to somehow identify the CnC infrastructure. The CnC communication can be intercepted by competitors and/or law enforcement to shut down or take over the botnet and Identify the bot master.
For this reason, botnet takedown attempts typically target the CnC infrastructure.

### IP address and Domain Fluxing

A CnC resource with a given Fully Qualified Domain Name (FQDN) is mapped to a new set of IP addresses as often as every few minutes.

The same FQDN connects to a different IP and CnC server every few minutes. IPs of unresponsive CnC nodes are taken out of flux

Availability is always maintained, gives quality of service & robustness.

Domain flux generates list of “rendezvous” points that may be used by the bot masters to control their bots.
Each bot independently computes a list of domain names using a Domain Generation Algorithm (DGA). These domain names are tried to connect to the command and control infrastructure.
The list of domain names is periodically refreshed. Not all generated domains must be valid for the botnet to be operative. Only the bot master knows the sequence of generated domain names.

![Screenshot 2023-01-11 at 12.04.44.png](/assets/images/Botnets/Screenshot_2023-01-11_at_12.04.44.png)

## Botnet Defence

### Sink-holing

A technique that is used to redirect the traffic from bots to an analysis server.
A sinkhole server gathers analytics and controls bots *(if the authentication is also reverse engineered)*

Reverse engineering of infected machines enables security researchers to replicate the DGA.

This allows the identification and registration of some of the “rendezvous” domains, and thereby
redirect all traffic of infected bots to the sinkhole server.

### ****Instrumentation of bot agents****

An infected machine exposes valuable botnet telemetry data.
Run bot agents in a instrumented and controlled environment. Bot generates domain names, which can be analysed.
Intercept bot configuration files when pushed to bot agent by bot master. 
Botnet configuration files provide a wealth of timely and accurate information on ongoing cyber crime campaigns and the organisations targeted by these campaigns.
The timely analysis of botnet configurations enables to track cyber crime campaigns at the
very source.

## IoT

![Screenshot 2023-01-11 at 12.11.04.png](/assets/images/Botnets/Screenshot_2023-01-11_at_12.11.04.png)

![Screenshot 2023-01-11 at 12.20.34.png](/assets/images/Botnets/Screenshot_2023-01-11_at_12.20.34.png)
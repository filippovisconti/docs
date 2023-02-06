# Anonymous Communication Systems

## Introduction

Since IP addresses still leak metadata information, there are use-cases where the communicating parties want to remain anonymous. However, anonymity is not a property of individual messages or flows (you cannot be anonymous on your own). 

## Terminology

- Sender anonymity:
    - sender is unknown, adversary knows/is receiver;
    - adversary may learn message;
    - ************************set of all senders is indistinguishable from real sender************************ (small set → little anonymity);
    - responses reach sender using a token provided by the original sender.
- Receiver anonymity:
    - receiver is unknown, adversary knows/is sender;
    - adversary may choose message;
    - ************************set of all receivers is indistinguishable from real receiver************************
    - traffic reaches destination using a known pseudonym (Onion service)
- Sender-receiver unlinkability:
    - adversary knows senders and receivers;
    - link between senders and receivers is unknown;
    - multiple users ********need******** to communicate at the same time;
    - anonymity comes from unlinkability.
- Unobservability:
    - adversary cannot tell whether any communication is taking place;
    - achieved through DSSS in wireless communication and by always sending traffic in a wired environment.
- Plausible deniability:
    - adversary cannot prove that any particular individual was responsible for a message

## Mix-nets

Intended for sending anonymous emails (or other individual messages), where latency is not a big concern. No connection setup, only individual messages. This solution is built on asymmetric cryptography.  Each mix has a public/private key pair $K_i/K_{i-1}$. Public keys 𝐾 and addresses 𝐼 are known to the senders

![Screenshot 2023-01-09 at 15.31.28.png](/assets/images/Anonymous/Screenshot_2023-01-09_at_15.31.28.png)

Problem: network attacker can observe in- and outgoing messages. 

Each proxy should perform batching → collect several messages before forwarding (threshold). Additionally, the proxies should change the order of (mix) the messages. This is called a threshold mix.

Important: messages need to be padded to a fixed length to make them indistinguishable!

Often, users only communicate with a small subset of other users
Attacker’s idea: every time a message is seen by the target, register the sets of destinations. To achieve full unobservability, use cover traffic, both for sending and for receiving, which prevents statistical disclosure.

Often, the mix stores messages for receivers. Receivers regularly try to retrieve messages. If there is a message, it is downloaded, otherwise a dummy message is returned by the mix.
Now it’s possible to be fully anonymous... as long as at least one mix is honest!

### How to send replies

![Screenshot 2023-01-09 at 16.10.34.png](/assets/images/Anonymous/Screenshot_2023-01-09_at_16.10.34.png)

## Onion routing

It is possible to build a system that can support web browsing, but anonymity guarantees need to be lowered.  

Main ideas:

- Layered encryption, no batching and mixing, no cover traffic
- Flow-based: establish a virtual circuit (keys) once per flow,
reuse it for all packets in the flow using only symmetric key crypto
- Constrained threat model: only local adversary, which cannot launch confirmation (traffic analysis) attacks.

The nodes are called relays (also nodes or routers). The virtual circuit is also called tunnel (especially if it is at layer 3)

![Screenshot 2023-01-09 at 16.18.53.png](/assets/images/Anonymous/Screenshot_2023-01-09_at_16.18.53.png)

## Lifecycle of a circuit

- Circuit setup
    - Initially, sender knows long-term public keys of relays
    - The sender negotiates shared keys with all relays on the path; this requires (expensive) asymmetric cryptography
    - The relays store the necessary state
    - Details
        
        ![Screenshot 2023-01-09 at 22.30.48.png](/assets/images/Anonymous/Screenshot_2023-01-09_at_22.30.48.png)
        
        Establish state on relays by using normal packets as for mixes. Messages for each node contain the address of the next node and ephemeral DH share. Each node replies with its own ephemeral DH share. Encryption of **setup** packet uses long-term **asymmetric** keys of relays.
        
- Data forwarding
    - Packets for one or more flows are forwarded along the circuit
    - Only symmetric cryptography is used (AES)
    - Details
        
        ![Screenshot 2023-01-09 at 22.33.14.png](/assets/images/Anonymous/Screenshot_2023-01-09_at_22.33.14.png)
        
        The sender has established a circuit (symmetric keys and per-link IDs). Data packets are encrypted as usual (layered encryption). The ID of the next relay is added in clear text. 
        In order to protect against network adversaries, links can be encrypted (e.g.: using TLS)
        
- Circuit tear-down
    - The circuit is destroyed to free state on relays or to prevent attacks
    - Details
        
        It can be initiated by both the sender and the intermediate relays. The sender communicates the tear-down to one relay at a time, starting from the furthest away. the exit relay may tear down the circuit if a corrupt packet (or another attack) is detected.
        
        Circuits have a limited lifetime, so all will eventually be destroyed.
        

## Forward security

If longterm keys are compromised, anonymity of previously established circuits is preserved. The direct setup doesn’t provide immediate forward security for the link between communication parties, since no ephemeral information can be used to encrypt setup messages. Forward security is later achieved through DH exchanges.

### Deanonymization — Telescopic circuit setup

In order to obtain immediate forward security and prevent deanonymization, a technique called ************************telescopic circuit setup************************ can be used. 

![Screenshot 2023-01-09 at 22.42.19.png](/assets/images/Anonymous/Screenshot_2023-01-09_at_22.42.19.png)

With this setup, which is slightly slower, keys are negotiated one relay at a time, and, thus, the circuit is extended one hop at a time. By doing this, ephemeral session keys are negotiated before the circuit is extended.

As soon as the circuit is closed, session keys are deleted.

## Attacks

### Passive traffic analysis

The adversary observes the edges of the network, recording traffic patterns, such as flow length, bandwidth pattern, inter-packet timings.

Real time detection is challenging — store and compare later (this needs a large amount of storage)

### Active traffic analysis

The adversary actively modifies packet timings (inter-packet timing — delaying/reordering) or drops packets (detectable).

It can do **********************************flow watermarking********************************** (injecting one bit — marked or not) or ********flow fingerprinting******** (inject multiple bits)

### Website fingerprinting

The adversary has a database of fingerprints of websites, and only needs one observation point. This attack is particularly effective for interactive applications. 

### Higher layer attacks

There are different IP tunnels, but an end-to-end TCP (or even HTTP or TLS) connection.

However, most of the deanonymization is done through other means (downloading malware, or a file that will access the Internet directly).

To achieve anonymity, all layers need to be anonymized.

## TOR — onion routing 2.0

Founded in 2006, it’s the most widely used anonymous communication system. 

Circuits are established over **3** relays, using telescopic setup to ensure immediate forward security. 

It uses **********************per-hop TCP**********************, established on the fly, to avoid TCP stack fingerprinting. 

It also uses ********per-hop TLS******** (except on the last hop), with end-to-end HTTPS still possible and multiple circuits over the same TLS connection.

TOR supports SOCKS proxy, enabling any TCP application to make use of a TOR connection.

TOR also provides receiver anonymity, by not using DNS and having `.onion` URLs.

### Tor cells

Every cell is 512 bytes long and contains a ********************circuit ID******************** and a **************command field************** in cleartext. 

![Screenshot 2023-01-10 at 11.24.55.png](/assets/images/Anonymous/Screenshot_2023-01-10_at_11.24.55.png)

A relay cell’s payload is decrypted and its digest is checked. If correct, this means the relay is the intended recipient of the cell) → check command.
Otherwise, it is an intermediate node relaying the cell → replace circuit ID and forward cell along.

Only exit relay sees unencrypted payload.

### Circuit extension

Tor `extend` cells can only be contained in `relay_early` cells, and each relay only allows 8 `relay_early` cells per circuit, which **limits** the **maximum path length at 9**.

### Onion services

To authenticate onion services which want to be anonymous, the hash of the service’s public key is used as the identifier of the hidden service.

The service has connection to a set of special relays called *******************introduction points******************* (IP). To communicate, a client connects to an IP, which suggests a rendezvous. The client can then connect to the rendezvous and start the communication.

### Directory authorities

There are ******10****** directory authorities, running a consensus algorithm, which track the state of the relays and store their public keys. TOR browsers come with a list of the authorities’ keys, and a client accepts a consensus document if it is signed by ≥ 50% of the authorities. 

<aside>
⚠️ An adversary compromising 5 authorities can compromise TOR

</aside>
---
layout: post
title: "SSL/TLS Public-Key Infrastructure"
categories: network-security lecture-notes
tags: network-security lecture-notes ssl tls pki crypto security ca certs
---

# SSL/TLS Public-Key Infrastructure

## Introduction

We need to bring security to the uppermost level of the Protocol Stack, in order to protect application data.

The goal of TLS is to secure Internet communication, by requiring secrecy - to prevent eavesdroppers to learn sensitive information, and entity and message authentication - to prevent message alteration/injection.

A sample TLS 1.2 session uses a Diffie-Hellman key agreement, which is subject to MitM attacks.

![Screenshot 2022-10-16 at 11.13.35.png](/assets/images/PKI/Screenshot_2022-10-16_at_11.13.35.png)

## PKI Overview

In symmetric cryptography, the main challenge is key distribution as keys need to be distributed via ************************confidential************************ and ******************authentic****************** channels.

In public-key system, the main challenge is key authentication (which key belongs to whom) as keys need to be distributed via ****************authentic**************** channels.

Public-key infrastructures provide a way to validate public keys.

### Terminology

- PKI: Public-Key infrastructure
- CA: Certificate Authority
- A public-key certificate is signed and binds a name to a public key
- Trust anchor, trust root: self signed certificates of public keys that are allowed to sign other certificates
- X.509: standard format of digital certificate

## Trust establishment

It’s not possible to establish trust out of thin air. For this reason, a Root of trust is used to establish trust in other entities. Cryptographic operations enable transfer of trust from one entity to another.

Metrics: size of trust root (how many entities need to be trusted?) and number of malicious entities that can be tolerated.

## X.509

X.509 was issued by the International Telecommunications Union in July 1988, in association with the X.500 electronic directory services standard.

X.509 defines a structure for public key certificates:

- Two sections:
    - Data section
    - Signature section
- A CA assigns a unique name to each user and issues a signed certificate
- Often ****name *********is the domain name or e-mail address.

The basic structure is very simple, but ends up being very complex in any reasonable application. 

Many vulnerabilities have been identified in certificate processing.

## Multi-Domain (aka Cruise-liner) by Content Delivery Networks

CDNs are hosting web sites for domains and thus need a certificate to service content. As such, CDNs are obtaining a single certificate for multiple domains.

## Trust Roots for Entity Validation

Trust roots do not scale to the world:

- Monopoly model: single root of trust
    - DNSSEC, BGPSEC/RPKI
    - Problem: world cannot agree on who controls root of trust
- Oligarchy model: numerous roots of trust
    - SSL/TLS PKI: over 1000 trusted root CA certificates
    - Problems:
        - Weakest link security: single compromised entity enables MitM attacks
        - Not trusting some trust roots results in unverifiable results

Current implementation of both models lack efficient update/maintenance of roots of trust.

## HTTP Strict Transport Security (HSTS)

The goal is to allow servers to declare that their clients should only use HTTPS (for a specified period)

Prevents some *********downgrade*********, *************SSL stripping*************, and *session hijacking* attacks.

It is implemented with an HTTP header: 

```jsx
Strict-Transport-Security: max-age=31536000
```

Browsers should automatically redirect to HTTPS or display a warning message.

## HTTP Public-key Pinning (HPKP)

The server sends a set of public keys to the client. These keys should be the only ones used for connections to this domain. It is implemented with an HTTPS header:

```jsx
Public-Key-Pins: max-age=2592000;
pin-sha256="...";
pin-sha256="...";
report-uri="..."; // (Pin validation failures are reported to the given URL.)
```

## Certificate Revocation

It’s a mechanism to invalidate certificates, for example

- after a private key is disclosed
- when a trusted employee / administrator leaves corporation
- when certificate expiration time is chosen too long

CAs periodically publish Certificate Revocation Lists (CRL). Delta CRLs only contain changes.

What is the problem with revocation? CAP (Consistency, Availability, tolerance to Partition) theorem: impossibile to achieve all 3, must select one to sacrifice.

## Online Certificate Status Protocol (OCSP)

It’s used to verify certificate status, ensure certificate is valid and has not been revoked. Each certificate contains an OCSP responder.
Problems: 

- OCSP servers can be slow!
- Some browsers ignore bogus OCSP responses
- All browsers avoid treating OCSP errors as fatal
- OCSP can leak browsing information outside of private browsing mode

### OCSP stapling

- eliminates the additional round trip required by the client to obtain the OCSP status from the OCSP server
- eliminates the leakage of the user’s browsing behaviour to the OCSP server
- increases availability as the OSCP server might not be available when the client requests the website

## DNS-based Authentication of Named Entities (DANE)

The goal is to authenticate TLS servers without a CA, by using DNSSEC to bind certificates to names.

Use cases:

- CA constraints: clients should only accept certificates by these CAs
- Cert constraints: clients should only accept this cert
- Trust anchor assertion: clients should use domain-provided trust anchor to validate certificates for that domain.

However, there is a heavy reliance on DNSSEC

## Certificate Transparency (CT)

It’s goal is to detect misbehaving CAs.

It will make all public end-entity TLS certificates public knowledge, and will hold CAs publicly accountable for all certificates they issue. It will do so without introducing another trusted third party.

### CT Log — Design

A CT log is an **append-only list of certificates**. The log server verifies the certificate chain: CA attribution for certificate mis-issuance and spam control. It will periodically append all new certificates to the append-only log and sign that list. It will publish all updates of the signed list of certificates (”the log”) to the world.

Because the log server can only periodically update its log, a valid certificate submitted by the CA cannot be immediately added to the log. The log server creates SCT as a promise to add the certificate to the log within some time period. The domain owner can use SCT to show the validity of the certificate to the user before the certificate is added to the log.
The log server creates SCTs.

### CT Log — Properties

A CT Log is not a “Super CA”. The log does not testify to the goodness of certificates: it merely notes their presence. 
The log is public: everyone can inspect all the certificates.
The log is untrusted: since the log is signed, the fact that everyone sees the same list of certificates is cryptographically verifiable.

The data structure used is the Merkle hash tree.

### Security of CT

Security is improved because browsers would require SCT for opening connection, and contact log server to ensure that the requested certificate is listed in the log.

Consequences: the **attack certificate would have to be listed in public log**, which would make the attack publicly known → deterrence

Advantages: CT is fully operational today, with no change to domain’s web servers required.

Disadvantages: **MitM attacks can still proceed, although they can be detected externally**; browsers still need to contact Log eventually to verify that certificate is listed in log; current CT does not support revocation; malicious log server can add bogus certificates; management of list of trusted log servers can introduce a kill switch.

![Screenshot 2022-10-16 at 12.26.49.png](/assets/images/PKI/Screenshot_2022-10-16_at_12.26.49.png)

![Screenshot 2022-10-16 at 12.27.02.png](/assets/images/PKI/Screenshot_2022-10-16_at_12.27.02.png)

Auditors should check that SCTs are honoured (promised certificates are actually included in the log) and verify that the log is actually append-only.

The log server provides the signed root hash and other necessary hashes (proof of Inclusion).
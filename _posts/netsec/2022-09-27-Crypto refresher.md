---
layout: post
title: "Crypto refresher"
categories: network-security lecture-notes
tags: network-security lecture-notes crypto auth
---

# Crypto refresher

**Secrecy vs Confidentiality**: keep data hidden from unintended receivers

**Privacy**: keep data about a person secret.

**Anonymity**: secrecy of an identity or a network identity, but also sometimes a property of data.

Integrity vs Authentication: often used interchangeably

**Data** integrity:

ensure data is correct, prevent unauthorised changes.

**Entity authentication** or identification:

verify the identity and liveness of another protocol participant.

**Data origin authentication**:

ensure that a data originates from a claimed sender.

Integrity is often a property of local or stored data.

Data auth is often used in network context.

## Basic Cryptographic Primitives

- Symmetric (Shared-key, same-key):

  A **single** key, used for both encryption and decryption.

  Encryption: $E_K(\text{plaintext}) = \text{ciphertext}$ also written as $(\text{plaintext})_K$

  Decryption: $D_K(\text{ciphertext}) = \text{plaintext}$

  Stream ciphers: One-time pad, use unique random keystream for each message. It leaks the length of the message. It must not be used more the ones.

  They use pseudo-random number generator (PRNG) to generate jeystreams form shared key and seed (aka initialisation vector, IV)

  keystream: $PRNG(k, IV)$

  $ciphertext = IV || plaintext \oplus PRNG(k, IV)$

  Same key k can be used multiple times, with different IV values

  ChaCha, option in TLS 1.3 and used in Wireguard VPN

  Main Vulnerabilities:

  Key-stream reuse attack: $c1 = p1 \oplus ks$, $c2 = p2 \oplus ks$

  Xor together the cipher-texts: $c1 \oplus c2 = p1 \oplus p2$ , if you know one of the plain-texts, it’s trivial to get the other one.

  Cipher-text modification attack: alteration of cipher-text will alter corresponding values in plaintext after decryption

  Stream ciphers do not provide data integrity.

  Block Ciphers: they are a keyed family of permutations: each key defines a one-to-one mapping of input block to output block.

  Substitution cipher with large block size

  Modelled formally as a pseudo-random permutation (PRP): computationally infeasible to distinguish outputs of a block cipher with random key from outputs of a random permutation.

  Ex: DES AES

  A block cipher alone should not be used for encryption. Needs to be used in a mode of operation.

  AES: advanced Encryption Standard. Officially adopted in 2001 for US gov work. Designed by NIST competition.

  It has a 128-bit block size, [128, 192,256]-bit key size.

  High-speed cipher, using native hardware instruction

  Block-Cipher Modes of Operation:

  ECB: don’t use

  Electronic Code Book: natural approach for encryption. Given a message M, split M up into blocks of size s bits. $ciphertext=E_K(M1),E_K(M2),...$

  It suffers from deterministic encryption.

  Adversary can replace blocks of other blocks, reorder blocks, delete blocks (no integrity)

  CBC: Cipher Block Chaining

  $C_0=IV$

  $C_j=E_K(P_j\ \oplus \ C_{j-1})$

  Pros:

  Achieves Semantic security

  Cons:

  No integrity

  Bit flipping influences at most

  PG 18

  IGE: exotic mode used in Telegram

  Desired Properties for Symmetric Encryption

  Semantic security: an adversary cannot do any better than random guessing, even after seeing many cipher-texts.

  Integrity: adversary cannot produce a new cipher-text that will be accepted by the decryption algorithm, even when it has seen many cipher-texts

  So no attacks based on flipping bits in cipher-texts, cutting and pasting blocks, etc.

- Asymmetric (public-private key)

- Others (unkeyed symmetric)

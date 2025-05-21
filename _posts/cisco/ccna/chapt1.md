---
tags: [Networks, Cisco, CCNA, foundations, osi]
title: Introduction to TCP/IP Networking
categories: ccna-notes
math: true
---

## Introduction

Do I Know This Already?

1. Which of the following protocols are examples of TCP/IP transport layer protocols?
   1. d. UDP, f. TCP
2. Which of the following protocols are examples of TCP/IP data-link layer protocols?
   1. a. Ethernet, g. PPP
3. The process of HTTP asking TCP to send some data and making sure that it is received correctly is an example of what?
   1. b. Adjacent-layer interaction
4. The process of TCP on one computer marking a TCP segment as segment 1, and the receiving computer then acknowledging the receipt of TCP segment 1 is an example of what?
   1. b. Same-layer interaction
5. The process of a web server adding a TCP header to the contents of a web page, followed by adding an IP header and then adding a data-link header and trailer, is an example of what?
   1. a. Data encapsulation
6. Which of the following terms is used specifically to identify the entity created when encapsulating data inside data-link layer headers and trailers?
   1. d. Frame
7. Which OSI encapsulation term can be used instead of the term frame?
   1. b. Layer 2 PDU

Although vendor-defined proprietary networking models often worked well, having an
open, vendor-neutral networking model would aid competition and reduce complexity.
The International Organization for Standardization (ISO) took on the task to create such a
model, starting as early as the late 1970s, beginning work on what would become known
as the Open Systems Interconnection (OSI) networking model. ISO had a noble goal for the
OSI model: to standardize data networking protocols to allow communication among all
computers across the entire planet.

The TCP/IP model both defines and references a large collection of protocols that allow
computers to communicate. To define a protocol, TCP/IP uses documents called Requests
For Comments (RFC). The TCP/IP model creates a set of rules that allows us all to take a computer (or mobile
device) out of the box, plug in all the right cables, turn it on, and connect to and use the
network.

|OSI Level|TCP/IP Model|Example Protocols|
|---|------------|--|
|5-7| Application|HTTP, POP3, SMTP|
|4|Transport|TCP, UDP|
|3|Network|IP, ICMP|
|2|Data Link|Ethernet, PPP, 802.11 (Wi-Fi)|
|1|Physical||

### TCP/IP Application Layer

The most popular TCP/IP application today is the web browser. Many major soft-
ware vendors either have already changed or are changing their application software to sup-
port access from a web browser.

To get the web page from Larry, at Step 1, Bob sends a message with an HTTP header.
Generally, protocols use headers as a place to put information used by that protocol. This
HTTP header includes the request to “get” a file. The request typically contains the name of
the file (home.htm, in this case), or if no filename is mentioned, the web server assumes that
Bob wants the default web page.
Step 2 in Figure 1-6 shows the response from web server Larry. The message begins with an
HTTP header, with a return code (200), which means something as simple as “OK” returned
in the header. HTTP also defines other return codes so that the server can tell the browser
whether the request worked. (Here is another example: If you ever looked for a web page
that was not found, and then received an HTTP 404 “not found” error, you received an HTTP
return code of 404.) The second message also includes the first part of the requested file.
Step 3 in Figure 1-6 shows another message from web server Larry to web browser Bob, but
this time without an HTTP header. HTTP transfers the data by sending multiple messages,
each with a part of the file. Rather than wasting space by sending repeated HTTP headers
that list the same information, these additional messages simply omit the header.

### TCP/IP Transport Layer

The two most commonly used transport layer protocols are
the Transmission Control Protocol (TCP) and the User Datagram Protocol (UDP).
TCP/IP needs a mechanism to guarantee delivery of data across a network. Because many
application layer protocols probably want a way to guarantee delivery of data across a net-
work, the creators of TCP included an error-recovery feature. To recover from errors, TCP
uses the concept of acknowledgments.
Figure 1-7 shows web server Larry sending a web page to web browser Bob, using three separate messages. Note that this figure shows the same HTTP headers as Figure 1-6, but it also
shows a TCP header. The TCP header shows a sequence number (SEQ) with each message. In
this example, the network has a problem, and the network fails to deliver the TCP message
(called a segment) with sequence number 2. When Bob receives messages with sequence
numbers 1 and 3, but does not receive a message with sequence number 2, Bob realizes that
message 2 was lost. That realization by Bob’s TCP logic causes Bob to send a TCP segment
back to Larry, asking Larry to send message 2 again.

> **Same-layer interaction on different computers:**
>
> The two computers use a protocol to communicate with the same layer on another computer. The protocol defines a header that communicates what each computer wants to do.

> **Adjacent-layer interaction on the same computer:**
>
> On a single computer, one lower layer provides a service to  he layer just above. The software or hardware that implements the higher layer requests that the next lower layer perform the needed function.

### TCP/IP Network Layer

The lower layers of the TCP/IP model act more like the postal service to deliver those messages
to the correct destinations. To do so, these lower layers must understand the underlying physical network because they must
choose how to best deliver the data from one host
to another.
 the network layer of the TCP/IP network-
ing model, primarily defined by the Internet Protocol (IP), works much like the postal ser-
vice. IP defines that each host computer should have a different IP address, just as the postal
service defines addressing that allows unique addresses for each house, apartment, and busi-
ness. Similarly, IP defines the process of routing so that devices called routers can work like
the post office, forwarding packets of data so that they are delivered to the correct destina-
tions. Just as the postal service created the necessary infrastructure to deliver letters—post
offices, sorting machines, trucks, planes, and personnel—the network layer defines the
details of how a network infrastructure should be created so that the network can deliver
data to all computers in the network.

#### Internet Protocol Addressing Basics

IP defines addresses for several important reasons. First, each device that uses TCP/IP—each
TCP/IP host—needs a unique address so that it can be identified in the network. IP also
defines how to group addresses together.

Routers are networking
devices that connect the parts of the TCP/IP network together for the purpose of routing
(forwarding) IP packets to the correct destination. Routers do the equivalent of the work
done by each post office site: They receive IP packets on various physical interfaces, make
decisions based on the IP address included with the packet, and then physically forward the
packet out some other network interface.

#### IP Routing Basics

The TCP/IP network layer, using the IP protocol, provides a service of forwarding IP packets
from one device to another. Any device with an IP address can connect to the TCP/IP net-
work and send packets. This section shows a basic IP routing example for perspective.

> The term IP host refers to any device, regardless of size or power, that has an IP address and connects to any TCP/IP network.

### TCP/IP Data-Link and Physical Layers

The TCP/IP model’s data-link and physical layers define the protocols and hardware required
to deliver data across some physical network. The two work together quite closely; in fact,
some standards define both the data-link and physical layer functions. The physical layer
defines the cabling and energy (for example, electrical signals) that flow over the cables.
Some rules and conventions exist when sending data over the cable; however, those rules
exist in the data-link layer of the TCP/IP model.
Focusing on the data-link layer for a moment, just like every layer in any networking model,
the TCP/IP data-link layer provides services to the layer above it in the model (the network
layer). When a host’s or router’s IP process chooses to send an IP packet to another router
or host, that host or router then uses link-layer details to send that packet to the next host/
router.

Figure 1-11 shows four steps. The first two occur on Larry, and the last two occur on Router
R1, as follows:
1. Larry encapsulates the IP packet between an Ethernet header and Ethernet
trailer, creating an Ethernet frame.
2. Larry physically transmits the bits of this Ethernet frame, using electricity
flowing over the Ethernet cabling.
3. Router R1 physically receives the electrical signal over a cable and re-creates the
same bits by interpreting the meaning of the electrical signals.
4. Router R1 de-encapsulates the IP packet from the Ethernet frame by removing
and discarding the Ethernet header and trailer.

By the end of this process, Larry and R1 have worked together to deliver the packet from
Larry to Router R1.

> In short, the TCP/IP physical and data-link layers include two distinct functions, respectively: functions related to the physical transmission of the data, plus the protocols and rules
that control the use of the physical media.

## Data Encapsulation Terminology

The process by which a TCP/IP host sends data can be viewed as a **five-step process**. The
first four steps relate to the encapsulation performed by the four TCP/IP layers, and the last
step is the actual physical transmission of the data by the host. In fact, if you use the five-
layer TCP/IP model, one step corresponds to the role of each layer.

### Names of TCP/IP Messages
When talking and writing about networking, people use segment, packet,
and frame to refer to the messages shown in Figure 1-13 and the related list. Each term has a
specific meaning, referring to the headers (and possibly trailers) defined by a particular layer
and the data encapsulated following that header. Each term, however, refers to a different
layer: segment for the transport layer, packet for the network layer, and frame for the link
layer. The following table shows each layer along with the associated term.

|Association||
|--|--|
|TCP|Segment|
|IP| Packet|
|Ethernet| Frame|

OSI uses a more generic term to refer to messages, rather than frame, packet, and segment.
OSI uses the term protocol data unit (PDU). A PDU represents the bits that include the
headers and trailers for that layer, as well as the encapsulated data. For example, an IP packet, is a Layer 3 PDU
(abbreviated L3PDU) because IP is a Layer 3 protocol.

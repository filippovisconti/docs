---
tags: [Networks, Routing, Network-verification]
title: Network Verification
categories: adv-comm-net lecture-notes
math: true
---

## Introduction

You’re an ISP operator. A customer calls you: they cannot reach their favorite website anymore.

1st try: Check connectivity to the website from the closest router.

- PRO: excludes a lot of error sources
- CON: does not prevent the problem from happening (reactive, not proactive), very poor coverage (both with respect to time and location)

How could you prevent reachability problems caused by misconfigurations moving forward? 2nd try: Regularly monitor the connectivity from different locations in the network.

- PRO: detects (some) misconfigurations as soon they affect traffic
- CON: still does not prevent the problem (still reactive, not proactive), costly to run if one wants to achieve high coverage

3rd try: Simulate the network's behaviour in different situations (routing inputs, failures...).

- PRO: pro-actively detects (some) misconfigurations
- CON: hard to provide guarantees (exponential number of situations), simulator-reality mismatch (false positives/negatives)

How can you guarantee reachability without simulating all scenarios? Using network verification!

{: .prompt-tip} >

> - routing/forwarding behavior (internal and external)
> - security policies (force passing firewall, DMZ)
> - performance (congestion, delay, packet loss)
> - other properties (e.g., convergence guarantees)

{: .prompt-tip} >

> - external routing inputs
> - failure scenarios
> - traffic demands

Verification either succeeds, or finds a counter-example. ![shutup](/assets/img/ScreenShot%202024-01-15%20at%2011.46.52.png)

Spectrum: From Validation to Verification ![shutup](/assets/img/ScreenShot%202024-01-15%20at%2011.47.20.png)

Example: ![shutup](/assets/img/Pasted%20image%2020240115115159.png)

### Key idea

Represent the network as a boolean formula which captures the network’s outputs given its inputs

- Model the network symbolically, as a combinatorial circuit
  - (as often done in the hardware literature).
- Model the network’s inputs/outputs and the semantic of the routing protocols using boolean variables and constraints on these variables.
  - These constraints specify how the inputs / outputs relate to each other.
- Given a boolean formula, use theorem provers to assess the satisfiability of the formula.
  - Find assignments to the variables that are compatible with the constraints, such that the entire formula is true, if possible.

Modeling the network behavior symbolically allows to use an automatic theorem-prover (Z3, an SMT - Satisfiability Modulo Theories - solver) for verification.

![shutup](/assets/img/Pasted%20image%2020240115115401.png)

SMT formulas support constraints in first-order logic. ![shutup](/assets/img/Pasted%20image%2020240115115426.png)

Using a solver requires to model everything symbolically. Topology and configuration are encoded in a symbolic network model. The specification provides constraints on the routing state. The
environments provide constraints on the routing inputs.

Once we have modelled everything symbolically, how do check if the specification holds in all the possible environments?

> Can the symbolic network model and the environment constraints be satisfied, while the specification 𝜓 is violated? ![shutup](/assets/img/Pasted%20image%2020240115115637.png) If satisfiable, then $𝜓$ does
> not hold for all Env ⇒ assignment is a counter-example. If unsatisfiable then $𝜓$ holds for all Env (= verified).

## Components of the SMT Encoding

1. Symbolic Network Model
   - Routing state:
     - Variables that describe the routing state of each router.
   - Routing semantics:
     - Route propagation
     - Route selection
     - Route transformation
2. Specification $𝜓$
3. Environment constraints

### Routing state

The routing state models one selected route per router. ![shutup](/assets/img/Pasted%20image%2020240115115931.png) If the router does not learn a route, the route is not _available_. LocalPref, NextHop (BGP
NextHop is not the forwarding next hop) and AsPath are BGP route attributes.

> We only consider one IP prefix each time (no symbolic IP prefix). We assume that different IP prefixes do not interfere with each other.

Each router must select a route from one of its neighbours. ![shutup](/assets/img/Pasted%20image%2020240115120133.png) The SelectsFrom field encodes the router advertising the best route.

![shutup](/assets/img/Pasted%20image%2020240115120235.png) Each router propagates its selected route to neighbours. ![shutup](/assets/img/Pasted%20image%2020240115120414.png)

When can rA select a route from rB? `rA.SelectsFrom == rB.id ⇒ Enc["rB propagates to rA"] ∧ rA.Route == rB.Route` ![shutup](/assets/img/Pasted%20image%2020240115120531.png)

> In reality, rA doesn’t see rB’s original route, but a "transformed" version of it. (example: BGP NextHop)

Each session of rA can be modelled identically. ![shutup](/assets/img/Pasted%20image%2020240115120522.png) But which route does rA actually select? Let’s assume rA selects rC's route. Then, rA must prefer
rC’s route over rB’s route. In other words, rB’s route must be rejected in favour of the selected route.

- preferred with respect to BGP's route selection
- i.e., higher local preference value, shorter AS Path length, etc.

`rA.SelectsFrom ≠ rB.id ∧ Enc["rB propagates to rA"] ⇒ rA.Route > rB.Route` We obtain two constraints for the session rB → rA. ![shutup](/assets/img/Pasted%20image%2020240115121102.png)
![shutup](/assets/img/Pasted%20image%2020240115121108.png) Have we considered all routing semantics?

![shutup](/assets/img/Pasted%20image%2020240115121119.png)

Let’s assume only rC propagates its route to rA.

![shutup](/assets/img/Pasted%20image%2020240115121137.png) (...)

rA selects from someone if and only if anyone propagates to rA. `Enc["rA selects from someone"] ⇔ Enc["rA receives any route"]` ![shutup](/assets/img/Pasted%20image%2020240115121545.png)
![shutup](/assets/img/Pasted%20image%2020240115121557.png)

### Specification

We encode 𝜓 as constraints on the routing states.

- "Always prefer the route from the customer."
- "Never transit routes between two providers."
- "Always tag every incoming route."

We could also extend 𝜓 to verify forwarding (BGP + OSPF + static routes) states.

- "All packets traverse the waypoint X."
- "There is no packet forwarding loop."
- "Load balancing for packets from X to Y."

#### 𝜓: "Always prefer the route from the customer."

`Enc["customer advertises a route"] ⇒ Enc["all routers select the customer’s route"]` ![shutup](/assets/img/Pasted%20image%2020240115121754.png) ![shutup](/assets/img/Pasted%20image%2020240115121804.png)

### Environment constraints

Env encodes constraints on the routing inputs. We consider any(∀) valid routing inputs from external neighbours.

## Example

```python
from z3 import *
from example import net, NetworkModel, Customer, A, B, C, D
## define the specification
Spec = Implies(Customer.Route.Available,
    And(C.SelectsFrom == Customer.id,
     A.SelectsFrom == C.id,
     B.SelectsFrom == C.id,
     D.SelectsFrom == C.id))
s = Solver()
s.add(NetworkModel) ## pre-encoded in example.py
s.add(Not(Spec))

s.check() ## runs the solver, returns 'sat'
print(s.model()) ## print the complete model

net.pprint(s) ## print the formatted counter-example
```

Symbolic variables describe the advertised routes. ![shutup](/assets/img/Pasted%20image%2020240115152104.png)

The solver must assign these variables to violate the specification ⇒ counter-example.

Symbolic variables describe each router’s selected route. ![shutup](/assets/img/Pasted%20image%2020240115152159.png) The solver cannot assign arbitrary values to routing state variables. Equations constrain
the routing state on the routing inputs. BGP semantics describe how the routing inputs affect the routing state. We must come up with equations that capture this semantics for SMT.

![shutup](/assets/img/Pasted%20image%2020240115152258.png)

Routers learn their selected route from a neighbour.

![shutup](/assets/img/Pasted%20image%2020240115152451.png)

The SelectsFrom field Can be either:

- the ID of a neighbor,
- or invalid.

![shutup](/assets/img/Pasted%20image%2020240115152545.png) ![shutup](/assets/img/Pasted%20image%2020240115152557.png) ![shutup](/assets/img/Pasted%20image%2020240115152650.png)
![shutup](/assets/img/Pasted%20image%2020240115152704.png) ![shutup](/assets/img/Pasted%20image%2020240115152719.png)

> What does rA receive from rB in BGP? The Available field could change because a route map could drop a route. The LocalPref field could change because a route map could modify the value. The nextHop
> field will necessarily be set to rB. ![shutup](/assets/img/Pasted%20image%2020240115152943.png)

### How can we express this in SMT?

![shutup](/assets/img/Pasted%20image%2020240115153204.png) The route rA receives from rB is not the route that rB selects! All variables of B->A.Route depend on rB.Route! ⇒ No variables necessary!

### The transformed attributes are symbolic expressions

![shutup](/assets/img/Pasted%20image%2020240115153220.png)

![shutup](/assets/img/Pasted%20image%2020240115153304.png)

![shutup](/assets/img/Pasted%20image%2020240115153310.png)

### Routers learn their selected route from a neighbour

![shutup](/assets/img/Pasted%20image%2020240115153342.png) ![shutup](/assets/img/Pasted%20image%2020240115153354.png) ![shutup](/assets/img/Pasted%20image%2020240115153421.png)
![shutup](/assets/img/Pasted%20image%2020240115153441.png) ![shutup](/assets/img/Pasted%20image%2020240115153538.png)

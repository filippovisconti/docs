---
tags: [Networks, Routing, Network-synthesis]
title: Network Synthesis
categories: adv-comm-net lecture-notes
math: true
---

## Repairing the network is not always easy

- A **counter** example **does not** show the **mistake**, much less how to fix it.
- The **operator** must **consider** the **entire** specification, not just the part that is violated.
- What if the configuration does not meet a performance objective?
  - **Finding** the **optimal** configuration is **very** **difficult**.

## Configuration Synthesis

Find a configuration that satisfies the specification.
![shutup](/assets/img/Pasted%20image%2020240115153736.png){: width="50%"}
![shutup](/assets/img/Pasted%20image%2020240115153754.png){: width="50%"}

**Configuration** synthesis makes **verification** **obsolete**, **if** the **synthesizer** is **complete** (always finds a solution if one exists).

This is thanks to:

- **Automatic** configuration **repair**
- **Intent**-based networking
- Network **optimization**

## How to synthesize configurations (SMT + CEGIS)

**Find** a configuration for which the **specification** is **satisfied** for **all** environments.

> SMT can **only** find an **assignment** of variables that **make** a **formula** **true**.
>
> ⇒ We need to parametrize the configuration
{: .prompt-warning}

For network **synthesis**, we **parametrize** the **configuration**.

- Link weights
- Route maps
- ...

1. Create symbolic variables for each parameter
2. Write the network equations in terms of those parameters.
3. Let SMT do its magic.
4. Reconstruct the configuration from the model.

Parameters can simply be **constants** in the **configuration** that are yet **unknown**. **Replace** all constants in the symbolic network equations **with** **symbolic** variables that **represent** the parameters.
![shutup](/assets/img/Pasted%20image%2020240115170036.png){: width="50%"}

Can the network running configuration C compute state Y under inputs X? $$𝝍(Y): specification$$
![shutup](/assets/img/Pasted%20image%2020240115154025.png){: width="50%"}

> Steady state equations with configuration parameters: $$Net(X,Y,C)$$

Can the network running configuration C compute state Y under inputs X?
$$\text{find } C \text{ such that } ∀ X, Y: Net(X,Y,C) ⇒ 𝝍(Y)$$

> If the network computes state Y from inputs X, then the specification must be satisfied.
{: .prompt-tip}

SMT uses many techniques / heuristics to deal with quantifiers. It might take too long to find a solution (or SMT might return undecidable).

![shutup](/assets/img/Pasted%20image%2020240115171625.png)

### Verification vs Synthesis

For **verification**, we can **avoid** quantifiers.

> **Verification**
>
> Find one set of routing inputs such that the specification is violated.
{: .prompt-tip}

For **synthesis**, we **need** them.

> **Synthesis**
>
> Find a configuration for which the specification is satisfied **for** **all** routing inputs.
{: .prompt-tip}

### What does SMT do with the universal quantifier $\forall$?

$∀$ routing inputs : the corresponding routing state satisfies the specification. ![shutup](/assets/img/Pasted%20image%2020240115154314.png) There are a lot of possible routing inputs! SMT scales
exponentially in the input size.

> **Idea**
>
> Find a configuration for only a few inputs env and hope that the configuration works for all inputs.
{: .prompt-info}

Does the the configuration work for all inputs? ⤷ Use verification.

Which inputs should we consider in env? ⤷ Use the counter examples from the verification.

### Counter Example Guided Inductive Synthesis (CEGIS)

![shutup](/assets/img/Pasted%20image%2020240115154538.png)
![shutup](/assets/img/Pasted%20image%2020240115172110.png)

#### Example

![shutup](/assets/img/Pasted%20image%2020240115154550.png)

|The configuration satisfies the specification if $C_{cust} > C_{prov}$|![shutup](/assets/img/Pasted%20image%2020240115154617.png)|
|Let’s pick parameters $C_{cust}, C_{prov}$ "randomly".|![shutup](/assets/img/Pasted%20image%2020240115154641.png)|
|The verifier finds a counter example x1:|![shutup](/assets/img/Pasted%20image%2020240115154656.png)|
|x1 "invalidates" the parameter space where $C_{cust} < C_{prov}$|![shutup](/assets/img/Pasted%20image%2020240115154720.png)|
|The synthesizer then picks parameters that satisfy x1|![shutup](/assets/img/Pasted%20image%2020240115154755.png)|
|The synthesizer then finds a counter example x2|![shutup](/assets/img/Pasted%20image%2020240115154815.png)|
|x2 "invalidates" the parameter space where $C_{cust} = C_{prov}$|
|The synthesizer picks parameters that satisfy x1 and x2.|![shutup](/assets/img/Pasted%20image%2020240115154855.png)|

### How can we implement the network behavior in SMT?

We describe the network behavior using equations.

|![shutup](/assets/img/Pasted%20image%2020240115165559.png)|![shutup](/assets/img/Pasted%20image%2020240115165613.png)|
|![shutup](/assets/img/Pasted%20image%2020240115165725.png)||
|![shutup](/assets/img/Pasted%20image%2020240115165802.png)|![shutup](/assets/img/Pasted%20image%2020240115165746.png)|
|![shutup](/assets/img/Pasted%20image%2020240115165911.png)||

### How can we implement the synthesis block in SMT?

Goal: $$\text{find } C \text{ such that } ∀ X, Y: [X∈ env ∧ Net(X,Y,C)] ⇒ 𝝍(Y)$$ We still have the ∀ quantifier here (first-order logic). The solver may not be able to solve this problem efficiently.

### Implementation

We only iterate over the environments from our counter examples!

|![shutup](/assets/img/Pasted%20image%2020240115172301.png)|![shutup](/assets/img/Pasted%20image%2020240115172327.png)|

Configurations can be **arbitrarily** complex. What configuration parameters to consider? We need to decide which parameters to include!

- Too **few** parameters
  - ⇒ solution may **not** **exist**!
- Too **many** parameters
  - ⇒ configuration too **complex** for humans to understand.
  - ⇒ configuration can **only** cover the counter examples as corner cases.

> **Idea**:
>
> - **Start** with a **small** configuration space C.
> - **Synthesize** configurations **from** the space **C**.
> - **If** **no** **configuration** within C "**works**", **increase** **C**.
{: .prompt-tip}

![shutup](/assets/img/Pasted%20image%2020240115172551.png)

### Will CEGIS always terminate?

We have four observations:

1. $C_i$ gets smaller in each step,
    - i.e., $$C_{i+1}\subset C_i$$
2. $C_i$ always includes all configurations,
    - i.e.,$$C_{sol} \subseteq C_i$$
3. We synthesize configurations from $C_i$,
    - i.e.,$$C_{i+1}\in C_i$$
4. $C_i$ can be infinite.

> In **theory**, CEGIS might run **forever**. In **practice**, CEGIS is **efficient**.
{: .prompt-warning}

## Applying synthesis to different networking tasks

All it takes is to **view** the **problem** **from** a **different** **perspective**.

### Configuration repair

Synthesize a **correct** configuration that is similar to the original configuration.
![shutup](/assets/img/Pasted%20image%2020240115173024.png){: width="50%"}

Configuration **repair** is just **synthesizing** a configuration that **maximizes** the **similarity** to the old configuration.

Use **Syntax** **Guided** Synthesis:

1. **Start with** the configuration space C to **only** contain the **old configuration**.
2. **Increase** the configuration space C slightly **when** the **synthesis** step **fails**
   - ⇒ We will synthesize a configuration that is similar to the initial configuration.

### Optimization

|Can we find a configuration that maximizes an optimization function?|![shutup](/assets/img/Pasted%20image%2020240115173121.png)|

Performance **properties** depend on **all** destinations! But our current network **model** only considers a **single** destination at a time.

- SMT is NP-Complete
- With only a single destination, SMT takes **minutes** to find a solution (for small to medium sized networks).

Some synthesis problems in Networking are **better** **suited** **for** tools like **Linear** **Programming** than for SMT.

Let’s assume a **central** controller to configure the FIBs. A **single** entity **computes** the network-wide **forwarding** **state**, and then **configures** the **actual** routing **tables** accordingly.

- We are **given** the current traffic **demand** for each source-destination **pair**.
- Allocate network **paths** such that **maximum** link **utilization** is **minimized**.
  - ⇒ **Distribute** the traffic **equally** in the network
  - ⇒ Allow the largest deviation in traffic demand

### Configuration is not the only thing we can synthesize

|Can we understand what the network does?|![shutup](/assets/img/Pasted%20image%2020240115173254.png)|

Find the **largest** specification that a **configuration** **satisfies** in a given **set** of **environments**.

- Config2Spec finds the maximal set of specifications that are implemented by the configuration.
- The list is too large for humans to understand what the network actually does.

|In **which** **environments** does the network what we **want**?|![shutup](/assets/img/Pasted%20image%2020240115173352.png)|

Find the set of environments in which the network satisfies a given specification.

- Invert the specification ⇒ get the entire space of counter examples.
- How "**robust**" is the network **against** **external** events and **failures**?

### How to safely reconfigure a network?

A **reconfiguration** triggers a **convergence** process. Each **intermediate** state must **satisfy** the **specification**.

- Idea: synthesize intermediate configuration
 ![shutup](/assets/img/Pasted%20image%2020240115173519.png)

### Research projects

Snowcap finds an ordering of reconfiguration commands. Chameleon synthesizes temporary configurations that guarantee safety in all transient states during convergence. The network reconfiguration
problem is all about planned events.

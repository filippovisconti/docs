---
tags: [Parallel-computing, Multithread, Questions]
title: "DPHPC Exam Questions"
categories: dphpc lecture-notes
math: true
---

# Questions

## Implement `MPI_Barrier(MPI_Comm comm)`

It blocks all processes calling it, until all processes in `comm` have called this function. The efficiency of your implementation is not important for this task, only correctness.

```c
void MPI_Barrier(MPI_Comm comm){
 int buf, rank, size;

 MPI_Comm_rank(comm, &rank);
 MPI_Comm_size(comm, &size);
 int tag = 42;
 if (rank == 0){

  for(int rank = 1; rank < size; rank++)
   MPI_Recv(&buf, 1, MPI_INT, i, tag, comm, MPI_STATUS_IGNORE);


  for(int rank = 1; rank < size; rank++)
   MPI_Send(&buf, 1, MPI_INT, i, tag, comm);
 } else {
 buf = 99;
 MPI_Send(&buf, 1, MPI_INT, 0, tag, comm);
 MPI_Recv(&buf, 1, MPI_INT, 0, tag, comm, MPI_STATUS_IGNORE);

 }
}

int main(char* argv[], int argc){
 MPI_init(&argv, &argc);
 MPI_Barrier(MPI_COMM_WORLD)
 MPI_Finalize();
}
```

## Outline in detail a depth optimal algorithm to compute the sum of two $N\times N$ matrices

Depending on the number of processors, divide the matrices into blocks (or submatrices) and assign each block to one processor. Now each processor will perform a matrix addition on the assigned
blocks, executing ${\frac n b}^2$ additions.

## What is the work, depth and average parallelism of your algorithm?

The total work will be $W(n) = n^2$, while the depth will be dependant on how many processors we have. If we have $n^2$ processors, the depth would be $1$. This means that$\text{ for } p\rightarrow
\infty, D(n)= 1$. The average parallelism is thus $n^2$.

## A task has a sequential fraction of 40%. What is the best possible speedup for that task using Amdahl's law?

According to Amdahl's law, it's $\frac 1 {0.4} = 2.5$

### How many parallel processing units are required to complete the task 4 times faster than the sequential execution?

It's impossible to achieve. With infinitely many processors, the maximum speedup, according to Amdahl's law, is 2.5.

## What does it mean to say a program is data oblivious? Give a definition

For each problem size, The execution trace, the memory locations read and written do not depend on any input, and are determined by the input size.

## What does it mean to say a program is structurally oblivious? Give a definition

The code does only contain if-statements which depend on the input variables that contain the problem size, and no other input.

## Draw a roofline plot for this system

Assume a system with a CPU that has peak performance $\pi$ of 4 single precision FLOPS per cycle, and with a memory bandwidth $\beta$ of 8 bytes per cycle. The last level cache is directly mapped and
has size $w$ 2MiB.

Horizontal line at 4 FLOPS/cycle

Intersection at $\pi=\beta I\rightarrow 4 = 8I\rightarrow I = \frac 1 2$

Diagonal line defined by $y= \beta I= 8I$.

![Roofline Plot](/assets/roofline.svg){: width="800"}

## Describe the difference between the greedy and work-stealing scheduling strategies

In the greedy scheduling strategy, there is a central algorithm that tries to assign work to processors, hopefully in a uniform manner.

In the work-stealing scheduling strategy, each processor runs a distributed algorithm, which starts with a uniform distribution of work, and then, if a processor finishes its work, it will steal work from another peer which still has work in the queue.

## What is the advantage of using a work-stealing scheduler instead of a greedy one?

It's more efficient in case work is not evenly distributed among processors. This is because idle workers can steal work from overloaded workers.

## What is the difference between strong- and weak-scaling?

Strong scaling measures the speedup for a fixed problem size as $p\rightarrow \infty$ . Basically, complete the same amount of work faster. It focuses on keeping the problem size constant and
increasing the number of processors to see how performance improves.

Weak scaling measures the speedup as $p\rightarrow \infty, n\rightarrow \infty$ . In other words, more processors allow us to do more work. It scales both the problem size and the number of processors
to maintain a balanced workload per processor and assess the system's ability to handle larger problems efficiently.

## State the difference between spatial and temporal locality

Spatial locality anticipates the usage of data stored in adjacent memory areas (e.g. if you access 1 element of an array, you will probably also need the second). Temporal locality anticipates that
previously used data might be used again in the near future.

## State the difference between cache coherence and memory consistency

Both aim to ensure that data is maintained up to date. However, cache coherence takes care of the problem of multiple copies of the same memory location in different caches, whereas memory consistency
takes care of propagating changes made in a single cache to main memory, often by multiple processors.

- **Focus:**
  - **Cache Coherence:** Focuses on ensuring that different caches have consistent copies of shared data.
  - **Memory Consistency:** Focuses on establishing rules for the order in which memory operations are observed across different processors.

- **Concern:**
  - **Cache Coherence:** Primarily addresses the issue of maintaining consistency among cached copies of shared data.
  - **Memory Consistency:** Primarily addresses the order in which memory operations become visible to different processors.

- **Mechanisms:**
  - **Cache Coherence:** Implemented through cache coherence protocols (e.g., MESI) that dictate how caches interact to keep data consistent.
  - **Memory Consistency:** Implemented through memory consistency models that define the rules for ordering memory operations across processors.

## What is the difference between write-through and write-back?

These are two different write policies for caches. With a write-through policy, as soon as a data in cache is modified, the modification is perpetuated to main memory. A write-back policy, however,
propagates the modification in a lazier way, waiting as much as it can, until the cache line needs to be evicted. Only at that point will the modification be propagated to main memory.

## What is the difference between write-allocate and no-write-allocate?

On a write miss, with a write-allocate policy, data is loaded into cache and then modified by the CPU. With a no-write-allocate policy, the CPU writes data straight to memory, bypassing the cache.

## What is the difference between program order and visibility order?

Program order is the order according to which instructions are executed by a single processor.

Visibility order is the order in which memory operations are observed by different processors.

## What is the difference between the shared memory model and the message passing model?

In the shared memory model, multiple processors share the same address space. In the message passing model, each processor has its own memory space, and communication between processors is done by
sending messages, explicitly, and requiring manual synchronization.

## What does it mean for an algorithm to be balanced with respect to a given architecture?

Compute time = Data transfer time

## Describe the difference between a memory bound and a compute bound application

A memory bound application's performance is limited by the memory bandwidth, while a compute bound application's performance is limited by the peak performance of the CPU.

This is because a memory bound application performs very few operations on each data element (low computational intensity), while a compute bound application performs many operations on each data element (high computational intensity).

A memory bound application basically doesn't use the CPU much, while a compute bound application uses the CPU a lot, and "wastes" time transferring data.

## Cache exercise

Assume a system with 4KiB of RAM, and a 2-way associative LRU cache, with a total size of 256B and cache blocks of 32B. The addresses are in the format (tag, set, offset). The cache is initially
empty. The size of a double is 8 bytes.

### Fill the Table 1 by specifying the tag, set and offset bits of the accessed memory location, and if it leads to a cache miss

| Address | in Binary          | Tag | Set | Array Index | Column | Offset | Miss? | Notes |
| ------- | ------------------ | --- | --- | ----------- | ------ | ------ | ----- | ----- |
| `0x050` | `0b00000-10-10000` | 0   | 2   | 10          | 2      | 16     | Yes   |       |
| `0x028` | `0b00000-01-01000` | 0   | 1   | 5           | 1      | 8      | Yes   |       |
| `0x158` | `0b00010-10-11000` | 2   | 2   | 43          | 3      | 24     | Yes   |       |
| `0x0E0` | `0b00001-11-00000` | 1   | 3   | 28          | 0      | 0      | Yes   |       |
| `0x040` | `0b00000-10-00000` | 0   | 2   | 8           | 0      | 0      | No    |       |
| `0x080` | `0b00001-00-00000` | 1   | 0   | 16          | 0      | 0      | Yes   |       |

### Use table 2 to show the cache state after the last access

| set # | Block 0 c0 | c1    | c2     | c3 | Block 1 c0 | c1 | c2 | c3     |
| ----- | ---------- | ----- | ------ | -- | ---------- | -- | -- | ------ |
| Set 0 | **16**     | 17    | 18     | 19 |            |    |    |        |
| Set 1 | 4          | **5** | 6      | 7  |            |    |    |        |
| Set 2 | **8**      | 9     | **10** | 11 | 40         | 41 | 42 | **43** |
| Set 3 | **28**     | 29    | 30     | 31 |            |    |    |        |

## Cache exercise 2

Assume a machine with 32-bit addresses and 4 processors with directly mapped L1 caches. Each cache is 4 MiB in size, with 128B wide cache lines. MESI is used as a cache-coherency mechanism. The memory
is byte addressable.

### How many bits of the 32-bit address are used for the tag, set and offset?

- Offset $o=\log_2(128)=7$ bit
- Set $s=\log_2(\frac {\text{Cache size}} {\text{Cache line size }\cdot \text{ associativity}})= \log_2(\frac {4MiB} {128B}) = \log_2(\frac {2^{22}} {2^7})= \log_2(2^15) = 15$ bit
- Tag $t=32- 15 -7=10$ bit

### For the following addresses, fill in the table. Fill only the fields that change their value after an instruction

| Instr                | P1 CL | P1 State | P2 CL | P2 State | P3 CL | P3 State | P4 CL | P4 State | Bus Signal |
| -------------------- | ----- | -------- | ----- | -------- | ----- | -------- | ----- | -------- | ---------- |
| `P1:R(0xFF0-001001)` | 32    | E        |       |          |       |          |       |          | BusRd      |
| `P2:R(0xFF0-001034)` | 32    | S        | 32    | S        |       |          |       |          | BusRd      |
| `P3:W(0xFF0-040023)` |       |          |       |          | 2048  | M        |       |          | BusRdX     |
| `P1:W(0xFF0-001023)` | 32    | M        | 32    | I        |       |          |       |          | BusRdX     |
| `P3:R(0xFF0-040078)` |       |          |       |          | 2048  | M        |       |          | BusRd      |
| `P4:W(0xFF0-040000)` |       |          |       |          | 2048  | I        | 2048  | M        | BusRdX     |

Note that `P3:R(0xFF0-040078)` doesn't change the cache line state, because it's already in the M state, available in `P3` cache.

### For these other addresses, fill in the table. Fill only the fields that change their value after an instruction

| Instr               | P1 CL | P1 State | P2 CL | P2 State | P3 CL | P3 State | P4 CL | P4 State | Bus Signal |
| ------------------- | ----- | -------- | ----- | -------- | ----- | -------- | ----- | -------- | ---------- |
| `P1:R(0x001-00041)` | 0     | E        |       |          |       |          |       |          | BusRd      |
| `P3:R(0x001-00159)` |       |          |       |          | 8194  | E        |       |          | BusRd      |
| `P1:R(0x001-00178)` | 8194  | S        |       |          | 8194  | S        |       |          | BusRd      |
| `P4:W(0x001-0014E)` | 8194  | I        |       |          | 8194  | I        | 8194  | M        | BusRdX     |
| `P2:R(0x001-00186)` |       |          | 8195  | E        |       |          |       |          | BusRd      |
| `P1:W(0x001-00186)` | 8195  | M        | 8195  | I        |       |          |       |          | BusRdX     |

## What is a memory model? Why is it useful?

A memory model is a set of rules that governs the order in which memory operations are observed by different processors. It is useful because it allows for optimizations, and it allows programmers to
have guarantees about the order in which memory operations are observed. It needs to be specified in order to write correct programs.

## What is the difference between x86 memory model and sequential consistency?

The x86 memory model allows reads to be re-ordered with older writes if these concern different memory locations.

## Define the starvation- and deadlock-freedom properties of a lock

A **starvation**-free lock ensures that, eventually, each thread which require access to a critical region will be granted access.

A **deadlock**-free lock ensures that if there are threads waiting for access to a critical region, then at least one of them will eventually be granted access.

The starvation-freedom property implies the deadlock-freedom property.

## Describe the Lamport's bakery algorithm

In the Lamport's bakery algorithm, each thread wanting to access the critical region is assigned a ticket number (like in a bakery). The ticket is, obviously, incremented at each request. While there
are threads with a lower ticket number, the thread will wait. When it is its turn, it will enter the critical region. When it is done, it will set its ticket number to 0.

### Is it starvation-free?

Yes, as each thread will eventually be granted access to the critical region. No thread can access the critical region infinitely many times in a row (if there are other threads waiting).

### Is it deadlock-free?

Being starvation-free, it is also deadlock-free, since the starvation-freedom property implies and is stronger than the deadlock-freedom property.

## Assume a linked list `L` is shared among $n>2$ threads

### Fill in the table

| Locking Scheme | Advantage           | Disadvantage      |
| -------------- | ------------------- | ----------------- |
| Coarse-grained | Easier to implement | Worse performance |
| Fine-grained   | Better performance  | More complex      |

### The `L.contains(x)` method returns true if `x` is in the linked list. Can this method be implemented in a wait-free manner? If so, how?

Every algorithm can be implemented in a wait-free manner, assuming an atomic operation with infinite consensus number is available, such as a Compare-and-Swap. However, it will not necessarily be
fast.

## Performance Models questions

Assume a search engine receives a search query every $0.1$s. It takes $0.4$s to serve a query.

### If a query needs $8$KiB of memory to be stored, how much memory does the search engine need to buffer the incoming search queries?

Number of queries in buffer $N=\lambda \cdot \text{ time spent in queue}=\frac 1 {0.1} 0.4 = 4$, according to Little's law.

Each query needs $8$KiB of memory, so the total memory needed is $4\cdot 8$ KiB = $32$ Kib.

### To serve a query, the search engine spends the $40\%$ in a serial computation. The degree of parallelism can be increased by a factor of $6$. Use Amhdal's law to give an upper bound on the expected speedup

The speedup is given by $S=\frac 1 {0.4 + \frac {0.6} 6} = \frac 1 {0.5} = 2$

### Assume a single-core system with an LRU data cache, a peak performance of $\pi=4$ FLOPS/cycle and a memory bandwidth of $\beta=8$ bytes/cycle and a memory bandwidth $\beta=8$ bytes/cycle

The ridge point is at $I=\frac \pi \beta = \frac 4 8 = \frac 1 2$.

### Consider the following function operating on a matrix `A` (row major order) of $n^2$ floats

Assume that the cache size $\gamma$ is much smaller than $n$ and that a cache block has size 64 bytes. The cache is initially empty.

```c
void foo(float A[n][n]){
    for(int j = 0; j < n; j++)
        for(int i = 1; i < n; i++)
            A[0][j] = A[0][j] + A[i][j];
}
```

#### What is the operational intensity of the code above?

$$I(n)=\frac {W(n)} {Q(n)}= \frac {\text{num FLOPS}} {\text{bytes transferred between cache and RAM}}$$

$W(n)=n(n-1)$ FLOPS

$n$ misses from `A[0][j]`

$8n(n-1)$ misses from `A[i][j]`

$8$ bytes per element.

Thus, $Q_m=8*(n+8n(n-1))$ bytes.

This results in $I(n) = \frac {n(n-1)} {8(n+8n(n-1))}= \frac {n(n-1)} {8n(1+8(n-1))}=\frac {(n-1)} {8 +64(n-1)} \approx \frac {(n-1)} {64(n-1)} = \frac 1 {64} < \frac 1 2$, which is the ridge point,
meaning the turning point between memory and compute bound operations.

#### Is it compute or memory bound on this system?

This means that the function is memory bound on this system.

### Compute the operational intensity of the given code and say if it is memory or compute bound with respect to the given system

$\pi=8\text{ FLOPS/cycle }, \beta=16\text{ bytes/cycle } \rightarrow \text{ridge point}=\frac {\pi} {\beta} = \frac 1 2$

```c
float a[N], b[N], c[N]; // c is always in cache
float acc = 0;          // acc assumed in a register, or always in cache

for (int i = 0; i < N; i++){
    c[i] = a[i] * b[i];
    acc += c[i];
}
```

#### Operational intensity

$W(n)=2n$, having 2 operations per iteration, and having $n$ iterations.

$Q(n)=2n \text{ elements} = 4\cdot 2n \text{ bytes}= 8n \text{ bytes}$, being the  number of misses from `a[i]` + number of misses from `b[i]`

$I(n)=\frac {W(n)} {Q(n)}=\frac {2n} {8n}=\frac 1 4 < \frac 1 2$, which means that the function is memory bound.

### Cache size scaling

Assume a program with an $I(n)=\theta(\sqrt \gamma)$ that is balanced with respect to a given architecture (single-core).

#### If the peak performance ($\pi$) doubles every 2 years and the memory bandwidth ($\beta$) doubles every 4 years, with which yearly rate does the cache size $\gamma$ need to increase in order to keep the balance?

After 4 years, $\pi'=4\pi,\beta'=2\beta$.

Since the operational intensity (and thus the ratio between peak performance and memory bandwidth) needs to stay the same, $\frac {4\pi} {2\beta}=\sqrt {\gamma'}$ and $\frac {\pi} \beta =(\sqrt
\gamma)$. This results in $\sqrt {\gamma'}=2\sqrt {\gamma}=\sqrt {4\gamma}$, by substituting $\frac {\pi} {\beta}$.

This means that the cache size needs to increase by a factor of $4$ every 4 years, or $\sqrt2$ every year.

### Upgrade a system from 1 to 4 cores. The computation is parallel for 80% of the time. The rest is sequential. What is the maximum expected speedup?

According to Amdahl's law, the maximum speedup is calculated with the formula $\frac 1 {\text{sequential fraction}+\frac {\text{parallel fraction}}{\text{num processors}}} = \frac 1 {0.2 + \frac {0.8} 4} = 2.5$

## LogOP Questions

A process $i=0$ needs to broadcast $k$ messages of $s$ bytes to the remaining $n-1$ processes. The processes communicate in a linear fashion, i.e. $0\rightarrow 1\rightarrow 2\rightarrow \dots
\rightarrow n-1$.

### Express the total cost of this broadcast as function of the latency $\alpha$ and the cost per byte $\beta$

We need to send $k(n-1)$ messages, of size $s$ bytes.

The latency cost will be paid once per processor, assuming that the messages are sent one right after the other. We are assuming that $\alpha$ is the latency cost paid by each processor when sending
the first message.

$$C_1 = (n-1)\alpha$$

The bandwidth cost will be paid for each message, and for each processor. This means that the total bandwidth cost will be $$C_2=k(n-1)s\beta$$

The final total cost will be $$C = C_1 + C_2 = (n-1)(\alpha + ks\beta)$$

If, however, we can assume that a processor can send a message to the next processor while receiving a message from the previous one, then the latency cost will be paid only once, and not $n-1$ times.

## Define false sharing and describe how it can affect the performance of an application

False sharing is a performance issue where a parallel program doesn't scale well because of the way the data is laid out in memory. It occurs when two or more threads are accessing data residing in
the cache line, which is thrown around between cores. This means that the threads are constantly invalidating each other's cache lines, which is expensive.

## When does false sharing occur? How can it be limited?

False sharing occurs when two or more threads are accessing data residing in the same cacheline. One way to limit it is to pad the data so that each thread accesses data in a different cacheline.

## Can a Test-And-Set lock result in poor performance? If yes, how can it be improved?

Yes, because the lock is busy-waiting, meaning the threads loop until they can manage to get a lock, which is expensive because cache lines are thrown around between cores. Also, TAS in x86 is a full
memory barrier.

It can be improved using a Test-and-Test-And-Set lock, which first checks if the lock is free, and only then uses the Test-And-Set lock. By doing this, most accesses are read only, which are faster
since.

To further avoid contention, exponential backoff can be used.

## What is the semantic of a memory barrier?

It's an instruction that prevents the CPU from reordering memory operations across the barrier.

## What does it mean for a class to solve the n-tread consensus? State one requirement that a consensus protocol has to satisfy

A class of consensus protocols solves the n-thread consensus, wait-free problem if there exists a consensus protocol that uses any number of objects from the class and any number of atomic registers

- Consistency: all threads decide on the same value
- Validity: the decided value must be proposed by one of the threads

## Describe the function of write buffers and explain how they can harm sequential consistency

Write buffers are used to avoid writing data back to memory, in order to improve performance. They can harm sequential consistency because they might prevent other processors to see that data has indeed been updated, but the update has not been propagated back to main memory.

## Give an example where write buffers invalidate sequential consistency

For example, if a thread writes to a variable, and then another one reads it right after, it might read the old value, because the write is still in the write buffer.

More formally, the total order $P_1:W(x,1) \rightarrow P_2:R(x,1)$ is sequentially consistent.

However, when using write buffers, $P_1:W(x,1)$ may not be visible to P2. Therefore, this could lead to the following (non-sequentially consistent) total ordering: $P_1:W(x,1) \rightarrow P2:R(x,0)$

## Describe the two main requirements of a cache coherent memory system

- Write-propagation: all memory updates must be eventually observed by all readers.
- Write-serialization: different processors must observe memory operations in the same order.

## Describe snooping and directory-based cache coherence protocols

Snooping is a cache coherence protocol in which processors actively listen on the requests done on the bus and autonomously keep data up to date.

Directory-based protocols are protocols in which a directory keeps states for each cache line, and each processor will fetch updates from that. Additional memory is needed to store the states for each
cache line.

### When should one be preferred over the other?

On small systems, snooping is preferred, because it's simpler and more efficient, with less overhead since they do not require additional memory. On larger systems, directory-based protocols are
preferred, because they scale better.

## Describe how the MESI protocol reacts if a processor sees a local write hit to a cacheline that is in shared state in several caches. Report the message(s) sent on the bus and the state changes

The protocol needs to invalidate all other copies of the cache line, so it sends a `BusRdX` message on the bus, and the state changes to `M` on the processor which is updating the value, and to `I` on
all other processes which had the line in their cache.

## In a linked-list based bounded FIFO queue we have two locks that are used for enqueueing and dequeueing. Provide the pseudo-code of the enqueue method
  
```c
// adding elements to the tail, removing from the head
void enqueue(int x){
    Node new_node = new Node(x);
    if (queue.isEmpty()) {
        // create a new queue of 1 element
        queue.head = new_node;
        queue.tail = new_node;
    }
    else {
        // add element after the tail
        lock(queue.tail_lock);
        queue.tail.next = new_node;
        queue.tail = new_node;
        unlock(queue.tail_lock);
    }

}
```

## Provide the C implementation of a Test-and-Set Lock (`lock()` and `unlock()` functions). Describe the TAS semantic

```c
void lock(int *flag){
    // loop until flag is set to 0 by another thread
    while(TestAndSet(flag, 1)==1);
}

void unlock(bool *flag){
    *flag = 0;
}
```

### What are the main drawbacks of this solution?

TAS instruction is a memory barrier and it's very expensive. It also causes cache contention if multiple threads are trying to acquire the lock, which worsens performance.

### Describe two optimizations that can be applied to the simple TAS lock

Test-and-Test-and-Set locks perform better because they loop only with a test instruction and not a TAS instruction, which is more expensive. They only perform a TAS instruction when they know that the lock is free.
Exponential backoff to reduce contention.

## Provide the definition of starvation-free lock

A lock is starvation-free if, eventually, in a finite amount of time, all the threads which require are let into the critical region.

### Is it a required property?

It's required if you need a guarantee that all threads will eventually be let into the critical region.

### Outline the proof of the Peterson lock starvation-free property

The Peterson lock uses a `victim` variable, which is used to determine which thread should be let into the critical region. The `victim` variable is set to the thread which is trying to acquire the lock, and the other thread will wait until the `victim` variable is set to itself. This means that, if thread A leaves CR and tries right after to re-enter it, it will not be able to do so, because the `victim` variable, which was set to `B`, will now be set to `A`, making it wait. This means that thread A will not be able to re-enter the critical region infinitely many times in a row (if B is waiting), and thus the lock is starvation-free.

## Describe why the naive Peterson lock is not usable on x86 systems

x86 systems allow reordering of instructions in order to improve performance. However, if the instructions are reordered, the lock will not work as expected.

## Describe the difference between a spinning lock and a blocking lock

With a spinning lock, threads will be looping until they can acquire the lock. With a blocking lock, threads will be put to sleep until they can acquire the lock.

### What are the advantages and disadvantages of each?

A spinning lock has faster response times, but wastes a lot of resources. A blocking lock frees up resources, but it's slower to resume execution.

### When should one type of lock be preferred over the other?

A spinning lock should be preferred when the lock is expected to be held for a short amount of time, and when there are few threads contending for the lock. A blocking lock should be preferred when the lock is expected to be held for a long time, and when there are many threads contending for the lock.

## What is the difference between a lock-free and a wait-free algorithm?

A ***wait-free*** algorithm guarantees that all processes will complete their operations in a finite number of steps. A ***lock-free*** algorithm guarantees that at least one process will complete its operation in a finite number of steps.

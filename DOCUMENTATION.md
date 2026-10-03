# Job Scheduling with Deadlines: Comprehensive DAA Documentation

---

## 1. Executive Summary & Problem Formulation

### 1.1 Problem Statement
A company receives several jobs. Each job requires **one unit of processing time**, has an integer **deadline**, and yields a designated **profit** if and only if it is completed before or at its deadline. 

The machine or processor can execute at most **one job at any given time unit**. The objective is to determine a feasible schedule of jobs that **maximizes total profit**.

### 1.2 Mathematical Formulation
Let the set of submitted jobs be:
$$\mathcal{J} = \{j_1, j_2, \dots, j_n\}$$

Each job $j_i$ is characterized by the tuple:
$$j_i = (id_i, d_i, p_i)$$
where:
- $id_i$: Unique identifier of the job (e.g., $J_1, J_2$).
- $d_i \in \mathbb{Z}^+$: Deadline of the job ($d_i \ge 1$).
- $p_i \in \mathbb{R}^+$: Profit earned if $j_i$ is completed in time slot $t \le d_i$.
- Processing time: Exactly $1$ unit of time for every job.

Time is discretized into contiguous unit intervals:
$$\text{Slot } t = [t - 1, t] \quad \text{for } t \in \{1, 2, \dots, D\}$$
where $D = \max(d_1, d_2, \dots, d_n)$ represents the maximum deadline across all jobs.

#### Constraints:
1. **Single-processor capacity**: At most one job can be assigned to time slot $t$.
2. **Deadline feasibility**: If job $j_i$ is scheduled in slot $t$, it must satisfy $1 \le t \le d_i$.
3. **Non-preemption & Unit duration**: Each scheduled job runs uninterrupted for its entire unit duration.

#### Objective Function:
Find a subset of jobs $S \subseteq \mathcal{J}$ and an assignment $\sigma: S \to \{1, \dots, D\}$ such that:
$$\max \sum_{j \in S} p_j \quad \text{subject to } \sigma(j) \le d_j \text{ and } \sigma(j) \neq \sigma(k) \; \forall j \neq k \in S$$

---

## 2. Theoretical Foundations (Design & Analysis of Algorithms)

The Job Sequencing with Deadlines problem is a canonical problem solved using the **Greedy Method**.

### 2.1 Greedy Choice Property
At each step, we make the locally optimal choice in hopes of arriving at a globally optimal solution.
- **Priority by Profit**: Jobs that generate higher profit should be given priority over jobs that generate lower profit. Therefore, jobs are evaluated in strictly non-increasing order of profit:
  $$p_1 \ge p_2 \ge \dots \ge p_n$$
- **Latest Feasible Slot Assignment**: When placing a job $j_i$ with deadline $d_i$, we always allocate it to the **latest unoccupied slot $t \le d_i$**.

> **Why the latest available slot?**  
> If we place a job earlier than necessary (e.g., slot 1 instead of slot 3 when deadline is 3), we prematurely consume early slots that could have accommodated jobs with tight deadlines (e.g., jobs with deadline 1). Delaying execution as close to the deadline as possible preserves maximum scheduling flexibility for subsequent jobs.

### 2.2 Optimal Substructure & Matroid Theory
The feasible sets of jobs form an **Independent Set System** over a **Scheduling Matroid** $M = (S, \mathcal{I})$:
- **Ground set $S$**: All submitted jobs.
- **Independent sets $\mathcal{I}$**: Any subset of jobs that can be scheduled without violating deadlines.

By the **Rado-Edmonds Theorem**, whenever an optimization problem can be formulated as finding a maximum-weight independent set in a matroid, the standard **Greedy Algorithm is guaranteed to yield the exact global optimum**.

---

## 3. Algorithmic Implementations

### 3.1 Standard Greedy Algorithm ($O(N^2)$)

#### Pseudocode:
```text
Algorithm JobSchedulingGreedy(Jobs):
    1. Sort Jobs in descending order of profit (p_1 >= p_2 >= ... >= p_n)
    2. D = max(deadline of all jobs in Jobs)
    3. Initialize Slots[1 .. D] = NULL
    4. TotalProfit = 0
    5. ScheduledList = []
    
    6. For each job j in Jobs:
         For t = min(j.deadline, D) down to 1:
             If Slots[t] is NULL:
                 Slots[t] = j
                 TotalProfit += j.profit
                 ScheduledList.append(j, t)
                 Break  // Job successfully scheduled
                 
    7. Return ScheduledList, Slots, TotalProfit
```

---

### 3.2 Optimized Disjoint Set Union (DSU) Algorithm ($O(N \log N)$)

When the maximum deadline $D$ is large, searching backward through slots in the standard greedy approach takes $O(D)$ time per job, leading to an overall complexity of $O(N \cdot D)$.

Using **Disjoint Set Union (DSU / Union-Find) with Path Compression**:
- We initialize parent pointers: $\text{parent}[i] = i$ for all $i \in \{0, 1, \dots, D\}$.
- $\text{find}(t)$ returns the **greatest available empty slot $\le t$**.
- Once slot $t$ is allocated, we union $t$ with $t - 1$ ($\text{parent}[t] = \text{find}(t - 1)$).
- If $\text{find}(d_i) = 0$, it indicates that all slots from $1$ to $d_i$ are full, so the job is dropped.

#### DSU Pseudocode:
```text
Class DSU:
    Initialize parent[0 .. D] where parent[i] = i
    
    Function find(i):
        If parent[i] == i:
            Return i
        parent[i] = find(parent[i])  // Path compression
        Return parent[i]

    Function union(u, v):
        parent[u] = v

Algorithm JobSchedulingDSU(Jobs):
    1. Sort Jobs descending by profit
    2. D = max(deadline of all jobs)
    3. dsu = DSU(D)
    4. For each job j in Jobs:
         available_slot = dsu.find(min(j.deadline, D))
         If available_slot > 0:
             Allocate job j to available_slot
             dsu.union(available_slot, dsu.find(available_slot - 1))
             TotalProfit += j.profit
         Else:
             Job j is rejected (no free slots)
```

---

## 4. Step-by-Step Hand Dry Run (Horowitz & Sahni Benchmark)

Consider the classic benchmark problem:

| Job ID | Deadline ($d$) | Profit ($p$) |
| :---: | :---: | :---: |
| **J1** | 2 | 100 |
| **J2** | 1 | 19 |
| **J3** | 2 | 27 |
| **J4** | 1 | 25 |
| **J5** | 3 | 15 |

### Phase 1: Sort Jobs by Profit (Descending)
1. **J1**: Profit = 100, Deadline = 2
2. **J3**: Profit = 27, Deadline = 2
3. **J4**: Profit = 25, Deadline = 1
4. **J2**: Profit = 19, Deadline = 1
5. **J5**: Profit = 15, Deadline = 3

Max Deadline $D = \max(2, 1, 2, 1, 3) = 3$.  
Slots available: `[Slot 1, Slot 2, Slot 3]`, all initially empty.

---

### Phase 2: Iterative Slot Allocation

#### Step 1: Evaluate J1 ($p=100, d=2$)
- Target deadline is 2. Search backward from Slot 2.
- Slot 2 is empty $\rightarrow$ **Assign J1 to Slot 2**.
- Accumulated Profit: **100**
- State: `[Slot 1: Empty, Slot 2: J1, Slot 3: Empty]`

#### Step 2: Evaluate J3 ($p=27, d=2$)
- Target deadline is 2. Check Slot 2 $\rightarrow$ occupied by J1.
- Move backward to Slot 1 $\rightarrow$ empty!
- **Assign J3 to Slot 1**.
- Accumulated Profit: $100 + 27 =$ **127**
- State: `[Slot 1: J3, Slot 2: J1, Slot 3: Empty]`

#### Step 3: Evaluate J4 ($p=25, d=1$)
- Target deadline is 1. Check Slot 1 $\rightarrow$ occupied by J3.
- No free slots $\le 1$ remain.
- **Reject J4**.
- Accumulated Profit: **127**

#### Step 4: Evaluate J2 ($p=19, d=1$)
- Target deadline is 1. Check Slot 1 $\rightarrow$ occupied by J3.
- No free slots $\le 1$ remain.
- **Reject J2**.
- Accumulated Profit: **127**

#### Step 5: Evaluate J5 ($p=15, d=3$)
- Target deadline is 3. Check Slot 3 $\rightarrow$ empty!
- **Assign J5 to Slot 3**.
- Accumulated Profit: $127 + 15 =$ **142**
- State: `[Slot 1: J3, Slot 2: J1, Slot 3: J5]`

---

### Final Outcome:
- **Optimal Scheduled Sequence**: `[Slot 1: J3, Slot 2: J1, Slot 3: J5]`
- **Jobs Executed**: 3 of 5 (60% acceptance)
- **Total Maximum Profit**: **$142**
- **Slot Utilization**: 100% (3 of 3 slots filled)

---

## 5. Complexity Analysis

| Metric | Standard Greedy Algorithm | DSU-Optimized Algorithm |
| :--- | :--- | :--- |
| **Sorting Time** | $O(N \log N)$ | $O(N \log N)$ |
| **Slot Search Time** | $O(N \cdot \min(N, D))$ | $O(N \cdot \alpha(D))$ |
| **Total Time Complexity** | **$O(N \log N + N \cdot D)$** | **$O(N \log N + N \cdot \alpha(D))$** |
| **Auxiliary Space** | $O(D)$ for slot timeline array | $O(D)$ for parent pointers array |

*Note: $\alpha$ is the Inverse Ackermann function, which grows so slowly that $\alpha(D) < 5$ for any practically conceivable value of $D$, making DSU slot lookup effectively nearly $O(1)$.*

---

## 6. Web Application Architecture & Features

The web application is built strictly according to your specifications:
- **Python Backend**: Built with Flask (`app.py`), exposing clean REST APIs for both Standard Greedy and DSU methods.
- **Cool White Theme**:
  - Background: Crisp, ultra-clean ice-slate tone (`#f8fafc`) with subtle ambient blue-mesh glows (`#eff6ff` / `#dbeafe`).
  - Cards: Pure white (`#ffffff`) surfaces with frosted backdrop filters, crisp borders (`#e2e8f0`), and soft drop shadows.
  - Accent colors: Electric Blue (`#2563eb`) and Emerald Green (`#059669`) for positive status indicators.
- **Simple, Focused Features**:
  1. **Interactive Gantt Slot Timeline**: Visualizes discrete 1-hour slots $[0-1], [1-2], \dots$, showing scheduled jobs and idle slots.
  2. **Step-by-Step Playback Controller**: Step forward, backward, or auto-play through each decision. The timeline visually mutates at each step to demonstrate how slots are claimed.
  3. **Algorithm Engine Switcher**: Switch between **Standard Greedy** and **DSU Optimized** modes with live complexity and runtime readouts.
  4. **Textbook Presets**: Instant 1-click loading for classic problems (Horowitz & Sahni, CLRS Cormen, High Contention, Wide Horizon) plus a random job generator.
  5. **Dynamic Job Pool**: Add, edit, or delete jobs with live validation.
  6. **In-App Documentation Drawer**: Access the complete mathematical proof and algorithm notes without leaving the page.

---

## 7. How to Run the Application

### 7.1 Running the Web Server
Open terminal in the project directory:
```bash
python app.py
```
Open your web browser and visit:
```
http://127.0.0.1:5000
```

### 7.2 Running the Automated Tests
Verify algorithm correctness against standard textbook test cases:
```bash
python test_scheduler.py
```
Expected output:
```text
Ran 3 tests in 0.001s
OK
```

---

## 8. Summary Table of Files

- [`app.py`](file:///c:/Users/SRI%20CHARAN/OneDrive/Documents/DAA%20Hackathon/app.py): Flask application with Greedy & DSU algorithms, step tracking, and API routes.
- [`templates/index.html`](file:///c:/Users/SRI%20CHARAN/OneDrive/Documents/DAA%20Hackathon/templates/index.html): Semantic single-page HTML with cool white theme styling and Gantt visualization.
- [`static/style.css`](file:///c:/Users/SRI%20CHARAN/OneDrive/Documents/DAA%20Hackathon/static/style.css): Modern cool white styling, responsive layout, and clean cards.
- [`static/app.js`](file:///c:/Users/SRI%20CHARAN/OneDrive/Documents/DAA%20Hackathon/static/app.js): Dynamic client-side logic, timeline rendering, step-by-step playback, and API calls.
- [`test_scheduler.py`](file:///c:/Users/SRI%20CHARAN/OneDrive/Documents/DAA%20Hackathon/test_scheduler.py): Unit tests verifying algorithm correctness.
- [`DOCUMENTATION.md`](file:///c:/Users/SRI%20CHARAN/OneDrive/Documents/DAA%20Hackathon/DOCUMENTATION.md): Complete algorithmic and technical explanation document.

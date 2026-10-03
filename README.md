# Job Scheduling with Deadlines — DAA Optimization Web App

A clean, responsive web application implementing the **Job Sequencing with Deadlines** problem from Design and Analysis of Algorithms (DAA). It features a modern **Cool White Theme**, visual Gantt slot timeline, step-by-step playback controller, and algorithmic comparisons (Standard Greedy vs. DSU Union-Find).

---

## Quickstart

### 1. Prerequisites
- Python 3.8+ (tested with Python 3.13)
- `Flask`

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Run the Web Application
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### 4. Run Unit Tests
```bash
python test_scheduler.py
```

---

## Features

- **Cool White Aesthetic**: Clean ice-white backgrounds, frosted glass cards, subtle blue glows, and refined typography.
- **DAA Greedy Algorithm**: Sorts jobs by descending profit and greedily assigns each to the latest feasible available slot.
- **DSU (Disjoint Set Union) Engine**: Fast $O(N \log N + N \cdot \alpha(D))$ slot lookup using path compression.
- **Visual Gantt Timeline**: Displays discrete 1-hour time slots $[t-1, t]$ with scheduled jobs and idle slots.
- **Step-by-Step Playback**: Step through or auto-play each greedy decision with live schedule mutation.
- **Textbook Presets**: 1-click loading for classic Horowitz & Sahni, CLRS Cormen benchmarks, and custom random jobs.
- **In-App & Markdown Documentation**: Complete DAA theory, matroid proofs, and complexity analysis.

For complete academic and algorithmic explanations, see [DOCUMENTATION.md](file:///c:/Users/SRI%20CHARAN/OneDrive/Documents/DAA%20Hackathon/DOCUMENTATION.md).

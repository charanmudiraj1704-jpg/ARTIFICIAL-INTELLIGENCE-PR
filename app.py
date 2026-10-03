from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

class DisjointSet:
    """Disjoint Set Union (DSU) with Path Compression for O(N log N) slot allocation."""
    def __init__(self, n):
        # parent[i] points to the greatest available slot <= i
        self.parent = list(range(n + 1))

    def find(self, i):
        if i == self.parent[i]:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, u, v):
        # Attach slot u to slot v (where v is available slot before u)
        self.parent[u] = v


def solve_job_sequencing_greedy(jobs_data):
    """
    Standard Greedy Job Sequencing with Deadlines.
    Time Complexity: O(N log N + N * min(N, max_deadline))
    Space Complexity: O(max_deadline)
    """
    if not jobs_data:
        return {
            "scheduled": [],
            "rejected": [],
            "timeline": [],
            "total_profit": 0,
            "max_deadline": 0,
            "steps": [],
            "utilization": 0,
            "runtime_ms": 0
        }

    start_time = time.perf_counter()

    # Normalize and validate inputs
    cleaned_jobs = []
    for idx, item in enumerate(jobs_data):
        job_id = str(item.get("id", f"J{idx+1}")).strip()
        deadline = max(1, int(item.get("deadline", 1)))
        profit = max(0, float(item.get("profit", 0)))
        cleaned_jobs.append({
            "id": job_id,
            "deadline": deadline,
            "profit": profit,
            "original_index": idx
        })

    # Step 1: Sort jobs in descending order of profit
    # Secondary key: deadline ascending to give earlier deadline jobs equal priority
    sorted_jobs = sorted(cleaned_jobs, key=lambda x: (-x["profit"], x["deadline"]))

    max_deadline = max(job["deadline"] for job in sorted_jobs)
    # Timeline slots are 1-indexed up to max_deadline
    # slots[t] stores job info or None for slot t (1 <= t <= max_deadline)
    slots = [None] * (max_deadline + 1)

    steps = []
    scheduled = []
    rejected = []
    total_profit = 0

    for step_num, job in enumerate(sorted_jobs, 1):
        assigned_slot = None
        searched_slots = []
        limit = min(job["deadline"], max_deadline)

        # Step 2: Search backwards from min(deadline, max_deadline) to 1
        for t in range(limit, 0, -1):
            searched_slots.append(t)
            if slots[t] is None:
                slots[t] = {
                    "id": job["id"],
                    "deadline": job["deadline"],
                    "profit": job["profit"],
                    "slot": t
                }
                assigned_slot = t
                total_profit += job["profit"]
                break

        # Record timeline snapshot for step-by-step playback
        timeline_snapshot = []
        for s in range(1, max_deadline + 1):
            if slots[s] is not None:
                timeline_snapshot.append({
                    "slot": s,
                    "job_id": slots[s]["id"],
                    "profit": slots[s]["profit"],
                    "deadline": slots[s]["deadline"]
                })
            else:
                timeline_snapshot.append({
                    "slot": s,
                    "job_id": None,
                    "profit": 0,
                    "deadline": None
                })

        if assigned_slot is not None:
            scheduled.append({
                "id": job["id"],
                "deadline": job["deadline"],
                "profit": job["profit"],
                "slot": assigned_slot
            })
            decision = f"Assigned to Slot {assigned_slot} (latest free slot <= {job['deadline']})"
            status = "scheduled"
        else:
            rejected.append({
                "id": job["id"],
                "deadline": job["deadline"],
                "profit": job["profit"],
                "reason": f"No available slots from 1 to {limit}"
            })
            decision = f"Rejected: all slots 1..{limit} are already occupied"
            status = "rejected"

        steps.append({
            "step": step_num,
            "job": job,
            "searched_slots": searched_slots,
            "assigned_slot": assigned_slot,
            "status": status,
            "decision": decision,
            "current_profit": total_profit,
            "timeline_snapshot": timeline_snapshot
        })

    end_time = time.perf_counter()
    runtime_ms = round((end_time - start_time) * 1000, 3)

    # Clean timeline representation
    final_timeline = []
    filled_count = 0
    for s in range(1, max_deadline + 1):
        if slots[s] is not None:
            filled_count += 1
            final_timeline.append({
                "slot": s,
                "job_id": slots[s]["id"],
                "profit": slots[s]["profit"],
                "deadline": slots[s]["deadline"],
                "time_range": f"{s-1}:00 - {s}:00"
            })
        else:
            final_timeline.append({
                "slot": s,
                "job_id": None,
                "profit": 0,
                "deadline": None,
                "time_range": f"{s-1}:00 - {s}:00"
            })

    utilization = round((filled_count / max_deadline * 100), 1) if max_deadline > 0 else 0

    return {
        "scheduled": scheduled,
        "rejected": rejected,
        "timeline": final_timeline,
        "total_profit": total_profit,
        "max_deadline": max_deadline,
        "steps": steps,
        "sorted_jobs": sorted_jobs,
        "utilization": utilization,
        "runtime_ms": runtime_ms,
        "total_jobs": len(cleaned_jobs)
    }


def solve_job_sequencing_dsu(jobs_data):
    """
    DSU-optimized Job Sequencing with Deadlines.
    Time Complexity: O(N log N + N * alpha(max_deadline))
    Space Complexity: O(max_deadline)
    """
    if not jobs_data:
        return solve_job_sequencing_greedy([])

    start_time = time.perf_counter()

    cleaned_jobs = []
    for idx, item in enumerate(jobs_data):
        job_id = str(item.get("id", f"J{idx+1}")).strip()
        deadline = max(1, int(item.get("deadline", 1)))
        profit = max(0, float(item.get("profit", 0)))
        cleaned_jobs.append({
            "id": job_id,
            "deadline": deadline,
            "profit": profit,
            "original_index": idx
        })

    sorted_jobs = sorted(cleaned_jobs, key=lambda x: (-x["profit"], x["deadline"]))
    max_deadline = max(job["deadline"] for job in sorted_jobs)

    dsu = DisjointSet(max_deadline)
    slots = [None] * (max_deadline + 1)
    scheduled = []
    rejected = []
    total_profit = 0
    steps = []

    for step_num, job in enumerate(sorted_jobs, 1):
        limit = min(job["deadline"], max_deadline)
        available_slot = dsu.find(limit)

        if available_slot > 0:
            slots[available_slot] = {
                "id": job["id"],
                "deadline": job["deadline"],
                "profit": job["profit"],
                "slot": available_slot
            }
            # Link available_slot to available_slot - 1
            dsu.union(available_slot, dsu.find(available_slot - 1))
            total_profit += job["profit"]
            scheduled.append({
                "id": job["id"],
                "deadline": job["deadline"],
                "profit": job["profit"],
                "slot": available_slot
            })
            status = "scheduled"
            decision = f"DSU found available slot {available_slot} in O(alpha(D)) time."
        else:
            rejected.append({
                "id": job["id"],
                "deadline": job["deadline"],
                "profit": job["profit"],
                "reason": "DSU root is 0, no available slots"
            })
            status = "rejected"
            decision = f"Rejected: available slot query returned 0 (all slots <= {limit} filled)."

        timeline_snapshot = []
        for s in range(1, max_deadline + 1):
            if slots[s] is not None:
                timeline_snapshot.append({
                    "slot": s,
                    "job_id": slots[s]["id"],
                    "profit": slots[s]["profit"],
                    "deadline": slots[s]["deadline"]
                })
            else:
                timeline_snapshot.append({
                    "slot": s,
                    "job_id": None,
                    "profit": 0,
                    "deadline": None
                })

        steps.append({
            "step": step_num,
            "job": job,
            "assigned_slot": available_slot if available_slot > 0 else None,
            "status": status,
            "decision": decision,
            "current_profit": total_profit,
            "timeline_snapshot": timeline_snapshot
        })

    end_time = time.perf_counter()
    runtime_ms = round((end_time - start_time) * 1000, 3)

    final_timeline = []
    filled_count = 0
    for s in range(1, max_deadline + 1):
        if slots[s] is not None:
            filled_count += 1
            final_timeline.append({
                "slot": s,
                "job_id": slots[s]["id"],
                "profit": slots[s]["profit"],
                "deadline": slots[s]["deadline"],
                "time_range": f"{s-1}:00 - {s}:00"
            })
        else:
            final_timeline.append({
                "slot": s,
                "job_id": None,
                "profit": 0,
                "deadline": None,
                "time_range": f"{s-1}:00 - {s}:00"
            })

    utilization = round((filled_count / max_deadline * 100), 1) if max_deadline > 0 else 0

    return {
        "scheduled": scheduled,
        "rejected": rejected,
        "timeline": final_timeline,
        "total_profit": total_profit,
        "max_deadline": max_deadline,
        "steps": steps,
        "sorted_jobs": sorted_jobs,
        "utilization": utilization,
        "runtime_ms": runtime_ms,
        "total_jobs": len(cleaned_jobs)
    }


PRESETS = {
    "classic_daa": {
        "name": "Classic DAA Textbook (Horowitz & Sahni)",
        "description": "Standard 5-job benchmark demonstrating backward slot search and rejection.",
        "jobs": [
            {"id": "J1", "deadline": 2, "profit": 100},
            {"id": "J2", "deadline": 1, "profit": 19},
            {"id": "J3", "deadline": 2, "profit": 27},
            {"id": "J4", "deadline": 1, "profit": 25},
            {"id": "J5", "deadline": 3, "profit": 15}
        ]
    },
    "clrs_benchmark": {
        "name": "CLRS Cormen Case",
        "description": "7 jobs with overlapping deadlines testing slot contention and profit maximization.",
        "jobs": [
            {"id": "A", "deadline": 4, "profit": 70},
            {"id": "B", "deadline": 2, "profit": 60},
            {"id": "C", "deadline": 4, "profit": 50},
            {"id": "D", "deadline": 3, "profit": 40},
            {"id": "E", "deadline": 1, "profit": 30},
            {"id": "F", "deadline": 4, "profit": 20},
            {"id": "G", "deadline": 6, "profit": 10}
        ]
    },
    "tight_deadlines": {
        "name": "High Contention (Bottleneck at Slot 1-2)",
        "description": "Multiple high-value jobs competing for very tight early deadlines.",
        "jobs": [
            {"id": "Alpha", "deadline": 1, "profit": 95},
            {"id": "Beta", "deadline": 1, "profit": 90},
            {"id": "Gamma", "deadline": 2, "profit": 85},
            {"id": "Delta", "deadline": 2, "profit": 80},
            {"id": "Epsilon", "deadline": 2, "profit": 75},
            {"id": "Zeta", "deadline": 5, "profit": 40}
        ]
    },
    "distributed_deadlines": {
        "name": "Wide Horizon (High Utilization)",
        "description": "Jobs distributed across larger deadline range allowing high completion rate.",
        "jobs": [
            {"id": "Task-1", "deadline": 4, "profit": 80},
            {"id": "Task-2", "deadline": 5, "profit": 65},
            {"id": "Task-3", "deadline": 6, "profit": 50},
            {"id": "Task-4", "deadline": 3, "profit": 70},
            {"id": "Task-5", "deadline": 2, "profit": 90},
            {"id": "Task-6", "deadline": 1, "profit": 110}
        ]
    }
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/presets", methods=["GET"])
def get_presets():
    return jsonify(PRESETS)


@app.route("/api/schedule", methods=["POST"])
def schedule_jobs():
    data = request.get_json() or {}
    jobs = data.get("jobs", [])
    algorithm = data.get("algorithm", "greedy")

    if not isinstance(jobs, list):
        return jsonify({"error": "Invalid format: jobs must be a list"}), 400

    if algorithm == "dsu":
        result = solve_job_sequencing_dsu(jobs)
    else:
        result = solve_job_sequencing_greedy(jobs)

    return jsonify(result)


if __name__ == "__main__":
    import os
    import socket
    
    port = int(os.environ.get("PORT", 5000))
    # Check if port is already in use
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        test_socket.bind(("127.0.0.1", port))
        test_socket.close()
    except OSError:
        port = 5050
        
    print(f"\n=======================================================")
    print(f" Job Scheduling with Deadlines Optimizer is running!  ")
    print(f" URL: http://127.0.0.1:{port}                         ")
    print(f"=======================================================\n")
    app.run(debug=True, port=port)


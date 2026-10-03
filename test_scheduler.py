import unittest
from app import solve_job_sequencing_greedy, solve_job_sequencing_dsu

class TestJobSequencing(unittest.TestCase):
    def test_classic_textbook(self):
        """
        Classic Horowitz & Sahni problem:
        J1: d=2, p=100
        J2: d=1, p=19
        J3: d=2, p=27
        J4: d=1, p=25
        J5: d=3, p=15
        
        Sorted: J1 (100, d=2), J3 (27, d=2), J4 (25, d=1), J2 (19, d=1), J5 (15, d=3)
        J1 takes slot 2
        J3 searches 2 (occupied), takes slot 1
        J4 searches 1 (occupied) -> rejected
        J2 searches 1 (occupied) -> rejected
        J5 searches 3 -> takes slot 3
        
        Expected scheduled: J1, J3, J5 (or slots: slot 1 = J3, slot 2 = J1, slot 3 = J5)
        Total profit: 100 + 27 + 15 = 142
        """
        jobs = [
            {"id": "J1", "deadline": 2, "profit": 100},
            {"id": "J2", "deadline": 1, "profit": 19},
            {"id": "J3", "deadline": 2, "profit": 27},
            {"id": "J4", "deadline": 1, "profit": 25},
            {"id": "J5", "deadline": 3, "profit": 15}
        ]

        greedy_res = solve_job_sequencing_greedy(jobs)
        self.assertEqual(greedy_res["total_profit"], 142)
        scheduled_ids = {j["id"] for j in greedy_res["scheduled"]}
        self.assertEqual(scheduled_ids, {"J1", "J3", "J5"})
        self.assertEqual(len(greedy_res["rejected"]), 2)

        dsu_res = solve_job_sequencing_dsu(jobs)
        self.assertEqual(dsu_res["total_profit"], 142)
        dsu_ids = {j["id"] for j in dsu_res["scheduled"]}
        self.assertEqual(dsu_ids, {"J1", "J3", "J5"})

    def test_clrs_case(self):
        jobs = [
            {"id": "A", "deadline": 4, "profit": 70},
            {"id": "B", "deadline": 2, "profit": 60},
            {"id": "C", "deadline": 4, "profit": 50},
            {"id": "D", "deadline": 3, "profit": 40},
            {"id": "E", "deadline": 1, "profit": 30},
            {"id": "F", "deadline": 4, "profit": 20},
            {"id": "G", "deadline": 6, "profit": 10}
        ]
        res = solve_job_sequencing_greedy(jobs)
        # Sorted order: A(70, d4), B(60, d2), C(50, d4), D(40, d3), E(30, d1), F(20, d4), G(10, d6)
        # A -> slot 4
        # B -> slot 2
        # C -> slot 3 (since 4 occupied)
        # D -> slot 1 (since 3, 2 occupied)
        # E -> rejected (slot 1 occupied)
        # F -> rejected (slots 4,3,2,1 occupied)
        # G -> slot 6
        # Scheduled: A, B, C, D, G => 70 + 60 + 50 + 40 + 10 = 230
        self.assertEqual(res["total_profit"], 230)
        scheduled_ids = [j["id"] for j in res["scheduled"]]
        self.assertEqual(set(scheduled_ids), {"A", "B", "C", "D", "G"})

    def test_empty_and_single(self):
        self.assertEqual(solve_job_sequencing_greedy([])["total_profit"], 0)
        single = [{"id": "Solo", "deadline": 1, "profit": 50}]
        res = solve_job_sequencing_greedy(single)
        self.assertEqual(res["total_profit"], 50)
        self.assertEqual(len(res["scheduled"]), 1)

if __name__ == "__main__":
    unittest.main()

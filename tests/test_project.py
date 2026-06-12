import unittest
from models.project import Project
from models.task import Task

class TestProject(unittest.TestCase):
    def test_add_task(self):
        p = Project("P", "desc")
        t = Task("T1")
        p.add_task(t)
        self.assertIn(t, p.tasks)
        self.assertEqual(t.project, p)

    def test_to_dict(self):
        p = Project("Proj", "Desc", "2025-12-31")
        d = p.to_dict()
        self.assertEqual(d["title"], "Proj")
        self.assertEqual(d["due_date"], "2025-12-31")

if __name__ == "__main__":
    unittest.main()

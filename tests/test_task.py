import unittest
from models.task import Task

class TestTask(unittest.TestCase):
    def test_mark_complete(self):
        t = Task("Do stuff")
        self.assertEqual(t.status, "pending")
        t.mark_complete()
        self.assertEqual(t.status, "complete")

if __name__ == "__main__":
    unittest.main()

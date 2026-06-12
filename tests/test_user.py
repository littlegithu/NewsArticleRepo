import unittest
from models.user import User
from models.project import Project

class TestUser(unittest.TestCase):
    def setUp(self):
        User.clear_all()

    def test_create_user(self):
        u = User("Alice", "a@b.com")
        self.assertEqual(u.name, "Alice")
        self.assertEqual(u.email, "a@b.com")

    def test_add_project(self):
        u = User("Bob", "b@c.com")
        p = Project("Test Proj")
        u.add_project(p)
        self.assertIn(p, u.projects)
        self.assertEqual(p.user, u)

    def test_find_by_name(self):
        u1 = User("Charlie", "c@d.com")
        User("Dave", "d@e.com")
        found = User.find_by_name("Charlie")
        self.assertEqual(found, u1)
        self.assertIsNone(User.find_by_name("Eve"))

if __name__ == "__main__":
    unittest.main()

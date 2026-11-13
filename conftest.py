import os
import sys

# Use an in-memory database for tests so they never touch netops.db.
# Must be set before application.py is imported.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

sys.path.insert(0, os.path.dirname(__file__))

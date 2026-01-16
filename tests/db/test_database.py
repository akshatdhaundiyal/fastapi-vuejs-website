# import sys
# import os
# # Ensure the parent directory is in the path for module imports
# parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
# print(f"Adding to sys.path: {parent_path}")
# sys.path.append(parent_path)


from src.db.database import get_db

def test_get_db():
    db = next(get_db())
    assert db is not None
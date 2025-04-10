import json
import csv
import random
import time
from uuid import uuid4
from faker import Faker
from datetime import datetime, timedelta
import pandas as pd

fake = Faker()
Faker.seed(0)
random.seed(0)

# Constants
NUM_USERS = 10
NUM_ENTRIES = 50
LANGUAGES = ["Go", "Python", "JavaScript"]
DIFFICULTIES = ["Easy", "Medium", "Hard"]

# Utils
def fake_object_id():
    return str(uuid4()).replace("-", "")[:24]

# Generate Users (PostgreSQL)
mock_users = []
user_ids = [str(uuid4()) for _ in range(NUM_USERS)]

for user_id in user_ids:
    mock_users.append({
        "id": user_id,
        "user_name": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "country": fake.country(),
        "role": random.choice(["user", "admin"]),
        "primary_language_id": random.choice(["go", "py", "js"]),
        "email": fake.email(),
        "auth_type": random.choice(["email", "google", "github"]),
        "salt": fake.sha1(),
        "hashed_password": fake.sha256(),
        "mute_notifications": fake.boolean(),
        "is_banned": fake.boolean(chance_of_getting_true=10),
        "ban_id": str(uuid4()),
        "two_factor_enabled": fake.boolean(),
        "is_verified": fake.boolean(),
        "two_factor_secret": fake.sha1(),
        "avatar_data": fake.image_url(),
        "github": f"https://github.com/{fake.user_name()}",
        "twitter": f"https://twitter.com/{fake.user_name()}",
        "linkedin": f"https://linkedin.com/in/{fake.user_name()}",
        "created_at": int(time.time()) - random.randint(10000, 500000),
        "updated_at": int(time.time()),
        "deleted_at": None,
        "following": [],
        "followers": []
    })

# Generate Submissions and ProblemsDone (MongoDB)
mock_submissions = []
mock_problems_done = []

for _ in range(NUM_ENTRIES):
    user_id = random.choice(user_ids)
    problem_id = fake_object_id()
    submission_id = fake_object_id()
    submitted_at = datetime.now() - timedelta(days=random.randint(0, 30))

    mock_submissions.append({
        "id": fake_object_id(),
        "userId": user_id,
        "problemId": problem_id,
        "challengeId": None,
        "title": fake.catch_phrase(),
        "submittedAt": submitted_at.isoformat(),
        "status": random.choice(["Accepted", "Wrong Answer", "Runtime Error"]),
        "score": random.randint(0, 100),
        "language": random.choice(LANGUAGES),
        "userCode": fake.text(max_nb_chars=200),
        "output": fake.text(max_nb_chars=100),
        "executionTime": round(random.uniform(0.1, 2.5), 2),
        "difficulty": random.choice(DIFFICULTIES),
        "isFirst": fake.boolean()
    })

    mock_problems_done.append({
        "id": fake_object_id(),
        "submissionId": submission_id,
        "problemId": problem_id,
        "userId": user_id,
        "title": fake.catch_phrase(),
        "language": random.choice(LANGUAGES),
        "difficulty": random.choice(DIFFICULTIES),
        "submittedAt": submitted_at.isoformat(),
        "score": random.randint(0, 100)
    })

# Write JSON Files
with open("mock_users.json", "w") as f:
    json.dump(mock_users, f, indent=2)

with open("mock_submissions.json", "w") as f:
    json.dump(mock_submissions, f, indent=2)

with open("mock_problems_done.json", "w") as f:
    json.dump(mock_problems_done, f, indent=2)

# Write CSV Files
pd.DataFrame(mock_users).to_csv("mock_users.csv", index=False)
pd.DataFrame(mock_submissions).to_csv("mock_submissions.csv", index=False)
pd.DataFrame(mock_problems_done).to_csv("mock_problems_done.csv", index=False)

print("✅ Mock data generated and saved to CSV/JSON.")

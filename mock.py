import random
import string
import uuid
from datetime import datetime, timedelta
import psycopg2
from pymongo import MongoClient
from bson import ObjectId
import time

# --- DB SETUP ---
pg_conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="admin",
    password="password",
    dbname="xcodedev"
)
pg_cursor = pg_conn.cursor()

mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client["submissions_db"]
submissions_col = db["submissions"]
problems_done_col = db["submissionsfirstsuccess"]

# --- UTILS ---
def now_unix():
    return int(time.time())

def random_country_code():
    return random.choice(["IN", "US", "UK", "DE", "FR", "JP", "CN", "BR", "AU", "CA"])

def random_language_code():
    return random.choice(["go", "py", "js"])

def random_language():
    return random.choice(["Go", "Python", "JavaScript"])

def random_difficulty():
    return random.choice(["Easy", "Medium", "Hard"])

def random_name():
    first = random.choice(["Alex", "Sam", "Jordan", "Taylor", "Riley", "Jamie", "Morgan", "Casey", "Drew", "Cameron"])
    last = random.choice(["Smith", "Johnson", "Lee", "Brown", "Jones", "Garcia", "Davis", "Rodriguez", "Martinez", "Lopez"])
    return first, last

# --- CREATE USERS ---
used_emails = set()
used_usernames = set()
users = []

while len(users) < 20:
    user_id = str(uuid.uuid4())
    first_name, last_name = random_name()
    email = f"{first_name.lower()}.{last_name.lower()}@example.com"
    if email in used_emails:
        continue
    used_emails.add(email)

    user_name = f"{first_name.lower()}{random.randint(100,999)}"
    if user_name in used_usernames:
        continue
    used_usernames.add(user_name)

    country = random_country_code()
    role = "user"
    primary_lang = random_language_code()
    auth_type = random.choice(["email", "google", "github"])
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    hashed_password = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    mute_notifications = random.choice([True, False])
    is_banned = False
    two_factor_enabled = False
    is_verified = random.choice([True, False])
    two_factor_secret = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    avatar_data = "data:image/png;base64," + ''.join(random.choices(string.ascii_letters + string.digits, k=100))
    github = f"https://github.com/{user_name}"
    twitter = f"https://twitter.com/{user_name}"
    linkedin = f"https://linkedin.com/in/{user_name}"
    created_at = now_unix()
    updated_at = created_at

    users.append({
        "id": user_id,
        "user_name": user_name,
        "first_name": first_name,
        "last_name": last_name,
        "country": country,
        "email": email
    })

    pg_cursor.execute("""
        INSERT INTO users (
            id, user_name, first_name, last_name, country,
            role, primary_language_id, email, auth_type,
            salt, hashed_password, mute_notifications,
            is_banned, ban_id, two_factor_enabled,
            is_verified, two_factor_secret, avatar_data,
            github, twitter, linkedin, created_at, updated_at
        ) VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s, %s, %s
        )
    """, (
        user_id, user_name, first_name, last_name, country,
        role, primary_lang, email, auth_type,
        salt, hashed_password, mute_notifications,
        is_banned, None, two_factor_enabled,
        is_verified, two_factor_secret, avatar_data,
        github, twitter, linkedin, created_at, updated_at
    ))

pg_conn.commit()

# --- GENERATE SUBMISSIONS & PROBLEMS DONE ---
submissions = []
problems_done = []
problem_ids = [f"prob-{i}" for i in range(50)]
accepted_map = {}

for _ in range(200):
    user = random.choice(users)
    problem_id = random.choice(problem_ids)
    lang = random_language()
    difficulty = random_difficulty()
    status = "SUCCESS" if random.random() < 0.7 else "FAILED"
    sub_id = ObjectId()
    score = random.randint(10, 100)
    created_at = datetime.utcnow() - timedelta(days=random.randint(0, 365))

    submissions.append({
        "_id": sub_id,
        "userId": user["id"],
        "problemId": problem_id,
        "challengeId": None,
        "title": f"Problem {problem_id}",
        "submittedAt": created_at,
        "status": status,
        "score": score,
        "language": lang,
        "userCode": f"// some code in {lang.lower()}",
        "output": "Expected Output",
        "executionTime": round(random.uniform(0.1, 3.0), 2),
        "difficulty": difficulty,
        "isFirst": False
    })

    key = f"{user['id']}_{problem_id}"
    if status == "SUCCESS" and key not in accepted_map:
        accepted_map[key] = True
        problems_done.append({
            "_id": ObjectId(),
            "submissionId": str(sub_id),
            "problemId": problem_id,
            "userId": user["id"],
            "title": f"Problem {problem_id}",
            "language": lang,
            "difficulty": difficulty,
            "submittedAt": created_at,
            "score": score,
        })

# --- INSERT INTO MONGODB ---
submissions_col.insert_many(submissions)
problems_done_col.insert_many(problems_done)

# --- CLEANUP ---
pg_cursor.close()
pg_conn.close()
print(f"✅ Inserted {len(users)} users, {len(submissions)} submissions, {len(problems_done)} problems done.")

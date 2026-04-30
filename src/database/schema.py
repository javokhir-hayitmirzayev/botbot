# Referral Bot Schema (SQLite)

TABLES = {}

TABLES["users"] = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    referrer_id INTEGER,
    username TEXT,
    first_name TEXT,
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

TABLES["pending_referrals"] = """
CREATE TABLE IF NOT EXISTS pending_referrals (
    user_id INTEGER PRIMARY KEY,
    referrer_id INTEGER,
    username TEXT,
    first_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# ---------- Indexes ----------
INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_referrer_id ON users(referrer_id);",
    "CREATE INDEX IF NOT EXISTS idx_pending_referrer_id ON pending_referrals(referrer_id);"
]

# ---------- SQL for Enums ----------
ENUM_SQL = ""  # SQLite doesn't support enums


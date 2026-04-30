# Project Overview

**Objective:** Build a Telegram Referral Bot that gates access based on channel membership, tracks user invitations using unique deep-linking, and provides a real-time leaderboard.

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** aiogram (v3.x preferred)
- **Database:** SQLite (sqlite3 library)
- **Tunneling:** ngrok (for webhook support)

---

## 1. Database Schema (SQLite)

The database will be lightweight. We will focus on a single table with an index to keep queries fast.

### Table Name: users

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| user_id | INTEGER | PRIMARY KEY | The user's unique Telegram ID. |
| referrer_id | INTEGER | NULLABLE | The ID of the user who invited them. |
| username | TEXT | NULLABLE | Telegram handle for the leaderboard. |
| join_date | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When the user first registered. |

**Optimization Note:** To ensure the /rating command is fast, the coding agent should create an index on the referrer_id column.

---

## 2. Functional Requirements & Logic Flow

### A. Membership Gate (Middleware/Check)

1. Define a REQUIRED_CHANNEL_ID and REQUIRED_CHANNEL_URL in the config.
2. Before any command (especially /start), the bot must use bot.get_chat_member to verify the user's status.
3. Status allowed: member, administrator, creator.
4. If not a member, the bot sends a message with a button to join and a "Check Membership" button.

### B. Registration & Referral (The /start Command)

The bot link format: `https://t.me/YourBot?start=REFERRER_ID`.

**Logic:**
1. Check if the user is already in the users database.
2. If new user:
   - Extract REFERRER_ID from the start command arguments.
   - If REFERRER_ID is present and valid (not the user's own ID), save the user with that referrer_id.
   - If no ID is present, save with referrer_id = NULL.
3. If existing user: Simply welcome them back.

### C. User Commands

**/link:**
- Generates a URL: `f"https://t.me/{bot_username}?start={user_id}"`.
- Displays it to the user so they can copy and share.

**/rating:**
- Query: Perform a COUNT on the users table grouped by referrer_id.
- Display: List the Top 10 users by invite count.
- Personal Info: Show the user their own invite count and mention who invited them (by fetching their referrer_id and getting that user's username).

---

## 3. Detailed Implementation Steps

### Step 1: Database Migration (PostgreSQL → SQLite)

**Current State:** The application currently uses PostgreSQL with asyncpg. Need to migrate to SQLite.

**Tasks:**
- Update database connection pool to use aiosqlite instead of asyncpg
- Update database schema to use SQLite syntax (remove PostgreSQL-specific features like SERIAL, enums, etc.)
- Update database manager methods to work with SQLite (replace $1, $2 placeholders with ?)
- Remove Docker Compose PostgreSQL setup
- Update .env.example to use SQLite database path instead of PostgreSQL connection string

### Step 2: Update Database Schema

Replace existing PostgreSQL schema with referral bot schema:
- Create `users` table with columns: user_id (INTEGER PRIMARY KEY), referrer_id (INTEGER NULLABLE), username (TEXT NULLABLE), join_date (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
- Create index on referrer_id column for performance
- Remove old tables (tests, questions, options, attempts, answers)

### Step 3: Update Database Manager

Update the DBManager class to handle referral-specific operations:
- add_user(user_id, referrer_id, username)
- is_user_exists(user_id)
- get_invite_count(user_id)
- get_top_referrers(limit=10)
- get_referrer_of_user(user_id)

### Step 4: Configuration File

Update config to include:
- BOT_TOKEN (already exists)
- CHANNEL_ID (e.g., -100...) - add this
- Remove SUPREME_TG_ID (admin panel not needed for referral bot)

### Step 5: Remove Admin Panel

Remove or disable admin panel functionality:
- Remove admin section routers
- Remove admin panel registration from initialization
- Keep admin-related code in place but don't register it (for potential future use)

### Step 6: Implement Membership Gate Middleware

Create middleware to check channel membership before allowing commands.

### Step 7: Implement Bot Commands

- /start with referral logic
- /link command
- /rating command with leaderboard

---

## 4. Scalability Note for SQLite

While SQLite is single-file, it is extremely efficient for this specific use case.

- **Read Performance:** SQLite can handle thousands of concurrent reads for the /rating command.
- **Write Performance:** Since registration happens once per user, write-locking won't be an issue even with tens of thousands of users.
- **Storage:** A table with 100,000 rows in this format will likely take up less than 10MB of space.
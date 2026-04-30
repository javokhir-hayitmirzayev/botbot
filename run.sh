#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${GREEN}🤖 Aiogram Bot Runner${NC}"
echo "================================"

# Check if .env file exists
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo "Creating .env from .env.example..."
    cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
    echo -e "${YELLOW}Please edit .env with your actual credentials:${NC}"
    echo "  - BOT_TOKEN"
    echo "  - CHANNEL_ID"
    echo "  - CHANNEL_URL"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
fi

# Check if docker compose is installed
if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}❌ docker compose is not installed${NC}"
    exit 1
fi

# Parse command line arguments
COMMAND="${1:-up}"

case "$COMMAND" in
    up)
        echo -e "${GREEN}Starting bot...${NC}"
        docker compose -f "$SCRIPT_DIR/docker-compose.yml" up -d
        echo -e "${GREEN}✅ Bot started in background${NC}"
        echo "View logs: ./run.sh logs"
        ;;
    down)
        echo -e "${YELLOW}Stopping bot...${NC}"
        docker compose -f "$SCRIPT_DIR/docker-compose.yml" down
        echo -e "${GREEN}✅ Bot stopped${NC}"
        ;;
    logs)
        docker compose -f "$SCRIPT_DIR/docker-compose.yml" logs -f bot
        ;;
    restart)
        echo -e "${YELLOW}Restarting bot...${NC}"
        docker compose -f "$SCRIPT_DIR/docker-compose.yml" restart bot
        echo -e "${GREEN}✅ Bot restarted${NC}"
        ;;
    status)
        echo -e "${GREEN}Bot status:${NC}"
        docker compose -f "$SCRIPT_DIR/docker-compose.yml" ps
        ;;
    build)
        echo -e "${GREEN}Building image...${NC}"
        docker compose -f "$SCRIPT_DIR/docker-compose.yml" build
        echo -e "${GREEN}✅ Build complete${NC}"
        ;;
    shell)
        echo -e "${GREEN}Opening container shell...${NC}"
        docker compose -f "$SCRIPT_DIR/docker-compose.yml" exec bot /bin/bash
        ;;
    db)
        docker compose -f "$SCRIPT_DIR/docker-compose.yml" exec -T bot python3 << 'EOF'
import sqlite3
import os

db_path = "/app/bot.db"
if not os.path.exists(db_path):
    print("❌ Database file not found")
    exit(1)

def print_table(cursor, headers):
    rows = cursor.fetchall()
    if not rows:
        print("(empty)")
        return

    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    sep = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    print(sep)
    print("| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |")
    print(sep)
    for row in rows:
        print("| " + " | ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(row)) + " |")
    print(sep)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\033[92m📊 Users Table:\033[0m")
cursor.execute("SELECT user_id, referrer_id, username, first_name, join_date FROM users ORDER BY user_id")
print_table(cursor, ["user_id", "referrer_id", "username", "first_name", "join_date"])

print()
print("\033[92m⏳ Pending Referrals Table:\033[0m")
cursor.execute("SELECT user_id, referrer_id, username, created_at FROM pending_referrals ORDER BY user_id")
print_table(cursor, ["user_id", "referrer_id", "username", "created_at"])

conn.close()
EOF
        ;;

    *)
        echo -e "${GREEN}Usage: ./run.sh [COMMAND]${NC}"
        echo ""
        echo "Commands:"
        echo "  up       - Start the bot (default)"
        echo "  down     - Stop the bot"
        echo "  logs     - Show bot logs (follow mode)"
        echo "  restart  - Restart the bot"
        echo "  status   - Show container status"
        echo "  build    - Build Docker image"
        echo "  shell    - Open shell in container"
        echo "  db       - Display database tables (users & pending_referrals)"
        echo ""
        echo "Examples:"
        echo "  ./run.sh          # Start bot"
        echo "  ./run.sh logs     # View logs"
        echo "  ./run.sh down     # Stop bot"
        echo "  ./run.sh db       # Show database"
        ;;
esac

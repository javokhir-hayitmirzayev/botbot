# Docker Setup Guide

## Running the Bot in Docker

### Prerequisites
- Docker and Docker Compose installed

### Quick Start

1. **Create .env file from example:**
```bash
cp .env.example .env
```

2. **Update .env with your credentials:**
```bash
# Edit .env and add:
BOT_TOKEN=your_actual_bot_token_here
CHANNEL_ID=your_channel_id_here
CHANNEL_URL=your_channel_url_here
TIMEZONE=Asia/Tashkent
DB_PATH=/app/data/bot.db
```

3. **Run with Docker Compose:**
```bash
docker-compose up -d
```

4. **View logs:**
```bash
docker-compose logs -f bot
```

5. **Stop the bot:**
```bash
docker-compose down
```

## Manual Docker Build & Run

### Build image:
```bash
docker build -t aiogram-bot .
```

### Run container:
```bash
docker run -d \
  --name aiogram-bot \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  --restart unless-stopped \
  aiogram-bot
```

## Environment Variables

All environment variables are read from the `.env` file:
- `BOT_TOKEN` - Telegram bot token from BotFather
- `CHANNEL_ID` - Target channel ID for membership checks
- `CHANNEL_URL` - Channel URL for invitations
- `TIMEZONE` - Application timezone (default: Asia/Tashkent)
- `DB_PATH` - Path to SQLite database (default: bot.db)

## Data Persistence

The `data/` directory is mounted as a Docker volume, ensuring:
- Database persists across container restarts
- Logs are preserved

## Troubleshooting

### Container keeps restarting?
```bash
docker-compose logs bot
```
Check .env configuration, especially BOT_TOKEN and CHANNEL_ID.

### Database file not found?
The `data/` directory is created automatically. Ensure proper permissions:
```bash
chmod 755 data/
```

### Permission denied errors?
Run as non-root or adjust volume permissions:
```bash
docker-compose exec bot chown -R nobody:nogroup /app/data
```

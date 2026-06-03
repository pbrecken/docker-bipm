# Docker Flask Titanic App

This project is a small Docker Compose web application for the BIPM Docker exercise.

It uses:

- Flask for the web app
- Redis for a visitor counter
- Docker Compose to run both services
- Pandas to load and display a Titanic CSV dataset

## Run

Create a local `.env` file first:

```bash
REDIS_PASSWORD=MyBIPMPassword
REDIS_HOST=redis
```

Then start the app:

```bash
docker compose up --build
```

Then open http://localhost:4000/.

# API Scanner - Self-Hosted Deployment

API Scanner is an automated API security testing tool that scans REST and SOAP APIs for vulnerabilities using OpenAPI/Swagger specifications and WSDL files.

**Docker Hub**: [`cysecurity/api-scanner`](https://hub.docker.com/r/cysecurity/api-scanner)

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2
- Python 3.6+ (for setup script)
- 8 GB RAM minimum (16 GB recommended)
- 20 GB disk space

## Quick Start

1. **Clone this repository**

```bash
git clone https://github.com/cysecurity/api-scanner.git
cd api-scanner
```

2. **Run setup**

```bash
python3 setup.py
```

The script will:
- Generate secure random passwords for all services
- Auto-detect your timezone
- Generate a self-signed TLS certificate (or use your own if already in `./certs/`)
- Write the `.env` configuration file
- Offer to start the Docker Compose stack

3. **Access the panel**

Open `https://localhost:4455` in your browser.

> If using a self-signed certificate, your browser will show a security warning — proceed to accept it.

## Manual Setup

If you prefer to configure manually instead of using the setup script:

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` and update:
   - All `change_me_*` passwords with strong random values
   - `CSRF_KEY` with a random 32+ character string
   - `ZAP_API_KEY` with a random string
   - `TRUSTED_ORIGINS` with your domain (e.g., `https://scanner.yourcompany.com`)
   - Ensure passwords in `DATABASE_URI` and `MONGO_DATABASE_URI` match the individual password variables

3. Start the stack:

```bash
docker compose up -d
```

## Architecture

| Service         | Image                              | Description                                        |
|-----------------|------------------------------------|----------------------------------------------------|
| **api-scanner** | `cysecurity/api-scanner:latest`    | Web panel + scan engine in a single container      |
| **zap**         | `ghcr.io/zaproxy/zaproxy:stable`   | OWASP ZAP security scanner                         |
| **mariadb**     | `mariadb:10.11`                    | User management and session storage                |
| **mongodb**     | `mongo:4.4`                        | Scan data, results, and reports                    |

## Configuration

All configuration is done through the `.env` file. See `.env.example` for all available options.

### Key Settings

| Variable | Description |
|----------|-------------|
| `MARIADB_PASSWORD` | MariaDB application user password |
| `MONGO_APP_PASSWORD` | MongoDB application user password |
| `CSRF_KEY` | CSRF protection key (32+ characters) |
| `ZAP_API_KEY` | ZAP API authentication key |
| `TRUSTED_ORIGINS` | Allowed HTTPS origins for the panel |
| `USE_TLS` | Enable HTTPS (default: `true`) |
| `TZ` | Timezone (default: `UTC`) |

## Data Persistence

All data is stored in Docker named volumes:

- `mariadb_data` — User accounts, roles, sessions
- `mongodb_data` — Scan records, results, reports
- `scanner_data` — Work files, uploaded specs, generated reports

## Updating

```bash
docker compose pull
docker compose up -d
```

## Stopping

```bash
docker compose down
```

To remove all data (destructive):

```bash
docker compose down -v
```

## Troubleshooting

**Check logs:**

```bash
docker compose logs api-scanner
docker compose logs zap
```

**Check service health:**

```bash
docker compose ps
```

**ZAP not starting:** Ensure at least 4 GB of free RAM. ZAP requires ~3 GB.

**Panel not accessible:** Verify TLS certificates are in `./certs/` and `TRUSTED_ORIGINS` matches your URL including the port (e.g., `https://localhost:4455`).

**Database connection errors:** Wait 30-60 seconds after first start for databases to initialize.

## Documentation

Full user manual: [https://cspf-founder.github.io/api-scanner-docker/](https://cspf-founder.github.io/api-scanner-docker/)

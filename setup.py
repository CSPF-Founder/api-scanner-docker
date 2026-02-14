#!/usr/bin/env python3
"""
API Scanner setup script.

Generates secure passwords, writes .env configuration, and optionally
starts the Docker Compose stack.

Requirements: Python 3.6+, Docker with Compose v2.
No third-party dependencies.
"""

import datetime
import os
import secrets
import shutil
import string
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(SCRIPT_DIR, ".env")
COMPOSE_FILE = os.path.join(SCRIPT_DIR, "docker-compose.yml")

ALPHABET = string.ascii_letters + string.digits

# CLDR "001" (default territory) mapping from Windows timezone IDs to IANA names.
# Source: https://github.com/unicode-org/cldr/blob/main/common/supplemental/windowsZones.xml
WINDOWS_TO_IANA = {
    "Dateline Standard Time": "Etc/GMT+12",
    "UTC-11": "Etc/GMT+11",
    "Aleutian Standard Time": "America/Adak",
    "Hawaiian Standard Time": "Pacific/Honolulu",
    "Marquesas Standard Time": "Pacific/Marquesas",
    "Alaskan Standard Time": "America/Anchorage",
    "UTC-09": "Etc/GMT+9",
    "Pacific Standard Time (Mexico)": "America/Tijuana",
    "UTC-08": "Etc/GMT+8",
    "Pacific Standard Time": "America/Los_Angeles",
    "US Mountain Standard Time": "America/Phoenix",
    "Mountain Standard Time (Mexico)": "America/Mazatlan",
    "Mountain Standard Time": "America/Denver",
    "Yukon Standard Time": "America/Whitehorse",
    "Central America Standard Time": "America/Guatemala",
    "Central Standard Time": "America/Chicago",
    "Easter Island Standard Time": "Pacific/Easter",
    "Central Standard Time (Mexico)": "America/Mexico_City",
    "Canada Central Standard Time": "America/Regina",
    "SA Pacific Standard Time": "America/Bogota",
    "Eastern Standard Time (Mexico)": "America/Cancun",
    "Eastern Standard Time": "America/New_York",
    "Haiti Standard Time": "America/Port-au-Prince",
    "Cuba Standard Time": "America/Havana",
    "US Eastern Standard Time": "America/Indianapolis",
    "Turks And Caicos Standard Time": "America/Grand_Turk",
    "Paraguay Standard Time": "America/Asuncion",
    "Atlantic Standard Time": "America/Halifax",
    "Venezuela Standard Time": "America/Caracas",
    "Central Brazilian Standard Time": "America/Cuiaba",
    "SA Western Standard Time": "America/La_Paz",
    "Pacific SA Standard Time": "America/Santiago",
    "Newfoundland Standard Time": "America/St_Johns",
    "Tocantins Standard Time": "America/Araguaina",
    "E. South America Standard Time": "America/Sao_Paulo",
    "SA Eastern Standard Time": "America/Cayenne",
    "Argentina Standard Time": "America/Buenos_Aires",
    "Greenland Standard Time": "America/Godthab",
    "Montevideo Standard Time": "America/Montevideo",
    "Magallanes Standard Time": "America/Punta_Arenas",
    "Saint Pierre Standard Time": "America/Miquelon",
    "Bahia Standard Time": "America/Bahia",
    "UTC-02": "Etc/GMT+2",
    "Azores Standard Time": "Atlantic/Azores",
    "Cape Verde Standard Time": "Atlantic/Cape_Verde",
    "UTC": "Etc/UTC",
    "GMT Standard Time": "Europe/London",
    "Greenwich Standard Time": "Atlantic/Reykjavik",
    "Sao Tome Standard Time": "Africa/Sao_Tome",
    "Morocco Standard Time": "Africa/Casablanca",
    "W. Europe Standard Time": "Europe/Berlin",
    "Central Europe Standard Time": "Europe/Budapest",
    "Romance Standard Time": "Europe/Paris",
    "Central European Standard Time": "Europe/Warsaw",
    "W. Central Africa Standard Time": "Africa/Lagos",
    "Jordan Standard Time": "Asia/Amman",
    "GTB Standard Time": "Europe/Bucharest",
    "Middle East Standard Time": "Asia/Beirut",
    "Egypt Standard Time": "Africa/Cairo",
    "E. Europe Standard Time": "Europe/Chisinau",
    "Syria Standard Time": "Asia/Damascus",
    "West Bank Standard Time": "Asia/Hebron",
    "South Africa Standard Time": "Africa/Johannesburg",
    "FLE Standard Time": "Europe/Kiev",
    "Israel Standard Time": "Asia/Jerusalem",
    "South Sudan Standard Time": "Africa/Juba",
    "Kaliningrad Standard Time": "Europe/Kaliningrad",
    "Sudan Standard Time": "Africa/Khartoum",
    "Libya Standard Time": "Africa/Tripoli",
    "Namibia Standard Time": "Africa/Windhoek",
    "Arabic Standard Time": "Asia/Baghdad",
    "Turkey Standard Time": "Europe/Istanbul",
    "Arab Standard Time": "Asia/Riyadh",
    "Belarus Standard Time": "Europe/Minsk",
    "Russian Standard Time": "Europe/Moscow",
    "E. Africa Standard Time": "Africa/Nairobi",
    "Iran Standard Time": "Asia/Tehran",
    "Arabian Standard Time": "Asia/Dubai",
    "Astrakhan Standard Time": "Europe/Astrakhan",
    "Azerbaijan Standard Time": "Asia/Baku",
    "Russia Time Zone 3": "Europe/Samara",
    "Mauritius Standard Time": "Indian/Mauritius",
    "Saratov Standard Time": "Europe/Saratov",
    "Georgian Standard Time": "Asia/Tbilisi",
    "Volgograd Standard Time": "Europe/Volgograd",
    "Caucasus Standard Time": "Asia/Yerevan",
    "Afghanistan Standard Time": "Asia/Kabul",
    "West Asia Standard Time": "Asia/Tashkent",
    "Ekaterinburg Standard Time": "Asia/Yekaterinburg",
    "Pakistan Standard Time": "Asia/Karachi",
    "Qyzylorda Standard Time": "Asia/Qyzylorda",
    "India Standard Time": "Asia/Calcutta",
    "Sri Lanka Standard Time": "Asia/Colombo",
    "Nepal Standard Time": "Asia/Katmandu",
    "Central Asia Standard Time": "Asia/Bishkek",
    "Bangladesh Standard Time": "Asia/Dhaka",
    "Omsk Standard Time": "Asia/Omsk",
    "Myanmar Standard Time": "Asia/Rangoon",
    "SE Asia Standard Time": "Asia/Bangkok",
    "Altai Standard Time": "Asia/Barnaul",
    "W. Mongolia Standard Time": "Asia/Hovd",
    "North Asia Standard Time": "Asia/Krasnoyarsk",
    "N. Central Asia Standard Time": "Asia/Novosibirsk",
    "Tomsk Standard Time": "Asia/Tomsk",
    "China Standard Time": "Asia/Shanghai",
    "North Asia East Standard Time": "Asia/Irkutsk",
    "Singapore Standard Time": "Asia/Singapore",
    "W. Australia Standard Time": "Australia/Perth",
    "Taipei Standard Time": "Asia/Taipei",
    "Ulaanbaatar Standard Time": "Asia/Ulaanbaatar",
    "Aus Central W. Standard Time": "Australia/Eucla",
    "Transbaikal Standard Time": "Asia/Chita",
    "Tokyo Standard Time": "Asia/Tokyo",
    "North Korea Standard Time": "Asia/Pyongyang",
    "Korea Standard Time": "Asia/Seoul",
    "Yakutsk Standard Time": "Asia/Yakutsk",
    "Cen. Australia Standard Time": "Australia/Adelaide",
    "AUS Central Standard Time": "Australia/Darwin",
    "E. Australia Standard Time": "Australia/Brisbane",
    "AUS Eastern Standard Time": "Australia/Sydney",
    "West Pacific Standard Time": "Pacific/Port_Moresby",
    "Tasmania Standard Time": "Australia/Hobart",
    "Vladivostok Standard Time": "Asia/Vladivostok",
    "Lord Howe Standard Time": "Australia/Lord_Howe",
    "Bougainville Standard Time": "Pacific/Bougainville",
    "Russia Time Zone 10": "Asia/Srednekolymsk",
    "Magadan Standard Time": "Asia/Magadan",
    "Norfolk Standard Time": "Pacific/Norfolk",
    "Sakhalin Standard Time": "Asia/Sakhalin",
    "Central Pacific Standard Time": "Pacific/Guadalcanal",
    "Russia Time Zone 11": "Asia/Kamchatka",
    "New Zealand Standard Time": "Pacific/Auckland",
    "UTC+12": "Etc/GMT-12",
    "Fiji Standard Time": "Pacific/Fiji",
    "Chatham Islands Standard Time": "Pacific/Chatham",
    "UTC+13": "Etc/GMT-13",
    "Tonga Standard Time": "Pacific/Tongatapu",
    "Samoa Standard Time": "Pacific/Apia",
    "Line Islands Standard Time": "Pacific/Kiritimati",
}


def generate_password(length: int) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def check_python_version() -> None:
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or later is required.")
        sys.exit(1)


def check_command(args: list) -> bool:
    try:
        result = subprocess.run(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def check_prerequisites() -> None:
    check_python_version()

    if not shutil.which("docker"):
        print("Error: 'docker' not found. Install Docker first.")
        sys.exit(1)

    if not check_command(["docker", "compose", "version"]):
        print("Error: 'docker compose' not available. Install Docker Compose v2.")
        sys.exit(1)

    if not check_command(["docker", "info"]):
        print("Error: Docker daemon is not running.")
        if sys.platform == "win32":
            print("Start Docker Desktop and try again.")
        else:
            print("Try: sudo systemctl start docker")
        sys.exit(1)

    if not os.path.isfile(COMPOSE_FILE):
        print(f"Error: docker-compose.yml not found at {COMPOSE_FILE}")
        print("Run this script from the deployment directory.")
        sys.exit(1)


def _utc_offset_hint() -> str:
    offset = datetime.datetime.now(datetime.timezone.utc).astimezone().utcoffset()
    if offset is None:
        return "UTC+?"
    total_seconds = int(offset.total_seconds())
    sign = "+" if total_seconds >= 0 else "-"
    hours, remainder = divmod(abs(total_seconds), 3600)
    minutes = remainder // 60
    if minutes:
        return f"UTC{sign}{hours}:{minutes:02d}"
    return f"UTC{sign}{hours}"


def _detect_timezone_windows() -> str:
    try:
        result = subprocess.run(
            ["tzutil", "/g"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            win_tz = result.stdout.strip()
            iana = WINDOWS_TO_IANA.get(win_tz)
            if iana:
                return iana

            hint = _utc_offset_hint()
            print(f"Windows timezone '{win_tz}' ({hint}) not in mapping.")
            try:
                user_tz = input("Enter IANA timezone (e.g. America/New_York): ").strip()
                if user_tz:
                    return user_tz
            except (EOFError, KeyboardInterrupt):
                print()
    except FileNotFoundError:
        pass

    return ""


def detect_timezone() -> str:
    # /etc/timezone (Debian/Ubuntu)
    try:
        with open("/etc/timezone") as f:
            tz = f.read().strip()
            if tz:
                return tz
    except OSError:
        pass

    # /etc/localtime symlink (Linux/macOS)
    try:
        link = os.path.realpath("/etc/localtime")
        marker = "zoneinfo/"
        idx = link.find(marker)
        if idx != -1:
            return link[idx + len(marker):]
    except OSError:
        pass

    # tzutil (Windows)
    if sys.platform == "win32":
        tz = _detect_timezone_windows()
        if tz:
            return tz

    return "UTC"


def confirm(question: str, default_yes: bool = False) -> bool:
    hint = "[Y/n]" if default_yes else "[y/N]"
    try:
        sys.stdout.flush()
        response = input(f"{question} {hint}: ").strip().lower()
    except EOFError:
        print("\nCould not read input (EOFError). Assuming default.")
        return default_yes
    except KeyboardInterrupt:
        print()
        return False
    if not response:
        return default_yes
    return response in ("y", "yes")


def build_env_content(passwords: dict, settings: dict) -> str:
    database_uri = (
        f"api_scanner:{passwords['MARIADB_PASSWORD']}"
        f"@tcp(mariadb:3306)/api_db?parseTime=True"
    )
    mongo_database_uri = (
        f"mongodb://apiscan_user:{passwords['MONGO_APP_PASSWORD']}"
        f"@mongodb:27017/apiscan_db?authMechanism=SCRAM-SHA-256"
    )

    lines = [
        "# =============================================================================",
        "# API Scanner Configuration",
        "# Generated by setup.py — do not commit this file",
        "# =============================================================================",
        "",
        "# --- MariaDB ---",
        f"MARIADB_ROOT_PASSWORD={passwords['MARIADB_ROOT_PASSWORD']}",
        "MARIADB_USER=api_scanner",
        f"MARIADB_PASSWORD={passwords['MARIADB_PASSWORD']}",
        "MARIADB_DATABASE=api_db",
        "",
        "# --- MongoDB ---",
        "MONGO_ROOT_USERNAME=root",
        f"MONGO_ROOT_PASSWORD={passwords['MONGO_ROOT_PASSWORD']}",
        "MONGO_DATABASE=apiscan_db",
        "MONGO_APP_USERNAME=apiscan_user",
        f"MONGO_APP_PASSWORD={passwords['MONGO_APP_PASSWORD']}",
        "",
        "# --- API Scanner ---",
        "SERVER_ADDRESS=0.0.0.0:443",
        "USE_TLS=true",
        "CERT_PATH=/app/certs/cert.pem",
        "KEY_PATH=/app/certs/key.pem",
        f"CSRF_KEY={passwords['CSRF_KEY']}",
        "CSRF_NAME=csrf_token",
        "ALLOWED_INTERNAL_HOSTS=localhost,127.0.0.1,api-scanner",
        f"TRUSTED_ORIGINS={settings['TRUSTED_ORIGINS']}",
        "",
        "DBMS_TYPE=mysql",
        "# Note: 'mariadb' here refers to the docker-compose service name",
        f"DATABASE_URI={database_uri}",
        "MIGRATIONS_PREFIX=/app/db/migrations",
        "",
        f"PRODUCT_TITLE={settings['PRODUCT_TITLE']}",
        f"COPYRIGHT_FOOTER_COMPANY={settings['COPYRIGHT_FOOTER_COMPANY']}",
        f"CONTACT_ADDRESS={settings['CONTACT_ADDRESS']}",
        "",
        "# Note: 'mongodb' here refers to the docker-compose service name",
        f"MONGO_DATABASE_URI={mongo_database_uri}",
        "MONGO_DATABASE_NAME=apiscan_db",
        "",
        "WORK_DIR=/app/data/work_dir",
        "TEMP_UPLOADS_DIR=/app/data/temp_uploads",
        "",
        "LOG_LEVEL=info",
        "LOG_FILENAME=/app/logs/app.log",
        "",
        "# Required by manager config but unused in Docker mode",
        "SCANNER_DOCKER=unused",
        "FUZZER_IMAGE=unused",
        "MAIN_DOMAIN=localhost",
        "",
        "# Required by panel config but unused in community edition",
        "LICENSE_VALIDATION_API=http://localhost",
        "",
        "# Note: 'zap' here refers to the docker-compose service name",
        "ZAP_HOST=zap",
        "ZAP_PORT=8080",
        f"ZAP_API_KEY={passwords['ZAP_API_KEY']}",
        "",
        "REMOTE_WORK_DIR=/app/data/work_dir/",
        "LOCAL_TEMP_DIR=/app/data/temp/",
        "",
        "CATS_BIN_PATH=/app/bin/cats",
        "REPORTER_BIN_PATH=/app/bin/reporter",
        "SCANNER_CMD=/app/bin/scanner",
        "",
        "# --- Timezone ---",
        f"TZ={settings['TZ']}",
    ]
    return "\n".join(lines) + "\n"


def print_summary(passwords: dict, timezone: str) -> None:
    print("\n" + "=" * 60)
    print("  Configuration Summary")
    print("=" * 60)

    print("\n  Generated credentials (save these somewhere safe):\n")
    col = max(len(k) for k in passwords) + 2
    for key, value in passwords.items():
        print(f"    {key:<{col}} {value}")

    print(f"\n  Timezone: {timezone}")

    print("\n" + "=" * 60)
    print(f"  .env written to: {ENV_FILE}")
    print("=" * 60)


def start_stack() -> None:
    print("\nStarting Docker Compose stack...")
    result = subprocess.run(
        ["docker", "compose", "up", "-d"],
        cwd=SCRIPT_DIR,
    )
    if result.returncode == 0:
        print("\nStack started successfully!")
        print("Access the panel at: https://localhost:4455")
        print(
            "\nNote: On first start, databases may take 30-60 seconds to initialize."
        )
        print("If using self-signed certs, your browser will show a security warning.")
    else:
        print("\nFailed to start the stack. Check the output above for errors.")
        sys.exit(1)


def main() -> None:
    print("API Scanner Setup")
    print("-" * 40)

    check_prerequisites()
    print("Prerequisites OK.\n")

    if os.path.isfile(ENV_FILE):
        print(f"An .env file already exists at:\n  {ENV_FILE}\n")
        if not confirm("Overwrite it with a new configuration?"):
            print("Aborted.")
            sys.exit(0)
        print()

    # Generate secure passwords
    passwords = {
        "MARIADB_ROOT_PASSWORD": generate_password(24),
        "MARIADB_PASSWORD": generate_password(24),
        "MONGO_ROOT_PASSWORD": generate_password(24),
        "MONGO_APP_PASSWORD": generate_password(24),
        "CSRF_KEY": generate_password(32),
        "ZAP_API_KEY": generate_password(24),
    }

    settings = {
        "PRODUCT_TITLE": "API Scanner",
        "COPYRIGHT_FOOTER_COMPANY": "CySecurity Pte Ltd",
        "CONTACT_ADDRESS": "support@localhost",
        "TRUSTED_ORIGINS": "https://localhost:4455",
        "TZ": detect_timezone(),
    }

    content = build_env_content(passwords, settings)

    with open(ENV_FILE, "w") as f:
        f.write(content)

    print_summary(passwords, settings["TZ"])

    os.makedirs(os.path.join(SCRIPT_DIR, "certs"), exist_ok=True)

    print()
    if confirm("Start the Docker Compose stack now?", default_yes=True):
        start_stack()
    else:
        print("\nTo start later, run:")
        print(f"  cd {SCRIPT_DIR}")
        print("  docker compose up -d")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)

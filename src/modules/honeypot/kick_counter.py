
import json
import asyncio
from pathlib import Path

from logging_setup import log


DATA_DIR = Path(__file__).resolve().parents[3] / "data"
COUNTER_FILE = DATA_DIR / "kick_counter.json"

_counter_lock = asyncio.Lock()


def _read_count():
    if not COUNTER_FILE.exists():
        return 0

    try:
        data = json.loads(COUNTER_FILE.read_text(encoding="utf-8"))
        return max(0, int(data.get("total", 0)))
    except (ValueError, TypeError, AttributeError, json.JSONDecodeError):
        log.warning("Kick counter file is invalid. Starting at zero.")
        return 0


async def get_kick_count():
    async with _counter_lock:
        return _read_count()


async def increment_kick_count():
    async with _counter_lock:
        count = _read_count() + 1

        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)

            temp_file = COUNTER_FILE.with_suffix(".tmp")
            temp_file.write_text(
                json.dumps({"total": count}, indent=4),
                encoding="utf-8",
            )
            temp_file.replace(COUNTER_FILE)

            log.info(f"Total honeypot kicks: {count}")
            return count

        except OSError as e:
            log.error(f"Failed to save kick counter: {e}")
            return count

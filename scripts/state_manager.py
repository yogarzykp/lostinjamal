import json
import os

STATE_KEY = "state"

# Redis import made optional (fallback to in-memory dict) to prevent
# trainer container from dying with ModuleNotFoundError when redis
# isn't installed in the active venv. State persistence degrades to
# process-local only when redis unavailable — training still runs.
try:
    import redis  # type: ignore
    _REDIS_AVAILABLE = True
except ImportError:
    redis = None  # type: ignore
    _REDIS_AVAILABLE = False
    print("[state_manager] redis module not available — using in-memory fallback", flush=True)

# In-memory fallback state (process-local only)
_FALLBACK_STATE: dict = {}


def _get_redis_client():
    """Get a Redis client connection with configuration from environment variables."""
    if not _REDIS_AVAILABLE:
        return None
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", 6379))
    password = os.getenv("REDIS_PASSWORD", None)
    db = int(os.getenv("REDIS_DB", 0))

    return redis.Redis(
        host=host,
        port=port,
        password=password,
        db=db,
        decode_responses=True
    )


def get_state() -> dict:
    """Return the parsed JSON state from redis, or in-memory fallback."""
    if not _REDIS_AVAILABLE:
        return dict(_FALLBACK_STATE)
    try:
        client = _get_redis_client()
        value = client.get(STATE_KEY)
        if value is None:
            return {}
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return {}
    except Exception as exc:
        # Redis available but connection failed — fall back gracefully
        print(f"[state_manager] redis get failed ({exc}) — using in-memory", flush=True)
        return dict(_FALLBACK_STATE)


def set_state(state: dict) -> None:
    """Persist state to redis, or in-memory fallback."""
    global _FALLBACK_STATE
    if not _REDIS_AVAILABLE:
        _FALLBACK_STATE = dict(state)
        return
    try:
        client = _get_redis_client()
        json_value = json.dumps(state)
        client.set(STATE_KEY, json_value)
    except Exception as exc:
        print(f"[state_manager] redis set failed ({exc}) — using in-memory", flush=True)
        _FALLBACK_STATE = dict(state)


def test():
    state = get_state()
    print(json.dumps(state, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    test()

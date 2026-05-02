"""Per-chat playback queue + seek state."""
from collections import defaultdict, deque

# chat_id -> deque[ {title, link, thumbnail, duration, file, video_id, requested_by} ]
QUEUES: dict[int, deque] = defaultdict(deque)

# chat_id -> currently playing track dict
NOW_PLAYING: dict[int, dict] = {}

# chat_id -> current playback offset (seconds) for seek
SEEK_OFFSET: dict[int, int] = defaultdict(int)


def push(chat_id: int, track: dict):
    QUEUES[chat_id].append(track)


def pop_next(chat_id: int):
    if QUEUES[chat_id]:
        return QUEUES[chat_id].popleft()
    return None


def clear(chat_id: int):
    QUEUES[chat_id].clear()
    NOW_PLAYING.pop(chat_id, None)
    SEEK_OFFSET.pop(chat_id, None)


def length(chat_id: int) -> int:
    return len(QUEUES[chat_id])

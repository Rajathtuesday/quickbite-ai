from collections import defaultdict

# session_id -> dish_id -> boost score
SESSION_MEMORY = defaultdict(lambda: defaultdict(float))

BOOST_VALUE = 0.20   # per click
MAX_BOOST = 0.60     # cap per dish


def boost_dish(session_id: str, dish_id: str):
    current = SESSION_MEMORY[session_id][dish_id]
    new_value = min(current + BOOST_VALUE, MAX_BOOST)
    SESSION_MEMORY[session_id][dish_id] = new_value


def get_boost(session_id: str, dish_id: str) -> float:
    return SESSION_MEMORY[session_id].get(dish_id, 0.0)

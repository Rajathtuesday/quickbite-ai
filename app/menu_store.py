import json
import os

MENU_DIR = "menus"
os.makedirs(MENU_DIR, exist_ok=True)


def save_menu(restaurant_id: str, menu: list):
    file_path = os.path.join(MENU_DIR, f"{restaurant_id}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(menu, f, indent=2)


def load_menu(restaurant_id: str):
    file_path = os.path.join(MENU_DIR, f"{restaurant_id}.json")

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

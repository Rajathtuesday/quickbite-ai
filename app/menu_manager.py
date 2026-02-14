import csv
from io import StringIO

_current_menu = []

def get_menu():
    return _current_menu


def load_menu_from_csv(content: str):
    global _current_menu

    reader = csv.DictReader(StringIO(content))
    dishes = []

    for idx, row in enumerate(reader, start=1):
        name = row["name"]
        price = float(row["price"])
        cost = float(row["cost"])
        category = row["category"].lower()

        margin = price - cost

        # Basic tag generation
        tags = []

        if "south" in category:
            tags.append("south_indian")
        if "north" in category:
            tags.append("north_indian")
        if "sweet" in category:
            tags.append("sweet")
        if "healthy" in category:
            tags.append("healthy")

        if price < 150:
            tags.append("budget")

        dish = {
            "dish_id": f"d{idx}",
            "name": name,
            "price": price,
            "cost": cost,
            "margin": margin,
            "tags": tags,
            "popularity": 0.5  # default
        }

        dishes.append(dish)

    _current_menu = dishes

    return len(dishes)

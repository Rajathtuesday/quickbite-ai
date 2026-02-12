# ----------------------------------------
# City Taste Bias
# ----------------------------------------

BANGALORE_BIAS = {
    "spicy": 0.8,
    "south_indian": 0.95,
    "north_indian": 0.6,
    "light_fresh": 0.9,
    "healthy": 0.85,
    "fried": 0.5,
    "creamy": 0.4,
    "sweet": 0.6,
    "street_food": 0.8,
    "comfort_food": 0.85
}

# ----------------------------------------
# Festivals
# ----------------------------------------

FESTIVALS = {
    "2026-11-01": "diwali",
    "2026-01-14": "pongal",
    "2026-03-25": "holi",
    "2026-08-15": "independence_day"
}

# ----------------------------------------
# Extended Dish Dataset
# ----------------------------------------

DISHES = [

    # ---- SOUTH INDIAN ----

    {
        "dish_id": "d1",
        "name": "Masala Dosa",
        "price": 120,
        "tags": ["spicy", "south_indian", "veg", "light_fresh", "comfort_food"],
        "contexts": ["office_lunch", "light_healthy", "quick_bite"],
        "time_suitable": ["morning", "lunch"],
        "festival_special": ["pongal"],
        "popularity": 0.92
    },

    {
        "dish_id": "d2",
        "name": "Idli Sambar",
        "price": 80,
        "tags": ["healthy", "south_indian", "veg", "light_fresh"],
        "contexts": ["breakfast", "light_healthy"],
        "time_suitable": ["morning"],
        "festival_special": ["pongal"],
        "popularity": 0.88
    },

    {
        "dish_id": "d3",
        "name": "Curd Rice",
        "price": 110,
        "tags": ["light_fresh", "south_indian", "veg", "comfort_food"],
        "contexts": ["office_lunch", "lazy_tired"],
        "time_suitable": ["lunch"],
        "festival_special": [],
        "popularity": 0.75
    },

    # ---- NORTH INDIAN ----

    {
        "dish_id": "d4",
        "name": "Paneer Butter Masala",
        "price": 220,
        "tags": ["creamy", "north_indian", "veg", "heavy_gravy", "indulgent"],
        "contexts": ["treat_myself", "group_order", "date_night"],
        "time_suitable": ["lunch", "night"],
        "festival_special": ["diwali"],
        "popularity": 0.85
    },

    {
        "dish_id": "d5",
        "name": "Chole Bhature",
        "price": 180,
        "tags": ["spicy", "north_indian", "fried", "street_food"],
        "contexts": ["weekend_brunch", "treat_myself"],
        "time_suitable": ["lunch"],
        "festival_special": [],
        "popularity": 0.83
    },

    # ---- STREET FOOD ----

    {
        "dish_id": "d6",
        "name": "Samosa",
        "price": 60,
        "tags": ["fried", "veg", "snack", "street_food"],
        "contexts": ["lazy_tired", "evening_snack"],
        "time_suitable": ["evening"],
        "festival_special": [],
        "popularity": 0.80
    },

    {
        "dish_id": "d7",
        "name": "Pani Puri",
        "price": 70,
        "tags": ["street_food", "spicy", "veg"],
        "contexts": ["hangout", "evening_snack"],
        "time_suitable": ["evening"],
        "festival_special": [],
        "popularity": 0.86
    },

    # ---- CHINESE / FAST ----

    {
        "dish_id": "d8",
        "name": "Veg Fried Rice",
        "price": 180,
        "tags": ["spicy", "fried", "veg"],
        "contexts": ["office_lunch", "quick_bite"],
        "time_suitable": ["lunch", "evening"],
        "festival_special": [],
        "popularity": 0.78
    },

    {
        "dish_id": "d9",
        "name": "Hakka Noodles",
        "price": 170,
        "tags": ["spicy", "street_food", "veg"],
        "contexts": ["office_lunch", "quick_bite"],
        "time_suitable": ["lunch", "evening"],
        "festival_special": [],
        "popularity": 0.77
    },

    # ---- DESSERTS ----

    {
        "dish_id": "d10",
        "name": "Gulab Jamun",
        "price": 90,
        "tags": ["sweet", "veg", "indulgent"],
        "contexts": ["treat_myself", "celebration"],
        "time_suitable": ["evening", "night"],
        "festival_special": ["diwali"],
        "popularity": 0.72
    },

    {
        "dish_id": "d11",
        "name": "Rasgulla",
        "price": 85,
        "tags": ["sweet", "veg", "light_fresh"],
        "contexts": ["celebration"],
        "time_suitable": ["evening", "night"],
        "festival_special": ["diwali"],
        "popularity": 0.70
    },

    # ---- HEALTHY ----

    {
        "dish_id": "d12",
        "name": "Grilled Veg Sandwich",
        "price": 150,
        "tags": ["healthy", "light_fresh", "veg"],
        "contexts": ["office_lunch", "light_healthy"],
        "time_suitable": ["morning", "lunch"],
        "festival_special": [],
        "popularity": 0.74
    }

]

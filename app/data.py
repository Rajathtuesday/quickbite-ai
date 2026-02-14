# Bangalore taste bias
BANGALORE_BIAS = {
    "spicy": 0.8,
    "south_indian": 0.9,
    "light_fresh": 0.9,
    "north_indian": 0.6,
    "creamy": 0.5,
    "fried": 0.4,
    "healthy": 0.8,
    "sweet": 0.6
}

FESTIVALS = {
    "2026-11-01": "diwali"
}

DISHES = [

    # SOUTH INDIAN
    {
        "dish_id": "d1",
        "name": "Masala Dosa",
        "price": 120,
        "cost": 45,
        "margin": 75,
        "tags": ["spicy", "south_indian", "veg", "light_fresh"],
        "contexts": ["office_lunch", "light_healthy"],
        "popularity": 0.9
    },
    {
        "dish_id": "d2",
        "name": "Idli Sambar",
        "price": 80,
        "cost": 30,
        "margin": 50,
        "tags": ["healthy", "south_indian", "veg", "light_fresh"],
        "contexts": ["morning", "light_healthy"],
        "popularity": 0.85
    },

    # NORTH INDIAN
    {
        "dish_id": "d3",
        "name": "Paneer Butter Masala",
        "price": 240,
        "cost": 110,
        "margin": 130,
        "tags": ["creamy", "north_indian", "veg", "indulgent"],
        "contexts": ["treat_myself", "celebration"],
        "popularity": 0.75
    },
    {
        "dish_id": "d4",
        "name": "Chole Bhature",
        "price": 180,
        "cost": 80,
        "margin": 100,
        "tags": ["spicy", "north_indian", "veg", "fried"],
        "contexts": ["office_lunch"],
        "popularity": 0.7
    },

    # STREET FOOD
    {
        "dish_id": "d5",
        "name": "Samosa",
        "price": 60,
        "cost": 20,
        "margin": 40,
        "tags": ["fried", "veg", "street_food"],
        "contexts": ["evening_snack", "lazy_tired"],
        "popularity": 0.8
    },
    {
        "dish_id": "d6",
        "name": "Veg Fried Rice",
        "price": 180,
        "cost": 90,
        "margin": 90,
        "tags": ["spicy", "fried", "veg"],
        "contexts": ["office_lunch"],
        "popularity": 0.75
    },
    {
        "dish_id": "d7",
        "name": "Hakka Noodles",
        "price": 170,
        "cost": 85,
        "margin": 85,
        "tags": ["spicy", "fried", "veg"],
        "contexts": ["office_lunch"],
        "popularity": 0.7
    },

    # DESSERTS
    {
        "dish_id": "d8",
        "name": "Gulab Jamun",
        "price": 90,
        "cost": 25,
        "margin": 65,
        "tags": ["sweet", "veg", "indulgent"],
        "contexts": ["treat_myself", "celebration"],
        "popularity": 0.6
    },
    {
        "dish_id": "d9",
        "name": "Rasgulla",
        "price": 100,
        "cost": 35,
        "margin": 65,
        "tags": ["sweet", "veg"],
        "contexts": ["celebration"],
        "popularity": 0.55
    },

    # HEALTHY
    {
        "dish_id": "d10",
        "name": "Grilled Veg Sandwich",
        "price": 150,
        "cost": 60,
        "margin": 90,
        "tags": ["healthy", "light_fresh", "veg"],
        "contexts": ["light_healthy", "office_lunch"],
        "popularity": 0.8
    }
]

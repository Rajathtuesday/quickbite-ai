import json
from collections import defaultdict

FILE = "logs/training_data.jsonl"

shown = 0
clicked = 0
ordered = 0

rank_stats = defaultdict(lambda: {"shown": 0, "clicked": 0})
dish_stats = defaultdict(lambda: {"shown": 0, "clicked": 0, "ordered": 0})
context_stats = defaultdict(lambda: {"shown": 0, "clicked": 0})

with open(FILE, "r", encoding="utf-8") as f:
    for line in f:
        row = json.loads(line)

        shown += 1
        clicked += row["clicked"]
        ordered += row["ordered"]

        # Rank analytics
        rank = row["rank"]
        rank_stats[rank]["shown"] += 1
        rank_stats[rank]["clicked"] += row["clicked"]

        # Dish analytics
        dish = row["dish_id"]
        dish_stats[dish]["shown"] += 1
        dish_stats[dish]["clicked"] += row["clicked"]
        dish_stats[dish]["ordered"] += row["ordered"]

        # Context analytics
        context = f'{row["situation"]} | {row["craving"]}'
        context_stats[context]["shown"] += 1
        context_stats[context]["clicked"] += row["clicked"]

print("\n=== OVERALL ===")
print(f"Shown: {shown}")
print(f"Clicked: {clicked}")
print(f"Ordered: {ordered}")
print(f"CTR: {clicked / shown:.2%}")
print(f"Order Rate: {ordered / shown:.2%}")

print("\n=== CTR BY RANK ===")
for r in sorted(rank_stats):
    s = rank_stats[r]["shown"]
    c = rank_stats[r]["clicked"]
    print(f"Rank {r}: {c}/{s} ({(c/s if s else 0):.2%})")

print("\n=== TOP DISH PERFORMANCE ===")
for dish, d in dish_stats.items():
    if d["shown"] >= 3:
        ctr = d["clicked"] / d["shown"]
        print(f"{dish}: CTR {ctr:.2%}, Orders {d['ordered']}")

print("\n=== CONTEXT PERFORMANCE ===")
for ctx, d in context_stats.items():
    ctr = d["clicked"] / d["shown"]
    print(f"{ctx}: CTR {ctr:.2%}")

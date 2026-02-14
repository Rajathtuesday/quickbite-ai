#!/usr/bin/env python3
"""
simulate_session.py

Robust simulation for QuickBite API.

Features:
- CLI options: sessions, base-url, seed, delay, mode
- Tries to import DISHES from app.data (falls back to defaults)
- Posts to /v1/recommend and /v1/feedback
- Prints progress every 50 sessions and final summary
- Handles API errors and unexpected responses
- Optional delay between requests to avoid spamming local server
"""

import argparse
import random
import requests
import time
import sys
from collections import Counter, defaultdict

DEFAULT_BASE_URL = "http://127.0.0.1:8000"

# ----------------------
# Try to import real DISHES if available
# ----------------------
try:
    from app.data import DISHES  # type: ignore
    HAS_APP_DATA = True
except Exception:
    HAS_APP_DATA = False
    # Minimal fallback (ids only)
    DISHES = [
        {"dish_id": f"d{i}", "name": f"Dish {i}", "margin": 50 + i * 5}
        for i in range(1, 13)
    ]

dish_lookup = {d["dish_id"]: d for d in DISHES}
dish_ids = list(dish_lookup.keys())

# ----------------------
# Simulation user-behaviour model (tweakable)
# ----------------------
def simulate_user_behavior_prob(dish_id, situation, craving):
    """
    Return click probability for a given dish + context.
    Rules:
      - Some simple bias rules for learnable patterns
      - Default low baseline
    """
    # strong bias: office_lunch + spicy prefers certain dishes (if present)
    spicy_office_targets = [d for d in dish_ids if d in ("d1", "d8", "d9")]
    sweet_lazy_targets = [d for d in dish_ids if d in ("d10", "d11")]
    creamy_treat_targets = [d for d in dish_ids if d in ("d4",)]

    if situation == "office_lunch" and craving == "spicy" and dish_id in spicy_office_targets:
        return 0.60

    if situation == "lazy_tired" and craving == "sweet" and dish_id in sweet_lazy_targets:
        return 0.70

    if situation == "treat_myself" and craving == "creamy" and dish_id in creamy_treat_targets:
        return 0.65

    # Price / margin slightly increases click chance (if margin present)
    margin = dish_lookup.get(dish_id, {}).get("margin", None)
    if margin is not None:
        if margin >= 100:
            return 0.08
        if margin >= 60:
            return 0.06

    # default weak click probability
    return 0.03

# ----------------------
# Main simulator
# ----------------------
def run_simulation(
    base_url,
    sessions,
    seed=None,
    delay=0.0,
    verbose=False,
    mode="profit",
):
    if seed is not None:
        random.seed(seed)

    stats = Counter()
    api_errors = 0
    unexpected_responses = 0
    bad_feedback = 0
    session_ordered = set()
    session_clicked = set()

    # optional revenue tracking if margins exist
    revenue = 0
    orders_count = 0
    clicks_count = 0

    cities = ["bangalore"]
    situations = [
        "office_lunch",
        "treat_myself",
        "lazy_tired",
        "light_healthy",
        "evening_snack",
        "celebration",
    ]
    cravings = ["spicy", "creamy", "sweet", "healthy", "fried"]
    constraints_pool = [
        [],
        ["veg_only"],
        ["under_250"],
        ["veg_only", "under_250"],
    ]

    start = time.time()
    for i in range(sessions):
        session_id = f"sim_{i}"
        payload = {
            "city": random.choice(cities),
            "session_id": session_id,
            "answers": {
                "situation": random.choice(situations),
                "craving": random.choice(cravings),
                "constraints": random.choice(constraints_pool),
            },
        }

        try:
            resp = requests.post(
                f"{base_url}/v1/recommend", json=payload, timeout=6
            )
        except Exception as e:
            api_errors += 1
            if verbose:
                print(f"[{i}] Request error: {e}")
            # keep going
            if i % 50 == 0:
                print(f"Simulated {i} sessions (api_errors={api_errors})")
            time.sleep(delay)
            continue

        if resp.status_code != 200:
            api_errors += 1
            if verbose:
                print(f"[{i}] Non-200 from recommend: {resp.status_code} {resp.text[:200]}")
            if i % 50 == 0:
                print(f"Simulated {i} sessions (api_errors={api_errors})")
            time.sleep(delay)
            continue

        try:
            data = resp.json()
        except Exception as e:
            unexpected_responses += 1
            if verbose:
                print(f"[{i}] JSON decode error: {e} -> {resp.text[:200]}")
            time.sleep(delay)
            continue

        # defensive: accept both your earlier "top_picks" and current "top_picks" shape:
        picks = None
        if isinstance(data, dict) and "top_picks" in data:
            picks = data["top_picks"]
        elif isinstance(data, dict) and "recommendations" in data:
            picks = data["recommendations"]
        else:
            unexpected_responses += 1
            if verbose:
                print(f"[{i}] Unexpected response shape: keys={list(data.keys())}")
            time.sleep(delay)
            continue

        # iterate picks and sample click/order
        for item in picks:
            # allow both structures (score, dish_id, name)
            dish_id = item.get("dish_id") or item.get("id") or None
            if dish_id is None:
                bad_feedback += 1
                continue

            click_prob = simulate_user_behavior_prob(
                dish_id, payload["answers"]["situation"], payload["answers"]["craving"]
            )

            # small variation by mode (if you want to simulate clicking more in "click" mode)
            if mode == "click":
                click_prob = min(1.0, click_prob * 1.2)

            if random.random() < click_prob:
                # log click
                try:
                    r = requests.post(
                        f"{base_url}/v1/feedback",
                        json={"session_id": session_id, "dish_id": dish_id, "action": "click"},
                        timeout=4,
                    )
                    clicks_count += 1
                    session_clicked.add(session_id)
                    if r.status_code != 200 and verbose:
                        print(f"[{i}] feedback click non-200: {r.status_code} {r.text[:200]}")
                except Exception as e:
                    api_errors += 1
                    if verbose:
                        print(f"[{i}] Error logging click: {e}")

                # 50% chance of order after click
                if random.random() < 0.5:
                    try:
                        r2 = requests.post(
                            f"{base_url}/v1/feedback",
                            json={"session_id": session_id, "dish_id": dish_id, "action": "order"},
                            timeout=4,
                        )
                        orders_count += 1
                        session_ordered.add(session_id)

                        # revenue if margin present
                        margin = dish_lookup.get(dish_id, {}).get("margin")
                        if margin:
                            revenue += margin

                        if r2.status_code != 200 and verbose:
                            print(f"[{i}] feedback order non-200: {r2.status_code} {r2.text[:200]}")
                    except Exception as e:
                        api_errors += 1
                        if verbose:
                            print(f"[{i}] Error logging order: {e}")

        # progress print
        if i % 50 == 0:
            print(f"Simulated {i} sessions")

        if delay:
            time.sleep(delay)

    elapsed = time.time() - start

    # summary
    print("\n🚀 Simulation complete")
    print(f"Sessions requested: {sessions}")
    print(f"Sessions that produced at least one click: {len(session_clicked)}")
    print(f"Sessions that produced at least one order: {len(session_ordered)}")
    print(f"Total clicks logged: {clicks_count}")
    print(f"Total orders logged: {orders_count}")
    print(f"Total revenue (if margins available): ₹{revenue}")
    print(f"API errors / bad responses: {api_errors + unexpected_responses + bad_feedback}")
    print(f"Elapsed time: {elapsed:.1f}s")
    print("Tip: run `python -m scripts.build_training_data` then `python -m scripts.train_model` to refresh the model after simulation.")

# ----------------------
# CLI
# ----------------------
def main():
    p = argparse.ArgumentParser(description="Simulate user sessions against QuickBite API")
    p.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Base URL for API")
    p.add_argument("--sessions", type=int, default=500, help="Number of sessions to simulate")
    p.add_argument("--seed", type=int, default=None, help="Random seed (for reproducibility)")
    p.add_argument("--delay", type=float, default=0.0, help="Delay (seconds) between sessions")
    p.add_argument("--mode", choices=["profit", "click"], default="profit", help="Mode param to /v1/recommend")
    p.add_argument("--verbose", action="store_true", help="Print verbose debug info")

    args = p.parse_args()

    # slight environment check: try calling health
    try:
        r = requests.get(f"{args.base_url}/", timeout=3)
        if r.status_code != 200:
            print("Warning: health endpoint returned non-200:", r.status_code)
    except Exception as e:
        print("Warning: cannot reach API at", args.base_url, "->", e)
        # Do not exit; user might want to run anyway.

    run_simulation(
        base_url=args.base_url,
        sessions=args.sessions,
        seed=args.seed,
        delay=args.delay,
        verbose=args.verbose,
        mode=args.mode,
    )


if __name__ == "__main__":
    main()

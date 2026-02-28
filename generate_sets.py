import random
import argparse
import os
import sys
from datetime import datetime

# ======================================
# NUMBER POOL
# ======================================
NUMBERS_POOL = [
    5,10,15,20,25,
    30,50,75,100,150,
    200,250,300,500,750,
    1000,1250,1500,1750,2000,
    3000,3500,4000,5000,
    5500,6000,6500,7000,7500,8000,
    8500,9000,9500,10000
]


# ======================================
# STREAM LOGGER
# ======================================
def stream(msg):
    print(msg)
    sys.stdout.flush()


# ======================================
# GRID PLACEMENT (NO ROW DUPLICATES)
# ======================================
def build_grid(numbers, grid_size):

    numbers = numbers[:]
    grid = []

    for _ in range(grid_size):
        row = []
        used = set()

        while len(row) < grid_size:
            for i, n in enumerate(numbers):
                if n not in used:
                    row.append(n)
                    used.add(n)
                    numbers.pop(i)
                    break

        grid.append(row)

    return grid


# ======================================
# GENERATE SINGLE SET
# ======================================
def generate_set(grid_size, special_rules):

    set_size = grid_size * grid_size
    current_set = []
    used_counts = {}

    # ----- Special numbers (3 repeats)
    for rule in special_rules:
        num = rule["number"]
        current_set += [num] * 3
        used_counts[num] = 3

    # ----- Random 2x repeat
    available = [
        n for n in NUMBERS_POOL
        if used_counts.get(n, 0) <= 1
    ]

    if available:
        n = random.choice(available)
        add = min(2, 3 - used_counts.get(n, 0))
        current_set += [n] * add
        used_counts[n] = used_counts.get(n, 0) + add

    # ----- Fill remaining
    remaining = set_size - len(current_set)

    fill_pool = []
    for n in NUMBERS_POOL:
        count = used_counts.get(n, 0)
        if count < 3:
            fill_pool += [n] * (3 - count)

    if remaining > len(fill_pool):
        raise ValueError("Cannot fill grid under constraints.")

    current_set += random.sample(fill_pool, remaining)

    random.shuffle(current_set)

    return build_grid(current_set, grid_size)


# ======================================
# MAIN GENERATOR
# ======================================
def run(total_sets, grid_size, special_rules, output, seed):

    if seed:
        random.seed(seed)

    stream("🚀 Generation started")
    stream(f"Sets: {total_sets}")
    stream(f"Grid: {grid_size}x{grid_size}")
    stream("----------------------------------")

    all_sets = []

    for i in range(total_sets):

        grid = generate_set(grid_size, special_rules)

        text_grid = "\n".join(
            ",".join(map(str, row)) for row in grid
        )

        all_sets.append(text_grid)

        # STREAM PROGRESS
        if (i + 1) % 10 == 0 or i == total_sets - 1:
            stream(f"✅ Generated {i+1}/{total_sets}")

    with open(output, "w") as f:
        f.write("\n\n".join(all_sets))

    stream("----------------------------------")
    stream(f"💾 Saved to: {os.path.abspath(output)}")
    stream("🎉 Done!")


# ======================================
# CLI
# ======================================
def parse_special_rules(rule_strings):
    """
    Format:
    --special 5000:100
    meaning number 5000 appears in 100 sets
    """
    rules = []

    for r in rule_strings:
        number, repeat_sets = r.split(":")
        rules.append({
            "number": int(number),
            "repeat_sets": int(repeat_sets)
        })

    return rules


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Multi Grid Generator (No Row Duplicate)"
    )

    parser.add_argument("--sets", type=int, required=True)
    parser.add_argument("--grid", type=int, default=5)
    parser.add_argument("--special", nargs="*", default=[])
    parser.add_argument("--output", default="output.txt")
    parser.add_argument("--seed", type=int, default=None)

    args = parser.parse_args()

    special_rules = parse_special_rules(args.special)

    run(
        total_sets=args.sets,
        grid_size=args.grid,
        special_rules=special_rules,
        output=args.output,
        seed=args.seed
    )

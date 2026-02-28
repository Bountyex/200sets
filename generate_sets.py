import random
import os

# ========== CONFIG ==========
TOTAL_SETS = int(input("Total sets: "))
GRID_SIZE = int(input("Grid size (5 for 5x5): "))

SPECIAL_COUNT = int(input("How many special numbers to control? "))
special_rules = []
for _ in range(SPECIAL_COUNT):
    num = int(input("Special number: "))
    repeat_sets = int(input(f"In how many sets {num} should appear (max 3 times per set)? "))
    special_rules.append({
        "number": num,
        "repeat_sets": repeat_sets
    })

OUTPUT_FILE = "streamed_multi_repeat_sets.txt"

numbers_pool = [
    5,10,15,20,25,
    30,50,75,100,150,
    200,250,300,500,750,
    1000,1250,1500,1750,2000,
    3000,3500,4000,5000,
    5500,6000,6500,7000,7500,8000,
    8500,9000,9500,10000
]

SET_SIZE = GRID_SIZE * GRID_SIZE

# ========== HELPER ==========
def generate_set(set_index):
    """Generate one 5x5 set respecting rules"""
    current_set = []
    used_counts = {}

    # Apply special numbers
    for rule in special_rules:
        if set_index < rule["repeat_sets"]:
            num = rule["number"]
            current_set += [num]*3
            used_counts[num] = 3

    # Random number repeat 2x
    available_for_random_repeat = [n for n in numbers_pool if used_counts.get(n,0) <= 1]
    if available_for_random_repeat:
        r_num = random.choice(available_for_random_repeat)
        times_to_add = min(2, 3 - used_counts.get(r_num,0))
        current_set += [r_num]*times_to_add
        used_counts[r_num] = used_counts.get(r_num,0)+times_to_add

    # Fill remaining
    remaining_slots = SET_SIZE - len(current_set)
    fill_pool = []
    for n in numbers_pool:
        c = used_counts.get(n,0)
        if c < 3:
            fill_pool += [n]*(3-c)

    if remaining_slots > len(fill_pool):
        raise ValueError("Cannot fill set without exceeding max 3 per number. Reduce special repeats or increase grid size.")

    current_set += random.sample(fill_pool, remaining_slots)
    random.shuffle(current_set)

    # Place numbers row-aware
    grid = []
    idx = 0
    for _ in range(GRID_SIZE):
        row_set = set()
        row = []
        while len(row) < GRID_SIZE:
            n = current_set[idx]
            if n not in row_set:
                row.append(n)
                row_set.add(n)
                idx += 1
            else:
                current_set.append(current_set.pop(idx))
        grid.append(row)
    return grid

# ========== STREAM & SAVE ==========
with open(OUTPUT_FILE, "w") as f:
    for i in range(TOTAL_SETS):
        grid = generate_set(i)
        for row in grid:
            f.write(",".join(map(str,row))+"\n")
        f.write("\n")  # empty line between sets
        # Streaming output to console
        print(f"Set {i+1}/{TOTAL_SETS} generated...")

print(f"\n✅ File saved as: {os.path.abspath(OUTPUT_FILE)}")

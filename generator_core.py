import random
import time

NUMBERS_POOL = [
    5,10,15,20,25,
    30,50,75,100,150,
    200,250,300,500,750,
    1000,1250,1500,1750,2000,
    3000,3500,4000,5000,
    5500,6000,6500,7000,7500,8000,
    8500,9000,9500,10000
]


def generate_grid(grid_size):
    nums = random.sample(NUMBERS_POOL, grid_size * grid_size)

    grid = []
    i = 0
    for _ in range(grid_size):
        row = nums[i:i+grid_size]
        grid.append(",".join(map(str, row)))
        i += grid_size

    return "\n".join(grid)


def generate_sets(total_sets, grid_size, progress_callback, cancel_flag):

    results = []
    start_time = time.time()

    for i in range(total_sets):

        if cancel_flag["stop"]:
            break

        grid = generate_grid(grid_size)
        results.append(grid)

        elapsed = time.time() - start_time
        rate = (i + 1) / elapsed if elapsed > 0 else 0
        remaining = (total_sets - (i + 1)) / rate if rate else 0

        progress_callback(i + 1, remaining, grid)

    return results

def get_prices_pool() -> list[int]:
    prices_pool = [300]                 # 1%
    prices_pool.extend([200] * 7)       # 8%
    prices_pool.extend([100] * 42)      # 50%
    prices_pool.extend([80] * 15)       # 65%
    prices_pool.extend([60] * 15)       # 80%
    prices_pool.extend([40] * 15)       # 95%
    prices_pool.extend([20] * 4)        # 99%
    prices_pool.append(0)               # 100%
    return prices_pool


def get_old_man_values_pool() -> list[int]:
    old_man_values_pool = [400]                 # 1%
    old_man_values_pool.extend([300] * 5)       # 6%
    old_man_values_pool.extend([200] * 14)      # 20%
    old_man_values_pool.extend([100] * 40)      # 60%
    old_man_values_pool.extend([50] * 20)       # 80%
    old_man_values_pool.extend([25] * 15)       # 95%
    old_man_values_pool.extend([10] * 4)        # 99%
    old_man_values_pool.append(1)               # 100%
    return old_man_values_pool

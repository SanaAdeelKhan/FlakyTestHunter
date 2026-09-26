import time
import random

def process_order(order_id):
    # Simulates a flaky dependency: sometimes "slow", sometimes not
    delay = random.uniform(0, 0.3)
    time.sleep(delay)
    if delay > 0.2:
        return {"status": "timeout"}
    return {"status": "success", "order_id": order_id}

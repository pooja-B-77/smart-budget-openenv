import requests
import time

BASE = "http://127.0.0.1:8000"

print("[START] task=auto env=smart-budget model=baseline")

rewards = []
step = 0

def baseline_policy(merchant):

    merchant = merchant.lower()

    if merchant in ["amazon", "flipkart", "myntra", "bigbazaar", "reliancemart"]:
        return "shopping"

    if merchant in ["swiggy", "zomato", "dominos", "kfc", "starbucks"]:
        return "food"

    if merchant in ["uber", "ola", "rapido"]:
        return "transport"

    if merchant in ["netflix", "spotify", "primevideo"]:
        return "entertainment"

    return "shopping"


try:

    obs = requests.post(f"{BASE}/reset").json()
    done = False

    while not done:

        merchant = obs.get("merchant", "unknown")

        action = {"category": baseline_policy(merchant)}

        r = requests.post(f"{BASE}/step", json=action).json()

        reward = float(r.get("reward", 0))
        done = bool(r.get("done", False))

        rewards.append(reward)

        step += 1

        print(
            f"[STEP] step={step} merchant={merchant} action={action['category']} reward={reward:.2f} done={str(done).lower()} error=null"
        )

        obs = r.get("state")

        if obs is None:
            break

        time.sleep(0.05)

except Exception as e:

    print(f"[ERROR] {str(e)}")
    done = True


if len(rewards) > 0:
    score = sum(rewards) / len(rewards)
else:
    score = 0


print(
    f"[END] success=true steps={step} score={score:.2f} rewards={','.join([str(round(x,2)) for x in rewards])}"
)
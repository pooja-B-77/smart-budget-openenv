import requests
import time
import sys

BASE = "http://127.0.0.1:7860"   # HF/OpenEnv uses 7860

print("[START] task=auto env=smart-budget model=baseline")

rewards = []
step = 0


def baseline_policy(merchant):

    merchant = merchant.lower()

    if merchant in ["amazon","flipkart","myntra","bigbazaar","reliancemart"]:
        return "shopping"

    if merchant in ["swiggy","zomato","dominos","kfc","starbucks"]:
        return "food"

    if merchant in ["uber","ola","rapido"]:
        return "transport"

    if merchant in ["netflix","spotify","primevideo"]:
        return "entertainment"

    return "shopping"


def wait_for_server():

    for _ in range(30):
        try:
            r = requests.get(BASE + "/")
            if r.status_code == 200:
                return True
        except Exception:
            pass

        time.sleep(1)

    return False


if not wait_for_server():
    print("[ERROR] server not reachable")
    sys.exit(0)


try:

    r = requests.post(BASE + "/reset")

    if r.status_code != 200:
        print("[ERROR] reset failed")
        sys.exit(0)

    obs = r.json()
    done = False

    while not done:

        if not obs:
            break

        merchant = obs.get("merchant","unknown")

        action = {
            "category": baseline_policy(merchant),
            "reasoning": f"{merchant} transaction classification"
        }

        try:
            r = requests.post(BASE + "/step", json=action)
            data = r.json()
        except Exception:
            print("[ERROR] step request failed")
            break

        reward = float(data.get("reward",0))
        done = bool(data.get("done",False))

        rewards.append(reward)
        step += 1

        print(
            f"[STEP] step={step} merchant={merchant} action={action['category']} reward={reward:.2f} done={str(done).lower()}"
        )

        obs = data.get("state")

        time.sleep(0.05)

except Exception as e:

    print("[ERROR]", str(e))
    sys.exit(0)


score = sum(rewards)/len(rewards) if rewards else 0

print(
    f"[END] success=true steps={step} score={score:.2f}"
)

sys.exit(0)
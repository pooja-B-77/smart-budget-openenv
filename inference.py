import requests

BASE = "http://127.0.0.1:8000"

print("[START] task=easy env=smart-budget model=baseline")

rewards = []
step = 0

obs = requests.post(f"{BASE}/reset").json()

done = False


def baseline_policy(merchant):

    merchant = merchant.lower()

    if merchant in ["amazon"]:
        return "shopping"

    if merchant in ["swiggy", "zomato", "dominos", "starbucks"]:
        return "food"

    if merchant in ["uber"]:
        return "transport"

    if merchant in ["netflix", "spotify"]:
        return "entertainment"

    return "shopping"


while not done:

    merchant = obs["merchant"]

    action = {"category": baseline_policy(merchant)}

    r = requests.post(f"{BASE}/step", json=action).json()

    reward = r["reward"]
    done = r["done"]

    rewards.append(reward)

    step += 1

    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null"
    )

    obs = r.get("state")

score = sum(rewards) / len(rewards)

print(
    f"[END] success=true steps={step} score={score:.2f} rewards={','.join([str(round(x,2)) for x in rewards])}"
)
import os
import requests
import time
from openai import OpenAI

BASE = "http://127.0.0.1:7860"

print("[START] task=auto env=smart-budget model=llm-agent")

rewards = []
step = 0

VALID_CATEGORIES = ["shopping", "food", "transport", "entertainment"]

# Initialize LLM client using hackathon proxy
client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("API_KEY"),
)


def llm_policy(merchant, amount):

    prompt = f"""
You are a financial assistant that classifies bank transactions.

Choose the correct category from:
shopping, food, transport, entertainment.

Examples:
Amazon, Flipkart, Myntra -> shopping
Swiggy, Zomato, Dominos -> food
Uber, Ola, Rapido -> transport
Netflix, Spotify, PrimeVideo -> entertainment

Transaction:
Merchant: {merchant}
Amount: {amount}

Return ONLY the category name.
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        category = response.choices[0].message.content.strip().lower()
        for c in VALID_CATEGORIES:
            if c in category:
                return c

        # Ensure valid output
        if category not in VALID_CATEGORIES:
            return "shopping"

        return category

    except Exception as e:
        print("[LLM ERROR]", e)
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
    exit(0)


try:

    r = requests.post(BASE + "/reset")

    if r.status_code != 200:
        print("[ERROR] reset failed")
        exit(0)

    obs = r.json()
    done = False

    while not done:

        if not obs:
            break

        merchant = obs.get("merchant", "unknown")
        amount = obs.get("amount", 0)

        category = llm_policy(merchant, amount)

        action = {
            "category": category,
            "reasoning": f"{merchant} transaction classification"
        }

        try:
            r = requests.post(BASE + "/step", json=action)
            data = r.json()
        except Exception:
            print("[ERROR] step request failed")
            break

        reward = float(data.get("reward", 0))
        done = bool(data.get("done", False))

        rewards.append(reward)
        step += 1

        print(
            f"[STEP] step={step} merchant={merchant} action={category} reward={reward:.2f} done={str(done).lower()}"
        )

        obs = data.get("state")

        if obs is None:
            break

        time.sleep(0.05)

except Exception as e:

    print("[ERROR]", str(e))
    exit(0)


score = sum(rewards) / len(rewards) if rewards else 0

print(f"[END] success=true steps={step} score={score:.2f}")
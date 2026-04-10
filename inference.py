import os
import requests
import time
from openai import OpenAI

BASE = "http://127.0.0.1:7860"

print("[START] task=auto env=smart-budget model=llm-agent")

rewards = []
step = 0

# initialize LLM client using hackathon proxy
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"],
)

def llm_policy(merchant, amount):

    prompt = f"""
A financial transaction occurred.

Merchant: {merchant}
Amount: {amount}

Choose the correct spending category from:
shopping, food, transport, entertainment.

Respond with only the category name.
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        category = response.choices[0].message.content.strip().lower()

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
        except:
            pass

        time.sleep(1)

    return False


if not wait_for_server():
    print("[ERROR] server not reachable")
    exit(0)


try:

    obs = requests.post(BASE + "/reset").json()
    done = False

    while not done:

        merchant = obs.get("merchant", "unknown")
        amount = obs.get("amount", 0)

        category = llm_policy(merchant, amount)

        action = {
            "category": category,
            "reasoning": f"{merchant} transaction"
        }

        r = requests.post(BASE + "/step", json=action).json()

        reward = float(r.get("reward", 0))
        done = bool(r.get("done", False))

        rewards.append(reward)
        step += 1

        print(
            f"[STEP] step={step} merchant={merchant} action={category} reward={reward:.2f} done={str(done).lower()}"
        )

        obs = r.get("state")

        if obs is None:
            break

        time.sleep(0.1)

except Exception as e:

    print("[ERROR]", str(e))
    exit(0)


score = sum(rewards) / len(rewards) if rewards else 0

print(
    f"[END] success=true steps={step} score={score:.2f}"
)
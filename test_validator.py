import requests

BASE = "http://127.0.0.1:7860"

TASKS = ["easy","medium","hard"]

for task in TASKS:

    print("\n==============================")
    print("TESTING TASK:", task)
    print("==============================")

    r = requests.post(f"{BASE}/reset?task={task}")
    obs = r.json()

    done = False
    step = 0
    rewards = []

    while not done:

        action = {
            "category": "shopping",
            "reasoning": "test agent"
        }

        r = requests.post(f"{BASE}/step", json=action)
        data = r.json()

        reward = data.get("reward", 0)
        done = data.get("done", False)

        rewards.append(reward)
        step += 1

        print("step:", step, "reward:", reward)

    avg_score = sum(rewards) / len(rewards)

    print("Average reward:", avg_score)
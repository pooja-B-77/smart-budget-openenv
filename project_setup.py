import os

files = {
"requirements.txt": """fastapi
uvicorn
pydantic
openai
openenv-core
""",

"openenv.yaml": """name: smart-budget-env
version: 1.0
tasks:

* easy
* medium
* hard
  """,

"env/budget_env.py": """class SmartBudgetEnv:

```
def __init__(self):
    self.balance = 5000
    self.current = 0
    self.transactions = [
        {"merchant":"Swiggy","amount":250,"category":"food"},
        {"merchant":"Uber","amount":120,"category":"transport"},
        {"merchant":"Amazon","amount":900,"category":"shopping"}
    ]

def reset(self):
    self.current = 0
    return self.transactions[self.current]

def step(self, action):

    correct = self.transactions[self.current]["category"]

    reward = 1.0 if action["category"] == correct else 0.0

    self.current += 1

    done = self.current >= len(self.transactions)

    state = None if done else self.transactions[self.current]

    return state, reward, done
```

""",

"server/app.py": """from fastapi import FastAPI
from env.budget_env import SmartBudgetEnv

app = FastAPI()

env = SmartBudgetEnv()

@app.post("/reset")
def reset():
return env.reset()

@app.post("/step")
def step(action:dict):

```
state,reward,done = env.step(action)

return {
    "state":state,
    "reward":reward,
    "done":done
}
```

""",

"inference.py": """from env.budget_env import SmartBudgetEnv

env = SmartBudgetEnv()

state = env.reset()

rewards=[]

print("[START] task=easy env=smart-budget model=test")

step=1
done=False

while not done:

```
action={"category":"food"}

state,reward,done = env.step(action)

rewards.append(reward)

print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

step+=1
```

print(f"[END] success=true steps={len(rewards)} score={sum(rewards)/len(rewards):.2f} rewards={','.join([str(r) for r in rewards])}")
""",

"Dockerfile": """FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 7860
CMD ["uvicorn","server.app:app","--host","0.0.0.0","--port","7860"]
"""
}

for path,content in files.items():
    folder = os.path.dirname(path)

    if folder:
        os.makedirs(folder,exist_ok=True)

    with open(path,"w") as f:
        f.write(content)

print("PROJECT CREATED SUCCESSFULLY")

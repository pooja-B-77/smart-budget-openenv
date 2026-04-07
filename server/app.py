from fastapi import FastAPI
from pydantic import BaseModel
from env.budget_env import SmartBudgetEnv

app = FastAPI()

env = SmartBudgetEnv()


class Action(BaseModel):
    category: str


@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.dict()


@app.get("/state")
def state():
    obs = env.state()
    return obs.dict() if obs else None


@app.post("/step")
def step(action: Action):

    state, reward, done = env.step(action.dict())

    return {
        "state": state.dict() if state else None,
        "reward": reward,
        "done": done
    }

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from env.budget_env import SmartBudgetEnv

app = FastAPI()

env = SmartBudgetEnv()


class Action(BaseModel):
    category: str
    reasoning: str | None = None


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
        "reward": float(reward),
        "done": bool(done)
    }


@app.get("/")
def health():
    return {"status": "ok"}


def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
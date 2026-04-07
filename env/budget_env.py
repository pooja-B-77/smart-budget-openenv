from pydantic import BaseModel
import random


class Observation(BaseModel):
    merchant: str
    amount: float
    step: int


class Action(BaseModel):
    category: str


class Reward(BaseModel):
    value: float


class SmartBudgetEnv:

    def __init__(self, task="easy"):
        self.task = task
        self.transactions = []
        self.step_id = 0
        self.done = False

        self.dataset = [
            {"merchant": "Amazon", "amount": 900, "category": "shopping"},
            {"merchant": "Uber", "amount": 350, "category": "transport"},
            {"merchant": "Starbucks", "amount": 200, "category": "food"},
            {"merchant": "Netflix", "amount": 499, "category": "entertainment"},
            {"merchant": "BigBasket", "amount": 800, "category": "food"},
        ]

    def reset(self):

        if self.task == "easy":
            self.transactions = random.sample(self.dataset, 3)

        elif self.task == "medium":
            self.transactions = random.sample(self.dataset, 4)

        else:
            self.transactions = random.sample(self.dataset, 5)

        self.step_id = 0
        self.done = False

        t = self.transactions[self.step_id]

        return Observation(
            merchant=t["merchant"],
            amount=t["amount"],
            step=self.step_id
        )

    def state(self):

        if self.step_id >= len(self.transactions):
            return None

        t = self.transactions[self.step_id]

        return Observation(
            merchant=t["merchant"],
            amount=t["amount"],
            step=self.step_id
        )

    def step(self, action: dict):

        correct = self.transactions[self.step_id]["category"]

        predicted = action.get("category", "")

        # reward shaping
        if predicted == correct:
            reward = 1.0

        elif predicted in ["shopping", "food", "transport", "entertainment"]:
            reward = 0.5

        else:
            reward = -0.2

        self.step_id += 1

        if self.step_id >= len(self.transactions):
            self.done = True
            return None, reward, True

        next_state = self.transactions[self.step_id]

        obs = Observation(
            merchant=next_state["merchant"],
            amount=next_state["amount"],
            step=self.step_id
        )

        return obs, reward, False
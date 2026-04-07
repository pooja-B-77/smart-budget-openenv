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


VALID_CATEGORIES = [
    "shopping",
    "food",
    "transport",
    "entertainment"
]


TASKS = {
    "easy": [
        {"merchant": "Amazon", "amount": 900, "category": "shopping"},
        {"merchant": "Swiggy", "amount": 250, "category": "food"},
        {"merchant": "Uber", "amount": 180, "category": "transport"},
    ],

    "medium": [
        {"merchant": "Amazon", "amount": 1200, "category": "shopping"},
        {"merchant": "Dominos", "amount": 500, "category": "food"},
        {"merchant": "Uber", "amount": 350, "category": "transport"},
        {"merchant": "Netflix", "amount": 650, "category": "entertainment"},
    ],

    "hard": [
        {"merchant": "Amazon", "amount": 1500, "category": "shopping"},
        {"merchant": "Zomato", "amount": 450, "category": "food"},
        {"merchant": "Uber", "amount": 320, "category": "transport"},
        {"merchant": "Spotify", "amount": 199, "category": "entertainment"},
        {"merchant": "Swiggy", "amount": 600, "category": "food"},
    ]
}


class SmartBudgetEnv:

    def __init__(self, task="easy"):

        self.task = task
        self.transactions = []
        self.step_id = 0
        self.done = False

    def reset(self):

        self.transactions = TASKS[self.task]

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

        if predicted == correct:
            reward = 1.0

        elif predicted in VALID_CATEGORIES:
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
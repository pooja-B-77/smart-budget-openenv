from pydantic import BaseModel
import random


class Observation(BaseModel):
    merchant: str
    amount: float
    merchant_hint: str
    step: int
    remaining_transactions: int
    valid_categories: list


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
        {"merchant": "Flipkart", "amount": 1100, "category": "shopping"},
        {"merchant": "Dominos", "amount": 420, "category": "food"},
        {"merchant": "Ola", "amount": 300, "category": "transport"},
        {"merchant": "Netflix", "amount": 650, "category": "entertainment"},
    ],

    "hard": [
        {"merchant": "RelianceMart", "amount": 950, "category": "shopping"},
        {"merchant": "Starbucks", "amount": 350, "category": "food"},
        {"merchant": "Rapido", "amount": 190, "category": "transport"},
        {"merchant": "Spotify", "amount": 119, "category": "entertainment"},
        {"merchant": "Amazon", "amount": 300, "category": "entertainment"},
    ]
}


MERCHANT_HINTS = {
    "Amazon": "online shopping marketplace",
    "Flipkart": "ecommerce shopping platform",
    "Swiggy": "food delivery service",
    "Dominos": "pizza restaurant",
    "Starbucks": "coffee shop",
    "Uber": "ride hailing transport service",
    "Ola": "taxi ride service",
    "Rapido": "bike taxi service",
    "Netflix": "video streaming subscription",
    "Spotify": "music streaming service",
    "RelianceMart": "retail store"
}


class SmartBudgetEnv:

    def __init__(self, task="easy"):
        self.task = task
        self.transactions = []
        self.step_id = 0
        self.correct = 0
        self.done = False

    def reset(self):

        self.transactions = TASKS[self.task].copy()
        random.shuffle(self.transactions)

        self.step_id = 0
        self.correct = 0
        self.done = False

        return self._build_obs()

    def state(self):

        if self.step_id >= len(self.transactions):
            return None

        return self._build_obs()

    def _build_obs(self):

        t = self.transactions[self.step_id]
        hint = MERCHANT_HINTS.get(t["merchant"], "unknown merchant")

        return Observation(
            merchant=t["merchant"],
            amount=t["amount"],
            merchant_hint=hint,
            step=self.step_id,
            remaining_transactions=len(self.transactions) - self.step_id,
            valid_categories=VALID_CATEGORIES
        )

    def step(self, action: dict):

        correct = self.transactions[self.step_id]["category"]
        predicted = action.get("category", "")

        reward = 0.0

        if predicted == correct:
            reward = 0.8
            self.correct += 1
        elif predicted in VALID_CATEGORIES:
            reward = 0.4
        else:
            reward = 0.2

        self.step_id += 1

        if self.step_id >= len(self.transactions):
            self.done = True
            # IMPORTANT: return reward, not score
            return None, reward, True

        return self._build_obs(), reward, False
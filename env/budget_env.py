from pydantic import BaseModel
import random


class Observation(BaseModel):
    merchant: str
    amount: float
    merchant_hint: str
    step: int
    remaining_transactions: int
    valid_categories: list


class Action(BaseModel):
    category: str
    reasoning: str | None = None


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
        {"merchant": "Flipkart", "amount": 1100, "category": "shopping"},
        {"merchant": "Swiggy", "amount": 250, "category": "food"},
        {"merchant": "Zomato", "amount": 320, "category": "food"},
        {"merchant": "Uber", "amount": 180, "category": "transport"},
    ],

    "medium": [
        {"merchant": "Amazon", "amount": 1200, "category": "shopping"},
        {"merchant": "Myntra", "amount": 1400, "category": "shopping"},
        {"merchant": "Dominos", "amount": 500, "category": "food"},
        {"merchant": "KFC", "amount": 420, "category": "food"},
        {"merchant": "Uber", "amount": 350, "category": "transport"},
        {"merchant": "Ola", "amount": 300, "category": "transport"},
        {"merchant": "Netflix", "amount": 650, "category": "entertainment"},
    ],

    "hard": [

    {"merchant": "RelianceMart", "amount": 950, "category": "shopping"},
    {"merchant": "BigBazaar", "amount": 800, "category": "shopping"},

    {"merchant": "Starbucks", "amount": 350, "category": "food"},
    {"merchant": "Dominos", "amount": 420, "category": "food"},

    {"merchant": "Uber", "amount": 320, "category": "transport"},
    {"merchant": "Rapido", "amount": 190, "category": "transport"},

    {"merchant": "Netflix", "amount": 199, "category": "entertainment"},
    {"merchant": "Spotify", "amount": 119, "category": "entertainment"},

    {"merchant": "Apple", "amount": 45000, "category": "shopping"},
    {"merchant": "Apple", "amount": 120, "category": "entertainment"},

    {"merchant": "Amazon", "amount": 300, "category": "entertainment"},
    {"merchant": "Amazon", "amount": 2500, "category": "shopping"},
]
}


MERCHANT_HINTS = {
    "Amazon": "online shopping marketplace",
    "Flipkart": "ecommerce shopping platform",
    "Myntra": "online fashion shopping",
    "BigBazaar": "supermarket retail store",
    "RelianceMart": "grocery and retail store",

    "Swiggy": "food delivery service",
    "Zomato": "restaurant food delivery platform",
    "Dominos": "pizza restaurant",
    "KFC": "fast food restaurant",
    "Starbucks": "coffee shop",

    "Uber": "ride hailing transport service",
    "Ola": "taxi ride service",
    "Rapido": "bike taxi service",

    "Netflix": "video streaming subscription",
    "Spotify": "music streaming service",
    "PrimeVideo": "video streaming subscription"
}


class SmartBudgetEnv:

    def __init__(self, task="easy"):

        self.task = task
        self.transactions = []
        self.step_id = 0
        self.done = False
        self.total_reward = 0

    def reset(self):

        self.transactions = TASKS[self.task].copy()

        random.shuffle(self.transactions)

        self.step_id = 0
        self.done = False
        self.total_reward = 0

        t = self.transactions[self.step_id]

        hint = MERCHANT_HINTS.get(t["merchant"], "unknown merchant")

        return Observation(
            merchant=t["merchant"],
            amount=t["amount"],
            merchant_hint=hint,
            step=self.step_id,
            remaining_transactions=len(self.transactions),
            valid_categories=VALID_CATEGORIES
        )

    def state(self):

        if self.step_id >= len(self.transactions):
            return None

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
        reasoning = action.get("reasoning", "")

        reward = 0

        if predicted == correct:
            reward = 1.5
        elif predicted in VALID_CATEGORIES:
            reward = 0.3
        else:
            reward = -0.5

        if reasoning:

            reasoning = reasoning.lower()
            merchant = self.transactions[self.step_id]["merchant"].lower()

            if merchant in reasoning:
                reward += 0.2

        amount = self.transactions[self.step_id]["amount"]

        if predicted == correct and amount > 1000:
            reward += 0.5

        self.total_reward += reward

        self.step_id += 1

        if self.step_id >= len(self.transactions):

            self.done = True

            accuracy = self.total_reward / len(self.transactions)

            if accuracy > 1:
                reward += 2
            elif accuracy < 0.5:
                reward -= 1

            return None, reward, True

        next_state = self.transactions[self.step_id]

        hint = MERCHANT_HINTS.get(next_state["merchant"], "unknown merchant")

        obs = Observation(
            merchant=next_state["merchant"],
            amount=next_state["amount"],
            merchant_hint=hint,
            step=self.step_id,
            remaining_transactions=len(self.transactions) - self.step_id,
            valid_categories=VALID_CATEGORIES
        )

        return obs, reward, False
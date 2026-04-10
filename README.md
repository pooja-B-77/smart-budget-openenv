---

title: Smart Budget OpenEnv
emoji: 💰
colorFrom: yellow
colorTo: blue
sdk: docker
pinned: false
short_description: OpenEnv environment for financial transaction classification
-------------------------------------------------------------------------------

# Smart Budget OpenEnv

Smart Budget OpenEnv is an **agent evaluation environment** where AI agents classify financial transactions into budget categories.

The environment simulates a real-world personal finance scenario where users categorize bank transactions such as purchases, subscriptions, or ride payments.

Agents receive observations about each transaction and must predict the correct spending category.

The environment rewards correct classifications and penalizes incorrect predictions.

---

# Environment Motivation

Many financial tools automatically categorize transactions for budgeting and analytics.

Examples include:

• expense tracking apps
• banking dashboards
• financial assistants
• fraud monitoring tools

This environment simulates that task and allows **AI agents to learn and evaluate transaction classification behavior**.

---

# Observation Space

At each step the agent receives the following observation:

| Field    | Type    | Description               |
| -------- | ------- | ------------------------- |
| merchant | string  | Merchant name             |
| amount   | float   | Transaction amount        |
| step     | integer | Current transaction index |

Example observation:

```json
{
 "merchant": "Amazon",
 "amount": 900,
 "step": 0
}
```

---

# Action Space

The agent must predict the transaction category.

| Field    | Type   | Description                |
| -------- | ------ | -------------------------- |
| category | string | Predicted expense category |

Allowed categories:

• shopping
• food
• transport
• entertainment

Example action:

```json
{
 "category": "shopping"
}
```

---

# Reward Function

The environment provides feedback based on prediction quality.

| Prediction                   | Reward |
| ---------------------------- | ------ |
| Correct classification       | +1.0   |
| Valid category but incorrect | +0.5   |
| Invalid category             | -0.2   |

This reward structure encourages agents to learn accurate transaction classification.

---

# Tasks

The environment contains **three difficulty levels**:

| Task   | Transactions | Description                |
| ------ | ------------ | -------------------------- |
| easy   | 3            | Clear merchant names       |
| medium | 4            | More diverse merchants     |
| hard   | 5            | Mixed transaction patterns |

---

# Merchant Coverage

The environment includes merchants from common spending categories.

Shopping
Amazon, Flipkart, Myntra, BigBazaar

Food
Swiggy, Zomato, Dominos, KFC, Starbucks

Transport
Uber, Ola, Rapido

Entertainment
Netflix, Spotify, PrimeVideo

This diverse merchant coverage allows agents to reason about transaction categories from real-world brand signals.

---

# Environment API

### Reset Environment

```
POST /reset
```

Returns the first observation of a new episode.

---

### Step

```
POST /step
```

Input:

```json
{
 "category": "shopping"
}
```

Output:

```json
{
 "state": {...},
 "reward": 1.0,
 "done": false
}
```

---

# Running Locally

Install dependencies:

```
pip install -r requirements.txt
```

Run the API server:

```
python -m uvicorn server.app:app --reload
```

Open the API docs:

```
http://127.0.0.1:8000/docs
```

---

# Baseline Agent

Run the baseline agent:

```
python inference.py
```

Example output:

```
[START] task=auto env=smart-budget model=baseline
[STEP] step=1 merchant=Amazon action=shopping reward=1.00 done=false
[STEP] step=2 merchant=Swiggy action=food reward=1.00 done=false
[STEP] step=3 merchant=Uber action=transport reward=1.00 done=true
[END] success=true steps=3 score=1.00 rewards=1.0,1.0,1.0
```

---

# Docker Deployment

Build container:

```
docker build -t smart-budget .
```

Run container:

```
docker run -p 7860:7860 smart-budget
```

Open:

```
http://localhost:7860/docs
```

---

# OpenEnv Metadata

Environment specification is defined in:

```
openenv.yaml
```

Validate locally:

```
openenv validate
```

---

# Project Structure

```
smart-budget-openenv
│
├── env
│   └── budget_env.py
│
├── server
│   └── app.py
│
├── inference.py
├── openenv.yaml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# Use Cases

This environment can evaluate:

• LLM agents
• reinforcement learning agents
• financial automation systems
• budgeting assistants

---

# License

MIT License

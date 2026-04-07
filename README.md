# Smart Budget OpenEnv

A reinforcement learning environment for **financial transaction classification**.
Agents must classify real-world expense transactions into appropriate budget categories.

This environment simulates a **common personal finance task**: automatically categorizing spending from merchants such as Amazon, Uber, or Swiggy.

Built using the **OpenEnv specification** for evaluating agentic systems.

---

# Environment Motivation

People frequently review bank transactions and categorize them into budgets such as:

* Food
* Shopping
* Transport
* Entertainment

This environment allows an AI agent to perform that task automatically and receive feedback through a reward signal.

---

# Observation Space

The environment provides the following observation at each step:

| Field    | Type    | Description                        |
| -------- | ------- | ---------------------------------- |
| merchant | string  | Merchant name from the transaction |
| amount   | float   | Transaction amount                 |
| step     | integer | Current step number                |

Example:

```
{
 "merchant": "Amazon",
 "amount": 900,
 "step": 1
}
```

---

# Action Space

The agent must predict a category for the transaction.

| Field    | Type   | Description                |
| -------- | ------ | -------------------------- |
| category | string | Predicted expense category |

Allowed categories:

* food
* shopping
* transport
* entertainment

Example action:

```
{
 "category": "shopping"
}
```

---

# Reward Function

The reward provides feedback based on classification quality.

| Prediction                   | Reward |
| ---------------------------- | ------ |
| Correct classification       | +1.0   |
| Valid category but incorrect | +0.5   |
| Invalid category             | -0.2   |

This reward shaping allows agents to improve performance gradually.

---

# Tasks

The environment contains **three difficulty levels**.

| Task   | Transactions | Description                                |
| ------ | ------------ | ------------------------------------------ |
| easy   | 3            | Simple merchant names                      |
| medium | 4            | Slightly ambiguous merchants               |
| hard   | 5            | Mixed merchant types and higher difficulty |

These tasks allow benchmarking agents across increasing difficulty levels.

---

# Environment API

The environment follows the **OpenEnv interface**.

### Reset Environment

```
POST /reset
```

Returns the initial observation.

### Step

```
POST /step
```

Input:

```
{
 "category": "shopping"
}
```

Output:

```
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

Start the environment server:

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
[START] task=easy env=smart-budget model=baseline
[STEP] step=1 reward=0.50
[STEP] step=2 reward=0.50
[STEP] step=3 reward=1.00
[END] success=true score=0.67
```

---

# Docker Deployment

Build the container:

```
docker build -t smart-budget .
```

Run the container:

```
docker run -p 7860:7860 smart-budget
```

Open the API:

```
http://localhost:7860/docs
```

---

# OpenEnv Metadata

Environment metadata is defined in:

```
openenv.yaml
```

This file describes the environment specification and allows validation with the OpenEnv tooling.

---

# HuggingFace Deployment

This environment is designed to run as a **Docker Hugging Face Space**.

Once deployed, the environment will be accessible via:

```
https://<your-space>.hf.space/docs
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

This environment can be used to evaluate:

* LLM agents
* Reinforcement learning agents
* Financial automation systems
* Autonomous budgeting tools

---

# License

MIT License

VALID = ["shopping", "food", "transport", "entertainment"]

def grade(rewards):
    if not rewards:
        return 0.5
    return sum(rewards) / len(rewards)
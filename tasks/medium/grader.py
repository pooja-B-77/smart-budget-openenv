VALID = ["shopping", "food", "transport", "entertainment"]

def grade(action, observation):

    category = action.get("category", "")

    if category in VALID:
        return True, 0.85

    return False, 0.15
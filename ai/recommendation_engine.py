from ai.agent_tools import recommend_insurance


def recommend_plans(age, category, budget, coverage_preference):
    return recommend_insurance(age, category, budget, coverage_preference)

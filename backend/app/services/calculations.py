from typing import List

def revenue_growth_rate(revenue: List[float]):
    growth = []
    for i in range(1, len(revenue)):
        if revenue[i-1] == 0:
            growth.append(0)
        else:
            g = ((revenue[i] - revenue[i-1]) / revenue[i-1]) * 100
            growth.append(g)
    return growth


def expense_growth_rate(expenses: List[float]):
    growth = []
    for i in range(1, len(expenses)):
        if expenses[i-1] == 0:
            growth.append(0)
        else:
            g = ((expenses[i] - expenses[i-1]) / expenses[i-1]) * 100
            growth.append(g)
    return growth


def net_cash_flow(revenue, expenses):
    return [r - e for r, e in zip(revenue, expenses)]


def burn_rate(revenue, expenses):
    losses = [e - r for r, e in zip(revenue, expenses) if e > r]
    if not losses:
        return 0
    return sum(losses) / len(losses)


def runway_days(cash_on_hand, burn_rate):
    if burn_rate <= 0:
        return None
    months = cash_on_hand / burn_rate
    return months * 30
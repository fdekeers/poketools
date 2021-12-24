# Statistical analysis for shiny odds
# Use binomial distribution with k = 1

import matplotlib.pyplot as plt


def proba_at_least_one(p, n):
    return 1 - (1-p) ** n


shiny_odds = 1 / 4096
tries = list(range(1, 20000))
probs = [proba_at_least_one(shiny_odds, n) for n in tries]

# Plot mass function
fig, ax = plt.subplots()
ax.plot(tries, probs)
fig.show()

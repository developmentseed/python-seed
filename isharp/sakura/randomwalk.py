import numpy as np
import matplotlib.pyplot as plt
import random


def randomwalk1D(n):
    x, y = 0, 0
    # Generate the time points [1, 2, 3, ... , n]
    timepoints = np.arange(n + 1)
    positions = [y]
    directions = ["UP", "DOWN"]
    for i in range(1, n + 1):
        # Randomly select either UP or DOWN
        step = random.choice(directions)

        # Move the object up or down
        if step == "UP":
            y += np.random.random_sample()
        elif step == "DOWN":
            y -= np.random.random_sample()
        # Keep track of the positions
        positions.append(y)
    return  positions
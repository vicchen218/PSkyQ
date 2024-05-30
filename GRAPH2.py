import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rc('font', family='Microsoft JhengHei')
# Data
categories = ['STATIC', 'DYNAMIC']
values = [4005/25604, 4005/12912]

# Create bar chart with specified colors and precision
plt.figure(figsize=(10, 6))
plt.bar(categories, values, color=['blue', 'red'])
plt.title('進入最終集合的數量比率差距')
plt.ylabel('比率')
plt.ylim(0, max(values)*1.1)  # Add some space above the tallest bar

# Show values on the bars with specified precision
for i, v in enumerate(values):
    plt.text(i, v + 0.01, f"{v:.2f}", ha='center')

# Show the plot
plt.show()

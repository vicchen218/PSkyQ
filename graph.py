import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rc('font', family='Microsoft JhengHei')
plt.rcParams['font.sans-serif'] = ['SimHei']  # Specify a font that supports Chinese characters
plt.rcParams['axes.unicode_minus'] = False  # Ensure negative values are displayed correctly
# Generate 100 random values centered around 0.02 within the range [0, 0.04]
random_values = 0.02 + (np.random.randn(100) * 0.005)  # Standard deviation adjusted to keep values close to 0.02
random_values = np.clip(random_values, 0, 0.04)  # Clipping values to stay within the range
random_values=[0.01942256, 0.02090371, 0.0310333 , 0.02606838, 0.02778251,
       0.02104189, 0.01618413, 0.01233462, 0.02725265, 0.02138241,
       0.01369592, 0.02213842, 0.02101121, 0.01850423, 0.03155804,
       0.01890837, 0.0254236 , 0.01429792, 0.0110458 , 0.0123844 ,
       0.01604962, 0.01982632, 0.02086727, 0.01899337, 0.02253619,
       0.02438239, 0.02321182, 0.02642065, 0.02524157, 0.02277975,
       0.02162954, 0.01269571, 0.01991873, 0.01624718, 0.02477424,
       0.01579323, 0.01603688, 0.01808009, 0.027075  , 0.02767423,
       0.02581407, 0.02173771, 0.02154159, 0.01214878, 0.01707472,
       0.02114836, 0.02410484, 0.01251365, 0.01686332, 0.0146708 ,
       0.02592387, 0.02182383, 0.01534511, 0.02092065, 0.0205074 ,
       0.01615236, 0.0145757 , 0.01975612, 0.02188599, 0.02350766,
       0.0191662 , 0.01809029, 0.01377199, 0.01583071, 0.01331086,
       0.01971501, 0.03180292, 0.02592605, 0.02448596, 0.01427473,
       0.01937941, 0.01505341, 0.02291284, 0.01317939, 0.02293562,
       0.02636833, 0.01248259, 0.00793926, 0.02495414, 0.02099291,
       0.0175556 , 0.01515189, 0.02090043, 0.01354757, 0.02399366,
       0.01963203, 0.02357713, 0.02297531, 0.02065315, 0.01922756,
       0.02016929, 0.02089433, 0.01486137, 0.03196566, 0.01232038,
       0.02123862, 0.02733539, 0.01915516, 0.022599  , 0.01964079]
# Creating a histogram for the generated random values
plt.figure(figsize=(10, 6))
plt.hist(random_values, bins=10, edgecolor='black',color="#ffaf00")
plt.xlabel('平均值')
plt.ylabel('數量')
plt.title('機率分布')
plt.grid(True)

# Show the plot
plt.show()

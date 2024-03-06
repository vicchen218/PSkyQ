import numpy as np
import pandas as pd

# 定義計算報酬的函數
def calculate_reward(probability, action, threshold):
    if probability >= threshold:
        return 2 if action == 1 else -2
    else:
        return 2 if action == 0 else -2

# 從CSV檔案讀取數據
def read_data(file_path):
    data = pd.read_csv(file_path)
    return data

# 初始化Q表參數
num_states = 10
num_actions = 2
Q_table = np.zeros((num_states, num_actions))
learning_rate = 0.1
discount_factor = 0.9
episodes = 1000  # 根據需要調整模擬的總次數
epsilon = 0.1

# 將概率值映射到狀態
def map_probability_to_state(probability, num_states=10):
    state = int(probability * num_states)
    return min(state, num_states - 1)

# 根據ε-貪婪策略選擇動作
def choose_action(state, epsilon):
    if np.random.rand() < epsilon:
        return np.random.choice([0, 1])
    else:
        return np.argmax(Q_table[state, :])

# 更新門檻值
def update_threshold(data, old_threshold):
    new_threshold = data['Probability'].mean()
    print(abs(new_threshold - old_threshold) > 0.0005)
    if abs(new_threshold - old_threshold) > 0.0005:
        return new_threshold, True  # 返回新的門檻值及更新標誌
    else:
        return old_threshold, False  # 返回舊的門檻值及不更新標誌

# 模擬Q學習訓練過程
def q_learning_train(data, threshold, epsilon):
    global Q_table
    probabilities = data['Probability']
    for episode in range(episodes):
        for probability in probabilities:
            state = map_probability_to_state(probability)
            action = choose_action(state, epsilon)
            reward = calculate_reward(probability, action, threshold)
            next_state = state
            Q_table[state, action] = (1 - learning_rate) * Q_table[state, action] + \
                                     learning_rate * (reward + discount_factor * np.max(Q_table[next_state, :]))

# 決定上傳的物件
def decide_uploads(data, Q_table, threshold):
    upload_set = set()
    for index, row in data.iterrows():
        probability = row['Probability']
        state = map_probability_to_state(probability)
        action = np.argmax(Q_table[state, :])
        if action == 1:  # 上傳動作
            upload_set.add(row['Object'])
    return upload_set

# 主要流程
file_path = "./PSkytestResult/object1000_instance3_probabilities.csv"
data = read_data(file_path)
window_size = 100
slide_step = 20

initial_data = data[:window_size]
initial_threshold = initial_data['Probability'].mean()
q_learning_train(initial_data, initial_threshold, epsilon)
last_upload_set = decide_uploads(initial_data, Q_table, initial_threshold)
print("Initial upload set:", last_upload_set)

for start in range(slide_step, len(data), slide_step):
    end = start + window_size
    if end > len(data):
        break
    window_data = data[start:end]
    new_threshold, should_update = update_threshold(window_data, initial_threshold)
    
    if should_update:
        # 如果應該更新門檻值，則使用新的門檻值重新訓練Q表
        q_learning_train(window_data, new_threshold, epsilon)
        initial_threshold = new_threshold  # 更新門檻值為新計算的門檻值
    # 否則繼續使用舊門檻值和Q表
    print(Q_table)
    print(new_threshold)
    current_upload_set = decide_uploads(window_data, Q_table, new_threshold)
    
    if current_upload_set == last_upload_set:
        print("新的set和舊的相同不上傳")
    else:
        print(f"Updated upload set for window starting at {start}:", current_upload_set)
        last_upload_set = current_upload_set

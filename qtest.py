import numpy as np
import pandas as pd

# 定義計算報酬的函數
def calculate_reward(probability, action, threshold):
    """
    根據概率值、選擇的動作和門檻值計算報酬。
    :param probability: 概率值。
    :param action: 選擇的動作，1表示上傳，0表示不上傳。
    :param threshold: 當前的門檻值。
    :return: 返回計算得到的報酬。
    """
    if probability >= threshold:
        return 1 if action == 1 else -1
    else:
        return 1 if action == 0 else -1

# 從CSV檔案讀取數據並計算初始門檻值
def read_data_and_calculate_initial_threshold(file_path):
    data = pd.read_csv(file_path)
    initial_threshold = data['Probability'].mean()
    return data, initial_threshold

# 更新門檻值
def update_threshold(combined_data, old_threshold):
    new_average = combined_data['Probability'].mean()
    print("new :" + str(new_average))
    if abs(new_average - old_threshold) > 0.01:
        print("new")
        return new_average
    print("old")
    return old_threshold

# 初始化Q表參數
num_states = 10  # 狀態數，將概率值離散化成10個等分
num_actions = 2  # 動作數，1表示上傳，0表示不上傳
Q_table = np.zeros((num_states, num_actions))  # 初始化Q表
learning_rate = 0.01  # 學習率
discount_factor = 0.95  # 折扣因子
episodes = 100  # 模擬的總次數

# 將概率值映射到狀態
def map_probability_to_state(probability, threshold):
    # 假設概率範圍是 0 到 1，等分成 num_states 狀態
    state = int((probability * num_states) // 1)
    return min(state, num_states - 1)  # 確保狀態不會超出範圍

# 模擬Q學習訓練過程
def q_learning_train(probabilities, threshold):
    global Q_table
    for episode in range(episodes):
        for probability in probabilities:
            state = map_probability_to_state(probability, threshold)
            action = np.random.choice([0, 1])  # 隨機選擇動作
            reward = calculate_reward(probability, action, threshold)  # 計算報酬
            next_state = state  # 簡化模型，假設狀態不變
            # 更新Q表
            Q_table[state, action] = (1 - learning_rate) * Q_table[state, action] + \
                                     learning_rate * (reward + discount_factor * np.max(Q_table[next_state, :]))

# 使用示例
file_path = "./manualData/qlearning(adjust) - 複製.csv"  # CSV檔案路徑
data, initial_threshold = read_data_and_calculate_initial_threshold(file_path)
q_learning_train(data['Probability'], initial_threshold)  # 使用初始門檻值進行訓練
print("初始的Q表:")
print(Q_table)
# print("init :" + str(initial_threshold))
# 假設有新數據進入
new_data = pd.DataFrame({'Probability': np.random.rand(5)})  # 模擬新數據
combined_data = pd.concat([data, new_data])
new_threshold = update_threshold(combined_data, initial_threshold)

if new_threshold != initial_threshold:
    # 如果門檻值有更新，使用新門檻值重新訓練
    print("new q table")
    q_learning_train(combined_data['Probability'], new_threshold)

# 打印更新後的Q表
print("更新後的Q表:")
print(Q_table)
print("新門檻值:", new_threshold)

# print(combined_data)

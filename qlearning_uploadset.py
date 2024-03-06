import numpy as np
import pandas as pd

# 定義計算報酬的函數
def calculate_reward(probability, action, threshold):
    if probability >= threshold:
        return 2 if action == 1 else -2
    else:
        return 2 if action == 0 else -2

# 從CSV檔案讀取數據並計算初始門檻值
def read_data_and_calculate_initial_threshold(file_path):
    data = pd.read_csv(file_path)
    initial_threshold = data['Probability'].mean()
    return data, initial_threshold

# 更新門檻值
def update_threshold(combined_data, old_threshold):
    new_average = combined_data['Probability'].mean()
    print("new avg:" + str(new_average))
    if abs(new_average - old_threshold) > 0.05:
        print("new avg跟舊門檻值差距太大")
        return new_average
    print("new avg和舊門檻值差距不大使用舊門檻值")
    return old_threshold

# 初始化Q表參數
num_states = 10  # 狀態數，將概率值離散化成10個等分
num_actions = 2  # 動作數，1表示上傳，0表示不上傳
Q_table = np.zeros((num_states, num_actions))  # 初始化Q表
learning_rate = 0.1  # 學習率
discount_factor = 0.9  # 折扣因子
episodes = 10000  # 模擬的總次數
epsilon = 0.1  # ε值，控制探索的概率

# 將概率值映射到狀態
def map_probability_to_state(probability, num_states=10):
    state = int(probability * num_states)
    return min(state, num_states - 1)


# 根據ε-貪婪策略選擇動作
def choose_action(state, epsilon):
    if np.random.rand() < epsilon:
        return np.random.choice([0, 1])  # 探索：隨機選擇動作
    else:
        return np.argmax(Q_table[state, :])  # 利用：選擇Q值最高的動作

# 模擬Q學習訓練過程
def q_learning_train(probabilities, threshold, epsilon):
    global Q_table
    for episode in range(episodes):
        for probability in probabilities:
            state = map_probability_to_state(probability)
            action = choose_action(state, epsilon)  # 使用ε-貪婪策略選擇動作
            reward = calculate_reward(probability, action, threshold)
            next_state = state
            # 更新Q表
            Q_table[state, action] = (1 - learning_rate) * Q_table[state, action] + \
                                     learning_rate * (reward + discount_factor * np.max(Q_table[next_state, :]))

# 使用示例
file_path = "./PSkytestResult/object50_instance3_probabilities.csv"
data, initial_threshold = read_data_and_calculate_initial_threshold(file_path)
q_learning_train(data['Probability'], initial_threshold, epsilon)  # 使用初始門檻值和ε-貪婪策略進行訓練

new_file_path = "./PSkytestResult/object100_instance3_probabilities.csv"
new_data = pd.read_csv(new_file_path)
combined_data = pd.concat([data, new_data])

new_threshold = update_threshold(combined_data, initial_threshold)

if new_threshold != initial_threshold:
    print("new q table")
    q_learning_train(combined_data['Probability'], new_threshold, epsilon)

# 印出更新後的Q表
print("更新後的Q表:")
print(Q_table)
print("目前的門檻值:", new_threshold)

def decide_uploads_using_q_table(data, Q_table, threshold):
    upload_set = set()
    for index, row in data.iterrows():
        probability = row['Probability']
        state = map_probability_to_state(probability)
        action = np.argmax(Q_table[state, :])  # 根據訓練好的Q表選擇動作
        if action == 1 and probability >= threshold:  # 如果動作是上傳且概率高於門檻值
            upload_set.add(row['Object'])  # 添加物件到上傳集合
    
    # 將集合轉換為列表並排序
    upload_list = sorted(list(upload_set), key=lambda x: int(x.replace('Object', '')))
    return upload_list

# 使用訓練好的Q表和門檻值判斷要上傳的物件
upload_list = decide_uploads_using_q_table(combined_data, Q_table, new_threshold)
print("決定要上傳的物件集合，並按物件名稱由小到大排列:")
print(upload_list)

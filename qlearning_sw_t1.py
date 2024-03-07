import numpy as np
import pandas as pd
from PSkytest_t1 import PSky
import itertools

class QLearning():
    # 定義計算報酬的函數
    def calculate_reward(self, probability, action, threshold):
        if probability >= threshold:
            return 2 if action == 1 else -2
        else:
            return 2 if action == 0 else -2

    # 從CSV檔案讀取數據
    def read_data(self, file_path):
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
    def map_probability_to_state(self, probability, num_states=10):
        state = int(probability * num_states)
        return min(state, num_states - 1)

    # 根據ε-貪婪策略選擇動作
    def choose_action(self, state, epsilon):
        if np.random.rand() < epsilon:
            return np.random.choice([0, 1])
        else:
            return np.argmax(self.Q_table[state, :])

    # 更新門檻值
    def update_threshold(self, data, old_threshold):
        new_threshold = data['Probability'].mean()
        print(abs(new_threshold - old_threshold) > 0.005)
        if abs(new_threshold - old_threshold) > 0.005:
            return new_threshold, True  # 返回新的門檻值及更新標誌
        else:
            return old_threshold, False  # 返回舊的門檻值及不更新標誌

    # 模擬Q學習訓練過程
    def q_learning_train(self, probabilities, threshold, epsilon):
        # global Q_table
        for episode in range(self.episodes):
            for probability in probabilities:
                state = self.map_probability_to_state(probability)
                action = self.choose_action(state, epsilon)
                reward = self.calculate_reward(probability, action, threshold)
                next_state = state
                self.Q_table[state, action] = (1 - self.learning_rate) * self.Q_table[state, action] + \
                                        self.learning_rate * (reward + self.discount_factor * np.max(self.Q_table[next_state, :]))
    # 決定上傳的物件
    def decide_uploads(self, probability_dict, Q_table, threshold):
        upload_set = set()
        for objectKey, probability in probability_dict.items():
            state = self.map_probability_to_state(probability)
            action = np.argmax(Q_table[state, :])
            if action == 1:  # 上傳動作
                upload_set.add(objectKey)
        return upload_set

    def runFun(self, original_data, index = 0):
        # 20 is slide_step
        # 100 is window_size
        print("Step start: runFun")
        index = 0
        # 主要流程
        print("1 time: ")
        slide_window_dict = dict(itertools.islice(original_data.items(), index, 100))
        index += 100
        self.runSlideWindow(slide_window_dict, 100 , 0)
        times = 1
        
        # for
        print("This is time: " + str(2))
        old_item_data = dict(itertools.islice(slide_window_dict.items(), 20, 100))
        new_item_data = dict(itertools.islice(original_data.items(), index, index + 20))
        index += 20
        # combine two dict (old & new)
        slide_window_dict = {**old_item_data, **new_item_data}
        # # print(slice_original_data)
        self.runSlideWindow(slide_window_dict, 100 , 20)
        # times += 1
        
    def runSlideWindow(self, original_data, window_size = 100, slide_step = 0):
        
        
        probability_dict = newPSky.calculate_probabilities(original_data)
        # get initial_threshold
        initial_threshold = 0.0
        for key, value in probability_dict.items():
            initial_threshold += value
        initial_threshold /= len(probability_dict.items())
        
        self.q_learning_train(probability_dict.values(), initial_threshold, self.epsilon)
        last_upload_set = self.decide_uploads(probability_dict, self.Q_table, initial_threshold)
        # print("Initial upload set:", last_upload_set)
        
        # Slide Window for loop
        if( slide_step != 0 ):
            # print(len(original_data))
            
            for start in range(slide_step, len(original_data), slide_step):
                end = start + window_size
                if end > len(original_data):
                    print("nytdu")
                    break
                window_data = original_data[start:end]
                new_threshold, should_update = self.update_threshold(window_data, initial_threshold)
                print("in")
                
                if should_update:
                    # 如果應該更新門檻值，則使用新的門檻值重新訓練Q表
                    self.q_learning_train(window_data, new_threshold, self.epsilon)
                    initial_threshold = new_threshold  # 更新門檻值為新計算的門檻值
                # 否則繼續使用舊門檻值和Q表
                print(self.Q_table)
                print(new_threshold)
                current_upload_set = self.decide_uploads(window_data, self.Q_table, new_threshold)
                
                if current_upload_set == last_upload_set:
                    print("新的set和舊的相同不上傳")
                else:
                    print(f"Updated upload set for window starting at {start}:", current_upload_set)
                    last_upload_set = current_upload_set
            # print("EMD")

newPSky = PSky()

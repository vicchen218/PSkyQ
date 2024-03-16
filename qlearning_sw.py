# 引入必要的函式庫
import numpy as np
import pandas as pd
from PSkytest import PSky
import itertools
import random

class QLearning():
    # 定義一個基於Q學習的類，用於決定是否上傳物件

    # 定義計算報酬的函數
    def calculate_reward(self, probability, action, threshold):
        """
        根據預測概率、採取的行動和設定的閾值來計算報酬。
        :param probability: 物件被預測為正類的概率。
        :param action: 採取的行動，0或1，其中1代表上傳，0代表不上傳。
        :param threshold: 決策閾值。
        :return: 計算得到的報酬值。
        """
        if probability >= threshold:
            return 2 if action == 1 else -2
        else:
            return 2 if action == 0 else -2

    # 從CSV檔案讀取數據
    def read_data(self, file_path):
        """
        從給定的CSV檔案路徑中讀取數據。
        :param file_path: CSV檔案的路徑。
        :return: 讀取到的DataFrame數據。
        """
        data = pd.read_csv(file_path)
        return data

    # 初始化Q學習相關的參數
    num_states = 10  # 定義狀態的數量
    num_actions = 2  # 定義行動的選項數量，這裡是上傳或不上傳
    Q_table = np.zeros((num_states, num_actions))  # 初始化Q表，所有值為0
    learning_rate = 0.1  # 設定學習率
    discount_factor = 0.9  # 設定折扣因子
    episodes = 1000  # 設定訓練的回合數
    epsilon = 0.1  # 設定ε，用於ε-貪婪策略控制探索和利用的平衡

    # 將概率值映射到狀態
    def map_probability_to_state(self, probability, num_states=10):
        """
        將概率映射到一個狀態值，用於Q表中的索引。
        :param probability: 物件被預測為正類的概率。
        :param num_states: 狀態的總數。
        :return: 對應的狀態索引。
        """
        state = int(probability * num_states)
        return min(state, num_states - 1)

    # 根據ε-貪婪策略選擇動作
    def choose_action(self, state, epsilon):
        """
        根據當前狀態和ε-貪婪策略選擇行動。
        :param state: 當前的狀態。
        :param epsilon: ε值，控制探索和利用的平衡。
        :return: 選擇的行動，0或1。
        """
        if np.random.rand() < epsilon:
            return np.random.choice([0, 1])
        else:
            return np.argmax(self.Q_table[state, :])

    # 更新門檻值
    def update_threshold(self, old_threshold, new_threshold):
        """
        根據新舊門檻值的差異決定是否更新門檻值。
        :param old_threshold: 舊的門檻值。
        :param new_threshold: 新計算的門檻值。
        :return: 更新後的門檻值和是否進行了更新的標誌。
        """
        print(abs(new_threshold - old_threshold))
        if abs(new_threshold - old_threshold) > 0.005:
            return new_threshold, True  # 返回新的門檻值及更新標誌
        else:
            return old_threshold, False  # 返回舊的門檻值及不更新標誌

    # 模擬Q學習訓練過程
    def q_learning_train(self, probabilities, threshold, epsilon):
        """
        執行Q學習算法進行訓練。
        :param probabilities: 一系列物件被預測為正類的概率。
        :param threshold: 決策閾值。
        :param epsilon: ε值，用於ε-貪婪策略。
        """
        for episode in range(self.episodes):
            for probability in probabilities:
                state = self.map_probability_to_state(probability)
                action = self.choose_action(state, epsilon)
                reward = self.calculate_reward(probability, action, threshold)
                next_state = state
                # 根據Q學習公式更新Q值
                self.Q_table[state, action] = (1 - self.learning_rate) * self.Q_table[state, action] + \
                                        self.learning_rate * (reward + self.discount_factor * np.max(self.Q_table[next_state, :]))

    # 決定上傳的物件集合
    def decide_uploads(self, probability_dict, Q_table, threshold):
        """
        根據當前的Q表和閾值，決定哪些物件應該上傳。
        :param probability_dict: 一個包含物件概率的字典，鍵是物件的標識，值是對應的概率。
        :param Q_table: 當前的Q表。
        :param threshold: 決策閾值。
        :return: 決定上傳的物件集合。
        """
        upload_set = set()
        for objectKey, probability in probability_dict.items():
            state = self.map_probability_to_state(probability)
            action = np.argmax(Q_table[state, :])
            if action == 1:  # 如果決定為上傳
                upload_set.add(objectKey)
        return upload_set

    # 下面的函數實現了滑動窗口機制，適應動態變化的數據集，進行連續的學習和決策更新。

    # 初始化滑動窗口
    def runSlideWindow(self, original_data, window_size=500, min_slide_step=100, max_slide_step=200):
        """
        執行滑動窗口機制的主要流程，每次進入的新物件數量在一個固定範圍內隨機。
        :param original_data: 原始數據集，以字典形式給出。
        :param window_size: 滑動窗口的大小，預設為500。
        :param min_slide_step: 每次滑動步長的最小值，預設為100。
        :param max_slide_step: 每次滑動步長的最大值，預設為200。
        """
        total_upload_set=set()
        print("Step start: runFun")
        index = 0
        total_upload_set_size = 0

        # 首次處理，根據window_size初始化滑動窗口
        print("Initial time: ")
        slide_window_dict = dict(itertools.islice(original_data.items(), index, window_size))
        index += random.randint(min_slide_step, max_slide_step)
        current_threshold, last_upload_set, total_upload_set_size,total_upload_set = self.SlideWindowInitialize(slide_window_dict, total_upload_set_size,total_upload_set)
        print("total_upload_set_size: " + str(len(total_upload_set)))
        
        print("initial_threshold", current_threshold)
        print("Initial upload set:", last_upload_set)
        times = 1
        
        # 進行滑動窗口更新
        while True:
            print(f"This is time: {times + 1}")
            # 隨機選擇這次更新的步長
            slide_step = random.randint(min_slide_step, max_slide_step)
            # 更新滑動窗口，刪除舊數據，添加新數據
            old_item_data = dict(itertools.islice(slide_window_dict.items(), slide_step, window_size))
            new_item_data = dict(itertools.islice(original_data.items(), index, index + slide_step))
            index += slide_step
            slide_window_dict = {**old_item_data, **new_item_data}
            
            # 檢查是否有足夠的新數據進行下一次更新
            if len(new_item_data) < slide_step:
                break

            print("SlideWindowUpdate")
            print("window_size: "+ str(window_size))
            print("slide_step: "+ str(slide_step))
            print("update times :" + str(times))
            current_threshold, last_upload_set, total_upload_set_size,total_upload_set = self.SlideWindowUpdate(slide_window_dict, current_threshold, last_upload_set, total_upload_set_size,total_upload_set)
            print("total_upload_set_size: " + str(len(total_upload_set)))
            times += 1
            if last_upload_set == None:
                break  # 如果上傳集合為空，結束更新循環
        print("total_upload_set_size: " + str(len(total_upload_set)))

    # 滑動窗口初始化
    def SlideWindowInitialize(self, original_data, total_upload_set_size,total_upload_set):
        """
        利用原始數據初始化滑動窗口，計算初始閾值和上傳集合。
        :param original_data: 初始滑動窗口的數據集。
        :return: 初始閾值和上傳集合。
        """
        # 計算初始概率並決定初始閾值
        probability_dict = newPSky.calculate_probabilities(original_data)
        initial_threshold = sum(probability_dict.values()) / len(probability_dict)
        print(initial_threshold)
        # 使用初始數據和閾值訓練Q學習模型
        self.q_learning_train(list(probability_dict.values()), initial_threshold, self.epsilon)
        # 決定初始上傳集合
        last_upload_set = self.decide_uploads(probability_dict, self.Q_table, initial_threshold)
        print(self.Q_table)

        total_upload_set= total_upload_set | last_upload_set
        total_upload_set_size += len(last_upload_set)
        
        
        return initial_threshold, last_upload_set, total_upload_set_size,total_upload_set

    # 滑動窗口更新
    def SlideWindowUpdate(self, original_data, old_threshold, last_upload_set, total_upload_set_size,total_upload_set):
        """
        更新滑動窗口，重新計算閾值和上傳集合。
        :param original_data: 當前滑動窗口的數據集。
        :param old_threshold: 上一次的閾值。
        :param last_upload_set: 上一次的上傳集合。
        :return: 新的閾值和上傳集合。
        """
        # 計算新的概率分佈
        probability_dict = newPSky.calculate_probabilities(original_data)
        if len(probability_dict) == 0:
            return 0, None  # 如果新的數據集為空，返回0和None

        # 計算新的閾值
        new_threshold = sum(probability_dict.values()) / len(probability_dict)
        print(new_threshold)
        
        # 根據新舊閾值差異決定是否更新閾值
        new_threshold, should_update_threshold = self.update_threshold(old_threshold, new_threshold)
        
        if should_update_threshold:
            # 如果需要更新閾值，重新訓練Q學習模型
            self.q_learning_train(list(probability_dict.values()), new_threshold, self.epsilon)

        # 根據新的Q表和閾值決定上傳集合
        current_upload_set = self.decide_uploads(probability_dict, self.Q_table, new_threshold)
        print(self.Q_table)

        # 根據是否更新閾值和上傳集合的變化決定返回值
        result_threshold = new_threshold if should_update_threshold else old_threshold
        if current_upload_set == last_upload_set:
            print("新的set和舊的相同不上傳")
            result_set = last_upload_set
        else:
            print("新的set和舊的不相同")
            total_upload_set_size += len(current_upload_set)
            result_set = current_upload_set
            print('set difference: ')
            print(total_upload_set ^ current_upload_set)
            total_upload_set=current_upload_set | total_upload_set
       
            
        return result_threshold, result_set, total_upload_set_size,total_upload_set

# 實例化PSky類，用於後續計算物件的概率
newPSky = PSky()

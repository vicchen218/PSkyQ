# 引入必要的函式庫
import numpy as np
import pandas as pd
from PSkytest import PSky
import itertools
import random

class QLearning():
    def __init__(self, window_size, epsilon=0.1, alpha=0.1, gamma=0.95):
        self.window_size = window_size
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.action_space = [-1/window_size, 0, 1/window_size]  # 動作空間: 減少、不變、增加門檻值
        self.state_size = int(2 * window_size + 1)  # 從 -1 到 1 的狀態
        self.Q = np.zeros((self.state_size, len(self.action_space)))
    
    def normalize_state(self, diff):
        # 將差異映射到狀態索引
        return int((diff + 1) * self.window_size)  # 將 [-1, 1] 映射到 [0, 狀態數量]

    def choose_action(self, state_index):
        # 採用 ε-greedy 策略選擇動作
        if random.random() < self.epsilon:
            action_index = random.randint(0, len(self.action_space) - 1)
        else:
            action_index = np.argmax(self.Q[state_index])
        return action_index

    def update_threshold(self, old_threshold, difference):
        state_index = self.normalize_state(difference)
        action_index = self.choose_action(state_index)
        print("gpt old old_threshold", old_threshold)

        # 選擇動作並計算新門檻值
        action = self.action_space[action_index]
        new_threshold = old_threshold + action
        new_threshold = max(0, min(new_threshold, 1))  # 確保門檻值在[0,1]範圍內

        # 避免門檻值陷入0或1
        if new_threshold == 0 and action == 0:
            if random.random() < 0.5:  # 隨機嘗試增加門檻值
                new_threshold = old_threshold + self.action_space[2]  # 最小增量
            else:
                new_threshold = old_threshold + self.action_space[0]  # 最小減量
        elif new_threshold == 1 and action == 0:
            if random.random() < 0.5:  # 隨機嘗試減少門檻值
                new_threshold = old_threshold + self.action_space[0]  # 最小減量
            else:
                new_threshold = old_threshold + self.action_space[2]  # 最小增量

        return new_threshold, state_index, action_index


    def update_Q_table(self, state_index, action_index, reward, new_difference):
        new_state_index = self.normalize_state(new_difference)
        # 更新 Q 表
        best_future_action = np.argmax(self.Q[new_state_index])
        self.Q[state_index, action_index] += self.alpha * (reward + self.gamma * self.Q[new_state_index, best_future_action] - self.Q[state_index, action_index])

    def compute_reward(self, previous_uploads, current_uploads):
        # 簡單的報酬函數: 若新的上傳集合大小小於舊的則獎勵
        if len(current_uploads) < len(previous_uploads):
            return 1
        elif len(current_uploads) > len(previous_uploads):
            return -1
        return 0  # 無變化時不獎勵也不懲罰
    
    
    
    
    
    
    # 從CSV檔案讀取數據
    def read_data(self, file_path):
        """
        從給定的CSV檔案路徑中讀取數據。
        :param file_path: CSV檔案的路徑。
        :return: 讀取到的DataFrame數據。
        """
        data = pd.read_csv(file_path)
        return data


    # 更新門檻值
    # def update_threshold(self, old_threshold, new_threshold):
    #     """
    #     根據新舊門檻值的差異決定是否更新門檻值。
    #     :param old_threshold: 舊的門檻值。
    #     :param new_threshold: 新計算的門檻值。
    #     :return: 更新後的門檻值和是否進行了更新的標誌。
    #     """
    #     print("abs new - old: ", abs(new_threshold - old_threshold))
    #     if abs(new_threshold - old_threshold) > 0.005:
    #         return new_threshold, True  # 返回新的門檻值及更新標誌
    #     else:
    #         return old_threshold, False  # 返回舊的門檻值及不更新標誌

    # 決定上傳的物件集合
    def decide_uploads(self, probability_dict, threshold):
        upload_set = set()
        for objectKey, probability in probability_dict.items():
            if probability > threshold:
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
        current_threshold, last_upload_set, total_upload_set_size, total_upload_set = self.SlideWindowInitialize(slide_window_dict, total_upload_set_size,total_upload_set)
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
        
        return total_upload_set
        

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
        # 決定初始上傳集合
        last_upload_set = self.decide_uploads(probability_dict, initial_threshold)

        total_upload_set= total_upload_set | last_upload_set
        total_upload_set_size += len(last_upload_set)
        
        
        return initial_threshold, last_upload_set, total_upload_set_size, total_upload_set

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

        # 計算新的門檻值
        new_threshold = sum(probability_dict.values()) / len(probability_dict)
        print("new_threshold: " , new_threshold)
        
        # 根據新舊閾值差異決定是否更新閾值
        # new_threshold, should_update_threshold = self.update_threshold(old_threshold, new_threshold)
        new_threshold, state_index, action_index= self.update_threshold(old_threshold, new_threshold)
       
        # 根據新的Q表和閾值決定上傳集合
        current_upload_set = self.decide_uploads(probability_dict, new_threshold)
        # 計算報酬
        reward = self.compute_reward(last_upload_set, current_upload_set)

        # 更新 Q 表
        new_difference = sum(probability_dict.values()) / len(probability_dict) - new_threshold
        self.update_Q_table(state_index, action_index, reward, new_difference)
        
        # print(self.Q, "\n\n")
        # 根據是否更新閾值和上傳集合的變化決定返回值
        result_threshold = new_threshold
        # result_threshold = new_threshold if should_update_threshold else old_threshold
        if current_upload_set == last_upload_set:
            print("新的set和舊的相同不上傳")
            result_set = last_upload_set
        else:
            print("新的set和舊的不相同")
            total_upload_set_size += len(current_upload_set)
            result_set = current_upload_set
            save_set = total_upload_set
            total_upload_set=current_upload_set | total_upload_set
            
            print(total_upload_set - save_set)

        return result_threshold, result_set, total_upload_set_size,total_upload_set

# 實例化PSky類，用於後續計算物件的概率
newPSky = PSky()
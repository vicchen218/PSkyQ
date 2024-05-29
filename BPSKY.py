# 引入必要的函式庫
import numpy as np
import pandas as pd
from PSkytest import PSky
import itertools
import random

class BruteMethod():
    
    threshold = 0
    
    def set_threshold(self, num):
        self.threshold = num
    # 從CSV檔案讀取數據
    def read_data(self, file_path):
        """
        從給定的CSV檔案路徑中讀取數據。
        :param file_path: CSV檔案的路徑。
        :return: 讀取到的DataFrame數據。
        """
        data = pd.read_csv(file_path)
        return data
    # 決定上傳的物件集合
    def upload_filter(self, probability_dict):
        """
        根據當前的Q表和閾值，決定哪些物件應該上傳。
        :param probability_dict: 一個包含物件概率的字典，鍵是物件的標識，值是對應的概率。
        :param Q_table: 當前的Q表。
        :param threshold: 決策閾值。
        :return: 決定上傳的物件集合。
        """
        upload_set = set()
        for objectKey, value in probability_dict.items():
            if(value >= self.threshold):
                upload_set.add(objectKey)
        print(upload_set)
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
        result_upload_set, total_upload_set = self.SlideWindowInitialize(slide_window_dict, total_upload_set)
        
        total_upload_set_size += len(result_upload_set)
        print("total_upload_set_size: " + str(len(total_upload_set)))
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
            result_upload_set, total_upload_set = self.SlideWindowUpdate(slide_window_dict, total_upload_set)
            total_upload_set_size += len(result_upload_set)
            print("total_upload_set_size: " + str(len(total_upload_set)))
            
            times += 1
            if result_upload_set == None:
                break  # 如果上傳集合為空，結束更新循環
            
        # print("End total_upload_set: ")
        # print(total_upload_set)
        # print("size: " + str(len(total_upload_set)))
        return total_upload_set
        
    # 滑動窗口初始化
    def SlideWindowInitialize(self, original_data, total_upload_set):
        """
        利用原始數據初始化滑動窗口，計算初始閾值和上傳集合。
        :param original_data: 初始滑動窗口的數據集。
        :return: 初始閾值和上傳集合。
        """
        probability_dict = newPSky.calculate_probabilities(original_data)
        result_upload_set = self.upload_filter(probability_dict)
        total_upload_set= total_upload_set | result_upload_set
        return result_upload_set,total_upload_set

    # 滑動窗口更新
    def SlideWindowUpdate(self, original_data, total_upload_set):
        """
        更新滑動窗口，重新計算閾值和上傳集合。
        :param original_data: 當前滑動窗口的數據集。
        :param old_threshold: 上一次的閾值。
        :param last_upload_set: 上一次的上傳集合。
        :return: 新的閾值和上傳集合。
        """
        probability_dict = newPSky.calculate_probabilities(original_data)
        if len(probability_dict) == 0:
            return 0, None  # 如果新的數據集為空，返回0和None
        
        result_upload_set = self.upload_filter(probability_dict)
        total_upload_set = total_upload_set | result_upload_set
        
        return result_upload_set, total_upload_set

# 實例化PSky類，用於後續計算物件的概率
newPSky = PSky()

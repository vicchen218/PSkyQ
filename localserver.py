import pandas as pd
from PSkytest import PSky
from qlearning_sw  import QLearning

# from qlearning_sw_t1 import get_skyline_set as process_second  # 假設函數名稱是 get_skyline_set

def main():
    # # 步驟1: 讀取CSV檔案
    input_csv_file_name = "A_object1000_instance3"
    
    # # 步驟2: 傳送到第一個外部程式進行處理，並產生新的CSV檔案
    print("Step 2: PSky")
    newSky = PSky()
    newSky.runFun(input_csv_file_name)
    # 步驟3: 讀取由第一個程式生成的CSV檔案
    
    # # 步驟4: 將處理後的CSV檔案傳送到第二個外部程式進行處理
    print("Step 4: QLearning")
    newQ = QLearning()
    newQ.runFun(input_csv_file_name)
    
    # # 步驟5: 比對原始資料與要上傳的天際線集合，並準備上傳的資料
    # todo
    
    # # 這裡添加上傳邏輯
    # print("準備上傳的物件資訊:")
    # print(upload_items)

if __name__ == "__main__":
    main()
    print("Finish")

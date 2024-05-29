import pandas as pd
from qlearning_sw import QLearning
from Read_CSV import Read_CSV
import time
import itertools

def main():
    #Change value here:
    window_size = 1000
    
    start_time = time.time()  # 獲取當前時間作為開始時間
    newQLearning = QLearning(window_size)
    
    # : 讀取CSV檔案
    csv_file_path = "./data/"
    input_csv_file_name = "TEST_object50000_instance3"
    original_data = Read_CSV.read_data_from_csv(csv_file_path + input_csv_file_name + '.csv')
    print(type(original_data))
    
    #First: simulate x local server and do action
    runTimes = 5
    fileSize = 100
    # for times in range(1, runTimes + 1):
    #     sliceData = dict(itertools.islice(original_data.items(), int((times-1) * (fileSize / runTimes)), int((times) * (fileSize / runTimes))))
    #     print(len(sliceData))
    #     result_upload_set = newQLearning.runSlideWindow(sliceData, window_size, min_slide_step=10, max_slide_step=20)
    #     print(result_upload_set)
    #     my_list = list(result_upload_set)
    #     df = pd.DataFrame(my_list, columns=["Result"])
    #     df.to_excel("./output_qlearning/" + input_csv_file_name + "_output_" + str(times) + ".xlsx", index=False)
        
    #Second: combine and do again local server (ex: 5) -> main server
    Combine_data = {}
    
    for times in range(1, runTimes + 1):
        print('read_slice_data_from_csv')
        get_key_data_list = Read_CSV.read_slice_data_from_csv("./output_qlearning/" + input_csv_file_name + "_output_" + str(times) + ".xlsx")
        for key in get_key_data_list:
            Combine_data[key] = original_data[key]
        Read_CSV.save_slice_data_into_csv(Combine_data, input_csv_file_name)
   
    end_time = time.time()  # 獲取當前時間作為結束時間
    print(f"Finish. The program took {end_time - start_time} seconds.")  # 計算並印出運行時間

    
if __name__ == "__main__":
    main()
    print("Finish")
import pandas as pd
from qlearning_sw import QLearning
from Read_CSV import Read_CSV
import time
import itertools
from MyDebuger import MyDebuger
import re

def main():
    
    #Change value here:
    window_size = 1000
    csv_attributeSize = 3
    
    #讀取CSV檔案
    csv_file_path = "./data_A" + str(csv_attributeSize) + "/"
    input_csv_file_name = "A_object1000_instance3"
    
    numbers = re.findall(r'\d+', input_csv_file_name)
    numbers = [int(num) for num in numbers]
    objectSize = numbers[0]
    
    original_data = Read_CSV.read_data_from_csv(csv_file_path + input_csv_file_name + '.csv', csv_attributeSize)
    
    # initialize
    start_time = time.time()  # 獲取當前時間作為開始時間
    newQLearning = QLearning(window_size)
    newMyDebuger = MyDebuger()
    
    # newMyDebuger.OutputDict(original_data)
    
    print("Start action.")
    #First: simulate x local server and do action
    runTimes = 5
    print("\nFirst: simulate x local server and do action\n")
    for times in range(1, runTimes + 1):
         sliceData = dict(itertools.islice(original_data.items(), int((times-1) * (objectSize / runTimes)), int((times) * (objectSize / runTimes))))
         print(len(sliceData))
         result_upload_set = newQLearning.runSlideWindow(sliceData, window_size, min_slide_step=20, max_slide_step=20)
         result_upload_list = list(result_upload_set)
         print('\n=================\nEnd total_upload_set:')
         print("size: " + str(len(result_upload_list)))
         print(result_upload_list)
         df = pd.DataFrame(result_upload_list, columns=["Result"])
         df.to_excel("./output_qlearning/" + input_csv_file_name + "_output_" + str(times) + ".xlsx", index=False)
        
    #Second: combine and do again local server (ex: 5) -> main server
    # print("\nSecond: combine and do again local server (ex: 5) -> main server\n")
    # combine_data = {}
    # for times in range(1, runTimes + 1):
    #     print('read_slice_data_from_csv')
    #     get_key_data_list = Read_CSV.read_slice_data_from_csv("./output_qlearning/" + input_csv_file_name + "_output_" + str(times) + ".xlsx")
    #     for key in get_key_data_list:
    #         combine_data[key] = original_data[key]
    #     Read_CSV.save_slice_data_into_csv(combine_data, input_csv_file_name)
   

    #Third: Using combine data and run main server
    #only_third_mode = True
   # print("\nThird: Using combine data and run main server\n")
    #if(only_third_mode):
        #combine_data = Read_CSV.read_data_from_csv('./output_qlearning/' + input_csv_file_name + '_output_combine' + '.csv')
    
    #result_upload_set = newQLearning.runSlideWindow(combine_data, window_size, min_slide_step=10, max_slide_step=20)
    #print("Main server result upload set: ")
    #print(result_upload_set)
    #my_list = list(result_upload_set)
    #df = pd.DataFrame(my_list, columns=["Result"])
    #df.to_excel("./output_qlearning/" + input_csv_file_name + "_output_final.xlsx", index=False)
    
    
    end_time = time.time()  # 獲取當前時間作為結束時間
    print(f"\nFinish. The program took {end_time - start_time} seconds.")  # 計算並印出運行時間
    
if __name__ == "__main__":
    main()
    print("Finish")
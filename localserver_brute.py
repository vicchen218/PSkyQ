import pandas as pd
from BPSKY import BruteMethod
from Read_CSV import Read_CSV
import time
import itertools

def main():
    start_time = time.time()  # 獲取當前時間作為開始時間
    newBruteMethod = BruteMethod()
    
    # : 讀取CSV檔案
    csv_file_path = "./data_A3/"
    input_csv_file_name = "INSTANCE9_object10000_instance9"
    original_data = Read_CSV.read_data_from_csv(csv_file_path + input_csv_file_name + '.csv')
    
    #First: set default threshold and run BSky
    newBruteMethod.set_threshold(0.01)
    result_upload_set = newBruteMethod.runSlideWindow(original_data, window_size=1000, min_slide_step=10, max_slide_step=20)
    
    #Second: save list into xlsx
    key_list = list(result_upload_set)
    df = pd.DataFrame(key_list, columns=["Result"])
    df.to_excel("./output_brute/" + input_csv_file_name + "_output.xlsx", index=False)
        
    #Third: using key to find target value and save into another csv file
    combine_data = {}
    for key in key_list:
        combine_data[key] = original_data[key]
    Read_CSV.save_slice_data_into_csv(combine_data, input_csv_file_name)
    
    
    end_time = time.time()  # 獲取當前時間作為結束時間
    print(f"Finish. The program took {end_time - start_time} seconds.")  # 計算並印出運行時間

    
if __name__ == "__main__":
    main()
    print("Finish")
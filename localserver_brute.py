import pandas as pd
from BPSKY import BruteMethod
from Read_CSV import Read_CSV
import time
import itertools

def main():
    start_time = time.time()  # 獲取當前時間作為開始時間
    newBruteMethod = BruteMethod()
    
    # : 讀取CSV檔案
    csv_file_path = "./data/"
    input_csv_file_name = "TEST_object50000_instance3"
    original_data = Read_CSV.read_data_from_csv(csv_file_path + input_csv_file_name + '.csv')
    
    newBruteMethod.set_threshold(0.01)
    
    result_upload_set = newBruteMethod.runSlideWindow(original_data, window_size=1000, min_slide_step=10, max_slide_step=20)
        
    my_list = list(result_upload_set)
    df = pd.DataFrame(my_list, columns=["Result"])
    df.to_excel("./output_brute/" + input_csv_file_name + "_output.xlsx", index=False)
        
    
    end_time = time.time()  # 獲取當前時間作為結束時間
    print(f"Finish. The program took {end_time - start_time} seconds.")  # 計算並印出運行時間

    
if __name__ == "__main__":
    main()
    print("Finish")
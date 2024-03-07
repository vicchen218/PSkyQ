from qlearning_sw_t1 import QLearning

def main():
    input_csv_file_name = "A_object1000_instance3.csv"  # 假設檔案名稱已包含副檔名
    print("Step: QLearning")
    qlearning_instance = QLearning()
    qlearning_instance.runFun(input_csv_file_name)

if __name__ == "__main__":
    main()
    print("Finish")

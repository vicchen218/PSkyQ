import pandas as pd

class FileManager():
    # from qlearning_sw_t1 import get_skyline_set as process_second  # 假設函數名稱是 get_skyline_set
    def read_data_from_csv(csv_file_path):
        # 從CSV檔案讀取數據
        df = pd.read_csv(csv_file_path)
        # 將DataFrame轉換為所需的數據結構
        data = {}
        for _, row in df.iterrows():
            object_name = row['Object']
            instances_data = []
            # 對於每個實例，提取其屬性和概率
            for i in range(1, ((len(row) - 1) // 5) + 1):  # 假設每個實例有5個欄位（包含實例名稱）
                instance_id = row[f'Instance{i}']
                prob = row[f'Probability_{i}']
                attributes = [row[f'Attribute1_{i}'], row[f'Attribute2_{i}'], row[f'Attribute3_{i}']]
                instances_data.append((instance_id, prob, attributes))
            data[object_name] = instances_data
        return data

    def save_probabilities_to_csv(self,probabilities, output_file_path):
        # 將計算結果轉換為DataFrame
        df = pd.DataFrame(list(probabilities.items()), columns=['Object', 'Probability'])
        # 保存到CSV檔案
        df.to_csv(output_file_path, index=False)
        print(f'Probabilities have been saved to {output_file_path}')

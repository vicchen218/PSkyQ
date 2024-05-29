import pandas as pd

class Read_CSV():
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

    def read_slice_data_from_csv(csv_file_path):
        print(csv_file_path)
        # 從CSV檔案讀取數據
        df = pd.read_excel(csv_file_path, engine='openpyxl')
        
        # 將DataFrame轉換為所需的數據結構
        if 'Result' in df.columns:
            result_list = df['Result'].dropna().tolist()
            # result_set = set(result_list)
            # print("\nList:")
            print(result_list)

            # print("\nSet:")
            # print(result_set)    
        return result_list
    def save_slice_data_into_csv(data_dict, file_name):
       # Initialize the header and data list
        header = ["Object"]
        data = []

        # Construct the header based on the maximum number of instances
        max_instances = max(len(v) for v in data_dict.values())
        for i in range(1, max_instances + 1):
            header.extend([
                f"Instance{i}",
                f"Attribute1_{i}",
                f"Attribute2_{i}",
                f"Attribute3_{i}",
                f"Probability_{i}"
            ])

        # Construct the data rows
        for obj, instances in data_dict.items():
            row = [obj]
            for instance in instances:
                instance_name, probability, attributes = instance
                row.extend([instance_name] + attributes + [probability])
            # Pad the row if it has fewer instances than the max_instances
            while len(row) < len(header):
                row.extend([""] * 5)
            data.append(row)

        # Create DataFrame
        df = pd.DataFrame(data, columns=header)

        # Save to CSV
        df.to_csv("./output_qlearning/" + file_name + 'output_combine'+ '.csv', index=False)

        # Display the DataFrame
        # print(df)
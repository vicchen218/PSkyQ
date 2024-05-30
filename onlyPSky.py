import pandas as pd

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

def is_dominated(u_i_a, u_j_r_a):
    # 判斷實例u_j^r是否在所有屬性上都優於u_i^a
    return all(a_j_r <= a_i for a_j_r, a_i in zip(u_j_r_a, u_i_a))

def calculate_probabilities(data):
    probabilities = {}
    # 對每個物件進行計算
    for object_name in data.keys():
        S_u_i = 0  # 物件u_i成為概率天際線的概率

        # 遍歷該物件的所有實例
        for u_i_b, P_u_i_b, u_i_a in data[object_name]:
            product_term = 1  # ∏部分的計算結果

            # 遍歷其他物件
            for other_object, instances in data.items():
                if other_object != object_name:
                    sum_term = 0  # ∑部分的計算結果

                    # 遍歷其他物件的實例
                    for u_j_r, P_u_j_r, u_j_r_a in instances:
                        # 判斷是否優於u_i^a
                        if is_dominated(u_i_a, u_j_r_a):
                            sum_term += P_u_j_r

                    product_term *= (1 - sum_term)

            S_u_i += P_u_i_b * product_term

        probabilities[object_name] = S_u_i

    return probabilities

def save_probabilities_to_csv(probabilities, output_file_path):
    # 將計算結果轉換為DataFrame
    df = pd.DataFrame(list(probabilities.items()), columns=['Object', 'Probability'])
    # 保存到CSV檔案
    df.to_csv(output_file_path, index=False)
    print(f'Probabilities have been saved to {output_file_path}')

# 讀取CSV檔案
csv_file_path = "./data/"
file_name = 'D_object10000_instance3'  # 更改為您的CSV檔案路徑
data = read_data_from_csv(csv_file_path + file_name + '.csv')
# print(data)
# 計算並返回結果
probabilities = calculate_probabilities(data)
# 保存計算結果到CSV檔案
output_file_path = 'PSkytestResult/' + file_name + '_probabilities.csv'  # 指定輸出檔案的路徑
save_probabilities_to_csv(probabilities, output_file_path)
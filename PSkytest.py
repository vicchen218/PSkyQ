# Sliding window brute force PSky
import os, sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from itertools import product
import pandas as pd

# 提供的数据
# data1 = {
#     'A': [('a1', 0.6, [5, 3, 5, 4]), ('a2', 0.2, [3, 2, 4, 5]), ('a3', 0.2, [4, 3, 4, 4])],
#     'B': [('b1', 0.3, [3, 3, 3, 4]), ('b2', 0.4, [2, 3, 4, 3]), ('b3', 0.3, [3, 4, 3, 4])],
#     'C': [('c1', 0.5, [3, 2, 3, 3]), ('c2', 0.2, [2, 4, 4, 4]), ('c3', 0.3, [4, 3, 4, 3])]
# }


def read_data_from_csv(csv_file_path):
    # 从CSV文件读取数据
    df = pd.read_csv(csv_file_path)
    # 将DataFrame转换为所需的数据结构
    data = {}
    for _, row in df.iterrows():
        hotel = row['Hotel']
        instance_id = row['Instance']
        prob = row['Prob']
        attributes = [row['Amenities'], row['Location'], row['Price'], row['Service']]
        
        if hotel not in data:
            data[hotel] = []
        data[hotel].append((instance_id, prob, attributes))
    
    return data


# 判断实例u_j^r是否在所有属性上都优于u_i^a
def is_dominated(u_i_a, u_j_r_a):
    return all(a_j_r <= a_i for a_j_r, a_i in zip(u_j_r_a, u_i_a))

# 计算每个酒店成为概率天际线的概率
def calculate_probabilities(data):
    probabilities = {}

    # 对每个酒店进行计算
    for hotel in data.keys():
        S_u_i = 0  # 酒店u_i成为概率天际线的概率

        # 遍历该酒店的所有实例
        for u_i_b, P_u_i_b, u_i_a in data[hotel]:
            product_term = 1  # ∏部分的计算结果

            # 遍历其他酒店
            for other_hotel, instances in data.items():
                if other_hotel != hotel:
                    sum_term = 0  # ∑部分的计算结果

                    # 遍历其他酒店的实例
                    for u_j_r, P_u_j_r, u_j_r_a in instances:
                        # 判断是否优于u_i^a
                        if is_dominated(u_i_a, u_j_r_a):
                            sum_term += P_u_j_r

                    product_term *= (1 - sum_term)

            S_u_i += P_u_i_b * product_term

        probabilities[hotel] = S_u_i

    return probabilities


# 读取CSV文件
csv_file_path = 'hotel_data.csv'  # 更改为您的CSV文件路径
data = read_data_from_csv(csv_file_path)
# print(data)
# print(data == data1)
# 计算并返回结果

print(calculate_probabilities(data))

# if __name__ == '__main__':
#     print("")
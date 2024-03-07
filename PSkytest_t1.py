import pandas as pd

class PSky():
    def is_dominated(self,u_i_a, u_j_r_a):
        # 判斷實例u_j^r是否在所有屬性上都優於u_i^a
        return all(a_j_r <= a_i for a_j_r, a_i in zip(u_j_r_a, u_i_a))

    def calculate_probabilities(self,data):
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
                            if self.is_dominated(u_i_a, u_j_r_a):
                                sum_term += P_u_j_r

                        product_term *= (1 - sum_term)

                S_u_i += P_u_i_b * product_term

            probabilities[object_name] = S_u_i

        return probabilities


    def runFun(self, input_csv_file_name):
        # 讀取CSV檔案
        csv_file_path = "./data/"
        data = self.read_data_from_csv(csv_file_path + input_csv_file_name + '.csv')
        # 計算並返回結果
        probabilities = self.calculate_probabilities(data)
        print(probabilities)
        # 保存計算結果到CSV檔案

        #give values instand
        # output_file_path = 'PSkytestResult/' + input_csv_file_name + '_probabilities.csv'  # 指定輸出檔案的路徑
        # self.save_probabilities_to_csv(probabilities, output_file_path)

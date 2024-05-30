

class MyDebuger():
    def OutputDict(self, my_dict):
        print('\n=====================================')
        
        for key, value in my_dict.items():
            print(f"'{key}': {value},")
        print('======================================\n')
        
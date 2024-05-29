import csv
import random

def generate_csv(filename, object_count, instances_per_object, localName):
    # 動態生成列名
    fieldnames = ['Object']
    for i in range(1, instances_per_object + 1):
        fieldnames.extend([
            f'Instance{i}', f'Attribute1_{i}', f'Attribute2_{i}', f'Attribute3_{i}', f'Probability_{i}'
        ])
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for obj_index in range(1, object_count + 1):
            row_dict = {'Object': f'Object{obj_index}' + '_' + localName}
            total_probability = 0
            attribute1 = random.randint(1, 1000)
            attribute3_value = random.randint(1, 20) * 10
            for instance_index in range(1, instances_per_object + 1):
                if instance_index == instances_per_object:
                    probability = 1 - total_probability
                else:
                    probability = random.uniform(0, 1 - total_probability)
                total_probability += probability
                
                
                attribute2 = random.randint(-50, -1)
                
                row_dict.update({
                    f'Instance{instance_index}': f'Instance{instance_index}',
                    f'Attribute1_{instance_index}': attribute1,
                    f'Attribute2_{instance_index}': attribute2,
                    f'Attribute3_{instance_index}': attribute3_value,
                    f'Probability_{instance_index}': round(probability, 2),
                })
            
            writer.writerow(row_dict)

    print(f'File {filename} has been created.')

# Example usage:
# filename = input("Enter the desired filename (including .csv extension): ")
localName = input("Enter local name: ")
object_count = int(input("Enter object count: "))
instances_per_object = int(input("Enter instances per object: "))
folder_path = "./data/"
filename = folder_path + ( localName  + "_" + "object" + str(object_count) + "_instance" + str(instances_per_object)  + ".csv")


generate_csv(filename, object_count, instances_per_object, localName)

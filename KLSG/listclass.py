import os

# 类别映射字典
class_mapping = {
    0: "aircraft",
    1: "fish",
    2: "other",
    3:"shipwreck"
}

def count_classes_in_txt_files(directory):
    # 初始化统计字典
    class_counts = {class_name: 0 for class_name in class_mapping.values()}
    total_files = 0
    
    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            total_files += 1
            filepath = os.path.join(directory, filename)
            
            try:
                with open(filepath, 'r') as file:
                    # 读取文件的第一行
                    first_line = file.readline().strip()
                    if first_line:
                        # 提取第一个数字（类别）
                        parts = first_line.split()
                        if parts:
                            class_id = int(parts[0])
                            # 查找对应的类别名称
                            class_name = class_mapping.get(class_id, "unknown")
                            if class_name != "unknown":
                                class_counts[class_name] += 1
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
    
    # 打印结果
    print(f"all_num is {total_files}")
    print("Found classes:")
    for class_name, count in class_counts.items():
        if count > 0:  # 只显示有计数的类别
            print(f"{class_name}: {count}")

# 使用示例
directory_path = "/home/mazhe/KLSG/test/labels"
count_classes_in_txt_files(directory_path)
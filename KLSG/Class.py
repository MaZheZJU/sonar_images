import os

# 原索引到新索引的映射
label_map = {
    '0': '6',   # aircraft -> plane
    '1': None,  # fish -> 忽略
    '2': None,  # other -> 忽略
    '3': '10'   # shipwreck -> ship
}

# 标签目录
label_dir = "/home/mazhe/KLSG/valid/labels"

# 遍历所有 .txt 文件
for filename in os.listdir(label_dir):
    if not filename.endswith('.txt'):
        continue

    input_path = os.path.join(label_dir, filename)

    with open(input_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 5:
            continue  # 非法格式

        class_id = parts[0]
        new_class = label_map.get(class_id, None)
        if new_class is not None:
            new_line = ' '.join([new_class] + parts[1:]) + '\n'
            new_lines.append(new_line)
        # else 忽略该类

    # 覆盖保存
    with open(input_path, 'w') as f:
        f.writelines(new_lines)

print("✅ 标签替换完成，已忽略 fish/other 类别。")

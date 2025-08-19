import xml.etree.ElementTree as ET
import os

# 类别映射
class_mapping = {"aircraft": 6, "human": 4, "ship": 10}

def convert(size, box):
    dw, dh = 1./size[0], 1./size[1]
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w, h = box[1] - box[0], box[3] - box[2]
    return x*dw, y*dh, w*dw, h*dh

def convert_annotation(xml_path, txt_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    size = root.find('size')
    w, h = int(size.find('width').text), int(size.find('height').text)
    
    with open(txt_path, 'w') as f:
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in class_mapping:
                continue
            
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            f.write(f"{class_mapping[cls]} {' '.join(str(x) for x in bb)}\n")

# 遍历Annotations目录下所有XML文件
os.makedirs('labels', exist_ok=True)
for xml_file in os.listdir('annotations'):
    if xml_file.endswith('.xml'):
        image_id = os.path.splitext(xml_file)[0]
        convert_annotation(
            f'annotations/{xml_file}',
            f'labels/{image_id}.txt'
        )
import os
import shutil
import argparse

def clean_empty_labels(labels_dir, images_dir, backup=True, dry_run=False):
    """
    删除空标签文件及对应图片，可选择备份
    
    参数:
        labels_dir (str): 标签文件目录路径
        images_dir (str): 图片文件目录路径
        backup (bool): 是否备份被删除文件（默认True）
        dry_run (bool): 仅打印将要删除的文件而不实际执行（默认False）
    """
    # 创建备份目录（如果启用备份）
    backup_dir = os.path.join(os.path.dirname(labels_dir), "backup_deleted")
    if backup and not dry_run:
        os.makedirs(os.path.join(backup_dir, "labels"), exist_ok=True)
        os.makedirs(os.path.join(backup_dir, "images"), exist_ok=True)

    deleted_files = []
    
    # 遍历标签文件
    for label_file in os.listdir(labels_dir):
        if not label_file.endswith('.txt'):
            continue
            
        label_path = os.path.join(labels_dir, label_file)
        
        # 检查是否为空文件
        if os.path.getsize(label_path) == 0:
            # 获取对应的图片文件名（支持多种图片格式）
            image_base = os.path.splitext(label_file)[0]
            image_file = None
            for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                test_path = os.path.join(images_dir, image_base + ext)
                if os.path.exists(test_path):
                    image_file = image_base + ext
                    break
            
            if image_file:
                if dry_run:
                    print(f"[DRY RUN] 将删除: 标签 {label_file} -> 图片 {image_file}")
                else:
                    # 移动文件到备份目录（如果启用备份）
                    if backup:
                        shutil.move(label_path, os.path.join(backup_dir, "labels", label_file))
                        shutil.move(os.path.join(images_dir, image_file), 
                                   os.path.join(backup_dir, "images", image_file))
                    else:
                        os.remove(label_path)
                        os.remove(os.path.join(images_dir, image_file))
                    
                    deleted_files.append((label_file, image_file))
    
    # 输出报告
    print(f"\n操作完成！共删除 {len(deleted_files)} 个空标签及其对应图片")
    if deleted_files:
        print("\n被删除的文件对：")
        for label, image in deleted_files:
            print(f"  - 标签: {label} -> 图片: {image}")
        
        if backup and not dry_run:
            print(f"\n备份文件已保存到: {backup_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='删除空标签文件及对应图片')
    parser.add_argument('--labels', type=str, required=True, help='标签文件目录路径')
    parser.add_argument('--images', type=str, required=True, help='图片文件目录路径')
    parser.add_argument('--no-backup', action='store_false', dest='backup', 
                       help='禁用备份（直接永久删除）')
    parser.add_argument('--dry-run', action='store_true', 
                       help='试运行模式（仅显示将要删除的文件）')
    args = parser.parse_args()

    clean_empty_labels(
        labels_dir=args.labels,
        images_dir=args.images,
        backup=args.backup,
        dry_run=args.dry_run
    )
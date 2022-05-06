import os
import glob
import random
import shutil
from matplotlib import pyplot as plt
from PIL import Image

"""对所有图片讲行RGB转化，并且统一调整到一致大小，但不让图片发生变形或扭曲，划分了训练集和测试"""
if __name__ == '__main__':
    test_split_ratio = 0.05
    desired_size = 128  # 图片缩放后的统一大小
    raw_path = 'raw'
    # 找到该目录下所有文件（包括目录）
    dirs = glob.glob(os.path.join(raw_path, '*'))
    # 只要目录
    dirs = [d for d in dirs if os.path.isdir(d)]
    print(f'Totally {len(dirs)} classes: {dirs} ')
    for path in dirs:
        # 把前面的路径去掉，只要类别名
        path = path.split('\\')[-1]
        os.makedirs(f'train/{path}', exist_ok=True)
        os.makedirs(f'test/{path}', exist_ok=True)
        files = glob.glob(os.path.join(raw_path, path, '*.jpg'))
        files += glob.glob(os.path.join(raw_path, path, '*.JPG'))
        files += glob.glob(os.path.join(raw_path, path, '*.png '))

        random.shuffle(files)

        # 训练集和测试集边界
        boundary = int(len(files) * test_split_ratio)

        # 因为要用到i，所以要用enumerate这个枚举
        for i, file in enumerate(files):
            img = Image.open(file).convert('RGB')
            old_size = img.size  # old_size[0] is in (width,height) format
            ratio = float(desired_size) / max(old_size)

            # 实现等比例缩放
            new_size = tuple([int(x * ratio) for x in old_size])
            im = img.resize(new_size, Image.ANTIALIAS)
            new_im = Image.new("RGB", (desired_size, desired_size))
            new_im.paste(im, ((desired_size - new_size[0]) // 2,
                              (desired_size - new_size[1]) // 2))
            assert new_im.mode == 'RGB'
            if i <= boundary:
                new_im.save(os.path.join(f'test/{path}', file.split('\\')[-1].split('.')[0] + '.jpg'))
            else:
                new_im.save(os.path.join(f'train/{path}', file.split('\\')[-1].split('.')[0] + '.jpg'))
    test_files = glob.glob(os.path.join('test', '*', '*.jpg'))
    train_files = glob.glob(os.path.join('train', '*', '*.jpg'))
    print(f'Totally {len(train_files)} files for training')
    print(f'Totally {len(test_files)} files for test')

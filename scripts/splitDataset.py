def csvSpit():
    import pandas as pd
    from sklearn.model_selection import train_test_split

    # 读取原始CSV文件
    original_data = pd.read_csv('Dataset/remove_newline_reviews_single_col.csv')

    # 使用train_test_split函数将数据分成训练集和测试集
    train_data, test_data = train_test_split(original_data, test_size=0.2, random_state=42)

    # 将分割后的数据保存为两个CSV文件
    train_data.to_csv('Dataset/ali2-train.csv', index=False)
    test_data.to_csv('Dataset/ali2-test.csv', index=False)

    import random

    # 输入文本文件和输出训练集、测试集文件的文件名



def txtSplit():
    import random
    input_file = 'Dataset/txt/ali-complete.txt'
    train_file = 'Dataset/txt/ali-train.txt'
    test_file = 'Dataset/txt/ali-test.txt'
    # 打开输入文本文件并创建训练集和测试集文件
    with open(input_file, 'r') as input_txt, open(train_file, 'w') as train_txt, open(test_file, 'w') as test_txt:
        lines = input_txt.readlines()
        total_lines = len(lines)
        test_lines_count = int(0.2 * total_lines)  # 20% 的行数作为测试集

        # 随机选择测试集行
        test_lines = random.sample(lines, test_lines_count)

        for line in lines:
            if line in test_lines:
                # 写入测试集文件
                test_txt.write(line)
            else:
                # 写入训练集文件
                train_txt.write(line)

    print("处理完成，训练集文件为:", train_file)
    print("处理完成，测试集文件为:", test_file)

txtSplit()
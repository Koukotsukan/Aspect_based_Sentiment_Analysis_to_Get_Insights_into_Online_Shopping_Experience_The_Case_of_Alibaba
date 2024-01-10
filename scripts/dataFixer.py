import csv

def process_csv(file_name):
    with open(file_name, 'r') as file:
        data = list(csv.reader(file))
    i = 0
    while i < len(data):
        sentence = data[i][0].replace('$T$', data[i+1][0])
        if i > 0 and data[i-3][0] == data[i][0]:
            print('A情况:')
            print('全文: ', sentence)
            print('全文split()后的列表: ', sentence.split())
            print('第二行和第三行: ', data[i+1:i+3])
        else:
            print('非A情况:')
            print('全文: ', sentence)
            print('第二行和第三行: ', data[i+1:i+3])
        add = input('是否添加? (y/n): ')
        while add.lower() == 'y':
            index = int(input('请输入A sentence.split()的index: '))
            temp_sentence = sentence.split()
            temp_word = temp_sentence[index]
            temp_sentence[index] = '$T$'
            sentiment = input('请输入sentiment polarity ("["表示"Positive", "]"表示"Negative"): ')
            sentiment = 'Positive' if sentiment == '[' else 'Negative'
            new_data = [' '.join(temp_sentence), temp_word, sentiment]
            data.insert(i, new_data)
            add = input('是否继续添加? (y/n): ')
        i += 3
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

process_csv('Dataset/test/ali2-train.csv')

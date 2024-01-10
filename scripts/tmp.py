# 输入包含两行文本
input_text1 = input("请输入第一行文本:\n")
input_text2 = input("请输入第二行文本:\n")

# 合并两行文本
input_text = input_text1 + "\n" + input_text2
input_text = input_text.replace("$T$", input_text2)

# 按换行符分割输入文本
input_lines = input_text.strip().split('\n')

if len(input_lines) == 2:
    # 提取两行文本
    text = input_lines[0]
    replacement_word = input_lines[1]

    # 将文本分割成单词并添加索引
    words = text.split()
    words_with_index = [(word, index) for index, word in enumerate(words)]

    # 打印每个词和其索引
    print("文章全文段落:")
    # 创建一个空列表来存储带有索引的词语
    wordZ = []

    for word, index in words_with_index:
        # 将带有索引的词语添加到列表中
        wordZ.append(word + str(index))

    # 以段落并在词语之间添加空格的方式构建输出
    output_paragraphs = [' '.join(wordZ[i:i + 5]) for i in range(0, len(wordZ), 5)]

    # 打印包含词语和索引的段落
    for paragraph in output_paragraphs:
        print(paragraph)
    # 请求你输入要替代第二行词语的词的索引

    # 请求你输入要替代第二行词语的词的索引
    index_to_replace = int(input("请输入要替代第二行词语的词的索引: "))

    if 0 <= index_to_replace < len(words_with_index):
        # 获取要替代的词
        word_to_replace, index_to_replace = words_with_index[index_to_replace]

        # 替换第二行的词语
        words[index_to_replace] = '$T$'

        # 输出最终文本和第二行词语
        text = ' '.join(words)
        print(text)
        print(word_to_replace+"\nPositive")
        print('-----UP PO  DN NE-----')
        print(text )
        print(word_to_replace+ "\nNegative")
    else:
        print("无效的索引。请输入有效的索引。")
else:
    print("输入应包含两行文本。")

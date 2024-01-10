from pyabsa import AspectTermExtraction as ATEPC
from collections import Counter
import csv

# atepc_examples = 'Dataset/ali2-test.csv'
aspect_extractor = ATEPC.AspectExtractor(
    checkpoint="checkpoints/fast_lcf_atepc_custom_dataset_cdw_apcacc_91.06_apcf1_91.07_atef1_83.09",
    auto_device=True,
    cal_perplexity=True,
    save_result=True,
    print_result=True

)


result = aspect_extractor.batch_predict(
    target_file='Dataset/ali-train.csv',
    save_result=True,
    # save_result=False,
    print_result=True,
    pred_sentiment=True,
)
# result = aspect_extractor.predict(
#     text="I love to use Alibaba. But I hate their items",
#     # save_result=True,
#     save_result=False,
#     print_result=True,
#     pred_sentiment=True,
# )

print(result)
# 提取Aspect term和Sentiment并生成频率表
aspect_sentiment_pairs = [(item['aspect_term'], item['sentiment']) for item in result]
frequency_table = Counter(aspect_sentiment_pairs)

# 保存为CSV文件
with open('frequency_table.csv', 'w', newline='') as csvfile:
    fieldnames = ['Aspect Term', 'Sentiment', 'Frequency']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for pair, freq in frequency_table.items():
        writer.writerow({'Aspect Term': pair[0], 'Sentiment': pair[1], 'Frequency': freq})
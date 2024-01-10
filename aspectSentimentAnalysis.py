import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns


def generateAspectSentimentCSV():
    # Read JSON data from file
    json_file_path = "Alibaba_Result.json"  # Replace with the path to your JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Extract data
    results = []

    for item in data:
        aspects = item.get("aspect", [])
        sentiments = item.get("sentiment", [])

        for aspect, sentiment in zip(aspects, sentiments):
            results.append({"Aspect": aspect, "Sentiment": sentiment})

    # Write to CSV file
    csv_file_path = "Alibaba_Analysis.csv"
    fieldnames = ["Aspect", "Sentiment"]

    with open(csv_file_path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data
        for result in results:
            writer.writerow(result)

    print(f"CSV file generated: {csv_file_path}")


def read_csv(file_path):
    return pd.read_csv(file_path)


def filter_by_sentiment(df, sentiment):
    return df[df['Sentiment'] == sentiment]


def generate_csv(data, filename):
    data.to_csv(filename, index=False)


def generate_word_cloud(data, title, color_map=None):
    if color_map:
        color_func = lambda word, font_size, position, orientation, random_state, **kwargs: color_map[word]
    else:
        color_func = None

    wordcloud_data = data['Aspect'].str.cat(sep=' ')
    wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False,
                          color_func=color_func).generate(wordcloud_data.lower())
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.show()


def generate_histogram(data, title, color):
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Frequency', y='Aspect', data=data, color=color)  # Use color directly instead of palette
    plt.xlabel('Frequency')
    plt.ylabel('Aspect')
    plt.title(title)
    plt.show()


# generateAspectSentimentCSV()
# 读取CSV文件
csv_file_path = "Alibaba_Analysis.csv"  # 替换为你的CSV文件路径
df = read_csv(csv_file_path)

# # 1. 统计Positive Sentiments中相同Aspect出现的频次，生成Positive_Aspect.csv
# positive_data = filter_by_sentiment(df, 'Positive')['Aspect'].str.lower().value_counts().reset_index()
# positive_data.columns = ['Aspect', 'Frequency']
# generate_csv(positive_data.head(20), 'Top20_Positive_Aspect.csv')
positive_data = read_csv("Positive_Aspect.csv")
generate_csv(positive_data.head(20), 'Top20_Positive_Aspect.csv')
generate_histogram(positive_data.head(20), 'Top 20 Aspects - Positive Sentiment', 'green')

# # 2. 统计Negative Sentiments中相同Aspect出现的频次，生成Negative_Aspect.csv
# negative_data = filter_by_sentiment(df, 'Negative')['Aspect'].str.lower().value_counts().reset_index()
# negative_data.columns = ['Aspect', 'Frequency']
negative_data = read_csv("Negative_Aspect.csv")
generate_csv(negative_data.head(20), 'Top20_Negative_Aspect.csv')
generate_histogram(negative_data.head(20), 'Top 20 Aspects - Negative Sentiment', 'red')

# # 3. 统计Neutral Sentiments中相同Aspect出现的频次，生成Neutral_Aspect.csv
neutral_data = filter_by_sentiment(df, 'Neutral')['Aspect'].str.lower().value_counts().reset_index()
neutral_data.columns = ['Aspect', 'Frequency']
generate_csv(neutral_data.head(20), 'Top20_Neutral_Aspect.csv')
generate_histogram(neutral_data.head(20), 'Top 20 Aspects - Neutral Sentiment', 'gray')

# 4. 统计所有Aspect，按照频次给Aspect排序，生成Aspect_Frequency.csv
all_aspects_data = df['Aspect'].str.lower().value_counts().reset_index()
all_aspects_data.columns = ['Aspect', 'Frequency']
generate_csv(all_aspects_data, 'Aspect_Frequency.csv')

import matplotlib.pyplot as plt


# ... (Previous code remains unchanged)

def generate_sentiment_pie_chart(df):
    # Calculate the proportion of each sentiment
    sentiment_counts = df['Sentiment'].value_counts()
    labels = sentiment_counts.index
    sizes = sentiment_counts.values

    # Plot the pie chart
    colors = ['green', 'red', 'gray']
    explode = (0.1, 0, 0)  # Explode the first slice (Positive)

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, explode=explode)
    plt.title('Proportion of Sentiments')

    # Draw circle to create a donut chart
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.show()


# ... (Previous code remains unchanged)

# Generate the pie chart for the proportion of each sentiment
generate_sentiment_pie_chart(df)

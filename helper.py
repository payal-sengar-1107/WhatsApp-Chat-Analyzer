from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter

extract = URLExtract()


# 1. Stats nikalne ke liye
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['messages']:
        words.extend(message.split())

    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):

    df = df[df['users'] != 'group_notification']
    x = df['users'].value_counts().head()
    df_percent = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'users': 'percent'}
    )
    return x, df_percent

def remove_stop_words(message):
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read()
    y = []
    for word in str(message).lower().split():
        if word not in stop_words:
            y.append(word)
    return " ".join(y)

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # Filtering out system notifications and media tags
    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    temp = temp[temp['messages'] != '<media omitted>\n']

    # Applying stop words removal
    temp['messages'] = temp['messages'].apply(remove_stop_words)

    # Generating the wordcloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')

    text_data = temp['messages'].str.cat(sep=" ").strip()
    if not text_data:
        text_data = "No_Messages_Found"

    df_wc = wc.generate(text_data)

    # Creating the plot and removing the axis numbers (0, 100, 200)
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(df_wc)
    plt.axis("off")  # 👈 This line removes the unwanted numbers and border lines

    return fig


def most_common_words(selected_user, df):
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)
    return user_heatmap



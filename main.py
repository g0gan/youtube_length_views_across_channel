import os
import googleapiclient.discovery
import csv
from pytube import YouTube

# api key here
API_KEY = 'was here'

# Инициализируем YouTube Data API клиент
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

def get_channel_videos(channel_id):
    videos = []
    next_page_token = None

    # Получаем видеоролики канала
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        maxResults=5,  # Берем только 5 последних видео
        pageToken=next_page_token,
        type='video'
    )
    response = request.execute()

    # get all url's to list
    for item in response['items']:
        videos.append('https://www.youtube.com/watch?v=' + item['id']['videoId'])

    return videos

def save_videos_to_file(videos, filename='videos.txt'):
    with open(filename, 'w') as file:
        for video in videos:
            file.write(video + '\n')

# Функция для получения данных о видео
def get_video_info(video_url):
    yt = YouTube(video_url)
    title = yt.title
    length_seconds = yt.length
    length_minutes = length_seconds // 60  # Переводим секунды в минуты
    views = yt.views
    return title, length_minutes, views

# Функция для чтения ссылок из файла и получения данных о видео для каждой ссылки
def parse_links_from_file(input_file, output_file):
    with open(input_file, 'r') as f_in:
        links = [line.strip() for line in f_in.readlines()]

    results = []
    for link in links:
        title, length_minutes, views = get_video_info(link)
        results.append({'link': link, 'title': title, 'length': length_minutes, 'views': views})

    with open(output_file, 'w', newline='', encoding='utf-8') as f_out:
        fieldnames = ['link', 'title', 'length', 'views']
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

if __name__ == '__main__':
    channel_id = 'id_was_here'  # choose id channel here, you can find channel ID by using this service https://ytlarge.com/youtube/channel-id-finder/ 
    videos = get_channel_videos(channel_id)
    save_videos_to_file(videos)
    
    input_file = 'videos.txt'  # Файл с URL-ами видео
    output_file = 'output_results.csv'  # Файл для сохранения результатов

    parse_links_from_file(input_file, output_file)
    print('Парсинг завершен. Результаты сохранены в файле output_results.csv')

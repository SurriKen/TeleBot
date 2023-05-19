import gdown
import requests
from urllib.parse import urlencode
from pytube import YouTube


def load_video_from_yandex_disc(public_key: str, save_path: str = 'temp/video.mp4'):
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'

    # Получаем загрузочную ссылку
    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']

    # Загружаем файл и сохраняем его
    download_response = requests.get(download_url)
    with open(save_path, 'wb') as f:  # Здесь укажите нужный путь к файлу
        f.write(download_response.content)


def load_video_from_google_drive(google_drive_link: str, google_api: str, save_path: str = 'temp/video.mp4'):
    """
    [Guide] How to Quickly Download Large Files from Google Drive
    https://cleandrive.app/download-large-files-drive/

    :param folder_id:
    :param google_api:
    :param save_path:
    :return:
    """
    # [Guide] How to Quickly Download Large Files from Google Drive
    # https://cleandrive.app/download-large-files-drive/

    # folder which want to download from Drive
    # folder_id = '1mo0mMvPYw6ttRbvP5larXwt0yMQCM0wV'
    # google_api = 'AIzaSyCUto8qWyQQluo-PN4PlhVzh_IidC8PHDY'
    file_id = google_drive_link.split('/')[-2]
    url = f'https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key={google_api}'
    # d.downloadFile(fileId=folder_id, filePath=output_directory)
    gdown.download(url, save_path, quiet=False)


def load_video_from_youtube(link, save_path: str = 'temp/', filename='video.mp4'):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download(output_path=save_path, filename=filename)
        return True, "Successfully downloaded video"
    except Exception as err:
        return False, f"An error has occurred during downloading: {err}"


# gdisk = 'https://drive.google.com/file/d/1mo0mMvPYw6ttRbvP5larXwt0yMQCM0wV/view?usp=sharing'
# gphoto = 'https://photos.google.com/photo/AF1QipP30--t168Nfz4v6rLQ1c089rnUFAnKS3iM85sB'
# ydisc = 'https://disk.yandex.ru/i/iuGA8ffxn2e4CQ'
# download_file_from_google_drive(
#     google_drive_link=gdisk,
#     google_api='AIzaSyCUto8qWyQQluo-PN4PlhVzh_IidC8PHDY',
# )

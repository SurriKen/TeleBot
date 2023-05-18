from zdrive import Downloader
import gdown

gdisk = 'https://drive.google.com/file/d/1mo0mMvPYw6ttRbvP5larXwt0yMQCM0wV/view?usp=share_link'

output_directory = "temp/vid.mp4"

# [Guide] How to Quickly Download Large Files from Google Drive
# https://cleandrive.app/download-large-files-drive/

# folder which want to download from Drive
folder_id = '1mo0mMvPYw6ttRbvP5larXwt0yMQCM0wV'
google_api = 'AIzaSyCUto8qWyQQluo-PN4PlhVzh_IidC8PHDY'
url = f'https://www.googleapis.com/drive/v3/files/{folder_id}?alt=media&key={google_api}'
# d.downloadFile(fileId=folder_id, filePath=output_directory)
gdown.download(url, output_directory, quiet=False)
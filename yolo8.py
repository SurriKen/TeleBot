import colorsys
import random
import shutil

import requests
from torchvision.utils import draw_bounding_boxes
import numpy as np
import torch
import torchvision
from ultralytics import YOLO
import os
import wget
import requests
from urllib.parse import urlencode


class YOLOv8:

    def __init__(self, weights_path: str = ''):
        if weights_path:
            self.model = YOLO(weights_path)
        else:
            if not os.path.isfile('yolov8n.pt'):
                self.load_weights()
            self.model = YOLO('yolov8n.pt')
        self.message = ''
        self.status = True


    @staticmethod
    def load_weights():
        # if not os.path.isdir('yolov8n.pt'):
        url = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
        wget.download(url, 'yolov8n.pt')

    @staticmethod
    def get_colors(name_classes: list):
        length = 10 * len(name_classes)
        hsv_tuples = [(x / length, 1., 1.) for x in range(length)]
        colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))
        random.shuffle(colors)
        return colors[:len(name_classes)]

    @staticmethod
    def get_coords_from_predict(predict) -> list:
        coords = []
        if len(predict[0].boxes):
            for i, det0 in enumerate(predict[0].boxes):
                *xyxy0, conf0, cls0 = det0.boxes.tolist()[0]
                xyxy0 = [int(x) for x in xyxy0]
                if xyxy0:
                    xyxy0.extend([conf0, int(cls0)])
                    coords.append(xyxy0)
        return coords

    @staticmethod
    def put_box_on_image(save_path: str, results, labels: list, color_list: list, coordinates: list) -> None:
        image = results[0].orig_img[:, :, ::-1].copy()
        image = np.transpose(image, (2, 0, 1))
        w, h = image.shape[:2]
        image = torch.from_numpy(image)
        coord = []
        for box in coordinates:
            coord.append([
                int(box[0]),
                int(box[1]),
                int(box[2]),
                int(box[3]),
            ])
        bbox = torch.tensor(coord, dtype=torch.int)
        if bbox.tolist():
            image_true = draw_bounding_boxes(
                image, bbox, width=3, labels=labels, colors=color_list, fill=True, font='arial.ttf',
                font_size=int(h * 0.05))
            image = torchvision.transforms.ToPILImage()(image_true)
        else:
            image = torchvision.transforms.ToPILImage()(image)
        image.save(f'{save_path}')


    def detect_image(self, image_path, save_path='temp/predict.jpg'):

        # Get names and colors
        names = list(self.model.model.names.values())
        colors = self.get_colors(names)

        res = self.model(image_path)
        coords = self.get_coords_from_predict(res)

        if coords:
            labels = [
                f"# {i+1} {self.model.model.names[coords[i][-1]]} {coords[i][-2]:0.2f}"
                for i in range(len(coords))
            ]

            if len(labels) > 1:
                cl = colors * len(labels)
            else:
                cl = colors

            self.put_box_on_image(
                save_path=save_path,
                results=res,
                labels=labels,
                color_list=cl,
                coordinates=coords
            )
            self.message = 'There is some objects on the image\n'
            for lbl in labels:
                self.message = f"{self.message}{lbl}\n"

            self.status = True
        else:
            shutil.copy2(image_path, 'temp/predict.jpg')
            self.message = "No object was found"
            self.status = False


    def detect_video(self, video_path, save_path='temp/predict.mp4'):
        self.model.predict(source=video_path, save=True)
        vid_name = video_path.split('/')[-1]
        shutil.copy2(src=f'runs/detect/predict/{vid_name}', dst=save_path)
        shutil.rmtree('runs')
        self.message = 'Video detection is finished'
        self.status = True


if __name__ == "__main__":
    link = 'https://disk.yandex.ru/i/iuGA8ffxn2e4CQ'
    save = 'temp/big_video.mp4'

    import requests
    from urllib.parse import urlencode

    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    public_key = link  # Сюда вписываете вашу ссылку
    google_url = "https://docs.google.com/uc?export=download"
    google_key = 'https://photos.google.com/photo/AF1QipP30--t168Nfz4v6rLQ1c089rnUFAnKS3iM85sB'

    # Получаем загрузочную ссылку
    final_url = google_url + urlencode(dict(public_key=google_key))
    response = requests.get(final_url)
    download_url = response.json()['href']

    # Загружаем файл и сохраняем его
    download_response = requests.get(download_url)
    with open(save, 'wb') as f:  # Здесь укажите нужный путь к файлу
        f.write(download_response.content)

    # model = YOLOv8()
    # model.detect_video(video_path='video.mp4')

import numpy as np
import secrets
from cv2 import cv2
from Utils.Utils import make_cache_dir, remove_extension


class ImageProcessor:
    def __init__(self):
        self.result_images = None
        make_cache_dir()

    def process(self):
        out_image_names = []
        for img in self.result_images:
            hash_name = f'./caches/{secrets.token_urlsafe(16)}.jpg'
            if not cv2.imwrite(hash_name, img):
                raise Exception('Failed to create image')
            out_image_names.append(remove_extension(hash_name))
        return out_image_names

    def from_binary_list(self, binary_list):
        image_list = [self.__binary_to_image(binary.read()) for binary in binary_list]
        self.result_images = self.__concat_and_split_images(image_list)
        return self

    def __concat_and_split_images(self, images: []):
        concated_img = np.vstack(images)
        img_height = concated_img.shape[0]
        splited_imgs = []
        for i in range(4):
            splited_imgs.append(concated_img[int(img_height * i / 4):int(img_height * (i + 1) / 4), ])

        return splited_imgs

    def __binary_to_image(self, binary):
        encoded_img = np.fromstring(binary, dtype=np.uint8)
        return cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

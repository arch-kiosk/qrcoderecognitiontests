from image_manipulation.imagemanipulationstrategy import ImageManipulationStrategy
from PIL import Image
import numpy as np


class PillowManipulationComposition(ImageManipulationStrategy):

    def __init__(self, name: str, debug=False):
        super().__init__(name=name, debug=debug)

    def _save_image(self, img):
        img.save(self.dest_file_name)

    def _open(self, src_file: str):
        return Image.open(src_file)

    def _isnull(self, img):
        return img is None

    def _to_np_array(self, img):
        return np.array(img, dtype=np.uint8)

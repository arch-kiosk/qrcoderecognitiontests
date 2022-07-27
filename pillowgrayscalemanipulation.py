from PIL.Image import Image

from pillowimagemanipulation import PillowImageManipulation


class PillowGrayScaleManipulation(PillowImageManipulation):
    def execute_manipulation(self, image: Image) -> Image:

        return image.convert("L")

    def get_parameters(self):
        return ["gray",]


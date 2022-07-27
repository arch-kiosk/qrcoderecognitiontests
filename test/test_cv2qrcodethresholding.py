import logging
import os

import pytest

import kioskstdlib
from image_manipulation.cv2qrcodethresholding import CV2QrCodeThresholding

test_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(test_dir, "config", "urap_dev.log")


class TestCV2QrCodeThresholding:

    @pytest.fixture(scope="module")
    def log(self):
        # Initialize logging and settings
        logging.basicConfig(format='>[%(module)s.%(levelname)s at %(asctime)s]: %(message)s', level=logging.ERROR)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        if log_file:
            ch = logging.FileHandler(filename=log_file)
            ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter('>[%(module)s.%(levelname)s at %(asctime)s]: %(message)s')
            ch.setFormatter(formatter)
            logger.addHandler(ch)
            logging.info("Logging....")

    def test_init(self, log):
        strategy = CV2QrCodeThresholding("thresholding_63_1", {"block_size": 63})
        assert strategy
        assert strategy.manipulation_list[0].__class__.__name__ == "CV2AdaptiveThresholdManipulation"

        strategy = CV2QrCodeThresholding("thresholding_0.5_7_63_1", {"block_size": 63,
                                                                     "scale_factor": .5,
                                                                     "blur": 6
                                                                     })
        assert strategy
        assert strategy.manipulation_list[0].__class__.__name__ == "CV2ScaleManipulation"
        assert strategy.manipulation_list[1].__class__.__name__ == "CV2BlurManipulation"
        assert strategy.manipulation_list[2].__class__.__name__ == "CV2AdaptiveThresholdManipulation"

        strategy = CV2QrCodeThresholding("thresholding_0.5_7_63_1", {"block_size": 63,
                                                                     "scale_factor": 1.0,
                                                                     "blur": 0
                                                                     })
        assert strategy
        assert strategy.manipulation_list[0].__class__.__name__ == "CV2AdaptiveThresholdManipulation"

    def test_execute(self, log):
        parent_dir = kioskstdlib.get_parent_dir(test_dir)
        qrcode_file = os.path.join(parent_dir, "data", "DSC_1211.jpg")
        strategy = CV2QrCodeThresholding("thresholding_33_1", {"block_size": 63})
        assert strategy.execute(qrcode_file)
        assert strategy.get_result_np_array().size > 0

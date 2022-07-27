import logging
import os

import pytest
from image_manipulation.imagemanipulationstrategyfactory import ImageManipulationStrategyFactory
from sync_config import SyncConfig
from test.testhelpers import KioskPyTestHelper

test_dir = os.path.dirname(os.path.abspath(__file__))

this_test_dir = test_dir
config_file = os.path.join(this_test_dir, "config", "config_kiosk_qrcoderecognitiontests.yml")
log_file = os.path.join(test_dir, "log", "test.log")


class TestImageManipulationStrategyFactory(KioskPyTestHelper):

    @pytest.fixture()
    def sync_config(self, shared_datadir):
        cfg = self.get_config(config_file, log_file)
        self.set_file_repos_dir(cfg, shared_datadir)
        return cfg

    def test_create_from_dict(self, sync_config):
        strategy = ImageManipulationStrategyFactory.create_from_dict("cv2_qrcode_thresholding_0.5_63_7",
                                                                     {
                                                                         "type": "CV2QrCodeThresholding",
                                                                         "scale_factor": 0.5,
                                                                         "block_size": 63,
                                                                         "blur": 7,
                                                                     }
                                                                     )
        assert strategy
        assert strategy.manipulation_list[0].__class__.__name__ == "CV2ScaleManipulation"
        assert strategy.manipulation_list[1].__class__.__name__ == "CV2BlurManipulation"
        assert strategy.manipulation_list[2].__class__.__name__ == "CV2AdaptiveThresholdManipulation"

    def test_get_image_manipulation_config(self, sync_config):
        ImageManipulationStrategyFactory._get_image_manipulation_config()
        assert ImageManipulationStrategyFactory._image_manipulation_config
        assert "strategies" in ImageManipulationStrategyFactory._image_manipulation_config

    def test_create_from_config(self, sync_config):
        strategy = ImageManipulationStrategyFactory.create_from_config("cv2_qrcode_thresholding_0.5_63_0")
        assert strategy
        assert strategy.manipulation_list[0].__class__.__name__ == "CV2ScaleManipulation"
        assert strategy.manipulation_list[1].__class__.__name__ == "CV2AdaptiveThresholdManipulation"

        strategy = ImageManipulationStrategyFactory.create_from_config("cv2_qrcode_thresholding_0.5_63_7")
        assert strategy
        assert strategy.manipulation_list[0].__class__.__name__ == "CV2ScaleManipulation"
        assert strategy.manipulation_list[1].__class__.__name__ == "CV2BlurManipulation"
        assert strategy.manipulation_list[2].__class__.__name__ == "CV2AdaptiveThresholdManipulation"

        strategy = ImageManipulationStrategyFactory.create_from_config("cv2_qrcode_thresholding_1.0_33_0")
        assert strategy
        assert strategy.manipulation_list[0].__class__.__name__ == "CV2AdaptiveThresholdManipulation"

    def test_get_image_manipulation_set_descriptors(self, sync_config):
        sets = ImageManipulationStrategyFactory.get_image_manipulation_set_descriptors()
        assert sets
        for a_set in sets:
            assert a_set["id"] in ["qr_code_sahara", "qr_code_black_velvet"]
            if a_set["id"] == "qr_code_sahara":
                assert a_set["name"] == "QR Coded Sahara"
                assert a_set["description"] == "Use this strategy to make QR Codes recognizable in " \
                                             "a typical desert surrounding"

    def test_image_manipulation_set_strategies(self, sync_config):
        strategies = ImageManipulationStrategyFactory.image_manipulation_set_strategies("qr_code_sahara")
        assert strategies
        assert next(iter(strategies)).name == "cv2_qrcode_thresholding_0.5_63_0"
        assert next(iter(strategies)).name == "cv2_qrcode_thresholding_0.5_33_0"
        assert next(iter(strategies)).name == "cv2_qrcode_thresholding_0.5_63_7"
        assert next(iter(strategies)).name == "cv2_qrcode_thresholding_0.5_33_7"
        assert next(iter(strategies)).name == "cv2_qrcode_thresholding_1.0_33_0"
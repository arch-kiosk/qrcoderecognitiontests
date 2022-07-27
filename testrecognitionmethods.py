import datetime
import logging
import os
import sys
import kioskstdlib
from image_manipulation.directoryfilesource import DirectoryFileSource
from pillowmanipulationcomposition import PillowManipulationComposition
from fileimportqrcodefilter.qrcodetester import QRCodeTester
from pillowgrayscalemanipulation import PillowGrayScaleManipulation
from pillowthresholdmanipulation import PillowThresholdManipulation
from pillowbitplanemanipulation import PillowBitplaneManipulation
from pillowhistogramequalization import PillowHistogramEqualization
from image_manipulation.cv2manipulationcomposition import CV2ManipulationComposition
from image_manipulation.cv2scalemanipulation import CV2ScaleManipulation
from image_manipulation.cv2adaptivethresholdmanipulation import CV2AdaptiveThresholdManipulation
from image_manipulation.cv2blurmanipulation import CV2BlurManipulation

test_path = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(test_path, r"config", "urap_test_config.yml")
log_file = os.path.join(test_path, r"log", "test_log.log")

report_file = None


def usage():
    print("usage: testrecognitionmethods ")


def init_log():
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


def _report(qrcode_file: str, strategy_name: str, data, success: str):
    print(f"{datetime.datetime.now()}: {kioskstdlib.get_filename(qrcode_file)}, {strategy_name}, {success}, {data}")
    if report_file:
        report_file.write(
            f"{datetime.datetime.now()};{kioskstdlib.get_filename(qrcode_file)};{strategy_name};{success};{data}\n")


def thresholding_strategy():
    strategy = PillowManipulationComposition(f"grayscale, brightness + 10%, auto-threshold")
    # strategy.append_manipulation(PillowGrayScaleManipulation())
    # # strategy.append_manipulation(PillowContrastManipulation(enhance=0.9))
    # strategy.append_manipulation(PillowBrightnessManipulation(enhance=1.2))
    # strategy.append_manipulation(PillowThresholdManipulation(threshold=-1))
    # qrcode_tester.register_strategy(strategy)
    for threshold in [30, 40, 50, 60, 70, 80, 90]:
        for scale in [0.3]:
            strategy = PillowManipulationComposition(f"grayscale[threshold={threshold}]")
            # strategy.append_manipulation(PillowScaleManipulation(scalefactor=scale))
            strategy.append_manipulation(PillowGrayScaleManipulation())
            # strategy.append_manipulation(PillowContrastManipulation(enhance=0.9))
            # strategy.append_manipulation(PillowBrightnessManipulation(enhance=1.1))
            strategy.append_manipulation(PillowThresholdManipulation(threshold=threshold))
            strategy.debug = True
            qrcode_tester.register_strategy(strategy)


def bitplane_strategy():
    bitmasks = [255 ^ bits for bits in [8 + 64 + 128, 32 + 64 + 128, 64 + 128, 32 + 64, 16 + 32 + 64]]
    for mask in bitmasks:
        strategy = PillowManipulationComposition(f"bitplane_{mask}")
        strategy.append_manipulation(PillowGrayScaleManipulation())
        strategy.append_manipulation(PillowBitplaneManipulation(bitmask=mask))
        qrcode_tester.register_strategy(strategy)


def histogram_equalization_strategy():
    strategy = PillowManipulationComposition(f"equalization")
    strategy.append_manipulation(PillowGrayScaleManipulation())
    strategy.append_manipulation(PillowHistogramEqualization())
    # strategy.debug = True
    qrcode_tester.register_strategy(strategy)


def cv2_priority_thresholding():
    priorities = [
        (0.5, 63, 0),
        (0.5, 33, 0),
        (0.5, 63, 7),
        (0.3, 63, 0),
        (0, 33, 0),
        (0.5, 13, 0),
        (0.5, 33, 7),
    ]
    for scale_factor, block_size, blur_factor in priorities:
        strategy = CV2ManipulationComposition(
            f"cv2_thresholding_{scale_factor}_{blur_factor}_{block_size}")
        if scale_factor != 0:
            strategy.append_manipulation(CV2ScaleManipulation(scale_factor=scale_factor))
        if blur_factor != 0:
            strategy.append_manipulation(CV2BlurManipulation(blur_factor=blur_factor))
        strategy.append_manipulation(CV2AdaptiveThresholdManipulation(block_size=block_size, c=1))
        qrcode_tester.register_strategy(strategy)


def cv2_priority_thresholding_objects():
    priorities = [
        (0.3, 63, 0),
        (0.3, 63, 7),
        (0.5, 73, 0),
        (0.3, 63, 0),
    ]
    for scale_factor, block_size, blur_factor in priorities:
        strategy = CV2ManipulationComposition(
            f"cv2_thresholding_{scale_factor}_{blur_factor}_{block_size}")
        if scale_factor != 0:
            strategy.append_manipulation(CV2ScaleManipulation(scale_factor=scale_factor))
        if blur_factor != 0:
            strategy.append_manipulation(CV2BlurManipulation(blur_factor=blur_factor))
        strategy.append_manipulation(CV2AdaptiveThresholdManipulation(block_size=block_size, c=1))
        qrcode_tester.register_strategy(strategy)


def cv2_thresholding():
    for c in [1]:
        for blur_factor in [0, 7, 5, 3, 9, 11]:
            for scale_factor in [0.5, 0, 0.3, 0.7]:
                for block_size in [63, 33, 13, 53, 23, 63, 73]:
                    strategy = CV2ManipulationComposition(
                        f"cv2_thresholding_{scale_factor}_{blur_factor}_{block_size}_{c}")
                    if scale_factor != 0:
                        strategy.append_manipulation(CV2ScaleManipulation(scale_factor=scale_factor))
                    if blur_factor != 0:
                        strategy.append_manipulation(CV2BlurManipulation(blur_factor=blur_factor))
                    strategy.append_manipulation(CV2AdaptiveThresholdManipulation(block_size=block_size, c=c))
                    qrcode_tester.register_strategy(strategy)
    # strategy.debug = True


def cv2_thresholding_isolated():
    for c in [1]:
        for blur_factor in [0]:
            for scale_factor in [0]:
                for block_size in [33, 31, 27, 25, 23, 21, 17, 13]:
                    strategy = CV2ManipulationComposition(
                        f"cv2_thresholding_{scale_factor}_{blur_factor}_{block_size}_{c}")
                    if scale_factor != 0:
                        strategy.append_manipulation(CV2ScaleManipulation(scale_factor=scale_factor))
                    if blur_factor != 0:
                        strategy.append_manipulation(CV2BlurManipulation(blur_factor=blur_factor))
                    strategy.append_manipulation(CV2AdaptiveThresholdManipulation(block_size=block_size, c=c))
                    qrcode_tester.register_strategy(strategy)
    # strategy.debug = True


if __name__ == '__main__':
    options = {}
    init_log()
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) > 1:
        usage()
    # dfs = DirectoryFileSource(os.path.join(test_path, "test", "data", "qr_codes", "objects"))
    # dfs = DirectoryFileSource(os.path.join(test_path, "test", "data", "2ndstage"))
    dfs = DirectoryFileSource(os.path.join(test_path, "test", "data", "isolate"))
    # dfs = DirectoryFileSource(os.path.join(test_path, "test", "data"))
    # dfs = DirectoryFileSource(os.path.join(test_path, "test", "data","qr_codes","objects"))
    dst_path = os.path.join(dfs.path_name, kioskstdlib.get_directory_name_from_datetime())
    os.makedirs(dst_path)
    print(f"dest-path: {dst_path}")
    log_path_and_filename = os.path.join(dst_path,
                                         "qrcodelog_" + kioskstdlib.get_directory_name_from_datetime() + ".log")
    with open(log_path_and_filename, "w") as report_file:
        print(f"Loging to file {log_path_and_filename}")
        qrcode_tester = QRCodeTester(dfs, dst_path)
        qrcode_tester.set_report_func(_report)
        qrcode_tester.stop_on_recognition = True
        qrcode_tester.decode_qr_result = False
        qrcode_tester.try_original = False
        qrcode_tester.debug_cache = False

        # cv2_thresholding()
        # cv2_thresholding_isolated()
        # cv2_priority_thresholding()
        cv2_priority_thresholding_objects()

        print(f"Starting decoding: {datetime.datetime.now()}")
        c_files, c_files_decoded = qrcode_tester.execute(quick_decode=False)

    print(f"Decoding done: {datetime.datetime.now()}")
    print(f"{c_files_decoded} of {c_files} decoded = {c_files_decoded * 100 / c_files} %")
    print(f"these files were not decoded:")
    print(qrcode_tester.file_unrecognized)
    print(f"these strategies worked:")
    print(qrcode_tester.successful_strategies)

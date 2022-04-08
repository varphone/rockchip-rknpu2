
import cv2
import numpy as np

from rknn.api import RKNN
import os

if __name__ == '__main__':

    platform = 'rk3566'
    exp = 'mobilenet_v1_tf'
    Width = 224
    Height = 224
    MODEL_PATH = './onnx_models/mobilenet_v1_tf.onnx'
    NEED_BUILD_MODEL = True
    # NEED_BUILD_MODEL = False
    im_file = './dog_224x224.jpg'

    # Create RKNN object
    rknn = RKNN()

    OUT_DIR = "rknn_models"
    RKNN_MODEL_PATH = './{}/{}.rknn'.format(OUT_DIR,exp+'-'+str(Width)+'-'+str(Height))
    if NEED_BUILD_MODEL:
        DATASET = './dataset.txt'
        rknn.config(mean_values=[[0, 0, 0]], std_values=[[255, 255, 255]])
        # Load model
        print('--> Loading model')
        ret = rknn.load_onnx(MODEL_PATH)
        if ret != 0:
            print('load model failed!')
            exit(ret)
        print('done')

        # Build model
        print('--> Building model')
        ret = rknn.build(do_quantization=True, dataset=DATASET)
        if ret != 0:
            print('build model failed.')
            exit(ret)
        print('done')

        # Export rknn model
        if not os.path.exists(OUT_DIR):
            os.mkdir(OUT_DIR)
        print('--> Export RKNN model: {}'.format(RKNN_MODEL_PATH))
        ret = rknn.export_rknn(RKNN_MODEL_PATH)
        if ret != 0:
            print('Export rknn model failed.')
            exit(ret)
        print('done')
    else:
        ret = rknn.load_rknn(RKNN_MODEL_PATH)

    rknn.release()


import tensorflow as tf
import numpy as np
import backend.utils as utils
from movenet import Movenet

movenet = Movenet('movenet_thunder')


def detect(input_tensor, inference_count=10):
    """Runs detection on an input image.

    Args:
      input_tensor: A [height, width, 3] Tensor of type tf.float32.
        Note that height and width can be anything since the image will be
        immediately resized according to the needs of the model within this
        function.
      inference_count: Number of times the model should run repeatly on the
        same input image to improve detection accuracy.

    Returns:
      A Person entity detected by the MoveNet.SinglePose.
    """

    # Detect pose using the full input image
    movenet.detect(input_tensor.numpy(), reset_crop_region=True)

    # Repeatedly using previous detection result to identify the region of
    # interest and only croping that region to improve detection accuracy
    for _ in range(inference_count - 1):
        person = movenet.detect(input_tensor.numpy(),
                                reset_crop_region=False)

    return person


def calculation(heights, imgroute, output_overlayed=True):
    z = imgroute
    image = tf.io.read_file(z)
    # height = heights
    image = tf.io.decode_jpeg(image)
    pheight = image.get_shape()[0]
    person = detect(image)
    keys = []

    # Y-axis Distortion Correction
    def ydistortionWrapper(cheight, cdistance, sheight, numpixels):
        def ydistortion(pycoord):
            a1 = np.arctan2(cheight, cdistance)
            a2 = np.arctan2((sheight - cheight), cdistance)
            p2a = numpixels / (a1 + a2)
            a3 = (pheight - pycoord) / p2a

            return cdistance * (np.tan(a1) - np.tan(a1 - a3))

        return ydistortion

    # X-axis Distortion Correction
    def xdistortionWrapper(cheight, cdistance, sheight, numpixels):
        def xdistortion(pxcoord):
            a1 = np.arctan2(cheight, cdistance)
            a2 = np.arctan2((sheight - cheight), cdistance)
            p2a = numpixels / (a1 + a2)
            # a3 = pxcoord / p2a
            return pxcoord * cdistance / p2a

        return xdistortion

    # Distance Calculation
    def distance1(x1, y1, x2, y2):
        ydis = ydistortionWrapper(62, 111, heights, pheight)
        xdis = xdistortionWrapper(62, 111, heights, pheight)
        v = np.sqrt(pow(xdis(x1) - xdis(x2), 2) + pow(ydis(y1) - ydis(y2), 2))
        return v

    # Index the points to an array
    while len(keys) == 0:
        for z1 in range(len(person.keypoints)):
            if z1 in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]:
                keys.append(person.keypoints[z1])

    d1 = distance1(keys[6].coordinate.x, keys[6].coordinate.y, keys[8].coordinate.x, keys[8].coordinate.y)

    d2 = distance1(keys[7].coordinate.x, keys[7].coordinate.y, keys[9].coordinate.x, keys[9].coordinate.y)

    e1 = distance1(keys[1].coordinate.x, keys[1].coordinate.y, keys[3].coordinate.x, keys[3].coordinate.y) + distance1(
        keys[3].coordinate.x, keys[3].coordinate.y, keys[5].coordinate.x, keys[5].coordinate.y)
    e2 = distance1(keys[0].coordinate.x, keys[0].coordinate.y, keys[2].coordinate.x, keys[2].coordinate.y) + distance1(
        keys[2].coordinate.x, keys[2].coordinate.y, keys[4].coordinate.x, keys[4].coordinate.y)

    f1 = distance1(keys[0].coordinate.x, keys[0].coordinate.y, keys[1].coordinate.x, keys[1].coordinate.y)
    b1 = distance1(0, pheight, 0, keys[0].coordinate.y)
    b2 = distance1(0, pheight, 0, keys[1].coordinate.y)
    c2 = distance1(keys[9].coordinate.x, keys[9].coordinate.y, keys[11].coordinate.x, keys[11].coordinate.y) + d2
    c1 = distance1(keys[8].coordinate.x, keys[8].coordinate.y, keys[10].coordinate.x, keys[10].coordinate.y) + d1

    pred = [((b1 + b2) / 2), ((c1 + c2) / 2), ((d1 + d2) / 2), ((e1 + e2) / 2), f1]

    # Return prediction or (prediction, overlayed image) for use in analyze_and_display
    if output_overlayed:
        overlayed = utils.visualize(image.numpy(), [person])
        return pred, overlayed

    return pred

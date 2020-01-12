'''
Created on Jan 11, 2020

@author: Christian
'''

from skimage.metrics import structural_similarity
from time import sleep
import cv2
import os


video_stream = None
frame = None
ref_frame = None
metric_avg = 0
metric_threshold = 0.2


# Turn on the video
def start_video_stream(camera=0):
    global video_stream, ref_frame
    video_stream = cv2.VideoCapture(camera)
    if not video_stream.isOpened():
        video_stream.open()
    get_frame()
    ref_frame = frame


# Stop the video stream
def close_video_stream():
    global video_stream
    video_stream.release()
    cv2.destroyAllWindows()


# Gets a frame from the video (aka an image)
def get_frame():
    global video_stream, frame
    if video_stream == None:
        return None
    frame = video_stream.read()[1]
    return frame


# Loads the image path into an image
def get_image(path):
    if not os.path.exists(path):
        return None
    return cv2.imread(path, cv2.IMREAD_COLOR)


# Scales the image
def scale_image(image, percentage):
    width = int(image.shape[1] * percentage / 100)
    height = int(image.shape[0] * percentage / 100)
    return cv2.resize(image, (width, height))

# Turns a color photo into binary colors
def contrast_image(image, options=(255, 55, 1)):
    max_val, block_size, constant = options
    # Grayscale the image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply threshold
    return cv2.adaptiveThreshold(image, max_val, cv2.ADAPTIVE_THRESH_MEAN_C,
                                 cv2.THRESH_BINARY, block_size, constant)


# Automated scaling for comparison
def _force_scale(image, max_length=1200):
    height, width = image.shape[0], image.shape[1]
    if width > max_length:
        percentage = int(max_length * 100 / width)
        image = scale_image(image, percentage)
    if height > max_length:
        percentage = int(max_length * 100 / height)
        image = scale_image(image, percentage)
    return image


# Compares images
def compare_image(image1, image2):
    image1 = contrast_image(_force_scale(image1))
    image2 = contrast_image(_force_scale(image2))
    #cv2.imshow('Reference', image1)
    #cv2.imshow('Live', image2)
    return structural_similarity(image1, image2)


# Calibrates the metric value for the reference image
def calibrate(cycles=50):
    global ref_frame
    ref_frame = get_frame()
    sum_ = 0
    for i in range(cycles):
        sum_ += compare_image(ref_frame, frame)
        get_frame()
    return sum_ / cycles


# Main function to run the module
def run():
    global metric_avg
    while metric_avg <= 0.4:
        metric_avg = calibrate()
    get_frame()
    result = compare_image(ref_frame, frame)
    print(result,metric_avg)
    return result > metric_avg + metric_threshold or result < metric_avg - metric_threshold



if __name__ == '__main__':
    start_video_stream(0)
    calibrate()
    
    while True:
        if run():
            print('Subject has moved')
        print(compare_image(ref_frame, frame), metric_avg)
        sleep(0.10)

        # Wait for keyboard input indefinitely
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            # If keyboard input is 'q', then quit
            close_video_stream()
            break
        
        # Set reference frame
        if key & 0xFF == ord('r'):
            print('reference frame set')
            metric_avg = calibrate()
            

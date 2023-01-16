import cv2
import numpy as np
import time

# Read the video from file
video = cv2.VideoCapture("video.mp4")

# init text params
font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,650)
bottomLeftCornerOfText2 = (10,700)
fontScale              = 1
fontColor              = (255,255,255)
thickness              = 1
lineType               = 2


# Neutron : Pixel Ratio
nratio = 224

# Set the parameters for the saturated pixel detector
pixel_size = 5
pixel_intensity = 200

pxarray = []

# Iterate over each frame in the video
while True:
    # Read the next frame
    success, frame = video.read()

    # Initialize saturated pixel counter
    sp_count = 0

    # If the frame was not read successfully, we have reached the end of the video
    if not success:
        break

    # Preprocess the frame to enhance the visibility of the saturated pixels
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    preprocessed_frame = cv2.medianBlur(frame, 5)
    preprocessed_frame = cv2.equalizeHist(preprocessed_frame)
    
    # Segment the bright objects in the frame using thresholding
    _, thresholded_frame = cv2.threshold(preprocessed_frame, pixel_intensity, 255, cv2.THRESH_BINARY)
    
    # Remove noise and smooth the contours of the objects using morphological operations
    kernel = np.ones((3,3), np.uint8)
    thresholded_frame = cv2.erode(thresholded_frame, kernel, iterations=1)
    thresholded_frame = cv2.dilate(thresholded_frame, kernel, iterations=1)
    
    # Find the contours of the objects in the frame
    contours, _ = cv2.findContours(thresholded_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Iterate over the contours
    for contour in contours:
        # Use the size and intensity of the contour as features for a classifier
        size = cv2.contourArea(contour)
        intensity = np.mean(preprocessed_frame[contour[:, 0, 1], contour[:, 0, 0]])
                    

        # If the contour meets the size and intensity criteria for a saturated pixel, increment the saturated pixel (sp) count
        if size > pixel_size and intensity > pixel_intensity:
            sp_count += 1

    pxarray.append(sp_count)
    

    print("Saturated pixels in video: {sp_count}")

video.release()
video = cv2.VideoCapture("video.mp4")


index = 0
while True:
    success, frame = video.read()

    cv2.putText(frame, "Saturated Pixel Count: " + str(pxarray[index]), 
    bottomLeftCornerOfText, 
    font, 
    fontScale,
    fontColor,
    thickness,
    lineType)

    cv2.putText(frame, "Calibrated Neutron Count: " + str(round(pxarray[index]*nratio, 3)), 
    bottomLeftCornerOfText2, 
    font, 
    fontScale,
    fontColor,
    thickness,
    lineType)

    #   time.sleep(1)
    cv2.imshow("video.mp4", frame)

    key = cv2.waitKey(0)
    while key not in [ord('q'), ord('k')]:
        key = cv2.waitKey(0)
    # Quit when 'q' is pressed
    if key == ord('q'):
        break

    index += 1



# Release the video capture object

cv2.destroyWindow("video.mp4")

video.release()


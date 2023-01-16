import cv2


def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # draw circle here (etc...)
        print('x = %d, y = %d'%(x, y))

# Open the video file
cap = cv2.VideoCapture("piano (1).mp4")

# Read the first frame
ret, prev_frame = cap.read()

# Define the region of interest (ROI) as a small square in the center of the frame
roi = prev_frame[240:242, 320:322]
noteG = prev_frame[250:300, 100: 400]


while(cap.isOpened()):
    # Read the next frame
    ret, frame = cap.read()

    # Check if the frame is valid
    if not ret:
        break

    # Define the ROI in the current frame
    roi_current = frame[240:242, 320:322]

    # Calculate the absolute difference between the ROI in the previous and current frames
    diff = cv2.absdiff(roi, roi_current)

    # Apply a threshold to the difference image to only keep significant changes
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)


    # Check if there are any non-zero pixels in the thresholded image
    if cv2.countNonZero(gray) > 0:
        print("Change detected in ROI!")
    else:
        print("no change.")

    # Update the previous frame and ROI
    prev_frame = frame
    roi = roi_current

        # Draw a rectangle around the ROI in the current frame
    cv2.rectangle(frame, (320, 240), (360, 280), (0, 0, 255), 2)
    cv2.rectangle(frame, (250, 300), (100, 400), (0,0,255), 2)


    # Display the current frame
    cv2.imshow("piano.mp4", frame)


    cv2.setMouseCallback('piano.mp4', onMouse)

    # Wait for a key press

    key = cv2.waitKey(0)

    # Quit when 'q' is pressed
    if key == ord('q'):
        break


    """if cv2.waitKey(1) & 0xFF == ord('q'):
        break"""

# Release the video capture
cap.release()
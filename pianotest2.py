import cv2
import numpy as np
import winsound

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # draw circle here (etc...)
        print('x = %d, y = %d'%(x, y))

# Open the video file
cap = cv2.VideoCapture("piano_Uutiv0n7.mp4")

# Read the first frame
ret, prev_frame = cap.read()

# Define the region of interest (ROI) as a small square in the center of the frame
roi = prev_frame[240:242, 320:322]


while(cap.isOpened()):
    # Read the next frame
    ret, frame = cap.read()

    # Check if the frame is valid
    if not ret:
        break
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # lightest: rgb(203, 160, 145), darkest: rgb(125, 96, 90)
    # HSV: 16, 28.6, 79.6 | 10, 28, 49


    """   # convert to hsv colorspace
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # lower bound and upper bound for Green color
    upper_bound = np.array([16, 28, 79])	 
    lower_bound = np.array([0, 0, 255])

    # find the colors within the boundaries
    mask = cv2.inRange(hsv, lower_bound, upper_bound)


    #define kernel size  
    kernel = np.ones((7,7),np.uint8)

    # Remove unnecessary noise from mask

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)"""

    noteHighC = frame[121:194, 101:174]
    noteB = frame[121:194, 205:285]
    noteA = frame[121:194, 310:395]
    noteG = frame[121:194, 460:540]
    noteF = frame[110:184, 610:695]
    noteE = frame[101:194, 760:850]
    noteD = frame[95:184, 910:990]
    noteC = frame[101:194, 1030:1100]

    # Calculate the average brightness of the ROI  
    average_brightness_noteHighC = cv2.mean(noteHighC)[0]
    average_brightness_noteB = cv2.mean(noteB)[0]
    average_brightness_noteA = cv2.mean(noteA)[0]
    average_brightness_noteG = cv2.mean(noteG)[0]
    average_brightness_noteF = cv2.mean(noteF)[0]
    average_brightness_noteE = cv2.mean(noteE)[0]
    average_brightness_noteD = cv2.mean(noteD)[0]
    average_brightness_noteC = cv2.mean(noteC)[0]
    print("HighC: ", average_brightness_noteHighC, ", B: ", average_brightness_noteB, ", A: ", average_brightness_noteA, ", G: ", average_brightness_noteG, ", F: ", average_brightness_noteF, ", E: ", average_brightness_noteE, ", D: ", average_brightness_noteD, ", C: ", average_brightness_noteC)

    if (average_brightness_noteD > 85 and average_brightness_noteD < 105 ):
        print("D Being Played")
        winsound.Beep(293, 100 | winsound.SND_ASYNC)
    
    if (average_brightness_noteE > 90 and average_brightness_noteE < 135 ):
        print("E Being Played")        
        winsound.Beep(329, 100 | winsound.SND_ASYNC)

    if (average_brightness_noteC > 40 and average_brightness_noteC < 85 ):
        print("C Being Played")
        winsound.Beep(256, 100 | winsound.SND_ASYNC)
    
    if (average_brightness_noteG > 60 and average_brightness_noteG < 100 ):
        print("G Being Played")
        winsound.Beep(391, 100 | winsound.SND_ASYNC)



    #otsu_threshold, image_result = cv2.threshold(
    #    noteB, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    #)
    #print(otsu_threshold)


    # Draw a rectangle around the ROI in the current frame
    cv2.rectangle(frame, (101, 121), (174, 194), (0,0,255), 2)
    cv2.rectangle(frame, (205, 121), (285, 194), (0,0,255), 2)
    cv2.rectangle(frame, (310, 121), (395, 194), (0,0,255), 2)
    cv2.rectangle(frame, (460, 121), (540, 194), (0,0,255), 2)
    cv2.rectangle(frame, (610, 110), (695, 184), (0,0,255), 2)
    cv2.rectangle(frame, (760, 101), (850, 194), (0,0,255), 2)
    cv2.rectangle(frame, (910, 95), (990, 184), (0,0,255), 2)
    cv2.rectangle(frame, (1030, 101), (1100, 194), (0,0,255), 2)


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
import cv2
import imutils
from pynput.keyboard import Key, Controller
from PARAMETERS import *

RED    = (0, 0, 255)
BLUE   = (255, 0, 0,)
GREEN  = (0, 255, 0)
YELLOW = (0, 255, 255)


class Box:
    def __init__(self, coords, box_id, action=None):
        self.coords = coords
        self.id     = box_id
        self.action = action

def define_boxes():

    cam = cv2.VideoCapture(CAM_IDX)

    all_boxes = []
    box_id = 0

    while True:
            # show the output frame
        _, frame = cam.read()
        frame = imutils.resize(frame, width=400)
        frame = cv2.flip(frame, 1)

        
        for box in all_boxes:
            (x, y, w, h) = box.coords
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Frame", frame)
        
        key = cv2.waitKey(1) & 0xFF
        # if the 's' key is selected, we are going to "select" a bounding
        # box to track
        if key == ord("s"):

            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            initBB = cv2.selectROI("Frame", frame, fromCenter=False,
                showCrosshair=True)
            # all_boxes.append(initBB)

            action = input('Action :')
            all_boxes.append(Box(initBB, box_id, action))
            box_id += 1
            
            print(all_boxes)
            # print("Selected area coordinates :", initBB)
            print()
        
        
        # if the `q` key was pressed, break from the loop
        elif key == ord("q"):
            break

            cv2.destroyAllWindows()

    return all_boxes

def select_box(frame, cur_coords, all_boxes):
    # Returns the Box in which cur_coordinates lie (if any)
    xx, yy = cur_coords
    for box in all_boxes:
        (x, y, w, h) = box.coords
        if xx < x+w and xx > x and yy < y+h and yy > y:
            return box

def take_action(selected_box, last_action, mode):
    action = None
    if selected_box :
        action = selected_box.action

    if action:
        if ACTION_MODE == 0 and action != last_action:
            print('Tapping :', action)
            keyboard = Controller()
            keyboard.type(action)
            # keyboard.press(action)
            # keyboard.release(action)
        if ACTION_MODE == 1:
            print('Holding :', action)
            keyboard = Controller()
            keyboard.type(action)
            # keyboard.press(action)
            # keyboard.release(action)
    return action

def show_boxes(frame, selected_box, all_boxes):
    overlay = frame.copy()
    h, w, _ = frame.shape
    W, H    = (w//2, h//2)

    for box in all_boxes:
        color = BLUE        
        if selected_box:
            if selected_box.id == box.id:
                color = GREEN 
        (x, y, w, h) = box.coords
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

    return cv2.addWeighted(overlay, 1-ALPHA, frame, ALPHA, 0)

import cv2
import numpy as np
import time
import mss
import vgamepad as vg

SCREEN_REGION = {"left": 400, "top": 200, "width": 1120, "height": 680}

BLUE_LOWER = np.array([90, 100, 50])
BLUE_UPPER = np.array([140, 255, 255])

RED_LOWER1 = np.array([0, 120, 80])
RED_UPPER1 = np.array([10, 255, 255])
RED_LOWER2 = np.array([170, 120, 80])
RED_UPPER2 = np.array([180, 255, 255])

MIN_AREA = 30

gamepad = vg.VX360Gamepad()

def get_screen():
    with mss.mss() as sct:
        shot = sct.grab(SCREEN_REGION)
        frame = np.array(shot)
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

def find_targets(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    results = []
    kernel = np.ones((3, 3), np.uint8)

    mask_blue = cv2.inRange(hsv, BLUE_LOWER, BLUE_UPPER)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) >= MIN_AREA:
            x, y, w, h = cv2.boundingRect(cnt)
            results.append((x, y, w, h, "blue"))

    mask_red1 = cv2.inRange(hsv, RED_LOWER1, RED_UPPER1)
    mask_red2 = cv2.inRange(hsv, RED_LOWER2, RED_UPPER2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) >= MIN_AREA:
            x, y, w, h = cv2.boundingRect(cnt)
            results.append((x, y, w, h, "red"))

    return results

def press_button(btn):
    gamepad.press_button(button=btn)
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(button=btn)
    gamepad.update()

def main():
    print("Script started. Press Ctrl+C to stop.")
    time.sleep(3)

    press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
    time.sleep(1)

    try:
        while True:
            frame = get_screen()
            h, w = frame.shape[:2]
            center_x = w // 2
            
            targets = find_targets(frame)
            
            if targets:
                best_target = max(targets, key=lambda f: f[2] * f[3])
                cx = best_target[0] + best_target[2] // 2
                cy = best_target[1] + best_target[3] // 2
                fw, fh = best_target[2], best_target[3]
                color = best_target[4]

                offset_x = (cx - center_x) / center_x 
                steer_x = max(min(offset_x * 1.5, 1.0), -1.0)

                if fh > 50 and abs(cx - center_x) < 150:
                    print(f"[+] Interacting with {color} target (size: {fh})")
                    
                    gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
                    gamepad.update()
                    time.sleep(0.1)
                    
                    press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
                    time.sleep(0.7)
                    
                else:
                    gamepad.left_joystick_float(x_value_float=steer_x, y_value_float=1.0)
                    gamepad.update()
            
            else:
                gamepad.left_joystick_float(x_value_float=0.0, y_value_float=1.0)
                gamepad.update()
            
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nStopped.")
        gamepad.reset()
        gamepad.update()

if __name__ == "__main__":
    main()
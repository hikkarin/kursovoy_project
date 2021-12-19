import cv2


def select_file(path):
    cap = cv2.VideoCapture(path)
    return cap


def video_editing(frame1, frame2, blur_params, thresh_params, dilated_params):
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), blur_params)
    _, thresh = cv2.threshold(blur, thresh_params[0], thresh_params[1], cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=dilated_params)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return diff, blur, thresh, contours


def find_contours(contours, frame1):
    coord = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        coord = x, y, w, h
        if cv2.contourArea(contour) < 200:
            continue
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame1, f'X:{x} Y:{y}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 0, 255, 0), 2)
        print(f'{x + (w / 2)}, {y + (h / 2)}')

    return frame1, coord

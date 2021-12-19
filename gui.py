import PySimpleGUI as sg
import cv2
import main

final_layout = [
    [
        sg.Text("Final Frame", expand_x=True, font='arial', text_color="red"),
        sg.Text("Diff Frames", font='arial', text_color="red")
        ],
    [
        sg.Image(filename="", key="-IMAGE1-"),
        sg.Image(filename="", key="-IMAGE2-")
        ]
]

diff_layout = [
    [
        sg.Text("Blurred Frames", expand_x=True, font='arial', text_color="red"),
        sg.Text("Threshed Frames", font='arial', text_color="red")
    ],
    [
        sg.Image(filename="", key="-IMAGE3-"),
        sg.Image(filename="", key="-IMAGE4-")
    ]
]

layout = [
    [sg.Text("Motion Detecting")],
    [
        final_layout,
        diff_layout
    ],
    [
        [sg.Text(text="Blur"), sg.Slider((0, 15), 5, 1, size=(20, 10), orientation="h", key='-blur-'),
        sg.Text("Thresh"), sg.Slider((5, 60), 35, 1, size=(20, 10), orientation="h", key='-thresh1-')],
        [sg.Text("Thresh Color"), sg.Slider((0, 255), 255, 1, size=(20, 10), orientation="h", key='-thresh2-'),
        sg.Text("Dilated"), sg.Slider((1, 20), 10, 1, size=(20, 10), orientation="h", key='-dilated-')]
    ],
    [
        sg.Button("Stop")
    ],
    [sg.Checkbox(key='-camera-', text="Use camera")],
    [sg.FileBrowse(file_types=("Video Files", '*.mp4'), key="-browse-")],
    [sg.Button("Exit")]
]
frame1 = None
frame2 = None
path = None
cap = None
loop = True
blur_params = 0
thresh_params = [35, 255]
dilated_params = 10
window = sg.Window('Motion Detecting', layout)
while loop is True:
    while True:
        event, values = window.read(timeout=20)
        if event == 'exit' or event == sg.WIN_CLOSED:
            break
        if values['-camera-'] == False:
            if values['-browse-']:
                path = values['-browse-']
                cap = main.select_file(path)
                ret, frame1 = cap.read()
                ret, frame2 = cap.read()
                break
        if values['-camera-'] == True:
            cap = main.select_file(0)
            ret, frame1 = cap.read()
            ret, frame2 = cap.read()
            break

    while True:
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        event, values = window.read(timeout=20)
        if event == 'Stop':
            dict.clear(values)
            break
        if values['-blur-']:
            blur_params = int(values['-blur-'])
        if values['-thresh1-']:
            thresh_params[0] = int(values['-thresh1-'])
        if values['-thresh2-']:
            thresh_params[1] = int(values['-thresh2-'])
        if values['-dilated-']:
            dilated_params = int(values['-dilated-'])
        try:
            img_cont = main.video_editing(frame1, frame2, blur_params, thresh_params, dilated_params)
            contour = main.find_contours(img_cont[3], frame1)
            base_frame = cv2.resize(frame1, (480, 240), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
            frame_diff = cv2.resize(img_cont[0], (480, 240), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
            frame_blur = cv2.resize(img_cont[1], (480, 240), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
            frame_thresh = cv2.resize(img_cont[2], (480, 240), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
            imgbytes1 = cv2.imencode(".png", base_frame)[1].tobytes()
            imgbytes2 = cv2.imencode(".png", frame_diff)[1].tobytes()
            imgbytes3 = cv2.imencode(".png", frame_blur)[1].tobytes()
            imgbytes4 = cv2.imencode(".png", frame_thresh)[1].tobytes()
            frame1 = frame2
            ret, frame2 = cap.read()
            window["-IMAGE1-"].update(data=imgbytes1)
            window["-IMAGE2-"].update(data=imgbytes2)
            window["-IMAGE3-"].update(data=imgbytes3)
            window["-IMAGE4-"].update(data=imgbytes4)
        except:
            print("Something wrong")
            break
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break

window.close()

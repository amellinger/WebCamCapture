#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 13:50:37 2023

@author: axel
"""
#!/usr/bin/env python
import FreeSimpleGUI as sg
import cv2
import numpy as np
import time
import collections
import time
import tempfile
import shutil
import platform
import os
import sys
if getattr(sys, 'frozen', False):
    import pyi_splash
# import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
    
"""
Demo program that displays a webcam using OpenCV
"""
frame_width=800
frame_height=600
maxlen = 1000  # max. number of samples to determine the frame rate
t_deque = collections.deque(maxlen=maxlen)

WindowTitle = 'WebCam Capture — Physics Lab @ CMU    V 1.0'
MIN_SIZE = (1180, 720) # window minimum size
FONT = 'Arial 14'


#%%

# def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
#     if canvas.children:
#         for child in canvas.winfo_children():
#             child.destroy()
#     if canvas_toolbar.children:
#         for child in canvas_toolbar.winfo_children():
#             child.destroy()
#     figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
#     figure_canvas_agg.draw()
#     toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
#     toolbar.update()
#     figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)
#     return figure_canvas_agg

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller 
    From https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    print('****relative_path =', relative_path)
    print('****base_path =', base_path)
    print(os.path.join(base_path, relative_path))

    return os.path.join(base_path, relative_path)


def rel_to_abs_path(file_name: str) -> str:
    print('***file_name:', file_name)
    print('***joined:', os.path.join(os.path.dirname(__file__), file_name))
    return os.path.join(os.path.dirname(__file__), file_name)

# def LEDIndicator(key=None, radius=30):
#     return sg.Graph(canvas_size=(radius, radius),
#              graph_bottom_left=(-radius, -radius),
#              graph_top_right=(radius, radius),
#              pad=(0, 0), key=key)

# def SetLED(window, key, color):
#     graph = window[key]
#     graph.erase()
#     graph.draw_circle((0, 0), 12, fill_color=color, line_color=color)


def initialize_camera(camera):
    try: 
        s = platform.system()
        if s == 'Windows':
            cap = cv2.VideoCapture(camera, cv2.CAP_DSHOW)  # without CAP_DSHOW, camera opens very slowly
            window['-WEBCAMSETUP-'].update(disabled=False)
        else:
            cap = cv2.VideoCapture(camera)
        # cap = cv2.VideoCapture(camera, cv2.CAP_FFMPEG)
    except Exception as error:
        window['-STATUSTEXT-'].update('No camera found', text_color='lightred')
    else:
        if cap.isOpened():
            window['-STATUSTEXT-'].update('')
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G')) # must be first for some cameras...
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
            cap.set(cv2.CAP_PROP_FPS, fps0)
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G')) # ... and last for others
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
            time.sleep(0.5)
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
            cap.set(cv2.CAP_PROP_EXPOSURE, int(values['-EXPOSURE-']) ) 
            cap.set(cv2.CAP_PROP_GAIN, int(values['-GAIN-']) )
            cap.set(cv2.CAP_PROP_BRIGHTNESS, int(values['-BRIGHTNESS-']) )
            cap.set(cv2.CAP_PROP_CONTRAST, int(values['-CONTRAST-']) )        
            cap.set(cv2.CAP_PROP_SATURATION, int(values['-SATURATION-']) )
        else:
            window['-STATUSTEXT-'].update('No camera found', text_color='LightCoral')
        
    return cap
    
# 0. CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
# 1. CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
# 2. CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
# 3. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
# 4. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
# 5. CV_CAP_PROP_FPS Frame rate.
# 6. CV_CAP_PROP_FOURCC 4-character code of codec.
# 7. CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
# 8. CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
# 9. CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
# 10. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
# 11. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
# 12. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
# 13. CV_CAP_PROP_HUE Hue of the image (only for cameras).
# 14. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
# 15. CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
# 16. CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
# 17. CV_CAP_PROP_WHITE_BALANCE Currently unsupported
# 18. CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (

sg.theme('DarkPurple3')
sg.set_options(background_color='#6A0032', text_element_background_color='#6A0032', element_background_color='#6A0032',
               input_text_color='#FFFFFF', input_elements_background_color='#556B6F')



# define the window layout
#layout = [[sg.Frame(layout=[[sg.Image(resource_path('images/CMU-PHY_Logo_268px.png'), expand_x=True, expand_y=True ), 
layout = [[sg.Frame(layout=[[sg.Image(rel_to_abs_path('images/CMU-PHY_Logo_268px.png'), expand_x=True, expand_y=True ), 
                               sg.Text(text='WebCam Capture for Video Analysis', font=('Arial 36 bold'), expand_x=True, text_color='#FFC82E',
                                       justification='left')],
                           ], title='', size=(MIN_SIZE[0]-20,90))],
          [sg.Frame(layout=[[
               sg.Column(layout=[[sg.Image(filename='', key='image')]], vertical_alignment='top', size=(frame_width,frame_height)),
               sg.Column(layout=[
                   [sg.Frame(title='Status', title_color='#FFC82E', layout=[[sg.Text(text='', font='Arial 18 bold', text_color='yellow', 
                                                        # background_color='#808080',
                                                        key='-STATUSTEXT-')],
                                               ], 
                             size=(325,60), 
                             # background_color='#808080', 
                             relief=sg.DEFAULT_FRAME_RELIEF,
                             element_justification='center', vertical_alignment='c', key='-STATUS-'),
                    ],
                   [ sg.Button('Record', size=(9, 1)), sg.Push(), sg.Button('Stop', size=(9, 1), disabled=True), sg.Push(), 
                     sg.Button('Exit', size=(9, 1))],
                   [sg.Frame(title='Instructions', title_color='#FFC82E',
                             layout=([[sg.Text(text='• Set gain and brightness for optimum clarity.\n' +
                                                    '• For fast motion, keep exposure time short.\n' +
                                                    '• Wait until actual frame rate has stabilized.\n' +
                                                    '• Click "Record" to start recording.',
                                               font='Arial 12')]]), size=(325,100))],
                   [sg.Column([[]], size=(None, 10))],
                   [sg.Text('Frame Rate (per second):', size=(24, None)),
                    sg.Combo(values=(5, 10, 15, 20, 25, 30, 60), default_value=30, size=(5,1), key='-FPS-', enable_events=True, readonly=True)],
                   [sg.Text('Actual Frame Rate:'), sg.Text('', key='-ActualFPS-')],
                   [sg.Column([[]], size=(None, 10))],
                   [sg.Text('Exposure Time Setting:', size=(24, None)), 
                    sg.Spin(values=(-11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 5, 8, 10, 15, 20, 30, 50, 80, 100, 140, 200, 280, 400), initial_value=-9,
                            key='-EXPOSURE-', enable_events=True, size=(5,1), readonly=False)],
                   [sg.Text('Gain:', size=(24, None)), 
                    sg.Spin(values=(0, 1, 2, 5, 8, 10, 15, 20, 30, 40, 50, 80, 100, 140, 200, 255), initial_value=20,
                             key='-GAIN-', enable_events=True, size=(5,1), readonly=False)],
                   [sg.Text('Brightness:', size=(24, None)),
                    sg.Spin(values=(2, 5, 8, 10, 15, 20, 30, 40, 50, 80, 100, 120, 140, 170, 200, 255), initial_value=20,
                            key='-BRIGHTNESS-', enable_events=True, size=(5,1), readonly=False)],
                   [sg.Text('Contrast:', size=(24, None)),
                    sg.Spin(values=(2, 5, 8, 10, 15, 20, 30, 40, 50, 65, 80, 100, 120, 140, 170, 200, 255), initial_value=30,
                            key='-CONTRAST-', enable_events=True, size=(5,1), readonly=False)],
                   [sg.Text('Saturation:', size=(24, None)),
                    sg.Spin(values=(10, 15, 20, 30, 50, 65, 80, 100, 120, 140, 200, 255), initial_value=80,
                            key='-SATURATION-', enable_events=True, size=(5,1), readonly=False)],
                   [sg.Text('Camera No.:', size=(24, None)),
                    sg.Spin(values=(0,1,2,3), initial_value=0,
                             key='-CAMERA-', enable_events=True, size=(5,1))],
                   [sg.Column([[]], size=(None, 30))],
                   [sg.Push(), sg.Button('Webcam Setup Dialog', key='-WEBCAMSETUP-', disabled=True), sg.Push()],
                  ], vertical_alignment='top', s=(450, 600)),
               ]], title='', size=(MIN_SIZE[0]-20,600))]]



# Close splash screen (pyinstaller)
if getattr(sys, 'frozen', False):
    pyi_splash.close()

# Use this code to signal the splash screen removal. (Nuitka)
if "NUITKA_ONEFILE_PARENT" in os.environ:
   splash_filename = os.path.join(
      tempfile.gettempdir(),
      "onefile_%d_splash_feedback.tmp" % int(os.environ["NUITKA_ONEFILE_PARENT"]),
   )
   if os.path.exists(splash_filename):
      os.unlink(splash_filename)


# create the window and show it without the plot
window = sg.Window(WindowTitle,
                   layout, resizable=True, scaling=1.0,
                   font=FONT,
                   location=(0,0),
                   finalize=True)

#SetLED(window, '-REC-', 'gray')
# window.Maximize()

sg.set_options(element_size=(0.5, 0.5))

events, values = window.read(timeout=10)  # timeout is in ms


# enforce minimum window size
width, height = tuple(map(int, window.TKroot.geometry().split("+")[0].split("x")))
# print(width, height)
window.TKroot.minsize(max(MIN_SIZE[0], width), max(MIN_SIZE[1], height))


img = np.full((frame_height, frame_width), 32)
imgbytes = cv2.imencode('.png', img)[1].tobytes()
window['image'].update(data=imgbytes)

fps0 = values['-FPS-']
cap = initialize_camera(values['-CAMERA-'])

font = cv2.FONT_HERSHEY_SIMPLEX 

recording = False

   
cnt = -5
fps = fps0
fps_median = fps0

# fig, ax = plt.subplots(num=0)
# fig.clf()
# ax.hist(np.array(t_deque)/1000, np.linspace(150, 380, 50))
# fig.canvas.draw_idle()
# fig.canvas.flush_events()

# ---===--- Event LOOP Read and display frames, operate the GUI --- #
while True:
    event, values = window.read(timeout=0.1)
    # print(event, values)
    # print('before cap.read')
    ret, frame = cap.read()

    if cnt<=0:
        # t1 = datetime.datetime.now()
        t1 = time.time()
    else:
        # t2 = datetime.datetime.now()
        t2 = time.time()
        tdiff = t2-t1
        # t_deque.append(tdiff.seconds*1000000+tdiff.microseconds)
        t_deque.append(tdiff)
        t1 = t2
        fps = len(t_deque)/np.sum(t_deque)
    
    cnt += 1

#    cv2.putText(img=frame, text=f'{fps:.3f} fps', 
#                org=(7, 30), fontFace=font, fontScale=1,
#                color=(100, 255, 0),
#                thickness=2,
#                lineType=cv2.LINE_AA) 

    # cv2.putText(gray, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA) 

    if cnt<0:
        if cap.isOpened():
            window['-STATUSTEXT-'].update('Wait... measuring frame rate', text_color='yellow')
        window['Record'].update(disabled=True)
    elif cnt==500:
        if cap.isOpened():
            window['Record'].update(disabled=False)
            window['-STATUSTEXT-'].update('Ready', text_color='lightgreen')

    if recording:
        out.write(frame)
    else:
        # pass
        time.sleep(1e-3)      # compensate for out.write


    # print(ret, 'after cap.read')
    
    if event == 'Exit' or event == sg.WIN_CLOSED:
        # tstop = datetime.datetime.now()
        tstop = time.time()
        cap.release()
        
        window.close()
        cv2.destroyAllWindows()
        break

        

    elif event == 'Record':
        recording = True
        # SetLED(window, '-REC-', 'red')
        window['Record'].update(disabled=True)
        window['Stop'].update(disabled=False)
        window['-STATUSTEXT-'].update('Recording', text_color='LightCoral')

        tmpdir=tempfile.TemporaryDirectory()
        fn = os.path.join(tmpdir.name, 'video.mp4')
        out = cv2.VideoWriter(fn,
                              fourcc=cv2.VideoWriter_fourcc(*"mp4v"),
                              # apiPreference=cv2.CAP_FFMPEG,
                              fps=fps, frameSize=(frame_width,frame_height))

    elif event == 'Stop':
        recording = False
        # SetLED(window, '-REC-', 'gray')
        window['Record'].update(disabled=False)
        window['Stop'].update(disabled=True)
        window['-STATUSTEXT-'].update('')
        if 'out' in locals():
            out.release()
        fn2 = sg.popup_get_file("Save video file:", title = "Video", save_as=True, no_window=True,
                                font=FONT, file_types=(('Video Files', '*.mp4'),))
        if not (fn2==None):
            shutil.copy(fn, fn2)
        tmpdir.cleanup()
        t_deque.clear()
        cnt = -5   
#            

    elif event == '-FPS-':
        fps0 = int(values['-FPS-'])
        cap.release()
        cap = initialize_camera(values['-CAMERA-'])
        t_deque.clear()
        cnt = -5
        
    elif event == '-EXPOSURE-':
        cap.set(cv2.CAP_PROP_EXPOSURE, values['-EXPOSURE-'] ) 

    elif event == '-GAIN-':
        cap.set(cv2.CAP_PROP_GAIN, values['-GAIN-'] ) 

    elif event == '-BRIGHTNESS-':
        cap.set(cv2.CAP_PROP_BRIGHTNESS, values['-BRIGHTNESS-'] ) 

    elif event == '-CONTRAST-':
        cap.set(cv2.CAP_PROP_CONTRAST, values['-CONTRAST-'] ) 

    elif event == '-SATURATION-':
        cap.set(cv2.CAP_PROP_SATURATION, values['-SATURATION-'] ) 

    elif event == '-CAMERA-':
        cap.release()
        print(values['-CAMERA-'])
        cap = initialize_camera(values['-CAMERA-'])
        t_deque.clear()
        cnt = -5

        # a = cap.set(cv2.CAP_PROP_FPS, fps0)
        # print('a', a)
    
    elif event == '-WEBCAMSETUP-':
        cap.set(cv2.CAP_PROP_SETTINGS, 1)              # open settings dialog
        

    if not cnt%2:    # update display every other image to speed up loop 
        window['-ActualFPS-'].update(f'{fps:7.3f}   from {len(t_deque):4} samples')
        if cap.isOpened():
            try: 
                imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            except Exception as e:
                print(e)
                img = np.full((frame_height, frame_width), 32)
                imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['image'].update(data=imgbytes)
        else:
            img = np.full((frame_height, frame_width), 32)
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['image'].update(data=imgbytes)
        if (len(t_deque)>5) and (np.max(t_deque)>3./fps0):  # long delay; reset time queue
            t_deque.clear()
            cnt=-5
            if recording:
                recording = False
                # SetLED(window, '-REC-', 'gray')
                window['Record'].update(disabled=False)
                window['Stop'].update(disabled=True)
                if 'out' in locals():
                    out.release()
                sg.popup('Recording too slow.\nLet the frame rate stabilize\nand try again.', 
                         custom_text='Continue', title='Error')

        
    # if not cnt%30:
    #     ts = np.array(t_deque)*1000
    #     sg.cprint(np.array2string(ts[-13:], precision=1, floatmode='fixed'), key='-TEXT-')
    #     ts.sort()
    #     sg.cprint(np.array2string(ts[:12], precision=1, floatmode='fixed'), key='-TEXT2-')
    #     sg.cprint(np.array2string(ts[-18:], precision=1, floatmode='fixed'), key='-TEXT3-')



    # if not cnt%30:
    #     print(datetime.datetime.now())


#import matplotlib.pyplot as plt
#plt.hist(t_deque, bins=np.linspace(1./fps0*0.5, 1./fps0*2., 200))
#plt.show()

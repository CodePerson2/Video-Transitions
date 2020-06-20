import PySimpleGUI as sg
from funcs import play_video, wipe, dissolve
import cv2

#recognizer = cv2.face.LBPHFaceRecognizer_create()
sg.theme('DarkAmber')	    # dark theme

layout = [  [sg.Text('Video Transition Maker')],
            [sg.Text('Enter first video File (mp4):'), sg.InputText(), sg.Button('Play1')],
            [sg.Text('Enter second video File (mp4):'), sg.InputText(), sg.Button('Play2')],
            [sg.Text('Press Q anytime to exit pop-up video')],
            [sg.Text('')],
            [sg.Text('Enter new file name (or leave blank for default name):'), sg.InputText()],

            [sg.Frame(layout=[
            [sg.Radio('Top-Bottom', "RADIO1", size=(10,1), key='r1', default=True), sg.Radio('Bottom-Top', "RADIO1", key='r2'), 
            sg.Radio('Left-Right', "RADIO1", key='r3'), sg.Radio('Right-Left', "RADIO1", key='r4'), sg.Radio('Dissolve', "RADIO1", key='r5')]],
            title='Wipe Styles',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set wipe styles')],

            [sg.Frame(layout=[
            [sg.Slider(range=(-1, 5), default_value=1, size=(20, 10), orientation="h",enable_events=True, key="slider")]],
            title='Wipe Speed (fast-slow)',title_color='yellow', relief=sg.RELIEF_SUNKEN, tooltip='Wipe speed (0 = 0.5 speed)')],

            [sg.Frame(layout=[
            [sg.Radio('64X32', "RES", key='res1'), sg.Radio('256X128', "RES", key='res2'), 
            sg.Radio('512X256', "RES", key='res3'), sg.Radio('1024X512', "RES", key='res4'), sg.Radio('2048X1024', "RES", key='res5')]],
            title='Video Resolution',title_color='grey', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set video resolution')],

            [sg.Button('Run Transition'), sg.Button('Exit')]]

# Create Window
window = sg.Window('Window', layout)
# process events in window
res = (100, 50)
while True:
    event, values = window.read()
    if event in (None, 'Exit'):	        # exit window
        break

    if event in (None, 'Run Transition'):

        if values['res1']:
            res = (64, 32)

        elif values['res2']:
            res = (256, 128)

        elif values['res3']:
            res = (512, 256)

        elif values['res4']:
            res = (1024, 512)
        
        elif values['res5']:
            res = (2048, 1024)

        if values['r1']:
            wipe(values[0], values[1], values['slider'], values[2], 'top', res)
            continue

        elif values['r2']:
            wipe(values[0], values[1], values['slider'], values[2], 'bottom', res)
            continue

        elif values['r3']:
            wipe(values[0], values[1], values['slider'], values[2], 'left', res)
            continue

        elif values['r4']:
            wipe(values[0], values[1], values['slider'], values[2], 'right', res)
            continue

        elif values['r5']:
            dissolve(values[0], values[1], values['slider'], values[2], res)
            continue


    if event in (None, 'Play1'):
        play_video(values[0])
        continue

    if event in (None, 'Play2'):
        play_video(values[1])
        continue

window.close()
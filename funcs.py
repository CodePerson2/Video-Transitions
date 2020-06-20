import cv2
import numpy as np
import PySimpleGUI as sg



def wipe(x, y, speed, fileName = "video", wipeType = 'top', res = (500, 250)):

    early = False       # test for early abortion of wipe

    vidcap1 = cv2.VideoCapture(x)
    vidcap2 = cv2.VideoCapture(y)

    success1, image1 = vidcap1.read()
    success2, image2 = vidcap2.read()

    h1, w1, channels1 = image1.shape
    h2, w2, channels2 = image2.shape

    video = cv2.VideoWriter(fileName + '.mp4', 0x7634706d, 20.0, res)

    if wipeType == 'top':       #count
        max = res[1]
    elif wipeType == 'left':
        max = res[0]
    elif wipeType == 'bottom':
        max = res[1]
    elif wipeType == 'right':
        max = res[0]
    c = 1
    skip = 1
    while success1 and success2 and c <= max:

        image1 = cv2.resize(image1, res)
        image2 = cv2.resize(image2, res)

        if wipeType == 'top':
            image1[0:c, 0:res[0]] = (0,0,0)
            image2[c:res[1], 0:res[0]] = (0,0,0)
        elif wipeType == 'bottom':
            image1[res[1]-c:res[1], 0:res[0]] = (0,0,0)
            image2[0:res[1]-c, 0:res[0]] = (0,0,0)
        elif wipeType == 'left':
            image1[0:res[1], 0:c] = (0,0,0)
            image2[0:res[1], c:res[0]] = (0,0,0)
        elif wipeType == 'right':
            image1[0:res[1], res[0]-c:res[0]] = (0,0,0)
            image2[0:res[1], 0:res[0]-c] = (0,0,0)

        image1[0:res[1], 0:res[0]] += image2[0:res[1], 0:res[0]]

        video.write(image1)
        success1, image1 = vidcap1.read()
        success2, image2 = vidcap2.read()
        
        if speed == -1:
            c += 4
        elif speed == 0:
            c += 2
        elif skip == speed:
            c += 1
            skip = 1
        else:    
            skip+=1
        if c > max:
            c = max

        if not sg.OneLineProgressMeter('Loading..', c, max, key='prog'):
            early = True
            break

    sg.OneLineProgressMeterCancel('prog')
    if c != max:

        stmt = 'video entered was too short to do full wipe.\nRaise wipe speed.'
        if early == True:
            stmt = 'Wipe was aborted early.            '

        layout = [[sg.Text(stmt)],
        [sg.Button('Exit')]]

        window = sg.Window('ERROR', layout)

        while True:
            event, values = window.read()
            if event in (None, 'Exit'):	        # exit window
                break
        window.close()

    cv2.destroyAllWindows()
    video.release()
    play_video(fileName + '.mp4')

def dissolve(x, y, speed, fileName = "video", res = (500, 250)):
    early = False       # test for early abortion of wipe
    smooth = True
    m = 1/2
    wait = 1
    speed += 10

    vidcap1 = cv2.VideoCapture(x)
    vidcap2 = cv2.VideoCapture(y)

    length = int(vidcap2.get(cv2.CAP_PROP_FRAME_COUNT))

    success1, image1 = vidcap1.read()
    success2, image2 = vidcap2.read()

    h1, w1, channels1 = image1.shape
    h2, w2, channels2 = image2.shape

    video = cv2.VideoWriter(fileName + '.mp4', 0x7634706d, 20.0, res)
    
    w = res[0]
    h = res[1]
    c = 1
    while success2 and c < 400:

        if success1:
            image1 = cv2.resize(image1, res)
        image2 = cv2.resize(image2, res)

        if (w == 2 or m == 2) and success1:
            m = 2
            holder = image1
            image1 = image2
            image2 = holder
                                
        if success1:
            image1[::h, ::w] = (0,0,0)
            image1[::h, ::w] += image2[::h, ::w]

        video.write(image1)
        success1, image1 = vidcap1.read()
        success2, image2 = vidcap2.read()

        if not sg.OneLineProgressMeter('Loading..', c, 400, key='prog'):
            early = True
            break

        if w <= 16 and smooth:
            smooth = False

        elif w > 1 and wait % speed == 0:
            w = int(w * m)
            h = int(h * m)
            wait = 1
            smooth = True
            
        
        wait += 1
        c += 1

    sg.OneLineProgressMeterCancel('prog')
    if w < res[0] or h < res[1]:

        stmt = 'video entered was too short to do full wipe.\nRaise wipe speed.'
        if early == True:
            stmt = 'Wipe was aborted early.            '

        layout = [[sg.Text(stmt)],
        [sg.Button('Exit')]]

        window = sg.Window('ERROR', layout)

        while True:
            event, values = window.read()
            if event in (None, 'Exit'):	        # exit window
                break
        window.close()

    cv2.destroyAllWindows()
    video.release()
    play_video(fileName + '.mp4')



def play_video(x):  # play video
    vidcap = cv2.VideoCapture(x)
    while vidcap.isOpened():
        ret, frame = vidcap.read()

        if ret:

                cv2.imshow( 'video', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
        else:
            break
    vidcap.release()
    cv2.destroyAllWindows()
    return

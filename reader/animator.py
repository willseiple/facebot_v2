from cv2 import VideoCapture, namedWindow, destroyAllWindows, imshow, waitKey, resize

# set binds and frame locations
blink = (55, 20)
smile = (140, 110)
right = (288, 255)
left =  (585, 255)
idle =  (880, 620)

binds = {'b' : blink,
         's' : smile,
         'r' : right,
         'l' : left,
         'i' : idle,}


def crop(im, final_dims):
    '''
    final dims in form (x,y)
    crops image to fit in final_dims
    '''
    cury, curx = im.shape[:2]
    finx, finy = final_dims

    cur_ratio = curx / cury
    final_ratio = finx / finy

    if cur_ratio == final_ratio:
        return im

    else:
        if cur_ratio > final_ratio:
            xmult = final_ratio / cur_ratio
            xpix = curx - curx * xmult
            cropped = im[:, int(xpix/2)+1:int(curx-xpix/2)]

        if cur_ratio < final_ratio:
            ymult = cur_ratio / final_ratio
            ypix = cury - cury * ymult
            cropped = im[int(ypix/2):int(cury-ypix/2), 1:]

        return cropped


def play(start, duration, video, win_size, win_name, screen_fit=False, speed=1):
    '''
    play video for duration starting at frame, record next action
    '''
    start /= 2
    duration /= 2
    key = None
    cur = start

    # set current frame
    video.set(1, start)
    # iterate over all frames
    while cur < start + duration:

        for _ in range(speed):
            grabbed, frame = video.read()
        if not grabbed:
            break
            # take user input
        new = chr(waitKey(1) & 0xFF)
        if ord(new) != 255:
            if new == 'q' or new == 'c':
                return new
            key = new
        frame = resize(frame, win_size)
        if screen_fit:
            frame = crop(frame, screen_fit)
        imshow(win_name, frame)
        cur += speed

    return key


def wait(video, win_size, win_name, screen_fit=False):
    '''
    waits for input after displaying home frame
    '''
    video.set(1, 1)

    grabbed, frame = video.read()
    frame = resize(frame, win_size)
    if screen_fit:
        frame = crop(frame, screen_fit)
    imshow(win_name, frame)
    # listen for keypress forever
    follow = chr(waitKey() & 0xFF)
    return follow


def main(filename, win_size, win_name, screen_fit=False, speed=1):
    '''
    opens window and responds to user input
    closes when user presses "q"
    '''
    cap = VideoCapture(filename)
    namedWindow(win_name, 1)

    follow = None

    while cap.isOpened():
        if follow == 'q':
            break
        if follow in binds:
            follow = play(binds[follow][0], binds[follow][1], cap, win_size=win_size, win_name=win_name, speed=speed, screen_fit=screen_fit)
        else:
            follow = wait(cap, win_size=win_size, win_name=win_name, screen_fit=screen_fit)

    cap.release()
    destroyAllWindows()


if __name__ == '__main__':
    pass
    # main('data/willbot.mp4', (3840, 2160), 'window', (250, 1400))

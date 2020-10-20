import reader.animator
import reader.gui
import reader.download_files


def main():
    '''
    ''' 
    # downloads files to .facebot dir in home directory if not already downloaded
    home = reader.download_files.main()

    # retreives settings from gui
    cache = reader.gui.main(home)
    
    # sets variables 
    REL_PATH     = cache['model_path']
    clicked_flag = cache['clicked_flag']
    custom_flag  = cache['custom_flag']
    WINDOW_SIZE  = cache['dims']
    SCREEN_SIZE  = cache['screen_size']

    WINDOW_NAME = 'iDmission FaceBot'
    # reader
    FILENAME = home + '/.facebot/data/' + REL_PATH

    # if custom_flag:
    #     print('Custom input coming soon, please select one of the premade models.')
    #     return

    if clicked_flag:
        reader.animator.main(FILENAME, WINDOW_SIZE, WINDOW_NAME, SCREEN_SIZE)

if __name__ == '__main__':
    main()

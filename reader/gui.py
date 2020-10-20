import tkinter as tk
from PIL import ImageTk, Image


WIDTH = 400
HEIGHT = 200


# dims = dimensions['4k']
# model_name = 'Male bot'
# model_path = models[model_name]
# clicked_flag = False
# custom_flag = False


models = {
          'Sandra' : 'sandrabot.mp4',
          'Darius' : 'dariusbot.mp4',
          'Will' : 'willbot.mp4',
          'Deepfake' : 'willfake.mp4',
          # 'Custom...' : None,
         }

models_keys = list(models.keys())

dimensions = {
              # causes frame drop 
              '4k' : (3840, 2160),
              '1440p' : (2560, 1440),
              '1080p' : (1920, 1080),
              '720p' : (1280, 720),
              '480p' : (852, 480),
             }

dimensions_keys = list(dimensions.keys())

cache = {
         'dims' : dimensions['1440p'],
         'model_path' : 'sandrabot.mp4',
         'clicked_flag' : False,
         'custom_flag' : False,
         'check' : False,
         'model_name' : 'Sandra',
         'screen_size' : False,
        }


# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#     base_path = getattr(sys, '_MEIPASS', getcwd())
#     return path.join(base_path, relative_path)

def main(home):
    '''
    '''

    def find_screen_size():
        '''
        returns user screen resolution
        '''
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        return (screen_width, screen_height)


    def shorten_path(filename):
        '''
        returns final elem of path
        '''
        return filename.split('/')[-1]


    def selected_res(event):
        '''
        sets cache['dims'] to resolution selected in res_drop dropdown
        '''
        select = res_clicked.get()
        cache['dims'] = dimensions[select]


    def set_thumbnail(filename):
        '''
        '''
        new_im = Image.open(filename)
        new_im.thumbnail((200, 200))
        preview = ImageTk.PhotoImage(new_im)
        preview_label.image = preview
        preview_label.configure(image=preview)


    def selected_model(event):
        '''
        selects model from dropdown
        '''
        select = model_clicked.get()
        if select != 'Custom...':
            cache['custom_flag'] = False
            cache['model_name'] = select
            cache['model_path'] = models[select]
            model_png = cache['model_path'].split('.')[0] + '.png'
            # reader/data
            preview_filename = home + '/.facebot/data/' + model_png
            set_thumbnail(preview_filename)
        else:
            new_filename = tk.filedialog.askopenfilename(initialdir=".", title="Browse files", filetypes=(("png files", "*.png"),("all files", "*.*")))

            if new_filename == "":
                if cache['custom_flag'] == True:
                    model_clicked.set(shorten_path(cache['model_path']))
                else:
                    model_clicked.set(shorten_path(cache['model_name']))
            else:
                cache['custom_flag'] = True
                cache['model_path'] = new_filename
                model_clicked.set(shorten_path(cache['model_path']))
                set_thumbnail(cache['model_path'])


    def close():
        '''
        '''
        cache['clicked_flag'] = True
        cache['check'] = checkvar.get()
        if cache['check']:
            cache['screen_size'] = find_screen_size()
        root.destroy()

    # define root
    root = tk.Tk()

    # format window
    root.title('iDmission FaceBot')
    root.geometry(str(WIDTH) + "x" + str(HEIGHT))
    # icon = tk.Image('photo', file="reader/data/icon.gif")
    # root.tk.call('wm','iconphoto', root._w, icon)

    # define frames
    topframe = tk.Frame(root, height=50)
    topframe.pack(side='top', fill='x', pady=5)

    bottomframe = tk.Frame(root, height=50)
    bottomframe.pack(side='bottom', fill='x', pady=5)

    leftframe = tk.Frame(root)
    leftframe.pack(side='left', fill='y', pady=5)

    rightframe = tk.Frame(root)
    rightframe.pack(side='right', fill='y', pady=5)

    # header
    label = tk.Label(topframe, text='Settings')
    label.pack()

    # selection labels
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    res_label = tk.Label(leftframe, text="Resolution:").grid(row=1, column=0)
    model_label = tk.Label(leftframe, text="Model:").grid(row=0, column=0)
    check_label = tk.Label(leftframe, text="Fit to screen?").grid(row=2, column=0)

    # variable to save dropdown results
    res_clicked = tk.StringVar()
    res_clicked.set(dimensions_keys[0])
    model_clicked = tk.StringVar()
    model_clicked.set(models_keys[0])

    # drop down menus
    res_drop = tk.OptionMenu(leftframe, res_clicked, *dimensions_keys, command=selected_res)
    res_drop.grid(row=1, column=1, sticky='w')
    model_drop = tk.OptionMenu(leftframe, model_clicked, *models_keys, command=selected_model)
    model_drop.grid(row=0, column=1, sticky='w')

    # checkbox
    checkvar = tk.IntVar()
    checkvar.set(1)
    check = tk.Checkbutton(leftframe, variable=checkvar)
    check.grid(row=2, column=1, sticky='w')

    # preview box
    # 'reader/data/' + cache['model_path'].split('.')[0] + '.png'
    preview_path = home + '/.facebot/data/' + cache['model_path'].split('.')[0] + '.png'
    preview_im = Image.open(preview_path)
    preview_im.thumbnail((200,200))
    preview = ImageTk.PhotoImage(preview_im)
    preview_label = tk.Label(rightframe, image=preview)
    preview_label.image = preview
    preview_label.pack(side='right', fill='both')

    # submit settings and continue to FaceBot
    submit = tk.Button(bottomframe, text="Continue to FaceBot", command=close)
    submit.pack()

    root.mainloop()

    return cache

if __name__ == '__main__':
    pass
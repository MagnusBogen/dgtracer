import PySimpleGUI as sg
import os
from shutil import copyfile


class GUI:
    def __init__(self):
        self.front_picture = 'graphic/front_picture.png'
        sg.theme('DarkBlue')

        # ------------------------------------  LAYOUT COLUMNS  ------------------------------------
        # COLUMN 1
        self.file_list_column = [
            [
                sg.Text("Import Video"),
                sg.In(size=(30, 1), enable_events=True, key="-FOLDER-"),
                sg.FolderBrowse(),
            ],
            [
                sg.Button("Videos", enable_events=True, key="-VIDEO FOLDER-"),
                sg.Button("Analyzes", enable_events=True, key="-ANALYZES-"),
            ],

            [
                sg.Listbox(
                    values=[], enable_events=True, size=(25, 30), key='-FILE LIST-', auto_size_text=False,
                    font=("Helvetica", 20)
                ),
            ],
        ]

        # COLUMN 2
        self.image_viewer_column = [
            [
                sg.Text(text="Video options", size=(20, 1), font=("Helvetica", 15)),
            ],
            [
                sg.Button("Delete video", enable_events=True, key="-DELETE VIDEO-", disabled=True,
                          button_color=["white", "red"]),
                sg.Button("View video", enable_events=True, key="-VIEW VIDEO-", disabled=True),
                sg.Button("Analyze", enable_events=True, key="-CAM SHIFT-", disabled=True),
                sg.Text(text="Trace color:", size=(9, 1), key="-TRACE COLOR-", visible=True,),
                sg.CBox('Blue', key='-COLOR BLUE-', enable_events=True),
                sg.CBox('X-Velocity Color', key='-COLOR XV-', enable_events=True, default=True),
                sg.CBox('Y-Velocity Color', key='-COLOR YV-', enable_events=True),

            ],
            [
                sg.HSeparator(),
            ],
            [
                sg.In(size=(5, 1), enable_events=True, key="-H MIN-", default_text='0'),
                sg.In(size=(5, 1), enable_events=True, key="-H MAX-", default_text='255'),
                sg.In(size=(5, 1), enable_events=True, key="-S MIN-", default_text='0'),
                sg.In(size=(5, 1), enable_events=True, key="-S MAX-", default_text='255'),
                sg.In(size=(5, 1), enable_events=True, key="-V MIN-", default_text='254'),
                sg.In(size=(5, 1), enable_events=True, key="-V MAX-", default_text='255'),
                sg.CBox('Video', key='-HSV VIDEO-', default=True),
                sg.Button("HSV", enable_events=True, key="-HSV-", disabled=True),

            ],
            [
                sg.HSeparator(),
            ],
            [
                sg.Text(text="Max speed", size=(9, 1), key="-MS-", visible=True),
                sg.Text(text="none", size=(9, 1), key="-MAX SPEED-", visible=True),
            ],
            [
                sg.HSeparator(),
            ],
            [
                sg.Text(text="file_name", size=(40, 1), key="-TOUT-", visible=True, font=("Helvetica", 25)),
            ],
            [

                sg.Image(key="-IMAGE FRAME-", filename=self.front_picture),
            ],
        ]

        # ------------------------------------  FULL LAYOUT  ------------------------------------
        self.layout = [
            [
                sg.Text(text="Disc Golf Video Analyzer", size=(30, 1), key="-DGVA-", visible=True,
                        font=("Helvetica", 40), justification="center", pad=((400, 400),(1, 1)))
            ],
            [
                sg.HSeparator(),
            ],
            [
                sg.Column(self.file_list_column),
                sg.VSeperator(),
                sg.Column(self.image_viewer_column),
            ]
        ]

        self.window = sg.Window("Disc Golf Tracker", self.layout)


def run_event_loop(gui, handler):

    event, values = gui.window.read()

    # Exit Condition
    if event == "Exit" or event == sg.WIN_CLOSED:
            return 1

    # -------------------------------------- FOLDERS AND SELECTION ------------------------------------------------
    # Browse folders
    if event == "-FOLDER-":
        handler.selected_folder_dir = values["-FOLDER-"]
        folder = values["-FOLDER-"]
        try:

            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        file_names = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png", ".gif", ".mov"))
        ]
        gui.window["-FILE LIST-"].update(file_names)

    # Video folder selected
    elif event == "-VIDEO FOLDER-":
        # Update GUI window
        gui.window["-DELETE VIDEO-"].update(disabled=True)
        gui.window["-VIEW VIDEO-"].update(disabled=True)
        gui.window["-CAM SHIFT-"].update(disabled=True)
        gui.window["-HSV-"].update(disabled=True)

        # Update GUI variables
        handler.selected_folder_dir = os.path.join(handler.root_dir, handler.video_folder_dir)
        gui.window["-IMAGE FRAME-"].update(filename=gui.front_picture)
        gui.window["-TOUT-"].update(value="Disc Golf Tracker")

        try:
            # Get list of files in folder
            file_list = os.listdir(handler.selected_folder_dir)
        except:
            file_list = []

        file_names = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(handler.selected_folder_dir, f))
                and f.lower().endswith((".png", ".gif", ".mov", ".avi"))
        ]
        gui.window["-FILE LIST-"].update(file_names)

    # Analyzed video folder selected
    elif event == "-ANALYZES-":
        # Update GUI window
        gui.window["-DELETE VIDEO-"].update(disabled=True)
        gui.window["-VIEW VIDEO-"].update(disabled=True)
        gui.window["-CAM SHIFT-"].update(disabled=True)
        gui.window["-HSV-"].update(disabled=True)

        # Update GUI variables
        gui.window["-IMAGE FRAME-"].update(filename=gui.front_picture)
        gui.window["-TOUT-"].update(value="Disc Golf Tracker")
        handler.selected_folder_dir = os.path.join(handler.root_dir, handler.analyzes_folder_dir)

        try:
            # Get list of files in folder
            file_list = os.listdir(handler.selected_folder_dir)
        except:
            file_list = []

        file_names = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(handler.selected_folder_dir, f))
                and f.lower().endswith((".png", ".gif", ".mov", ".avi"))
        ]

        if not file_names:
            file_names = ["No analyzed videos"]
        gui.window["-FILE LIST-"].update(file_names)

    # A file was selected
    elif event == "-FILE LIST-":

        handler.selected_file_dir = os.path.join(handler.selected_folder_dir, values["-FILE LIST-"][0])

        handler.set_selected_video(file_dir=handler.selected_file_dir, filename=values["-FILE LIST-"][0])

        # Update GUI window
        gui.window["-DELETE VIDEO-"].update(disabled=False)
        gui.window["-VIEW VIDEO-"].update(disabled=False)
        gui.window["-CAM SHIFT-"].update(disabled=False)
        gui.window["-HSV-"].update(disabled=False)

        try:
            #thumb_nail_filename = os.path.join("/Users/magnusbogenbrurok/Documents/DiscTracker/frames",
            #                                    values["-FILE LIST-"][0] + ".png")
            print('settingTN: ', handler.thumbnail_dir)
            gui.window["-IMAGE FRAME-"].update(filename=handler.thumbnail_dir)
            gui.window["-TOUT-"].update(value=handler.get_selected_video_name())



        except:
            pass

    # -------------------------------------- VIDEO ACTIONS --------------------------------------------------------
    # View button pushed
    elif event == "-VIEW VIDEO-":
        handler.play_selected_video()
        #handler.selected_video.play()

    # Cam shift button pushed
    elif event == "-CAM SHIFT-":
        analyze_name = sg.popup_get_text('Enter filename') + ".avi"
        if analyze_name:
            max_spped = handler.cam_shift_selected_video(analyze_name, values['-H MIN-'], values['-H MAX-'],
                                        values['-S MIN-'], values['-S MAX-'],
                                        values['-V MIN-'], values['-V MAX-'])

        gui.window["-MAX SPEED-"].update(value=max_spped)
        print(max_spped)
    # Delete button pushed
    elif event == "-DELETE VIDEO-":
        if sg.popup_yes_no('Delete this video?') == "Yes":
            handler.delete_selected_video()
            sg.popup('Video deleted', keep_on_top=True)

        else:
            sg.popup('Enter new file name.', keep_on_top=True)

    # -------------------------------------- ACTION SETTINGS -------------------------------------------------------
    elif event == "-COLOR BLUE-":
        # Disable other checkboxes
        gui.window["-COLOR XV-"].update(value=False)
        gui.window["-COLOR YV-"].update(value=False)

        # Set handler variables
        handler.trace_color = 'BLUE'

    elif event == "-COLOR XV-":
        # Disable other checkboxes
        gui.window["-COLOR BLUE-"].update(value=False)
        gui.window["-COLOR YV-"].update(value=False)

        # Set handler variables
        handler.trace_color = 'XV'

    elif event == "-COLOR YV-":
        # Disable other checkboxes
        gui.window["-COLOR XV-"].update(value=False)
        gui.window["-COLOR BLUE-"].update(value=False)

        # Set handler variables
        handler.trace_color = 'XY'

    # -------------------------------------- VIDEO SETTINGS -------------------------------------------------------
    # HUE
    elif event == "-HUE-":
        thumb_nail_filename = os.path.join("/Users/magnusbogenbrurok/Documents/DiscTracker/frames",
                                            values["-FILE LIST-"][0] + "_hue.png")
        gui.window["-IMAGE FRAME-"].update(filename=thumb_nail_filename)

    # SATURATION
    elif event == "-SATURATION-":
        thumb_nail_filename = os.path.join("/Users/magnusbogenbrurok/Documents/DiscTracker/frames",
                                            values["-FILE LIST-"][0] + "_saturation.png")
        gui.window["-IMAGE FRAME-"].update(filename=thumb_nail_filename)

    # VALUE
    elif event == "-VALUE-":
        thumb_nail_filename = os.path.join("/Users/magnusbogenbrurok/Documents/DiscTracker/frames",
                                            values["-FILE LIST-"][0] + "_value.png")
        gui.window["-IMAGE FRAME-"].update(filename=thumb_nail_filename)

    # RGB thumbnail
    elif event == "-RGB-":
        thumb_nail_filename = os.path.join("/Users/magnusbogenbrurok/Documents/DiscTracker/frames",
                                            values["-FILE LIST-"][0] + ".png")
        gui.window["-IMAGE FRAME-"].update(filename=thumb_nail_filename)

    # HSV thumbnail
    elif event == "-HSV-":
        handler.hsv_selected_video(values['-H MIN-'], values['-H MAX-'],
                                    values['-S MIN-'], values['-S MAX-'],
                                    values['-V MIN-'], values['-V MAX-'],
                                    video=values['-HSV VIDEO-'])

import PySimpleGUI as sg
import os.path
from gui import GUI, ProgramHandler


def run_event_loop(gui, handler):

    event, values = gui.window.read()

    # Exit Condition
    if event == "Exit" or event == sg.WIN_CLOSED:
            return 1

    # -------------------------------------- FOLDERS AND SELECTION ------------------------------------------------
    # Browse folders
    if event == "-FOLDER-":
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
        print('root_dir: ', handler.root_dir)
        print('video_folder_dir: ', handler.video_folder_dir)
        print('selected folder: ', handler.selected_folder_dir)

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
            thumb_nail_filename = os.path.join("/Users/magnusbogenbrurok/Documents/DiscTracker/frames",
                                                values["-FILE LIST-"][0] + ".png")
            gui.window["-IMAGE FRAME-"].update(filename=thumb_nail_filename)
            gui.window["-TOUT-"].update(value=handler.get_selected_video_name())

        except:
            pass


        #try:
        #    handler.filename = os.path.join(
        #        values["-FOLDER-"], values["-FILE LIST-"][0]
        #    )
        #    copyfile(handler.filename, os.path.join(
        #        "/Users/magnusbogenbrurok/Documents/DiscTracker/img", values["-FILE LIST-"][0]))
        #except:
        #    pass

    # -------------------------------------- VIDEO ACTIONS --------------------------------------------------------
    # View button pushed
    elif event == "-VIEW VIDEO-":
        handler.play_selected_video()
        #handler.selected_video.play()

    # Cam shift button pushed
    elif event == "-CAM SHIFT-":
        analyze_name = sg.popup_get_text('Enter filename') + ".avi"
        if analyze_name:
            handler.cam_shift_selected_video(analyze_name, values['-H MIN-'], values['-H MAX-'],
                                        values['-S MIN-'], values['-S MAX-'],
                                        values['-V MIN-'], values['-V MAX-'])

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


if __name__ == "__main__":

    root_dir = os. getcwd()
    print('root: ', root_dir)

    # Initialize the GUI object
    program_gui = GUI()

    # Initialize the ProgramHandler object
    program_handler = ProgramHandler(root_dir)

    # Run the event loop
    while True:
        exit_condition = run_event_loop(gui=program_gui, handler=program_handler)
        if exit_condition:
            break

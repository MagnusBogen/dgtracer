from src.video_handler.video import Video, calculate_max_speed
import os.path


class ProgramHandler:
    def __init__(self, root):

        # ---------- DIR VARIABLES ----------- #
        self.root_dir = root
        self.video_folder_dir = 'files/videos'
        self.analyzes_folder_dir = 'files/analyzes'
        self.thumbnail_folder_dir = 'files/thumbnails'
        self.thumbnail_dir = ''
        self.selected_folder_dir = ''
        self.selected_file_dir = ''
        self.selected_file_name = ''

        # --------- VIDEO VARIABLES ---------- #
        self._selected_video = Video()

        # ------ VIDEO ACTION VARIABLES ------ #
        self.trace_color = 'XV'

        # ----- COMPARE VIDEO VARIABLES ------ #
        self._trace_1 = []
        self._trace_2 = []

    def set_selected_video(self, filename, file_dir):
        print('set_selected_video')
        self.selected_file_dir = file_dir
        self.selected_file_name = filename
        self.thumbnail_dir = os.path.join(self.thumbnail_folder_dir, (self.selected_file_name + '.png'))
        self._selected_video = Video(file_dir, filename, self.thumbnail_dir)
        self.print_attributes()

    def get_selected_video_name(self):
        print('get_selected_video_name')
        self.print_attributes()
        return self._selected_video.file_name

    def get_thumbnail_path(self):
        return self._thumbnail_dir

    def play_selected_video(self):
        print('play_selected_video')
        self.print_attributes()
        self._selected_video.play()

    def delete_selected_video(self):
        print('delete_selected_video')
        self.print_attributes()
        self._selected_video.delete()

    def cam_shift_selected_video(self, name='', h_min=0, h_max=0, s_min=0, s_max=0, v_min=0, v_max=0):
        print('cam_shift_selected_video')
        save_path = os.path.join(self.root_dir, self.analyzes_folder_dir, name)
        self.print_attributes()
        self._trace_2 = self._trace_1
        self._trace_1 = self._selected_video.cam_shift(name, h_min, h_max, s_min, s_max, v_min, v_max,
                                                       trace_color=self.trace_color, save_path=save_path)
        max_speed = calculate_max_speed(self._trace_1)
        return max_speed

    def track_selected_video(self, tracker="CRST", name='noname'):
        print('track_selected_video')
        self.print_attributes()
        self._selected_video.track(tracker, name)

    def hsv_selected_video(self, h_min=0, h_max=0, s_min=0, s_max=0, v_min=0, v_max=0, video=False):
        print('hsv_selected_video')
        self.print_attributes()
        self._selected_video.generate_hsv(h_min, h_max, s_min, s_max, v_min, v_max, video)

    def print_attributes(self):
        print('root_dir: ', self.root_dir)
        print('video_folder_dir: ', self.video_folder_dir)
        print('analyzes_folder_dir: ', self.analyzes_folder_dir)
        print('thumbnail_folder_dir: ', self.thumbnail_folder_dir)
        print('thumbnail_dir: ', self.thumbnail_dir)
        print('selected_folder: ', self.selected_folder_dir)
        print('selected_file_dir: ', self.selected_file_dir)
        print('selected_file_name: ', self.selected_file_name)
        print('selected video: ', self._selected_video.file_name)

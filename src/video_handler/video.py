import cv2
import os
import numpy as np
import math


class Video:
    def __init__(self, source='', name='', thumbnail_dir=''):
        self.file_name = name
        self.thumb_nail_dir = thumbnail_dir
        self.frame_rate = 0
        self.source = source
        self.detected_pixels = []
        self.line_list = []
        self.video_thumb_nails()

    def delete(self):
        if os.path.exists(self.source):
            #Delete video
            os.remove(self.source)
        else:
            pass
        #Delete TN

        if os.path.exists(self.thumb_nail_dir):
            os.remove(self.thumb_nail_dir)
        else:
            pass

    def play(self):
        cap = cv2.VideoCapture(self.source)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            gray = frame
            cv2.imshow(self.file_name, gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.read()
        cv2.destroyAllWindows()

    def video_thumb_nails(self):
        if not os.path.exists(self.thumb_nail_dir) and self.file_name != '':
            cap = cv2.VideoCapture(self.source)
            video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))-1
            frames =[]
            if cap.isOpened() and video_length > 0:
                frame_ids = [0]
                if video_length >= 4:
                    frame_ids = [0,
                                 round(video_length * 0.25),
                                 round(video_length * 0.5),
                                 round(video_length * 0.75),
                                 video_length - 1]
                count = 0
                success, image = cap.read()
                while success:
                    if count in frame_ids:
                        frames.append(image)
                    success, image = cap.read()
                    count += 1
            img = frames[3]
            scale_percent = 60  # percent of original size
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)
            # resize image
            resized_frame = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
            cv2.imwrite(self.thumb_nail_dir, resized_frame)
        else:
            pass

    def generate_hsv(self, h_min, h_max, s_min, s_max, v_min, v_max, video=False):
        cap = cv2.VideoCapture(self.source)

        # take first frame of the video
        ret, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, np.array((float(h_min), float(s_min), float(v_min))),
                                               np.array((float(h_max), float(s_max), float(v_max))))

        if video:
            while ret:
                ret, frame = cap.read()

                if ret:
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    mask = cv2.inRange(hsv, np.array((float(h_min), float(s_min), float(v_min))),
                                       np.array((float(h_max), float(s_max), float(v_max))))
                    cv2.imshow('img2', mask)
                    k = cv2.waitKey(60) & 0xff
                    if k == 27:
                        break

        else:
            cv2.imshow("mask_red", mask)
            while True:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cap.release()
        cv2.destroyAllWindows()

    def cam_shift(self, name='', h_min=0, h_max=0, s_min=0, s_max=0, v_min=0, v_max=0, trace_color='XV', c_trace=[],
                  save_path=''):
        # Reset line list
        self.line_list = []

        cap = cv2.VideoCapture(self.source)

        # take first frame of the video
        ret, frame = cap.read()

        bbox = cv2.selectROI("Select ROI", frame, False)

        # setup initial location of window
        c, r, h, w = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        track_window = (c, r, h, w)

        # set up the ROI for tracking
        roi = frame[r:r + w, c:c + h]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Auto mask
        # h_avg, s_avg, v_avg = average_hsv_detector(hsv_roi)

        # Manual mask
        mask = cv2.inRange(hsv_roi, np.array((float(h_min), float(s_min), float(v_min))),
                           np.array((float(h_max), float(s_max), float(v_max))))

        # Histogram
        roi_hist = cv2.calcHist([hsv_roi], [0], mask, [255], [0, 255])
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

        # Termination criteria, 10 iteration or move by at least 1 pt
        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
        out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 180.0, (1920, 1080))

        while 1:
            ret, frame = cap.read()

            if ret:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 255], 1)
                cv2.imshow('dst', dst)
                # Meanshift: Get new location
                ret, track_window = cv2.CamShift(dst, track_window, term_crit)

                # Save tracking coordinates
                x = int(ret[0][0])
                y = int(ret[0][1])
                self.line_list.append((x, y))

                # Draw trace on frame
                draw_line(self.line_list, frame, trace_color)

                if c_trace:
                    draw_line(c_trace, frame, trace_color)

                # Show frame
                cv2.imshow('Tracking', frame)

                # Write frame to output file
                out.write(frame)

                k = cv2.waitKey(60) & 0xff
                if k == 27:
                    break
                else:
                    cv2.imwrite(chr(k) + ".jpg", frame)

            else:
                break

        #color_list = get_final_trace_color(self.line_list, "XV")
        #b = create_blank(width=1920, height=1080)
        #draw_line(self.line_list, b, "XV", color_list)
        #show_image(b)
        cv2.destroyAllWindows()
        cap.release()
        out.release()

        return self.line_list


def create_blank(width, height, rgb_color=(0, 0, 0)):
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image


def draw_box(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x,y), ((x+w), (y+h)), (255, 0, 255), 3, 1)
    cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


def draw_line(pt_list, img, t_color, c_list=[]):
    if len(c_list)>2:
        for l in range(0, len(pt_list) - 1):
            if l:
                cv2.line(img, pt_list[l], pt_list[l + 1], c_list[l], 2)
            else:
                pass

    sum_dist = 0
    max_dist = 0

    if t_color == 'BLUE':
        for l in range(0, len(pt_list) - 1):
            if l:
                cv2.line(img, pt_list[l], pt_list[l + 1], (255, 0, 0), 2)
            else:
                pass
    else:
        for l in range(0, len(pt_list)-1):
            dist = euclidean_distance(pt_list[l], pt_list[l + 1])
            sum_dist += dist
            if dist > max_dist:
                max_dist = dist
            tr_color = get_trace_color(pt_list[l], pt_list[l + 1], t_color)
            if l:
                cv2.line(img, pt_list[l], pt_list[l+1], tr_color, 2)
            else:
                pass


def average_hsv_detector(frame):
    height, width, channels = frame.shape
    print(height, width, channels)
    h = 0
    s = 0
    v = 0

    for w in range(0, width-1):
        for he in range(0, height-1):
            h += int(frame[he, w, 0])
            s += int(frame[he, w, 1])
            v += int(frame[he, w, 2])
    h_avg = h/(width * height)
    s_avg = s/(width * height)
    v_avg = v/(width * height)

    return h_avg, s_avg, v_avg


def moving_average(in_data, filter_size=5):
    average_data = []
    for d in range(0, len(in_data)-6):
        sum_x_data = 0
        sum_y_data = 0
        for s in range(0, filter_size-1):
            sum_x_data += in_data[d+s][0]
            sum_y_data += in_data[d+s][1]
        average_data.append((int(sum_x_data/filter_size), int(sum_y_data/filter_size)))
    return average_data


def euclidean_distance(pt1, pt2):
    vector = points_to_vector(pt1, pt2)
    distance = math.sqrt(vector[0]**2 + vector[1]**2)
    return distance


def points_to_vector(pt1, pt2):
    x1 = pt1[0]
    y1 = pt1[1]
    x2 = pt2[0]
    y2 = pt2[1]
    dx = x2 - x1
    dy = y2 - y1
    vector = (dx, dy)
    return vector


def get_trace_color(pt1, pt2, v_dir):
    distance = euclidean_distance(pt1, pt2)
    vector = points_to_vector(pt1, pt2)
    color = None
    color_whiteness = 255 - (50 + (255/500)*(0.3*distance)**2)

    # Define axis
    if v_dir == 'XV':
        d_index = 0
    elif v_dir == 'YV':
        d_index = 1
    else:
        d_index = -1

    # IF vector goes in direction -x : RED
    if vector[d_index] <= 0:
        color = (255, color_whiteness, color_whiteness)

    elif vector[d_index] > 0:
        color = (color_whiteness, 255, color_whiteness)
    # IF vector goes in direction +x : BLUE

    return color


def show_image(frame):
    cv2.imshow('Comparison', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def calculate_max_speed(point_list):
    max_speed = 0
    for l in range(0, len(point_list)-1):
        speed = euclidean_distance(point_list[l], point_list[l+1])
        if speed > max_speed:
            max_speed = speed

    return max_speed



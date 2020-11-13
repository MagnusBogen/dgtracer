import video

p = [(10, 1), (10, 2), (-10, 3), (-10, 8), (10, 7), (10, 5), (-10, 14), (-10, 24), (-10, 26)]
video.get_final_trace_color(p, 'XV')

color_list = video.get_final_trace_color(p, "XV")
b = video.create_blank(width=1920, height=1080)
video.draw_line(p, b, "X", color_list)
video.show_image(b)
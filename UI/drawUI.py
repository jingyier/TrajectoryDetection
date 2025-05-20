import cv2
import numpy as np
import gradio as gr
from threading import Thread, Lock
from queue import Queue
from time import sleep

# 初始化全局变量
penColorHSV = [
    [86, 121, 205, 111, 245, 255],  # 蓝色范围
    [46, 78, 204, 71, 255, 255],  # 绿色范围
    [22, 70, 214, 31, 255, 255]  # 黄色范围
]
penColorBGR = [
    [255, 0, 0],  # 蓝色
    [0, 255, 0],  # 绿色
    [0, 255, 255]  # 黄色
]
drawPoints = []
current_color = 0
lock = Lock()
is_running = True

# 创建队列和共享缓冲区
frame_queue = Queue(maxsize=1)
frame_buffer = np.zeros((480, 640, 3), dtype=np.uint8)


def findPen(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for i in range(len(penColorHSV)):
        lower = np.array(penColorHSV[i][:3])
        upper = np.array(penColorHSV[i][3:6])
        mask = cv2.inRange(hsv, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(max_contour)
            if area > 500:
                ((x, y), radius) = cv2.minEnclosingCircle(max_contour)
                if radius > 10:
                    center = (int(x), int(y))
                    with lock:
                        drawPoints.append([center[0], center[1], i])
                        current_color = i
                    return img, center
    return img, None


def draw(points):
    temp_frame = frame_buffer.copy()
    for point in points:
        if point[2] == current_color:
            cv2.circle(temp_frame, (point[0], point[1]), 10, penColorBGR[current_color], -1)
    return temp_frame


def camera_worker():
    global is_running
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    while is_running:
        ret, frame = cap.read()
        if ret:
            processed_frame, _ = findPen(frame)
            if frame_queue.full():
                frame_queue.get()  # 移除旧帧
            frame_queue.put(processed_frame)
        sleep(0.03)
    cap.release()


def update_canvas():
    while is_running or not frame_queue.empty():
        if not frame_queue.empty():
            frame_buffer[:] = frame_queue.get()
        sleep(0.03)


def get_frame():
    with lock:
        return frame_buffer.copy()


def process_frame(h_params):
    global penColorHSV
    with lock:
        for i in range(3):
            penColorHSV[i] = [
                h_params[i * 6], h_params[i * 6 + 1], h_params[i * 6 + 2],
                h_params[i * 6 + 3], h_params[i * 6 + 4], h_params[i * 6 + 5]
            ]


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🖌️ 虚拟画笔系统")

    with gr.Row():
        canvas = gr.Image(type="numpy", label="画布", height=480)

        with gr.Column():
            gr.Markdown("## HSV参数调节")

            with gr.Accordion("蓝色参数", open=True):
                h_min1, h_max1 = gr.Slider(0, 179, value=86, label="H Min"), gr.Slider(0, 179, value=111, label="H Max")
                s_min1, s_max1 = gr.Slider(0, 255, value=205, label="S Min"), gr.Slider(0, 255, value=245,
                                                                                        label="S Max")
                v_min1, v_max1 = gr.Slider(0, 255, value=205, label="V Min"), gr.Slider(0, 255, value=255,
                                                                                        label="V Max")

            with gr.Accordion("绿色参数"):
                h_min2, h_max2 = gr.Slider(0, 179, value=46, label="H Min"), gr.Slider(0, 179, value=71, label="H Max")
                s_min2, s_max2 = gr.Slider(0, 255, value=204, label="S Min"), gr.Slider(0, 255, value=255,
                                                                                        label="S Max")
                v_min2, v_max2 = gr.Slider(0, 255, value=204, label="V Min"), gr.Slider(0, 255, value=255,
                                                                                        label="V Max")

            with gr.Accordion("黄色参数"):
                h_min3, h_max3 = gr.Slider(0, 179, value=22, label="H Min"), gr.Slider(0, 179, value=31, label="H Max")
                s_min3, s_max3 = gr.Slider(0, 255, value=214, label="S Min"), gr.Slider(0, 255, value=255,
                                                                                        label="S Max")
                v_min3, v_max3 = gr.Slider(0, 255, value=214, label="V Min"), gr.Slider(0, 255, value=255,
                                                                                        label="V Max")

            clear_btn = gr.Button("清空画布")
            clear_btn.click(lambda: [], None, drawPoints)


    # 新增图像更新回调
    def update_image(*args):
        return get_frame()


    canvas.change(
        fn=update_image,
        inputs=[],
        outputs=canvas
    )

# 启动工作线程
Thread(target=camera_worker, daemon=True).start()
Thread(target=update_canvas, daemon=True).start()

try:
    demo.launch(server_name='127.0.0.1', server_port=7860)
finally:
    is_running = False
    sleep(1)
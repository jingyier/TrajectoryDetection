import cv2
import numpy as np
import gradio as gr
from threading import Lock

# 全局状态管理
processing_lock = Lock()
is_detecting = False


def empty(_):
    pass


def process_frame(h_min, h_max, s_min, s_max, v_min, v_max):
    global is_detecting

    with processing_lock:
        if is_detecting:
            return None, None, None, "检测进行中..."

        is_detecting = True

    try:
        # 从摄像头读取最新帧
        ret, frame = cap.read()
        if not ret:
            return None, None, None, "摄像头连接失败"

        # 转换颜色空间
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 处理色相范围可能反转的情况
        h_min, h_max = min(h_min, h_max), max(h_min, h_max)
        s_min, s_max = min(s_min, s_max), max(s_min, s_max)
        v_min, v_max = min(v_min, v_max), max(v_min, v_max)

        # 创建HSV范围
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        # 生成掩膜
        mask = cv2.inRange(hsv, lower, upper)

        # 应用形态学操作去噪
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # 应用掩膜
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # 调整图像尺寸用于显示
        frame_small = cv2.resize(frame, (400, 300))
        mask_small = cv2.resize(mask, (400, 300))
        result_small = cv2.resize(result, (400, 300))

        return frame_small, mask_small, result_small, "检测完成"

    finally:
        with processing_lock:
            is_detecting = False


def reset_state():
    global is_detecting
    with processing_lock:
        is_detecting = False
    return None, None, None, ""


# 初始化摄像头
cap = cv2.VideoCapture(0)

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 实时颜色检测系统")

    with gr.Row():
        # 参数控制栏（占1/4宽度）
        with gr.Column(scale=1):
            gr.Markdown("## HSV参数调节")

            hue_group = gr.Group()
            with hue_group:
                h_min = gr.Slider(0, 179, value=0, label="Hue Min")
                h_max = gr.Slider(0, 179, value=179, label="Hue Max")

            sat_group = gr.Group()
            with sat_group:
                s_min = gr.Slider(0, 255, value=0, label="Sat Min")
                s_max = gr.Slider(0, 255, value=255, label="Sat Max")

            val_group = gr.Group()
            with val_group:
                v_min = gr.Slider(0, 255, value=0, label="Val Min")
                v_max = gr.Slider(0, 255, value=255, label="Val Max")

            btn_start = gr.Button("开始检测")
            btn_reset = gr.Button("重置状态")

            gr.Examples(
                examples=[["Hue Min: 30", "Hue Max: 90", "Sat Min: 50", "Sat Max: 255", "Val Min: 50", "Val Max: 255"]],
                inputs=[h_min, h_max, s_min, s_max, v_min, v_max],
                fn=process_frame
            )

        # 图像显示区（占3/4宽度）
        with gr.Column(scale=3):
            with gr.Row():
                img_out = gr.Image(label="原始图像", type="numpy")
                mask_out = gr.Image(label="颜色掩膜", type="numpy")
            with gr.Row():
                result_out = gr.Image(label="检测结果", type="numpy")
            status_output = gr.Textbox(label="状态", interactive=False)

    # 事件绑定
    btn_start.click(
        fn=process_frame,
        inputs=[h_min, h_max, s_min, s_max, v_min, v_max],
        outputs=[img_out, mask_out, result_out, status_output]
    )

    btn_reset.click(
        fn=reset_state,
        inputs=[],
        outputs=[img_out, mask_out, result_out, status_output]
    )

demo.launch()
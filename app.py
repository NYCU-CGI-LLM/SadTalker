import os, sys
import tempfile
import gradio as gr
from src.gradio_demo import SadTalker
# from src.utils.text2speech import TTSTalker
from huggingface_hub import snapshot_download

default_batch_size = int(os.environ.get('BATCH_SIZE', 4))
server_port = int(os.environ.get('SERVER_PORT', 7860))

def download_model():
    REPO_ID = 'vinthony/SadTalker-V002rc'
    snapshot_download(repo_id=REPO_ID, local_dir='./checkpoints', local_dir_use_symlinks=True)

def sadtalker_demo():

    download_model()

    sad_talker = SadTalker(lazy_load=True)
    # tts_talker = TTSTalker()

    # params that I didn't use
    length_of_audio = 5
    use_idle_mode = False
    ref_info = 'pose'
    use_ref_video = False

    with gr.Blocks() as demo:
        gr.Markdown(
        """
        <div style='text-align:center;'>影片生成工具</div>
        """)
        with gr.Accordion("使用說明"):
            gr.Markdown("請上傳一張照片以及一個音檔，並設定相關參數，按下生成即可看到結果。再進行下一次生成前，請先點擊重整頁面，並重新上傳圖片以及音檔")

        with gr.Row():
            with gr.Column():
                gr.Markdown("# 輸入資料")
                source_image = gr.Image(label="來源圖片", type='filepath', height=300)
                driven_audio = gr.Audio(label="輸入音訊", type='filepath')
                ref_video = gr.Video(label="Reference Video", visible=False)


            with gr.Column():
                gr.Markdown("# 參數設定")
                with gr.Column():
                    pose_style = gr.Slider(minimum=0, maximum=45, step=1, label="Pose style", value=0, interactive=True, visible=False)
                    exp_weight = gr.Slider(minimum=0, maximum=3, step=0.1, label="表情幅度 (數值越大，眼睛嘴巴移動越明顯)", value=1, interactive=True, visible=True)
                    batch_size = gr.Slider(label="Batch size in generation", step=1, maximum=10, value=default_batch_size, interactive=False, visible=False)

                with gr.Column():
                    size_of_image = gr.Radio([256, 512], value=512, label="Face model resolution", interactive=False, visible=False)
                    preprocess_type = gr.Radio(['crop', 'resize', 'full', 'extcrop', 'extfull'], value='full', label='Preprocess type', interactive=False, visible=False)
                    facerender = gr.Radio(['facevid2vid', 'pirender'], value='facevid2vid', label='Face render type', interactive=False, visible=False)
                with gr.Column():
                    blink_every = gr.Checkbox(label="是否在生成影片中啟用眨眼", value=True, interactive=True, visible=True)
                    is_still_mode = gr.Checkbox(label="Still Mode (fewer head motions)", value=True, interactive=False, visible=False)
                    enhancer = gr.Checkbox(label="Use GFPGAN as Face enhancer", value=True, interactive=False, visible=False)

                submit = gr.Button('生成', elem_id="sadtalker_generate", variant='primary')

                gr.Markdown("# 結果")
                gen_video = gr.Video(label="生成的影片", height=300)

        # events
        submit.click(
            fn=lambda img, audio, pre_type, still_mode, enhancer, batch_size, size, pose, render, exp, ref_video, blink:
                sad_talker.test(
                    img, audio, pre_type, still_mode, enhancer,
                    batch_size, size, pose, render, exp, use_ref_video,
                    ref_video, ref_info, use_idle_mode, length_of_audio, blink),
            inputs=[
                source_image,            # img
                driven_audio,            # audio
                preprocess_type,         # pre_type
                is_still_mode,           # still_mode
                enhancer,                # enhancer
                batch_size,              # batch_size
                size_of_image,           # size
                pose_style,              # pose
                facerender,              # render
                exp_weight,              # exp
                # use_ref_video,           # use_ref
                ref_video,               # ref_video
                # ref_info,               # ref_info
                # use_idle_mode,           # idle_mode
                # length_of_audio,         # length
                blink_every              # blink
            ],
            outputs=[gen_video]
        )

    return demo


if __name__ == "__main__":

    demo = sadtalker_demo()
    demo.queue(max_size=10, api_open=True)
    demo.launch(server_name="0.0.0.0", server_port=server_port)

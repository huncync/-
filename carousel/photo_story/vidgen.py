# 영상 장 만들기: 원본 영상(세로) → 1080×1350 자르기 · 채도/밝기 낮추기 · 글 상자 PNG 얹기 · 최대 6초 · 소리 없음 MP4 + 미리보기 JPG
import subprocess
def make(src, overlay_png, out_mp4, out_jpg, start=0.0, dur=6.0, yoff=285):
    vf = (f"scale=1080:1920,crop=1080:1350:0:{yoff},eq=saturation=0.5:brightness=-0.07:contrast=0.95[v];"
          f"[v][1:v]overlay=0:0,format=yuv420p")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(start), '-t', str(dur), '-i', src, '-i', overlay_png,
                    '-filter_complex', vf, '-an', '-r', '30', '-c:v', 'libx264', '-crf', '20', '-preset', 'medium',
                    '-movflags', '+faststart', out_mp4], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(min(1.0, dur / 2)), '-i', out_mp4, '-frames:v', '1', '-q:v', '3', out_jpg], check=True)

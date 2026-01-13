import subprocess
import os
import shutil
import time
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YOLO_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "yolov5"))
RESULT_FOLDER = os.path.join(BASE_DIR, "results")
WEIGHTS = "yolov5s.pt"

os.makedirs(RESULT_FOLDER, exist_ok=True)

def run_yolo(input_video, output_filename):
    output_path = os.path.join(RESULT_FOLDER, output_filename)

    if not os.path.exists(input_video):
        raise FileNotFoundError(f"Input video not found: {input_video}")
    
    print(f"✓ Input video exists: {input_video}")
    print(f"  File size: {os.path.getsize(input_video)/(1024*1024):.2f} MB")

    # Run YOLO in real-time, print logs as they appear
    command = f'python detect.py --weights {WEIGHTS} --source "{input_video}" --project runs/detect --name exp --exist-ok --nosave --view-img --conf 0.25 --vid-stride 2'
    
    print(f"\nRunning YOLO command:\n  {command}\nWorking dir: {YOLO_PATH}\n")
    
    start_time = time.time()
    vehicle_counts = {"lane_1":0, "lane_2":0, "lane_3":0, "lane_4":0}  # initial counts
    
    # Stream stdout live
    process = subprocess.Popen(
        command,
        cwd=YOLO_PATH,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in process.stdout:
        line = line.strip()
        if line:
            print(line)  # logs frame-by-frame to terminal

            # Optional: parse vehicle counts live from YOLO stdout
            # Example: look for "lane X: N" pattern
            match = re.findall(r'lane_(\d+):\s*(\d+)', line)
            for m in match:
                lane, count = m
                vehicle_counts[f"lane_{lane}"] = int(count)

    process.wait()
    elapsed_time = time.time() - start_time
    print(f"\n✓ YOLO completed in {elapsed_time:.2f} seconds\n")

    # YOLO output video is in runs/detect/exp
    yolo_output_dir = os.path.join(YOLO_PATH, "runs", "detect", "exp")
    files = os.listdir(yolo_output_dir)
    detected_video_path = None
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    
    for file in files:
        if any(file.lower().endswith(ext) for ext in video_extensions):
            detected_video_path = os.path.join(yolo_output_dir, file)
            break

    if not detected_video_path:
        raise FileNotFoundError(f"YOLO did not produce output video in {yolo_output_dir}")

    shutil.copy2(detected_video_path, output_path)
    print(f"✓ Video saved to results folder: {output_path}\n")

    return vehicle_counts, f"/results/{output_filename}"

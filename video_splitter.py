import os
import sys

def split_video(file_path, output_dir="fragments", num_parts=10):
    with open(file_path, 'rb') as f:
        video_data = f.read()
    size = len(video_data)
    fragment_size = size // num_parts

    os.makedirs(output_dir, exist_ok=True)

    for i in range(num_parts):
        start = i * fragment_size
        end = start + fragment_size if i < num_parts - 1 else size
        with open(f"{output_dir}/fragment_{i}.bin", "wb") as frag:
            frag.write(video_data[start:end])
    print(f"[✓] Video dividido en {num_parts} fragmentos.")

if __name__ == "__main__":
    split_video("prueba1.mp4")
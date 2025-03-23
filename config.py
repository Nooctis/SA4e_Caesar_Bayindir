import json
import subprocess
import sys

def load_track_config(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def start_segments(track_data):
    processes = []
    for track in track_data["tracks"]:
        for segment in track["segments"]:
            seg_id = segment["segmentId"]
            seg_type = segment["type"]
            next_segs = segment["nextSegments"]
            # Aufbau des Befehls für segment.py
            cmd = ["python", "segment.py", "--id", seg_id, "--type", seg_type, "--next"] + next_segs
            print(f"Starte Segment: {cmd}")
            processes.append(subprocess.Popen(cmd))
    return processes

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <track_config.json>")
        sys.exit(1)
    track_config_file = sys.argv[1]
    track_data = load_track_config(track_config_file)
    processes = start_segments(track_data)
    for p in processes:
        p.wait()

if __name__ == "__main__":
    main()

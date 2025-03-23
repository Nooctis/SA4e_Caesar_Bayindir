#!/usr/bin/env python3
import sys
import json
import random

def generate_tracks(num_tracks: int, length_of_track: int):
    """
    Generiert eine Datenstruktur mit 'num_tracks' kreisförmigen Strecken.
    Jeder Track hat 'length_of_track' Segmente:
      - Segment 1: immer 'start-goal'
      - Falls length_of_track >= 3: an einer zufälligen Position (außer 1 und letztem) wird ein 'caesar'-Segment eingefügt.
      - Für die übrigen Segmente: mit 20% Wahrscheinlichkeit 'bottleneck', sonst 'normal'.
      - Das letzte Segment (oder der letzte generierte) verweist zurück auf 'start-goal'.
    """
    all_tracks = []

    for t in range(1, num_tracks + 1):
        track_id = str(t)
        segments = []

        # 1. Start-/Zielsegment
        start_segment_id = f"start-and-goal-{t}"
        # Falls Track-Länge 1 => Schleife auf sich selbst
        if length_of_track == 1:
            next_segments = [start_segment_id]
        else:
            next_segments = [f"segment-{t}-1"]

        segments.append({
            "segmentId": start_segment_id,
            "type": "start-goal",
            "nextSegments": next_segments
        })

        # Bestimme, falls möglich, eine Position für das Caesar-Segment:
        caesar_index = None
        if length_of_track >= 3:
            # Wähle zufällig zwischen 2 und (L-1) als Caesar-Position
            caesar_index = random.randint(2, length_of_track - 1)

        # Erzeuge die restlichen Segmente:
        for c in range(1, length_of_track):
            seg_id = f"segment-{t}-{c}"
            # Letztes Segment: nächstes Segment ist der Start
            if c == length_of_track - 1:
                next_segs = [start_segment_id]
            else:
                next_segs = [f"segment-{t}-{c+1}"]

            # Entscheide den Segmenttyp:
            # Wenn c entspricht dem festgelegten caesar_index, dann Typ "caesar"
            if caesar_index and c == caesar_index:
                seg_type = "caesar"
            else:
                # Mit 20% Wahrscheinlichkeit Bottleneck, sonst normal
                seg_type = "bottleneck" if random.random() < 0.2 else "normal"

            segments.append({
                "segmentId": seg_id,
                "type": seg_type,
                "nextSegments": next_segs
            })

        track_definition = {
            "trackId": track_id,
            "segments": segments
        }
        all_tracks.append(track_definition)

    return {"tracks": all_tracks}

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <num_tracks> <length_of_track> <output_file>")
        sys.exit(1)

    num_tracks = int(sys.argv[1])
    length_of_track = int(sys.argv[2])
    output_file = sys.argv[3]

    tracks_data = generate_tracks(num_tracks, length_of_track)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(tracks_data, f, indent=2)
        f.write('\n')
    print(f"Successfully generated {num_tracks} track(s) of length {length_of_track} into '{output_file}'")

if __name__ == "__main__":
    main()

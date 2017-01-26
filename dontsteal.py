import math
import osuapi
import tkinter as tk
from tkinter import filedialog
from datetime import datetime, timedelta
from osrparse.replay import parse_replay_file
from osrparse.enums import GameMode, Mod


def open_replay():
    options = {"defaultextension": ".osr",
               "filetypes": [("osu! replay file", ".osr")],
               "title": "Open the replay files to analyze"}
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(**options)
    return parse_replay_file(file_path)


def analyze(replay):
    if replay.game_mode is GameMode.Standard and replay.game_version >= 20140226:
        print(str(osuapi.get_beatmap_info(replay.beatmap_hash))[2:-2])
        # convert windows ticks in datetime
        replay_date = datetime(1, 1, 1) + timedelta(microseconds=replay.timestamp / 10)
        print("REPLAY INFO: " + "played by " + replay.player_name + " on "
              + replay_date.strftime("%Y-%m-%d %H:%M:%S") + "\n")
        print("Mods:")
        for mods_used in replay.mod_combination:
            print(str(mods_used).split("Mod.")[1])
        score = ["\nTotal Score: %s" % replay.score, "300s: %s" % replay.number_300s,
                 "100s: %s" % replay.number_100s, "50s: %s" % replay.number_50s, "Gekis: %s" % replay.gekis,
                 "Katus: %s" % replay.katus, "Misses: %s" % replay.misses, "Max Combo: %s" % replay.max_combo]
        for sc in score:
            print(sc)
        if replay.is_perfect_combo:
            print("Perfect Combo!\n")
        else:
            print("")
    else:
        raise ValueError("Can't analyze this replay, it might be too old or not for osu!standard.")
    return


def get_events_per_second(replay):
    events = []
    time = 0

    for event in replay.play_data:
        time += event.time_since_previous_action
        if 1000*len(events) <= time:
            new_y = event.y if Mod.HardRock not in replay.mod_combination else 384-event.y
            events.append([event.x, new_y, event.keys_pressed])
    return events


def get_events_per_second_api(replay, mods):
    events = []
    time = 0
    replay_events = replay.split(",")

    for event in replay_events:
        values = event.split("|")
        try:
            time += float(values[0])
        except ValueError:
            continue
        if 1000*len(events) <= time:
            new_y = float(values[2]) if "HR" not in mods else 384-float(values[2])
            events.append([float(values[1]), new_y, float(values[3])])
    return events


def compare_data(positions1, positions2):
    length = len(positions1) if len(positions1) <= len(positions2) else len(positions2)
    closeness = []
    same_keys_pressed = 0
    not_same_keys_pressed = 0

    for x in range(0, length - 1):
        first_p = positions1[x]
        second_p = positions2[x]
        x = first_p[0] - second_p[0]
        y = first_p[1] - second_p[1]
        closeness.append(math.sqrt(x ** 2 + y ** 2))
        if first_p[2] == second_p[2]:
            same_keys_pressed += 1
        else:
            not_same_keys_pressed += 1

    same_key_percentage = (100 * same_keys_pressed) / (same_keys_pressed + not_same_keys_pressed)
    different_key_percentage = 100 - same_key_percentage
    return closeness, same_key_percentage, different_key_percentage


if __name__ == "__main__":
    fr = open_replay()
    sr = open_replay()
    analyze(fr)
    analyze(sr)
    fr_positions = get_events_per_second(fr)
    sr_positions = get_events_per_second(sr)

    print("Analyzing replay data...\n")

    comparison = compare_data(fr_positions, sr_positions)

    print("Cases where the same keys were pressed: %s%%\n" % comparison[1] +
          "Cases where the pressed keys were different: %s%%\n" % comparison[2])
    print("Lowest values:")

    for comp_values in sorted(comparison[0])[1:11]:
        print(comp_values)

    print("\nAverage of similarity:")
    print(sum(comparison[0]) / len(comparison[0]))

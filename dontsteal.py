import math
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
        print("Analyzing replay data...\n")
        # convert windows ticks in datetime
        replay_date = datetime(1, 1, 1) + timedelta(microseconds=replay.timestamp / 10)
        print("Played by " + replay.player_name + " on " + replay_date.strftime("%Y-%m-%d %H:%M:%S"))
        if replay.mod_combination is Mod.NoMod:
            pass
        else:
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
            pass
    else:
        print("Can't analyze this replay...please check if it's for osu!standard and it's not too old")
    return

fr = open_replay()
sr = open_replay()


def get_events_per_second(replay):
    events = []
    time = 0

    for event in replay.play_data:
        time += event.time_since_previous_action
        if 1000*len(events) <= time:
            events.append([event.x, event.y, event.keys_pressed])
    return events

analyze(fr)
analyze(sr)

fr_positions = get_events_per_second(fr)
sr_positions = get_events_per_second(sr)

length = len(fr_positions) if len(fr_positions) <= len(sr_positions) else len(sr_positions)

closeness = []
same_keys_pressed = 0
not_same_keys_pressed = 0

for x in range(0, length-1):
    first_p = fr_positions[x]
    second_p = sr_positions[x]
    x = first_p[0] - second_p[0]
    y = first_p[1] - second_p[1]
    closeness.append(math.sqrt(x**2 + y**2))
    if first_p[2] == second_p[2]:
        same_keys_pressed += 1
    else:
        not_same_keys_pressed += 1

same_key_percentage = (100*same_keys_pressed) / (same_keys_pressed+not_same_keys_pressed)
different_key_percentage = 100 - same_key_percentage

print("\nCases where the same keys were pressed: %s%%\n" % same_key_percentage +
      "Cases where the pressed keys were different: %s%%\n" % different_key_percentage)
print("Lowest values:")
for values in sorted(closeness)[1:11]:
    print(values)
print("\nAverage of similarity:")
print(sum(closeness)/len(closeness))

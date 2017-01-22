import dontsteal
import osuapi

da_replay = dontsteal.open_replay()
dontsteal.analyze(da_replay)
da_replay_events = dontsteal.get_events_per_second(da_replay)
le_beatmap_id = osuapi.get_beatmap(da_replay.beatmap_hash)
top_50_replays = osuapi.get_replays(le_beatmap_id)
output = ""


def print_chan(cute):
    global output
    output += "%s\n" % cute
    return

for top_replay in top_50_replays:
    replay_events = dontsteal.get_events_per_second_api(top_replay[0], top_replay[1])
    comparison = dontsteal.compare_data(da_replay_events, replay_events)
    print_chan("Comparing to %s's replay" % top_replay[2])
    print_chan("\nCases where the same keys were pressed: %s%%\n" % comparison[1] +
               "Cases where the pressed keys were different: %s%%\n" % comparison[2])
    if comparison[1] >= 90:
        print("Suspicious key-press percentage: %s with %s's replay" % (comparison[1], top_replay[2]))
    print_chan("Lowest values:")
    suspicious = True
    for values in sorted(comparison[0])[1:11]:
        if values >= 1:
            suspicious = False
        print_chan(values)
    if suspicious:
        print("Suspicious lowest values with %s's replay" % top_replay[2])
    print_chan("\nAverage of similarity:")
    average_value = sum(comparison[0]) / len(comparison[0])
    if average_value <= 15:
        print("Suspicious average: %s with %s's replay" % (average_value, top_replay[2]))
    print_chan(average_value)
try:
    with open("analysis.txt", "w") as f:
        f.write(output)
except OSError as e:
    print("Error: ", e)

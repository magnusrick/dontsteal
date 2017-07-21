"""Compares a replay against the top 50 of its beatmap"""
import sys
import osuapi
import dontsteal

da_replay = dontsteal.open_replay()
dontsteal.analyze(da_replay)
da_replay_events = dontsteal.get_events_per_second(da_replay)
le_beatmap_id = osuapi.get_beatmap(da_replay.beatmap_hash)
top_50_replays = osuapi.get_replays(le_beatmap_id)
output = ""


def print_chan(cute):
    """Print it cuter"""
    global output
    output += "%s\n" % cute
    return

if not top_50_replays:
    print("Beatmap not ranked, can't download replays!")
    sys.exit(1)

SUSPICIOUS = False
for top_replay in top_50_replays:
    replay_events = dontsteal.get_events_per_second_api(top_replay[0], top_replay[1])
    comparison = dontsteal.compare_data(da_replay_events, replay_events)
    print_chan("\nComparing to %s's replay" % top_replay[2])
    print_chan("\nCases where the same keys were pressed: %s%%" % comparison[1] +
               "\nCases where the pressed keys were different: %s%%" % comparison[2])
    if comparison[1] >= 95:
        SUSPICIOUS = True
        print("""Suspicious same keys pressed percentage:
              {0:.2f}% with {top_player}'s replay""".format(comparison[1],
                                                            top_player=top_replay[2]))
    print_chan("Lowest values:")
    suspicious_low_values = True
    for values in sorted(comparison[0])[1:11]:
        if values >= 1:
            suspicious_low_values = False
        print_chan(values)
    if suspicious_low_values:
        SUSPICIOUS = True
        print("""Suspicious lowest values with
              {top_player}'s replay""".format(top_player=top_replay[2]))
    print_chan("\nAverage of similarity:")
    average_value = sum(comparison[0]) / len(comparison[0])
    if average_value <= 15:
        SUSPICIOUS = True
        print("""Suspicious average of similarity:
              {0:.4f} with {top_player}'s replay""".format(average_value,
                                                           top_player=top_replay[2]))
    print_chan(average_value)
if not SUSPICIOUS:
    print("\nNothing suspicious going on here!")

try:
    with open("analysis.txt", "w") as f:
        f.write(output)
        f.close()
except OSError as error:
    print("OS Error: {0}".format(error))
    sys.exit(1)

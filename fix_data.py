import csv
import pathlib

DATA_DIR = pathlib.Path("./data")

file_in = DATA_DIR / "data.csv"
file_out = DATA_DIR / "data_fixed.csv"

f = open(file_in, "r")
g = open(file_out, "w", newline="")

reader = csv.reader(f)
writer = csv.writer(g, quoting=csv.QUOTE_ALL)

index = 0

last_player_line = ""

for row in reader:
    if reader.line_num == 1:
        writer.writerow(row)
        continue

    if index == 88594:
        index += 1
        writer.writerow(
            [
                index,
                "Taming of the Shrew",
                0,
                "",
                "ACT TITLE",
                "PROLOGUE",
            ]
        )

    data_line, play, player_linenumber, act_scene_line, player, player_line = row
    index += 1

    if player_line.startswith("ACT"):
        writer.writerow([index, play, 0, "", "ACT TITLE", player_line])
    elif player_line.startswith("SCENE"):
        writer.writerow([index, play, 0, "", "SCENE TITLE", player_line])
    elif player_line.startswith("PROLOGUE"):
        if last_player_line.startswith("ACT"):
            writer.writerow([index, play, 0, "", "SCENE TITLE", player_line])
        else:
            writer.writerow([index, play, 0, "", "ACT TITLE", player_line])
    elif act_scene_line == "":
        writer.writerow([index, play, 0, "", "ACTION", player_line])
    else:
        writer.writerow(
            [index, play, player_linenumber, act_scene_line, player, player_line]
        )

f.close()
g.close()

import csv
import pathlib
import shutil


INPUT_DIR = pathlib.Path("./input")
OUTPUT_DIR = pathlib.Path("./output")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


if (INPUT_DIR / "style.css").exists():
    shutil.copy(INPUT_DIR / "style.css", OUTPUT_DIR)


def write_html(path, style_path, content):
    with open(path, "w") as f:
        f.write(f'<link rel="stylesheet" href="{style_path}"/>')
        f.write(content)


with open(INPUT_DIR / "data.csv", "r") as f:
    reader = csv.reader(f)

    plays_index = ""
    play_index = ""
    act_content = ""

    curr_play = ""
    curr_act = ""
    curr_scene = ""
    curr_player = ""

    scene_number = 0

    plays_index += '<p class="toc-title">Table of Contents</p>'
    plays_index += '<ul class="play-list">'

    for row in reader:
        if reader.line_num == 1:
            continue

        data_line, play, player_linenumber, act_scene_line, player, player_line = row

        if play != curr_play:
            if curr_play != "":
                play_index += "</ul>"
                write_html(
                    OUTPUT_DIR / curr_play / f"{curr_act}.html",
                    "../style.css",
                    act_content,
                )

                play_index += "</ul>"
                write_html(
                    OUTPUT_DIR / curr_play / "index.html",
                    "../style.css",
                    play_index,
                )

                play_index = ""

            (OUTPUT_DIR / play).mkdir(exist_ok=True)

            curr_play = play
            curr_act = ""
            curr_scene = ""
            curr_player = ""

            scene_number = 0

            act_content = ""

            play_index += f'<p class="play-title">{play}</p>'
            play_index += '<ul class="act-list">'

            plays_index += (
                f'<li class="play-link"><a href="./{play}/index.html">{play}</a></li>'
            )

        if player_line.startswith("ACT"):
            if curr_act != "":
                play_index += "</ul>"

                write_html(
                    OUTPUT_DIR / curr_play / f"{curr_act}.html",
                    "../style.css",
                    act_content,
                )

            curr_act = player_line

            scene_number = 0

            act_content = ""

            act_content += f'<p class="play-title">{play}</p>'
            act_content += f'<p class="act-title">{player_line}</p>'

            play_index += f'<li class="act-link"><a href="./{curr_act}.html">{player_line}</a></li>'
            play_index += f'<ul class="scene-list">'

        elif player_line.startswith("SCENE") or player_line.startswith("PROLOGUE"):
            curr_scene = player_line

            scene_number += 1
            act_content += f'<p id="{scene_number}" class="scene-title">{player_line}</p>'

            play_index += f'<li class="scene-link"><a href="./{curr_act}.html#{scene_number}">{player_line}</a></li>'
        elif act_scene_line == "":
            act_content += f'<p class="action">{player_line}</p>'
        else:
            if player != curr_player:
                curr_player = player
                act_content += f'<p class="player">{player}</p>'
            act_content += f'<p class="line">{player_line}</p>'

    write_html(
        OUTPUT_DIR / curr_play / f"{curr_act}.html",
        "../style.css",
        act_content,
    )

    play_index += "</ul>"
    write_html(
        OUTPUT_DIR / curr_play / "index.html",
        "../style.css",
        play_index,
    )

    plays_index += "</ul>"
    write_html(OUTPUT_DIR / "index.html", "./style.css", plays_index)

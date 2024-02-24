import csv
import pathlib
import shutil


BASE_DIR = pathlib.Path("./")

DATA_DIR = BASE_DIR / "data"
CSS_DIR = BASE_DIR / "css"
OUTPUT_DIR = BASE_DIR / "docs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


if CSS_DIR.exists():
    shutil.copy(CSS_DIR / "style.css", OUTPUT_DIR)


def write_html(path, title, content):
    output_dir = pathlib.Path(path).parent
    output_dir_rel = pathlib.Path("./")

    while OUTPUT_DIR != output_dir:
        output_dir = output_dir.parent
        output_dir_rel /= ".."

    style_path = output_dir_rel / "style.css"

    with open(path, "w") as f:
        f.write(
            "<html>"
            + "<head>"
            + f"<title>{title}</title>"
            + f'<link rel="stylesheet" href="{style_path.as_posix()}"/>'
            + "</head>"
            + f"<body>{content}</body>"
            + "</html>"
        )


with open(DATA_DIR / "data_fixed.csv", "r") as f:
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
                    f"{curr_play}: {curr_act}",
                    act_content,
                )

                play_index += "</ul>"
                write_html(
                    OUTPUT_DIR / curr_play / "index.html",
                    curr_play,
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

        if player == "ACT TITLE":
            if curr_act != "":
                play_index += "</ul></li>"

                write_html(
                    OUTPUT_DIR / curr_play / f"{curr_act}.html",
                    f"{curr_play}: {curr_act}",
                    act_content,
                )

            curr_act = player_line

            scene_number = 0

            act_content = ""

            act_content += f'<p class="play-title">{play}</p>'
            act_content += f'<p class="act-title">{player_line}</p>'

            play_index += (
                f'<li class="act-link"><a href="./{curr_act}.html">{player_line}</a>'
            )
            play_index += f'<ul class="scene-list">'

        elif player == "SCENE TITLE":
            curr_scene = player_line

            scene_number += 1
            act_content += (
                f'<p id="{scene_number}" class="scene-title">{player_line}</p>'
            )

            play_index += f'<li class="scene-link"><a href="./{curr_act}.html#{scene_number}">{player_line}</a></li>'

        elif player == "ACTION":
            act_content += f'<p class="action">{player_line}</p>'

        else:
            if player != curr_player:
                curr_player = player
                act_content += f'<p class="player">{player}</p>'
            act_content += f'<p class="line">{player_line}</p>'

    write_html(
        OUTPUT_DIR / curr_play / f"{curr_act}.html",
        f"{curr_play}: {curr_act}",
        act_content,
    )

    play_index += "</ul>"
    write_html(
        OUTPUT_DIR / curr_play / "index.html",
        curr_play,
        play_index,
    )

    plays_index += "</ul>"
    write_html(OUTPUT_DIR / "index.html", "Table of Contents", plays_index)

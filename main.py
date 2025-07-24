# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pexpect>=4.9.0",
#     "termtosvg>=1.1.0",
# ]
# ///
from pathlib import Path
from string import Template
import subprocess
import tempfile
import sys
import re
import shlex

from termtosvg.main import record_render_subcommand, DEFAULT_LOOP_DELAY
from termtosvg.config import validate_geometry

# Config

PADDING = 10  # Size of the empty space around the borders of the image
GEOMETRY = sys.argv[2]  # Size in terminal cells of the output. Example: "117x22". Use "0" to try to adjust the size automatically (if the command uses ANSI escape sequences, it must automatically disable them when not printing to a tty)
COMMAND = " ".join(sys.argv[3:])  # Command to run
OUT_PATH = sys.argv[1]  # Path to the output file

COLORS = {  # Color palette used
    "foreground": "#000000",
    "background": "#eeeeee",
    "color0": "#ffffff",
    "color1": "#cc0403",
    "color2": "#19cb00",
    "color3": "#eb6e00",
    "color4": "#0d73cc",
    "color5": "#cb1ed1",
    "color6": "#0dcdcd",
    "color7": "#767676",
    "color8": "#dddddd",
    "color9": "#f2201f",
    "color10": "#189900",
    "color11": "#ff9800",
    "color12": "#1a8fff",
    "color13": "#fd28ff",
    "color14": "#00bbcc",
    "color15": "#000000",
}

# Generate template

colors_template = "\n            ".join(
    [f".{k} {{fill: {v};}}" for k, v in COLORS.items()]
)

# Termtosvg default template
template = Template(r"""
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" id="terminal" baseProfile="full" viewBox="0 0 $size_x $size_y" width="$size_x" version="1.1">
    <defs>
        <termtosvg:template_settings xmlns:termtosvg="https://github.com/nbedos/termtosvg">
            <termtosvg:screen_geometry columns="82" rows="19"/>
            <termtosvg:animation type="css"/>
        </termtosvg:template_settings>
        <style type="text/css" id="generated-style"></style>
        <style type="text/css" id="user-style">
            /* The colors defined below are the default 16 colors used for rendering text of the terminal. Adjust
               them as needed. */
            $colors
        </style>
    </defs>
    <rect id="terminalui" class="background" width="100%" height="100%"/>
    <svg id="screen" width="656" height="323" x="$padding" y="$padding" viewBox="0 0 656 323" preserveAspectRatio="xMidYMin slice">
    </svg>
</svg>
""")

_SIZE_X = 656
_SIZE_Y = 323
template = template.substitute(
    colors=colors_template,
    padding=PADDING,
    size_x=_SIZE_X + 2 * PADDING,
    size_y=_SIZE_Y + 2 * PADDING,
)

# Command to get the output from. We run a second script to adjust the
# formatting of the output
_CMD = f"{sys.executable} {Path(__file__).parent / 'print.py'} '{COMMAND}'"


def replacer(match: re.Match[str]) -> str:
    color = match.group(1)
    grey = color[:2]
    if color != grey * 3:
        return match.group(0)
    grey = int(grey, 16)
    grey = hex(255 - grey)[2:]
    return f'fill="#{grey * 3}"'


if __name__ == "__main__":
    if GEOMETRY == "0":
        # Try to automatically adjust the size of the terminal needed to avoid
        # line wraps
        res = subprocess.getoutput(f"{_CMD} 1")
        lines = res.splitlines()
        y = max(len(lines), 2)
        x = max(len(line) for line in lines)
        geometry = (x, y)
        print(f"Detected geometry: {x}x{y}")

    else:
        geometry = validate_geometry(GEOMETRY)

    # Termtosvg generates frames of a video, so we need to create a temp
    # directory to store them and then get the last one
    with tempfile.TemporaryDirectory(prefix="termsvg_out") as dir:
        record_render_subcommand(
            process_args=shlex.split(_CMD),
            still=True,
            template=template.encode(),
            geometry=geometry,
            output_path=dir,
            # defaults
            input_fileno=sys.stdin.fileno(),
            output_fileno=sys.stdout.fileno(),
            min_frame_duration=1,
            max_frame_duration=None,
            loop_delay=DEFAULT_LOOP_DELAY,
        )

        print("\033[?25h")  # Show the cursor again
        # Read the last frame
        results = list(Path(dir).iterdir())
        results.sort(key=lambda path: path.name)
        with open(results[-1], "r", encoding="UTF-8") as f:
            data = f.read()

    # Invert greyscale colors?
    # data = re.sub(r'fill="#([0-9a-fA-F]{6})"', replacer, data)

    # Write the last frame to the output path
    with open(OUT_PATH, "w", encoding="UTF-8") as f:
        f.write(data)

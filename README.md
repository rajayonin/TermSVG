# TermSVG

Small program to generate SVG images from terminal command output, preserving
formatting/colors of the command while automatically adding simple formatting
to the image:

- Command run
- Padding around the borders of the image
- Adjusts terminal size to avoid line wraps without leaving leftover empty space
- Hides the cursor

Also supports generating images for interactive commands, but they must be
manually automated. See `print.py` for more information on how to do this

> [!IMPORTANT]
> Due to limitations of termtosvg, this only works on Linux and MacOS
>
> For Windows users, we recommend using something like
> [WSL 2](https://learn.microsoft.com/windows/wsl/).


## Execution
The `main.py` script includes [inline script metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata),
which means that if you use a package manager such as
[uv](https://astral.sh/uv), [pipx](https://pipx.pypa.io/) or
[Hatch](https://hatch.pypa.io/), it should be as easy as doing
`<manager> run main.py`.

E.g., for uv:
```bash
uv run main.py
```

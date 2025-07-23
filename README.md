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

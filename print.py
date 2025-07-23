import pexpect
import subprocess
from typing import cast
import sys

cmd = sys.argv[1]
real = len(sys.argv) == 2

# If running to get the image, run in a pseudo-terminal (so that programs
# that conditionally add ANSI escape sequences think they are running on a tty)
if real:
    # Interactive command example:
    # term = pexpect.spawn("./spike", ["-d", "pk", "a.out"], encoding="UTF-8") # Start command
    # term.expect_exact("(spike)") # Wait for output
    # term.sendline("rs 100005") # Send input
    # term.expect_exact("(spike)")
    # term.sendline("rs")
    # term.expect(pexpect.EOF) # Wait for command exit
    # res = cast(str, term.before)
    res = cast(bytes, pexpect.run(cmd)).decode()
else:
    # Otherwise, just get the output without ANSI escape sequences
    res = subprocess.getoutput(cmd)

# Remove final new lines
while len(res) > 0 and res[-1] in "\n\r":
    res = res[:-1]

if real:
    print("\033[?25l", end="") # Hide the cursor

# Add a prompt with the command
print(f"$ {cmd}")
print(res, end="", flush=True)

import sys

out = []
# TODO: the log (offset -> value) and each consumer's position

for raw in sys.stdin.read().split("\n"):
    line = raw.rstrip("\r")
    if line == "":
        continue
    cmd, _, rest = line.partition(" ")
    # TODO: handle APPEND, READ, SEEK and END; append each output line to `out`
    pass

sys.stdout.write("".join(l + "\n" for l in out))

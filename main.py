import sys

class Broker:
    def __init__(self):
        self.logs: dict[int, str] = {}
        self.log_end_offset = 0

    def append_log(self, log: str):
        self.logs[self.log_end_offset] = log
        out.append(f"appended offset={self.log_end_offset}")
        self.log_end_offset += 1


class Consumer:
    def __init__(self, name: str):
        self.name: str = name
        self.offset: int = 0

    def set_offset(self, seek: int):
        self.offset = seek
        out.append(f"{self.name} next={self.offset}")

    def read_log(self):
        out.append(f"{self.name} offset={self.offset} value={broker.logs[self.offset]}")
        self.offset += 1
    

def get_consumer(name: str) -> Consumer:
    for c in consumers:
        if c.name == name:
            return c
    c = Consumer(name)
    consumers.append(c)
    return c

def handle_cmd(cmd: str, rest: str):
    match cmd:
        case "APPEND":
            broker.append_log(rest)
            
        case "READ":
            reader, _, offset = rest.partition(" ")

            consumer = get_consumer(reader)

            for _ in range(int(offset)):
                if consumer.offset >= broker.log_end_offset:
                    break

                consumer.read_log()

            out.append(f"{consumer.name} next={consumer.offset}")

        case "SEEK":
            reader, _, offset = rest.partition(" ")
            offset = int(offset)

            if offset < 0 or offset > broker.log_end_offset:
                out.append(f"ERR out of range")
            else:
                consumer.set_offset(offset)

        case "END":
            out.append(f"end={broker.log_end_offset}")

out = []
# TODO: the log (offset -> value) and each consumer's position
broker = Broker()
consumers: list[Consumer] = []

for raw in sys.stdin.read().split("\n"):
    line = raw.rstrip("\r")
    if line == "":
        continue
    cmd, _, rest = line.partition(" ")
    # TODO: handle APPEND, READ, SEEK and END; append each output line to `out`
    handle_cmd(cmd=cmd, rest=rest)

    pass

sys.stdout.write("".join(l + "\n" for l in out))

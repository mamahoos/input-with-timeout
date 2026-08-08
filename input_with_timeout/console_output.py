from __future__ import annotations

from sys import stdout


class Endl:
    pass


class Cout:
    def __lshift__(self, other: object) -> Cout:
        stdout.write("\r\n" if isinstance(other, Endl) else str(other))
        stdout.flush()
        return self


cout = Cout()
endl = Endl()

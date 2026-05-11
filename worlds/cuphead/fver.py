### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import Self

from typing_extensions import override


class FVersion:
    branch: str
    baseline: int
    revision: int
    release: int
    postfix: str

    def __init__(self, baseline: int, revision: int, release: int, branch: str = "v", postfix: str = ""):
        self.branch = branch
        self.baseline = baseline
        self.revision = revision
        self.release = release
        self.postfix = postfix

    @classmethod
    def from_int_tuple(cls, version: tuple[int, int, int, int], postfix: str = "") -> Self:
        if version[0] == 0:
            match version[1]:
                case 1:
                    branch = "preview"
                case 2:
                    branch = "alpha"
                case 3:
                    branch = "beta"
                case 4:
                    branch = "rc"
                case _:
                    branch = "unknown"
        else:
            branch = "v"
        return cls(version[2], version[3], 0, branch, postfix)

    def get_revision_letter(self) -> str:
        if self.revision < 0:
            raise ValueError("Number must be a non-negative integer")
        n = self.revision

        res: list[str] = []
        while n >= 0:
            n, r = divmod(n, 26)
            res.append(chr(r + ord("a")))
            n -= 1

        return "".join(res)

    @override
    def __str__(self) -> str:
        rel_str = f".{self.release}" if self.release > 0 else ""
        postfix_str = f"-{self.postfix}" if self.postfix else ""
        baseline = self.baseline + 1
        return f"{self.branch}{baseline:02d}{self.get_revision_letter()}{rel_str}{postfix_str}"

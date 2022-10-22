from __future__ import annotations

import functools
from enum import IntFlag
from enum import unique

from app.utils import escape_enum
from app.utils import pymysql_encode

__all__ = ("MappoolMods",)

# NOTE: the order of some of these = stupid


@unique
@pymysql_encode(escape_enum)
class MappoolMods(IntFlag):
    NOMOD = 0
    EASY = 1 << 1
    HIDDEN = 1 << 3
    HARDROCK = 1 << 4
    DOUBLETIME = 1 << 6
    FLASHLIGHT = 1 << 10
    FREEMODS = 1 << 31
    TIEBREAKER = 1 << 32

    def __repr__(self) -> str:
        if self.value == MappoolMods.NOMOD:
            return "NM"

        mod_str = []
        _dict = mod2modstr_dict  # global

        for mod in MappoolMods:
            if self.value & mod:
                mod_str.append(_dict[mod])

        return "".join(mod_str)

    def filter_tournament_mods(self) -> MappoolMods:
        """Remove any invalid mod combinations."""

        self &= ~TOURNAMENT_SPECIFIC_MODS

        return self;

    @classmethod
    @functools.lru_cache(maxsize=64)
    def from_modstr(cls, s: str) -> MappoolMods:
        # from fmt: `HDDTRX`
        mods = cls.NOMOD
        _dict = modstr2mod_dict  # global

        # split into 2 character chunks
        mod_strs = [s[idx : idx + 2].upper() for idx in range(0, len(s), 2)]

        # find matching mods
        for m in mod_strs:
            if m not in _dict:
                continue

            mods |= _dict[m]

        return mods


modstr2mod_dict = {
    "EZ": MappoolMods.EASY,
    "HD": MappoolMods.HIDDEN,
    "HR": MappoolMods.HARDROCK,
    "DT": MappoolMods.DOUBLETIME,
    "FL": MappoolMods.FLASHLIGHT,
    "FM": MappoolMods.FREEMODS,
    "TB": MappoolMods.TIEBREAKER,
}

mod2modstr_dict = {
    MappoolMods.EASY: "EZ",
    MappoolMods.HIDDEN: "HD",
    MappoolMods.HARDROCK: "HR",
    MappoolMods.DOUBLETIME: "DT",
    MappoolMods.FLASHLIGHT: "FL",
    MappoolMods.FREEMODS: "FM",
    MappoolMods.TIEBREAKER: "TB",
}

TOURNAMENT_SPECIFIC_MODS = MappoolMods.FREEMODS | MappoolMods.TIEBREAKER
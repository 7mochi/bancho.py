#!/usr/bin/env python3.9
"""
Tool to move first places to 4.6.6 first_places
This tool is destructive, don't run it if you don't know why it exists :3
"""
from __future__ import annotations

import asyncio
import os
import sys
import databases

sys.path.insert(0, os.path.abspath(os.pardir))
os.chdir(os.path.abspath(os.pardir))

import app.settings
from app.constants.gamemodes import GameMode
from app.constants.gamemodes import GAMEMODE_REPR_LIST

async def main() -> int:
    async with databases.Database(app.settings.DB_DSN) as db:
        async with (
            db.connection() as select_conn,
            db.connection() as insert_conn,
        ):
            # Ranked, approved and loved (Has leaderboard)
            print("Getting all maps")
            maps = await select_conn.fetch_all(f"SELECT * FROM maps WHERE status in (2,3,5)");
            
            for mode in GameMode.valid_gamemodes():
                print(f"Getting first places for {GAMEMODE_REPR_LIST[mode]}")
            
                for map in maps:
                    scores = await select_conn.fetch_all(
                        "SELECT s.map_md5, s.score, s.pp, s.acc, s.max_combo, s.mods, "
                        "s.n300, s.n100, s.n50, s.nmiss, s.ngeki, s.nkatu, s.grade, s.status, "
                        "s.mode, s.play_time, s.time_elapsed, s.client_flags, s.userid, s.perfect, "
                        "s.online_checksum, u.name player_name, u.country, "
                        "c.id clan_id, c.name clan_name, c.tag clan_tag "
                        "FROM scores s "
                        "INNER JOIN users u ON u.id = s.userid "
                        "LEFT JOIN clans c ON c.id = u.clan_id "
                        "WHERE s.map_md5 = :map_md5 "
                        "AND s.mode = :mode "
                        "AND s.status = 2 "
                        "AND u.priv & 1",
                        {"map_md5": map["md5"], "mode": mode}
                    )

                    if not scores:
                        continue
                    
                    score = scores[0]

                    await insert_conn.execute(
                        "INSERT INTO first_places "
                        "VALUES (NULL, "
                        ":map_md5, :score, :pp, :acc, "
                        ":max_combo, :mods, :n300, :n100, "
                        ":n50, :nmiss, :ngeki, :nkatu, "
                        ":grade, :status, :mode, :play_time, "
                        ":time_elapsed, :client_flags, :user_id, :perfect, "
                        ":checksum)",
                        {
                            "map_md5": score["map_md5"],
                            "score": score["score"],
                            "pp": score["pp"],
                            "acc": score["acc"],
                            "max_combo": score["max_combo"],
                            "mods": score["mods"],
                            "n300": score["n300"],
                            "n100": score["n100"],
                            "n50": score["n50"],
                            "nmiss": score["nmiss"],
                            "ngeki": score["ngeki"],
                            "nkatu": score["nkatu"],
                            "grade": score["grade"],
                            "status": score["status"],
                            "mode": score["mode"],
                            "play_time": score["play_time"],
                            "time_elapsed": score["time_elapsed"],
                            "client_flags": score["client_flags"],
                            "user_id": score["userid"],
                            "perfect": score["perfect"],
                            "checksum": score["online_checksum"],
                        },
                    )
            
            print("Finished migrating first places to the new table")

if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

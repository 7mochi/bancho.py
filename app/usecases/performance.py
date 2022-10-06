from __future__ import annotations

import math
from typing import Optional
from typing import TypedDict

from peace_performance_python.objects import Beatmap as PeaceMap
from peace_performance_python.objects import Calculator as PeaceCalculator

from rosu_pp_py import Calculator, ScoreParams
class DifficultyRating(TypedDict):
    performance: float
    star_rating: float


class StdTaikoCatchScore(TypedDict):
    mods: Optional[int]
    acc: Optional[float]
    combo: Optional[int]
    nmiss: Optional[int]


class ManiaScore(TypedDict):
    mods: Optional[int]
    score: Optional[int]


def calculate_performances_std(
    osu_file_path: str,
    scores: list[StdTaikoCatchScore],
) -> list[DifficultyRating]:
    results: list[DifficultyRating] = []

    calculator = Calculator(osu_file_path)

    for score in scores:
        mods = score["mods"] if score["mods"] != None else 0
        acc = score["acc"] if score["acc"] != None else 100.00
        nmisses = score["nmiss"] if score["nmiss"] != None else 0
        combo = score["combo"]

        params = ScoreParams(mods = mods, acc = acc, nMisses = nmisses, combo = combo)

        [result] = calculator.calculate(params)

        pp = result.pp
        sr = result.stars

        if math.isnan(pp) or math.isinf(pp):
            # TODO: report to logserver
            pp = 0.0
            sr = 0.0
        else:
            pp = round(pp, 5)

        results.append(
            {
                "performance": pp,
                "star_rating": sr,
            },
        )

    return results


def calculate_performances_taiko(
    osu_file_path: str,
    scores: list[StdTaikoCatchScore],
) -> list[DifficultyRating]:
    beatmap = PeaceMap(osu_file_path)  # type: ignore

    results: list[DifficultyRating] = []

    for score in scores:
        calculator = PeaceCalculator(
            {
                "mode": 1,
                "mods": score["mods"],
                "acc": score["acc"],
                "combo": score["combo"],
                "nmiss": score["nmiss"],
            },
        )

        result = calculator.calculate(beatmap)

        pp = result.pp
        sr = result.stars

        if math.isnan(pp) or math.isinf(pp):
            # TODO: report to logserver
            pp = 0.0
            sr = 0.0
        else:
            pp = round(pp, 5)

        results.append(
            {
                "performance": pp,
                "star_rating": sr,
            },
        )

    return results


def calculate_performances_catch(
    osu_file_path: str,
    scores: list[StdTaikoCatchScore],
) -> list[DifficultyRating]:
    beatmap = PeaceMap(osu_file_path)  # type: ignore

    results: list[DifficultyRating] = []

    for score in scores:
        calculator = PeaceCalculator(
            {
                "mode": 2,
                "mods": score["mods"],
                "acc": score["acc"],
                "combo": score["combo"],
                "nmiss": score["nmiss"],
            },
        )

        result = calculator.calculate(beatmap)

        pp = result.pp
        sr = result.stars

        if math.isnan(pp) or math.isinf(pp):
            # TODO: report to logserver
            pp = 0.0
            sr = 0.0
        else:
            pp = round(pp, 5)

        results.append(
            {
                "performance": pp,
                "star_rating": sr,
            },
        )

    return results


def calculate_performances_mania(
    osu_file_path: str,
    scores: list[ManiaScore],
) -> list[DifficultyRating]:
    beatmap = PeaceMap(osu_file_path)  # type: ignore

    results: list[DifficultyRating] = []

    for score in scores:
        calculator = PeaceCalculator(
            {
                "mode": 3,
                "mods": score["mods"],
                "score": score["score"],
            },
        )

        result = calculator.calculate(beatmap)

        pp = result.pp
        sr = result.stars

        if math.isnan(pp) or math.isinf(pp):
            # TODO: report to logserver
            pp = 0.0
            sr = 0.0
        else:
            pp = round(pp, 5)

        results.append(
            {
                "performance": pp,
                "star_rating": sr,
            },
        )

    return results


class ScoreDifficultyParams(TypedDict, total=False):
    # std, taiko, catch
    acc: float
    combo: int
    nmiss: int

    # mania
    score: int


def calculate_performances(
    osu_file_path: str,
    mode: int,
    mods: Optional[int],
    scores: list[ScoreDifficultyParams],
) -> list[DifficultyRating]:
    if mode in (0, 1, 2):
        std_taiko_catch_scores: list[StdTaikoCatchScore] = [
            {
                "mods": mods,
                "acc": score.get("acc"),
                "combo": score.get("combo"),
                "nmiss": score.get("nmiss"),
            }
            for score in scores
        ]

        if mode == 0:
            results = calculate_performances_std(
                osu_file_path=osu_file_path,
                scores=std_taiko_catch_scores,
            )
        elif mode == 1:
            results = calculate_performances_taiko(
                osu_file_path=osu_file_path,
                scores=std_taiko_catch_scores,
            )
        elif mode == 2:
            results = calculate_performances_catch(
                osu_file_path=osu_file_path,
                scores=std_taiko_catch_scores,
            )

    elif mode == 3:
        mania_scores: list[ManiaScore] = [
            {
                "mods": mods,
                "score": score.get("score"),
            }
            for score in scores
        ]

        results = calculate_performances_mania(
            osu_file_path=osu_file_path,
            scores=mania_scores,
        )
    else:
        raise NotImplementedError

    return results

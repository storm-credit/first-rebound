"""Reconstruct McGee's three short 2021 Denver playoff appearances.

The quarter starters and Denver substitutions are transcribed from official
NBA gamebooks. Phoenix/Portland substitutions are irrelevant to Denver's
five-man count. These are original-game clock witnesses, not selected results.
"""

import json
from decimal import Decimal
from pathlib import Path

import build_denver_2021_playoff_game4_lineups as game4


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "simulation/DENVER_2021_PLAYOFF_OTHER_LINEUPS.json"
MCGEE = game4.MCGEE
HARTENSTEIN = game4.HARTENSTEIN
MILLSAP = "Paul Millsap"
HOWARD = "Markus Howard"
CANCAR = "Vlatko Cancar"
NNAJI = "Zeke Nnaji"

GAMES = [
    {"date": "2021-05-29", "period": 4, "pages": [16, 17, 18],
     "book": "https://statsdmz.nba.com/pdfs/20210529/20210529_DENPOR_book.pdf",
     "official_mcgee_seconds": 434,
     "starters": [game4.GREEN, HOWARD, MILLSAP, game4.MORRIS, game4.CAMPAZZO],
     "subs": [("08:21.0", CANCAR, game4.GREEN),
              ("07:14.0", game4.HARRISON, MILLSAP),
              ("07:14.0", MCGEE, game4.CAMPAZZO),
              ("05:12.0", NNAJI, game4.MORRIS)]},
    {"date": "2021-06-01", "period": 1, "pages": [14, 15],
     "book": "https://statsdmz.nba.com/pdfs/20210601/20210601_PORDEN_book.pdf",
     "official_mcgee_seconds": 2,
     "starters": [game4.CAMPAZZO, game4.GORDON, game4.JOKIC, game4.PORTER, game4.RIVERS],
     "subs": [("04:53.0", game4.MORRIS, game4.PORTER),
              ("03:33.0", game4.GREEN, game4.CAMPAZZO),
              ("02:28.0", game4.PORTER, game4.RIVERS),
              ("02:28.0", HOWARD, game4.GORDON),
              ("00:02.1", MCGEE, game4.JOKIC)]},
    {"date": "2021-06-09", "period": 4, "pages": [15, 16, 17],
     "book": "https://statsdmz.nba.com/pdfs/20210609/20210609_DENPHX_book.pdf",
     "official_mcgee_seconds": 413,
     "starters": [game4.GREEN, game4.PORTER, MILLSAP, game4.MORRIS, HOWARD],
     "subs": [("08:35.0", game4.RIVERS, HOWARD),
              ("08:35.0", game4.CAMPAZZO, game4.PORTER),
              ("07:17.0", HOWARD, game4.CAMPAZZO),
              ("06:53.0", MCGEE, MILLSAP),
              ("06:05.0", game4.HARRISON, game4.GREEN),
              ("06:05.0", NNAJI, game4.MORRIS),
              ("06:05.0", CANCAR, game4.RIVERS)]},
]


def build():
    rows = []
    for game in GAMES:
        lineup = set(game["starters"])
        assert len(lineup) == 5
        remaining = Decimal(720)
        mcgee_seconds = Decimal(0)
        stints = []
        for clock, incoming, outgoing in game["subs"] + [("00:00.0", None, None)]:
            end = game4.seconds(clock)
            assert end <= remaining
            duration = remaining - end
            if MCGEE in lineup and duration:
                stints.append({
                    "period": game["period"],
                    "start_clock": f"{int(remaining // 60):02d}:{remaining % 60:04.1f}",
                    "end_clock": clock,
                    "duration_seconds": float(duration),
                    "original_denver_five": sorted(lineup),
                    "conditional_hartenstein_five": sorted((lineup - {MCGEE}) | {HARTENSTEIN}),
                })
                mcgee_seconds += duration
            remaining = end
            if incoming is not None:
                assert outgoing in lineup and incoming not in lineup
                lineup.remove(outgoing)
                lineup.add(incoming)
                assert len(lineup) == 5
        assert remaining == 0
        assert abs(mcgee_seconds - game["official_mcgee_seconds"]) <= Decimal("0.5")
        rows.append({**game, "mcgee_lineup_rows": stints,
                     "mcgee_clock_seconds": float(mcgee_seconds)})
    assert sum(row["official_mcgee_seconds"] for row in rows) == 849
    return {
        "stage": "O-15F14-F5_DENVER_THREE_SHORT_PLAYOFF_LINEUP_CLOCKS",
        "selected": False,
        "games": rows,
        "official_mcgee_total_seconds": 849,
        "limits": "Original-quarter clock and five-man identities only; not Hartenstein health or playoff outcome",
    }


if __name__ == "__main__":
    OUT.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT.relative_to(ROOT))

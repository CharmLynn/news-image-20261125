# The World in One Day — Wednesday, 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/CharmLynn/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/CharmLynn/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One 1024×1024 front page for 25 November 2026. A lead story in a
dark panel, four more stories on cards, a source line under each,
all drawn by code — no photographs, no pasted-in artwork.

## The day's five stories

- **Riyadh tower struck again.** A Houthi strike hits the PIF
  Tower, Riyadh's tallest skyscraper, for the second time in a
  week, wounding 11 people. The Saudi-led coalition calls it a
  terrorist attack.
  Sources: Reuters, AFP, The Jerusalem Post.
- **Shanghai chief probed for graft.** Chen Jining, Shanghai's
  party chief and a Politburo member, is put under investigation
  for suspected serious violations of discipline and law — the
  fourth Politburo member probed since 2025.
  Sources: Xinhua, Reuters, SCMP.
- **Trump honours Giuliani.** The president awards the Medal of
  Freedom, the nation's highest civilian honour, to former New
  York mayor Rudy Giuliani in a private ceremony in the Oval
  Office.
  Sources: Reuters, AP, The New York Times.
- **Hamas security chief killed.** An Israeli strike in Gaza City
  kills Naim Abu Nahal, head of Hamas's internal security, as the
  ceasefire frays.
  Sources: Reuters, Al Jazeera, Times of Israel.
- **Huang says sorry, in therapy.** A day after his return as
  Nvidia chief executive, Jensen Huang apologises to staff, says
  he is in therapy and admits "terrible mistakes".
  Sources: The New York Times, CNN, SCMP.

Each story above happened, or was first reported, on 25 November
2026.

## How it is built

`draw.py` paints `entry.png` with Pillow: a paper background,
serif headlines, and five small flat icons drawn from scratch in
code. Run it twice and the bytes are identical. `main.py`
(Python 3.13, standard library only) ships that image to
`$MAKEFUN_OUTPUT_DIR/entry.png` — `/output` in the grader — and
checks the copy's SHA-256, so the grader's two runs agree.
`LICENSE` is MIT.

```sh
python3 draw.py        # render entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The finished PNG is 1024×1024 pixels and well under the 1 MiB cap.
The program needs no network and no third-party packages.

---

<sub>Entered on [make.fun](https://make.fun/?ref=mpd17n5r&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>

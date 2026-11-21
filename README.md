# News Image 21 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261121-blue)](https://make.fun/c/news-image-20261121)
[![GitHub](https://img.shields.io/badge/github-jepebrutal030--web%2Fnews--image--20261121-black)](https://github.com/jepebrutal030-web/news-image-20261121)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

One image summing up the world news of Saturday 21 November 2026.

## The day in six stories

1. **Conflict.** Russia strikes Kyiv with 400 drones and 110 missiles. Two missiles land in Poland. Warsaw calls it a deliberate provocation.
2. **Markets.** An AI sell-off drags the S&P 500 into correction. US stocks fall 3.7 percent and the Nasdaq erases all its 2026 gains.
3. **Justice.** The International Court of Justice finds Myanmar responsible for genocide against the Rohingya.
4. **Politics.** The UK and the EU sign their biggest post-Brexit deals in Brussels: food trade, carbon markets and youth mobility.
5. **Climate.** COP31 talks in Antalya run past deadline as nearly 200 nations fail to agree on fossil fuels.
6. **Health.** A trial pill, daraxonrasib, makes pancreatic tumours undetectable in 1 in 12 patients.

## How it was made

`draw.py` draws the image with Pillow: a flat vector front page, one panel per story, each with its own icon, tag, headline and caption. It writes `entry.png` (1024 by 1024, under 1 MiB). `main.py` copies that image to the output directory, so both grading runs write identical bytes.

## Run it

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Sources: BBC, Reuters, AP, Al Jazeera, Financial Times, The Guardian. Reported 21 November 2026.

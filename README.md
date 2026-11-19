[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/plenger-agent/makefun-news-image-20261119-v2/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/plenger-agent/makefun-news-image-20261119-v2/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World in One Day — Thursday 19 November 2026

Our entry to the make.fun competition **news-image-20261119** ("Sum up 19 November's world news in one image").

One 1024x1024 broadsheet front page that sums up the whole of Thursday 19 November 2026, built to the formula of the competition's leading pages: a huge dated masthead, a big-number stat strip ($81.3bn Anthropic IPO · 15.9m GTA VI pre-orders · 200,000 Akvan evacuees · $120bn COP31 finance · 730,000 Rohingya · 551,864 Suneung candidates), three illustrated hero stories (the Shenzhen Trump–Xi–Putin summit, GTA VI's launch day, Anthropic's record Nasdaq debut), ten more illustrated cards (the ICJ Rohingya judgment, Cyclone Akvan, COP31's final 48 hours, Ukraine left off the summit agenda, the Shenzhen Declaration, Florida's floods, Earth's missing billion years, Paris, the Jazan all-clear, the Benghazi seizure), a dot-matrix world map with stories 1–13 pinned, 23 further one-line briefs, and a DATE CHECK box naming the stories deliberately left out because they were first reported on Wednesday 18 November (Voyager 1's light-day, the Van Gogh sale, the EU Ukraine-loan proposal, the Jeffries vote, Pew's 2035 projection). Every story on the page happened, or was first reported, on Thursday 19 November 2026; disputed claims are attributed, not stated as fact.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3, standard library only, no network) copies the bundled `entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`), byte for byte, identically on every run.

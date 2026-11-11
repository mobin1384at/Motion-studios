# Layout — safe zones and hard rules

## Safe zones

Keep all essential text and faces inside the safe zone. Anything outside
can be covered by platform UI (captions, buttons, progress bars).

| Format | Size | Safe zone (from edges) | Notes |
|---|---|---|---|
| 9:16 reel / Short | 1080×1920 | top 250 px, bottom 350 px, sides 80 px | Bottom 350 px is where captions + UI live; keep the caption centre at y ≈ 1400 (Lalezar recipe) |
| 16:9 YouTube | 1920×1080 | top 80 px, bottom 120 px, sides 120 px | Titles centred; lower-thirds above the bottom 120 px |
| 1:1 feed | 1080×1080 | 100 px all round | Centre-weighted composition |

## Hard rules

- Captions: never on the face; never outside the safe zone; never two
  chunks at once.
- Big words: centre of the screen (y ≈ 960 in 9:16), max width 900 px.
- Zoom: max 1.20×, centre on the face — never crop lips or eyes.
- Check the first, middle, and last frames plus every big-word moment in
  the contact sheet before shipping.
- Persian captions: RTL layout, first word on the right, 34 px word gap
  (Lalezar recipe), group width computed up front so words do not shift
  as they appear.

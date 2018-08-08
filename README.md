# SSBadge
Summer School Badge Auto-Generation

Usage:
1. generate all badges from the "attendants_list.csv"
python3 autogen_badges.py -genB
2. combine in 4x2 A4 combination of all badges in subfolder ./badges
python autogen_badges.py -combB
3. combine postcard in 4x2 reps
python autogen_badges.py -combP


Notes:
- The combo results of [2] and [3] must be modified setting(with inkscape):
-- A4 as the page dimension, 
-- group all the elements (G1)
-- vertical centering of G1 with respect to the page

- In case of attendants name/surname very long, the original badge in ./logo/drawing_2Logo_v2.svg
 must change the font size


Credits:
svg_stack from https://github.com/astraw/svg_stack
./postcard/Aeree_14.jpg from Fabio Mazzoni, www.immaginefoto.com
./postcard/villaggio-testa.jpg from Riva degli Etruschi Resort, www.rivadeglietruschi.it
./postcard/Populonia_grotte.jpg from Google search


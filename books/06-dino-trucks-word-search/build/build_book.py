"""Dino Trucks Word Search — interior builder (reportlab, vector grids, embedded TTF fonts).
Run from this folder: python3 build_book.py  -> ../final/interior.pdf
Art: reuses the Dino Trucks clean pages in ../../03-dino-trucks-mazes/art/ (0 image credits).
"""
import os, random, string
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import Color, black, white

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, '..', '..', '03-dino-trucks-mazes', 'art')
OUT = os.path.join(HERE, '..', 'final', 'interior.pdf')
for n, f in [('Lucky', 'LuckiestGuy'), ('Fred', 'Fredoka-SemiBold'), ('FredR', 'Fredoka-Regular')]:
    pdfmetrics.registerFont(TTFont(n, os.path.join(HERE, f + '.ttf')))

W, H = 612, 792
M = 43  # 0.6 in ink margin
GREY = Color(0.82, 0.82, 0.82); MID = Color(0.45, 0.45, 0.45)

THEMES = [
 ('Dino Basics', 'DINO EGG TAIL CLAW ROAR BONES TEETH FOSSIL NEST SCALES HORN SPIKES'),
 ('Construction Site', 'DIGGER CRANE DUMPER BRICKS HELMET SHOVEL CONCRETE LADDER TRUCK CONE BEAM DIRT'),
 ('Farm Life', 'TRACTOR BARN COW PIG HAY FARMER SHEEP GOAT FIELD CORN HEN MUD'),
 ('Colors', 'RED BLUE GREEN YELLOW ORANGE PURPLE PINK BLACK WHITE BROWN GRAY GOLD'),
 ('Monster Trucks', 'MONSTER WHEELS JUMP RAMP CRASH ENGINE TIRES MUD FLIP ARENA CROWD ROAR'),
 ('Pets', 'DOG CAT FISH HAMSTER BUNNY PARROT TURTLE PUPPY KITTEN BONE LEASH COLLAR'),
 ('Fire Rescue', 'FIRE HOSE LADDER SIREN HELMET WATER RESCUE ENGINE BOOTS AXE SMOKE BRAVE'),
 ('Fruits', 'APPLE BANANA GRAPE MANGO PEAR CHERRY LEMON ORANGE PEACH KIWI MELON PLUM'),
 ('Race Day', 'RACE CAR FLAG SPEED TRACK PITSTOP HELMET WINNER LAP ZOOM TROPHY FAST'),
 ('Weather', 'SUN RAIN CLOUD WIND SNOW STORM THUNDER RAINBOW FOG HAIL FROST WARM'),
 ('Dino Food', 'LEAVES FERNS MEAT PLANTS BERRIES SEEDS FISH TWIGS ROOTS EGGS CHOMP MUNCH'),
 ('Playground', 'SWING SLIDE SANDBOX BALL JUMP RUN SEESAW CLIMB TAG HOP FRIENDS PLAY'),
 ('Bugs', 'ANT BEE BEETLE SPIDER LADYBUG BUTTERFLY MOTH WORM FLY CRICKET SNAIL WASP'),
 ('Numbers', 'ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN TWENTY HUNDRED'),
 ('Trucks Galore', 'DUMP TOW FIRE GARBAGE MIXER TANKER PICKUP DELIVERY MAIL CEMENT LOG HAULER'),
 ('Ocean', 'WHALE SHARK FISH WAVE CRAB SHELL CORAL OCTOPUS SEAL SAND BOAT DOLPHIN'),
 ('Body', 'HEAD HAND FOOT ARM LEG NOSE EARS EYES MOUTH KNEE TOES HAIR'),
 ('Breakfast', 'EGGS TOAST CEREAL MILK JUICE PANCAKE WAFFLE BACON BERRY OATS BUTTER JAM'),
 ('Beach Day', 'SAND WAVES SHELL SUN TOWEL BUCKET SPADE SWIM SURF KITE CRAB HAT'),
 ('Clothes', 'SHIRT PANTS SOCKS SHOES HAT COAT DRESS SCARF GLOVES BOOTS JACKET CAP'),
 # ---- medium ----
 ('Dino Land', 'VOLCANO JUNGLE SWAMP LAVA CAVE RIVER CLIFF FERN ROCK MUD DESERT VALLEY'),
 ('Space', 'ROCKET MOON STAR PLANET COMET ORBIT ALIEN MARS GALAXY ASTRONAUT SATURN SUN'),
 ('Transport', 'BUS TRAIN PLANE BOAT BIKE CAR TRUCK SHIP TAXI SCOOTER HELICOPTER TRAM'),
 ('Shapes', 'CIRCLE SQUARE TRIANGLE STAR HEART OVAL DIAMOND CUBE CONE SPHERE ARROW RECTANGLE'),
 ('Fossil Dig', 'FOSSIL BONE SKULL DIG BRUSH SHOVEL SAND ROCK MUSEUM AMBER CLUE TOOTH'),
 ('School Day', 'PENCIL BOOK DESK TEACHER RULER CRAYON ERASER LUNCH RECESS CLASS MATH READ'),
 ('Veggies', 'CARROT PEA CORN BEAN POTATO ONION PUMPKIN BROCCOLI TOMATO LETTUCE PEPPER CELERY'),
 ('Trains', 'TRAIN TRACK ENGINE STEAM WHISTLE STATION TICKET CABOOSE TUNNEL BRIDGE RAIL CARGO'),
 ('Jungle', 'MONKEY TIGER PARROT SNAKE VINE JAGUAR SLOTH FROG TREE LEAF BANANA GORILLA'),
 ('Arctic', 'POLAR BEAR PENGUIN ICE SNOW SEAL WALRUS IGLOO FROZEN ORCA FOX OWL'),
 ('Flying Reptiles', 'PTERANODON WINGS SKY GLIDE SOAR BEAK CLIFF FLAP NEST CLOUD DIVE FLY'),
 ('Birthday Party', 'CAKE CANDLE BALLOON GIFT PARTY GAMES HAT CANDY FRIENDS WISH SING FUN'),
 ('Airport', 'PLANE PILOT RUNWAY WINGS JET TICKET GATE CLOUDS FLY BAGS TOWER CREW'),
 ('Garden', 'FLOWER SEED SOIL WATER ROSE TULIP SHOVEL BEE SUNFLOWER WORM GROW RAKE'),
 ('Music', 'DRUM GUITAR PIANO FLUTE SONG SING DANCE BEAT VIOLIN BAND HORN BELL'),
 ('Sea Reptiles', 'PLESIOSAUR MOSASAUR FLIPPER SWIM OCEAN DEEP WAVE FISH TAIL SPLASH DIVE TEETH'),
 ('Sports', 'SOCCER BASEBALL TENNIS GOLF HOCKEY SKATE SWIM GOAL TEAM BAT KICK SCORE'),
 ('Camping', 'TENT FIRE MARSHMALLOW FLASHLIGHT HIKE MAP STARS LOG BAG CANOE TRAIL LAKE'),
 ('Feelings', 'HAPPY SAD BRAVE CALM PROUD SILLY KIND EXCITED SHY GLAD CURIOUS FRIENDLY'),
 ('Trees', 'OAK PINE MAPLE LEAF BARK ROOT BRANCH ACORN TRUNK SEED FOREST NEST'),
 ('Big Dinos', 'BRONTO DIPLODOCUS GIANT HUGE TALL NECK STOMP HEAVY LONG MIGHTY TREES HERD'),
 ('Kitchen', 'SPOON FORK PLATE BOWL CUP OVEN PAN COOK BAKE MIXER TOAST APRON'),
 ('City', 'STREET BUILDING PARK SHOP BUS TAXI TOWER LIGHTS BRIDGE CROWD TRAFFIC SUBWAY'),
 ('Bedtime', 'PILLOW BED DREAM MOON STARS BLANKET STORY TEDDY PAJAMAS SLEEP LAMP YAWN'),
 ('Road Trip', 'MAP ROAD SNACKS MUSIC CAR SIGN GAS HOTEL TUNNEL BRIDGE WINDOW SEATBELT'),
 # ---- hard ----
 ('Tiny Dinos', 'SMALL QUICK FAST TINY BABY HATCH EGG FEATHER RUN HIDE SNEAK LITTLE'),
 ('Rescue Heroes', 'POLICE DOCTOR NURSE FIREFIGHTER PILOT HELP SAFE SIREN RADIO MEDIC TEAM BRAVE'),
 ('Under the Ground', 'ROOTS WORM MOLE ROCK CAVE TUNNEL DIRT ANT BONE GEM CLAY COAL'),
 ('Rainforest', 'RAIN FROG TOUCAN VINE SLOTH CANOPY JAGUAR LEAF BUG MOSS PARROT TREE'),
 ('Desert', 'SAND CACTUS CAMEL HOT DUNE LIZARD SNAKE OASIS SUN DRY SCORPION ROCK'),
 ('Mountains', 'PEAK SNOW CLIMB ROCK TRAIL GOAT EAGLE CLIFF VALLEY HIKE CAVE PINE'),
 ('Robots', 'ROBOT GEAR BOLT WIRE BEEP METAL LASER BATTERY ANTENNA BUTTON SCREEN CODE'),
 ('Superpowers', 'FLY FAST STRONG INVISIBLE CAPE MASK HERO SHIELD POWER SAVE ZAP LASER'),
 ('Pirates', 'PIRATE SHIP MAP GOLD TREASURE PARROT FLAG ANCHOR ISLAND SAIL CHEST HOOK'),
 ('Castle', 'KING QUEEN KNIGHT CASTLE TOWER DRAGON CROWN SHIELD MOAT HORSE FLAG GATE'),
 ('Circus', 'CLOWN TENT JUGGLE LION ACROBAT HOOP TICKET POPCORN RING MAGIC SHOW TRICK'),
 ('Art Time', 'PAINT BRUSH CRAYON GLUE PAPER COLOR DRAW CHALK MARKER PENCIL CLAY SCISSORS'),
 ('Winter Fun', 'SNOW SLED SKATE SKI MITTENS SCARF COCOA SNOWMAN ICE BOOTS CABIN FROST'),
 ('Opposites', 'BIG SMALL HOT COLD FAST SLOW DAY NIGHT OPEN SHUT LOUD QUIET'),
 ('Dino Champions', 'TREX RAPTOR TRICERATOPS STEGOSAURUS ANKYLOSAURUS SPINOSAURUS ROAR STOMP CHOMP HORNS PLATES CLUB'),
]
assert len(THEMES) == 60, len(THEMES)
# level: (name, stars, grid size, words per puzzle, max len, directions)
EASY = ('EASY', 1, 10, 7, 9, [(0, 1), (1, 0)])
MED = ('MEDIUM', 2, 12, 9, 11, [(0, 1), (1, 0), (1, 1)])
HARD = ('HARD', 3, 14, 11, 13, [(0, 1), (1, 0), (1, 1), (-1, 1)])
LEVELS = [EASY] * 20 + [MED] * 25 + [HARD] * 15
BAD = {'ASS', 'SEX', 'FUK', 'FUC', 'SHT', 'DIK', 'CUM', 'TIT', 'KKK', 'NAZI', 'XXX', 'FAG', 'WTF', 'DAMN', 'HELL', 'SUCK', 'POOP', 'BUTT'}


def make_puzzle(words, n, dirs, rng):
    for _ in range(400):
        g = [[None] * n for _ in range(n)]; placed = []
        ok = True
        for w in sorted(words, key=len, reverse=True):
            spots = []
            for dr, dc in dirs:
                for r in range(n):
                    for c in range(n):
                        er, ec = r + dr * (len(w) - 1), c + dc * (len(w) - 1)
                        if not (0 <= er < n and 0 <= ec < n): continue
                        cells = [(r + dr * i, c + dc * i) for i in range(len(w))]
                        if all(g[y][x] in (None, w[i]) for i, (y, x) in enumerate(cells)):
                            overlap = sum(g[y][x] == w[i] for i, (y, x) in enumerate(cells))
                            spots.append((overlap, rng.random(), cells))
            if not spots: ok = False; break
            spots.sort(reverse=True)
            pick = spots[0] if rng.random() < 0.3 else rng.choice(spots)
            for i, (y, x) in enumerate(pick[2]): g[y][x] = w[i]
            placed.append((w, pick[2]))
        if not ok: continue
        letters = 'AABCDEEFGHIIKLMNOOPRSTTUWY'
        base = [row[:] for row in g]
        for _fill in range(80):
            g = [row[:] for row in base]
            for r in range(n):
                for c in range(n):
                    if g[r][c] is None: g[r][c] = rng.choice(letters)
            if rude(g, n, placed): continue
            # every word appears exactly once in the directions kids search -> one clear answer
            if all(count(g, w, n, dirs) == 1 for w, _ in placed): return g, placed
    raise RuntimeError('could not place: ' + ' '.join(words))


def rude(g, n, placed):
    """True if a BAD word shows up anywhere (any direction) using at least one filler letter."""
    inside = [set(cells) for _, cells in placed]
    for dr, dc in [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1)]:
        for b in BAD:
            L = len(b)
            for r in range(n):
                for c in range(n):
                    cells = [(r + dr * i, c + dc * i) for i in range(L)]
                    if not all(0 <= y < n and 0 <= x < n for y, x in cells): continue
                    if ''.join(g[y][x] for y, x in cells) == b and not any(set(cells) <= w for w in inside): return True
    return False


def count(g, w, n, dirs):
    k = 0
    for dr, dc in dirs:
        for r in range(n):
            for c in range(n):
                er, ec = r + dr * (len(w) - 1), c + dc * (len(w) - 1)
                if 0 <= er < n and 0 <= ec < n and all(g[r + dr * i][c + dc * i] == w[i] for i in range(len(w))): k += 1
    return k


def stars(c, x, y, n, size=8):
    import math
    for i in range(3):
        cx = x + i * (size * 2.4); p = c.beginPath()
        for k in range(10):
            a = math.pi / 2 + k * math.pi / 5; rr = size if k % 2 == 0 else size * 0.45
            px, py = cx + rr * math.cos(a), y + rr * math.sin(a)
            p.moveTo(px, py) if k == 0 else p.lineTo(px, py)
        p.close(); c.setLineWidth(1)
        c.setFillColor(black if i < n else white); c.drawPath(p, fill=1, stroke=1); c.setFillColor(black)


def draw_grid(c, g, x0, ytop, size, font_sz, placed=None, line_w=1.6):
    n = len(g); cell = size / n
    if placed:  # answer capsules behind letters
        c.setStrokeColor(GREY); c.setLineWidth(cell * 0.78); c.setLineCap(1)
        for w, cells in placed:
            (r0, c0), (r1, c1) = cells[0], cells[-1]
            c.line(x0 + (c0 + .5) * cell, ytop - (r0 + .5) * cell, x0 + (c1 + .5) * cell, ytop - (r1 + .5) * cell)
        c.setLineCap(0)
    c.setStrokeColor(black); c.setLineWidth(line_w); c.roundRect(x0 - cell * .25, ytop - size - cell * .25, size + cell * .5, size + cell * .5, cell * .4)
    c.setFont('Fred', font_sz); c.setFillColor(black)
    for r in range(n):
        for k in range(n):
            c.drawCentredString(x0 + (k + .5) * cell, ytop - (r + .5) * cell - font_sz * .35, g[r][k])


def puzzle_page(c, num, title, lvl, g, placed, art_img):
    name, st, n, _, _, _ = lvl
    c.setFont('Lucky', 15); c.drawString(M, H - M - 12, f'PUZZLE {num}')
    c.setFont('Fred', 10); c.drawRightString(W - M - 58, H - M - 11, name); stars(c, W - M - 44, H - M - 7, st)
    c.setFont('Lucky', 34); c.drawCentredString(W / 2, H - M - 56, title.upper())
    size = 462; x0 = (W - size) / 2; ytop = H - M - 84
    draw_grid(c, g, x0, ytop, size, {10: 27, 12: 23, 14: 19}[n])
    # word list (left) + art to colour (right)
    words = sorted(w for w, _ in placed)
    ly = ytop - size - 36; cols = 2 if len(words) <= 8 else 3
    colw = 122; per = -(-len(words) // cols)
    c.setFont('Fred', 14)
    for i, w in enumerate(words):
        cx = M + 8 + (i // per) * colw; cy = ly - (i % per) * 24
        c.setLineWidth(1); c.rect(cx, cy - 2, 11, 11); c.drawString(cx + 17, cy - 1, w)
    aw = 175 if cols == 3 else 230
    iw, ih = art_img.size; s = min(aw / iw, (ly + 18 - M) / ih)
    c.drawImage(ImageReader(art_img), W - M - iw * s, M, iw * s, ih * s, mask='auto')
    c.setFont('FredR', 8); c.setFillColor(MID); c.drawString(M + 8, M + 2, 'Find every word, then color the picture!'); c.setFillColor(black)


def answers_page(c, items, first):
    c.setFont('Lucky', 30); c.drawCentredString(W / 2, H - M - 30, 'ANSWERS')
    bw = (W - 2 * M - 30) / 2; bh = (H - 2 * M - 70) / 2
    for i, (num, title, g, placed) in enumerate(items):
        col, row = i % 2, i // 2
        x = M + col * (bw + 30); ytop = H - M - 60 - row * (bh + 10)
        c.setFont('Fred', 11); c.drawString(x, ytop - 10, f'{num}. {title}')
        size = min(bw - 20, bh - 40); draw_grid(c, g, x + (bw - size) / 2, ytop - 26, size, {10: 13, 12: 11, 14: 9.5}[len(g)], placed, line_w=1)


def belongs(c):
    c.setFont('Lucky', 40); c.drawCentredString(W / 2, H - 170, 'THIS BOOK'); c.drawCentredString(W / 2, H - 218, 'BELONGS TO')
    c.setLineWidth(2); c.roundRect(90, H - 340, W - 180, 80, 16)
    img = art(13); iw, ih = img.size; s = 330 / ih
    c.drawImage(ImageReader(img), (W - iw * s) / 2, 110, iw * s, ih * s, mask='auto')


def how_to(c, rng):
    c.setFont('Lucky', 36); c.drawCentredString(W / 2, H - M - 40, 'HOW TO PLAY')
    c.setFont('FredR', 15)
    tips = ['Look at the word list under each puzzle.', 'Find each word hidden in the letter grid.',
            'Easy words go across or down. Medium words can also go diagonally.',
            'Hard puzzles also have words going diagonally up.', 'No words are ever backwards!',
            'Circle each word you find and tick its box.', 'Stuck? The answers are at the back of the book.',
            'Then color the dino truck picture on the page!']
    for i, t in enumerate(tips):
        c.circle(M + 30, H - M - 100 - i * 34 + 5, 4, fill=1); c.drawString(M + 44, H - M - 100 - i * 34, t)
    g, placed = make_puzzle(['DINO', 'TRUCK', 'ROAR'], 6, [(0, 1), (1, 0)], rng)
    c.setFont('Fred', 13); c.drawCentredString(W / 2, 330, 'Example: find DINO, TRUCK and ROAR')
    draw_grid(c, g, (W - 190) / 2, 310, 190, 22, placed)


def certificate(c):
    c.setLineWidth(6); c.roundRect(M + 10, M + 10, W - 2 * M - 20, H - 2 * M - 20, 24)
    c.setLineWidth(1.5); c.roundRect(M + 24, M + 24, W - 2 * M - 48, H - 2 * M - 48, 18)
    c.setFont('Lucky', 30); c.drawCentredString(W / 2, H - 150, 'CERTIFICATE')
    c.setFont('Lucky', 44); c.drawCentredString(W / 2, H - 210, 'WORD SEARCH')
    c.drawCentredString(W / 2, H - 260, 'CHAMPION')
    c.setFont('FredR', 15); c.drawCentredString(W / 2, H - 320, 'This award goes to')
    c.line(140, H - 380, W - 140, H - 380)
    c.drawCentredString(W / 2, H - 420, 'for finding every word in all 60 puzzles!')
    img = art(11); iw, ih = img.size; s = 240 / ih
    c.drawImage(ImageReader(img), (W - iw * s) / 2, 140, iw * s, ih * s, mask='auto')
    c.drawString(120, 110, 'Date: ____________'); c.drawRightString(W - 120, 110, 'Signed: ____________')


_cache = {}
def art(i):
    if i not in _cache:
        from PIL import Image
        _cache[i] = Image.open(os.path.join(ART, f'{i:02d}.png')).convert('L')
    return _cache[i]


def build():
    rng = random.Random(2026)
    c = canvas.Canvas(OUT, pagesize=(W, H), initialFontName='FredR')
    c.setTitle('Dino Trucks Word Search'); c.setAuthor('Bibhu Behera')
    belongs(c); c.showPage(); how_to(c, rng); c.showPage()
    done = []
    for i, ((title, words), lvl) in enumerate(zip(THEMES, LEVELS), 1):
        name, st, n, k, maxlen, dirs = lvl
        pool = [w for w in words.split() if 3 <= len(w) <= maxlen]
        chosen = []
        for w in pool:  # skip words hidden inside another word (BEE/BEETLE) -> keeps one clear answer each
            if len(chosen) < k and not any(w in o or o in w for o in chosen): chosen.append(w)
        assert len(chosen) == k, (title, chosen)
        g, placed = make_puzzle(chosen, n, dirs, rng)
        puzzle_page(c, i, title, lvl, g, placed, art((i - 1) % 25 + 1)); c.showPage()
        done.append((i, title, g, placed))
    for p in range(0, 60, 4):
        answers_page(c, done[p:p + 4], p + 1); c.showPage()
    certificate(c); c.showPage()
    c.save()
    pages = 2 + 60 + 15 + 1
    print('interior pages', pages)


if __name__ == '__main__':
    build()

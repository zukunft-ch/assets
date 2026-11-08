# Visuals · prompt kit

Images for die-zukunft.ch, generated with ChatGPT (image generation) in one consistent visual language:
**Switzerland in a tangible near future** — the Cyberparadism idea (a calm, advanced human place inside a
large, real landscape) applied to Swiss everyday life and politics.

## Rules (non-negotiable)

1. **Always labelled.** Every image is published with the caption «Visualisierung · KI-generiert». No exceptions.
2. **No real people, no recognisable real places presented as real.** No politicians, no identifiable
   faces, no photo-realistic «Basel in 2040». Generic Swiss settings only (a valley town, a lake shore, a farm).
3. **No text, logos, flags or signage** in the image (they come out garbled and look fake).
4. **One look.** Always paste the STYLE block below before the scene prompt. Do not freestyle the style.
5. **Keep the provenance.** Save each result as `visuals/incoming/<slot>.png` and paste the exact prompt
   you used into `visuals/incoming/<slot>.txt`. Claude turns these into web images + a provenance record.

## How to generate

- ChatGPT → new chat → paste **STYLE + SCENE** as one message. Ask for **landscape 3:2 (1536×1024)**.
- Generate 2–4 variants per slot, keep the one that best follows the rules. If people come out too large
  or too posed, reply: «same scene, people smaller and further away, seen from behind or in profile».
- If it drifts into sci-fi (neon, holograms, chrome, flying vehicles): reply «less futuristic, more like a
  quiet documentary photograph of an ordinary Swiss morning, technology barely noticeable».

## STYLE (paste before every scene)

> Documentary photograph, medium format, natural colour, subtle film grain, soft early-morning
> alpenglow light (pale rose and violet in the sky, warm light on the land, clear air, light haze in
> the distance). A real Swiss landscape dominates the frame (about two thirds): mountains, lake, meadows,
> forest or river. Human-made structures are small, calm and well made: pale ceramic, light timber, glass,
> low and integrated into the terrain. Technology is mature and quiet: matte white, rounded, functional,
> never the subject of the picture. Few people, small in the frame, natural and unposed, seen from a
> distance, behind or in profile, no recognisable faces. One small accent of warm rose or violet. Wide
> composition, high horizon, a sense of order and calm. No text, no logos, no flags, no signage, no
> screens or holograms, no neon, no chrome, no spaceships or flying vehicles, no crowds, no dystopia,
> no glossy CGI look.

## Vision · «Die Schweiz im Jahr 2040» (6 slots)

| Slot | Scene (paste after STYLE) |
|---|---|
| `vision-01-behoerden` | A small Swiss village administration building on a quiet square with a cherry tree. A woman walks out after a few minutes with a relaxed expression, the bright waiting area behind the glass is empty. Morning, mountains behind the village. |
| `vision-02-assistenz` | An older man sits on a timber balcony of a modest Swiss apartment above a lake, talking calmly into a small matte-white earpiece, a cup of coffee and a paper notebook on the table. Distant mountains, early light. |
| `vision-03-fabrik` | A compact, light-filled precision workshop in a green Alpine valley, glass façade open to the meadow. Inside, matte-white robot arms assemble small medical devices; two technicians in plain work clothes check a part. The landscape outside dominates. |
| `vision-04-bauen` | Prefabricated timber housing modules being placed by a slim crane next to a small regional train station on a lake shore; a compact white robot fastens a module, a few workers watch. Mountains and water dominate. |
| `vision-05-hof` | An Alpine farm in early morning dew: a small low autonomous field robot moves along neat vegetable rows, a farmer and a child watch from the edge of the field, wooden farmhouse and forested slopes behind. |
| `vision-06-zeit` | A riverside park in a Swiss town on a weekday afternoon: people of different ages reading, a parent with a toddler, two people in conversation on a bench, a cyclist. Calm river, trees, hills beyond. |

## Pillar heroes (13 slots)

| Slot | Pillar | Scene (paste after STYLE) |
|---|---|---|
| `pillar-souveraene-ki` | Souveräne KI & Rechenkraft | A low, discreet compute building with a timber and glass façade set into a hillside above a reservoir lake, warm air vents feeding a greenhouse next to it; mountains and a hydroelectric dam in the distance. |
| `pillar-digitale-souveraenitaet` | Digitale Souveränität | A quiet server room inside a mountain-side building, one large window open to a snowy valley; a technician in the distance inspects a rack. Order, calm, daylight. |
| `pillar-robotik` | Reindustrialisierung mit Robotik | Same visual family as `vision-03-fabrik`, but wider: a small industrial campus of three low buildings in a valley, solar roofs, a freight rail siding, meadows all around. |
| `pillar-uebergaenge` | Arbeit ohne Angst | A bright vocational workshop in a Swiss town where adults of different ages learn to service a small robot arm with an instructor; large windows onto a river. |
| `pillar-life-science` | Life Science & Gesundheit | A small modern health centre in a village, glass and timber, a nurse walking with an elderly patient in the garden; mountains behind. |
| `pillar-grundeinkommen` | Grundeinkommen | A young woman opens a small workshop in a village shop space, morning light, a neighbour helps carry a table; the valley behind. Feeling: a calm new start. |
| `pillar-stadte-wohnen` | Städte & Wohnen | A compact, green neighbourhood around a small train station on a lake: mid-rise timber buildings, trees, people walking and cycling, the lake and mountains dominating. |
| `pillar-research-innovation` | Forschung, Innovation & Commons | A university research garden on a hill: a small glass lab pavilion, two researchers with a field instrument among meadow plants, the city and lake far below. |
| `pillar-energy-resilience` | Energie & Infrastruktur-Resilienz | An Alpine reservoir and dam at dawn, a slim new pumped-storage intake, power lines tracing the valley; small maintenance vehicle, no people close. |
| `pillar-offener-staat` | Offener Staat | A bright, open public hall of a small Swiss town hall with tall windows; a few citizens at standing tables, a civil servant explaining something at a calm counter; mountains visible through the windows. |
| `pillar-neutralitaet-frieden` | Neutralität & Frieden | A lakeside conference villa in early morning, a long wooden table seen through tall windows, empty chairs set for a meeting; mist on the lake, mountains. |
| `pillar-talent-integration` | Talent, Integration & Rechtsstaat | A small group of researchers and founders of different backgrounds arriving with luggage at a regional train station, a host greeting them; lake and mountains behind. Seen from a distance. |
| `pillar-sprache-verstaendigung` | Sprache & Verständigung | A village square at a language border: a café terrace with people in quiet conversation, a market stall, a bilingual atmosphere without any visible text; Jura hills behind. |

## Zukunftslabor (1 slot)

| Slot | Scene |
|---|---|
| `lab-hero` | A calm research room with a long timber table, printed charts and a laptop, a window onto a lake and mountains; one person writing in a notebook in the distance. Evening alpenglow. |

## After generating

Put files in `visuals/incoming/` (PNG + TXT per slot) and tell Claude. It will:
create WebP/AVIF at 800 and 1600 px, wire them into the site with the caption «Visualisierung · KI-generiert»
and alt texts in four languages, and record prompt, tool and date per image in `visuals/provenance.json`.

## The Future (the-future.world)

The international site uses the same rules with a placeless style (any continent, no Swiss cues).
Its slots, style block, scene prompts and alt texts live in the site repo:
`the-future.world/visuals/slots.toml` (13 areas, join page, homepage scene). Paste `style` + a slot's
`scene`, save as `the-future.world/visuals/incoming/<slot>.png` (+ `<slot>.txt` with the exact
prompt), then run `mise run visuals` there.

# Deck specification

See runnable [technical](../examples/technical.json) and [activity](../examples/activity.json) examples.

Required deck fields:

| Field | Type / meaning |
|---|---|
| `title`, `language` | Non-empty strings, e.g. `zh-CN` or `en` |
| `mode` | `technical`, `activity`, `innovation`, `medical`, `heritage` |
| `style` | One existing `styles/<id>.json` |
| `aspect_ratio` | `16:9` in this release |
| `slide_count` | Integer matching slides length |
| `slides` | Non-empty list of page objects |

Required page fields:

| Field | Meaning |
|---|---|
| `page` | Sequential integer starting at 1 |
| `type` | Layout ID from [layouts](layouts.md) |
| `title` | Must occur verbatim in `visible_text` |
| `visible_text` | Non-empty list of exact strings; include title, visible citations, page markers and navigation if desired |
| `key_message` | Purpose for planning/notes, not rendered by default |
| `layout` | Composition and directed relationships, not visible copy |
| `evidence_status` | `confirmed`, `supplied-quote`, `synthetic-demo`, `placeholder`, `unverified` |

Optional page fields: `visual_elements` and `source_basis` (text lists), `speaker_notes` (string), `image` (page image path), `reviewed` (boolean), `source_image` (original evidence path), `preserve_pixels` (boolean), `image_box` (`[left, top, width, height]`, normalized 0–1), `image_box_color` (Pillow-compatible color).

Preserving originals requires `source_image` and `image_box`. The package script scales proportionally and letterboxes inside the slot. Original file content is retained, although scaling changes pixel values. Review the composite after insertion.

Paths resolve relative to the specification file, not the shell working directory. Copying a spec requires checking its relative paths. A `reviewed: true` flag records an external visual review; no script can infer that review took place.

Keep a separate fact ledger when the project needs it: claim, source file/section, date, units, status, caveat. `source_basis` contains references to that evidence. Structural validation does not verify cited files, factual truth, visual quality or narrative completeness. If a synthetic/unknown status matters to interpretation, add an explicit disclosure to `visible_text`; metadata alone does not inform the audience.

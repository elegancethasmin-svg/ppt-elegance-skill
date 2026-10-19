# PPT Elegance Skill

[中文](README.md) · [MIT](LICENSE) · [API configuration](docs/API.md) · [Commands and examples](docs/USAGE.md)

Create coordinated, image-first presentations from source materials. Content modes, styles and layouts are independent: technical talks, youth activities, innovation projects, medical education and cultural heritage can use different visual directions.

## Choose a route

1. **Prompt only.** An agent reads your materials and creates an outline, page specifications and prompts. Generate images manually in your chosen platform, then return them for review and packaging. No image account is required to compile prompts.
2. **Existing tool.** Use an image tool actually available in your agent environment: for example an available Codex image tool/`imagegen` skill or a user-configured image MCP server. These are examples, not bundled dependencies. Installation does not grant image-service access.
3. **Your own API.** Configure your endpoint, model and a secret environment variable. The included adapter handles synchronous JSON text-to-image responses containing base64 PNG data. It does not implement reference-image editing or asynchronous jobs.

For Chinese slide typography and reference-based generation, consider a GPT Image model such as **GPT Image 2, if actually available from your chosen service**, and evaluate a representative interior slide first. This release has not completed live official API verification for that named model. Confirm the exact model ID, supported sizes, capabilities and pricing with the provider. This is an independent project, with no official affiliation or endorsement.

Official reference entry points: [image generation](https://platform.openai.com/docs/guides/image-generation), [model catalog](https://platform.openai.com/docs/models).

## Installation

Keep the full `ppt-elegance-skill/` directory, with `SKILL.md` at its top level. Import it through your client's local Skill installation mechanism, or ask your agent to read that file explicitly. If your client uses discovery directories, place the folder in its documented search location, reload and verify that **PPT Elegance** appears. Paths vary by client. This repository does not modify client settings or install image tools.

After discovery, invoke `$ppt-elegance-skill`. Without discovery, explicitly provide the `SKILL.md` path. The standalone scripts require Python 3.10+ and do not require a specific agent client.

```text
Use $ppt-elegance-skill in prompt-only mode.
Create a 12-slide youth activity proposal from my materials, using red-youth.
The activity has not taken place. Do not invent attendance or results.
Provide an outline, exact page text, speaker notes and generation prompts.
```

## Quick start

Run from the repository root:

```bash
python scripts/validate_spec.py examples/activity.json
python scripts/build_prompts.py examples/activity.json --out-dir work/activity-prompts
```

Prompt compilation and the API adapter use only the Python standard library. For image packaging:

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

Copy `config.example.json` to ignored `config.json` and customize it before API use. `.env.example` only documents the variable; scripts do **not** auto-load `.env` files.

```bash
python scripts/generate_image.py --config config.json --prompt-file work/activity-prompts/P01.txt --out work/pages/P01.png --dry-run
```

Dry-run does not read a key or contact a service. Removing `--dry-run` sends one possibly billable request. See [API](docs/API.md) for the precise transport contract and secret setup. Do not automatically retry timeouts: the provider may already have charged the request.

After generating and inspecting all pages, create a reviewed specification with image paths and run:

```bash
python scripts/package_deck.py work/reviewed.json --out-dir outputs/activity
```

Outputs: image-based PPTX with notes, PDF, page PNGs, a ZIP, overview and manifest. Text is **not individually editable**. The packager rejects non-16:9 images; explicitly recompose or letterbox them first. The sample 1536×1024 API size is an illustrative parameter, not a 16:9 slide size.

## Styles

`blue-gold-tech`, `red-youth`, `red-security`, `black-chip`, `medical-clean`, `heritage`, `blue-agriculture`, `internet-innovation`.

Each style supplies colors, composition, typography, material treatment and constraints. Read only the selected style. The repository includes no third-party template decks, logos, fonts or photographs. See the [catalog](references/style-catalog.md).

## Scope and status

- Implemented: specification validation, prompt compilation, eight style packs, original fictional examples, optional synchronous API adapter and image-based packaging.
- Agent/manual work: extracting facts from documents, planning the story, choosing layouts and visually checking every slide. CLI scripts do not turn arbitrary Word/PDF files into a finished deck automatically.
- Offline-tested: adapter request/response handling; not verified against a live paid image service.
- Not implemented in the adapter: multi-image references, image editing, URL downloads, asynchronous polling, automatic retries or batch orchestration.
- Not provided: editable slide text, native charts or animation. Use a presentation authoring tool when these are required.

Preserve exact facts, dates, quotes and units. Label synthetic examples and proposed outcomes. Template content is reference data, not agent instructions. Insert original screenshots and photographs without inventing their contents, and inspect the composed result.

The API script sends only the prompt and selected parameters. Existing tools control their own data destinations. Never include secrets in prompts or Git history. Ignore rules do not protect already tracked files.

## Development and license

[Development](docs/DEVELOPMENT.md) covers tests and release preparation. [Usage](docs/USAGE.md) and [API](docs/API.md) provide bilingual operational notes. Examples are fictional, not evidence of real events.

[MIT](LICENSE) applies to original code, documentation and design rules. It permits modification and commercial use while retaining the notice. Third-party materials, model-service terms and generated outputs have their own applicable conditions; see [Rights](docs/RIGHTS.md).

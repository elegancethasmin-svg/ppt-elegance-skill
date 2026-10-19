# Usage / 使用流程

Run commands from the repository root with Python 3.10+. Prompt-only scripts require no dependencies or account. Agents can create the JSON for users who prefer natural-language input.

## A. Prompt-only example / 无接口示例

```bash
python scripts/validate_spec.py examples/technical.json
python scripts/build_prompts.py examples/technical.json --out-dir work/technical-prompts
python scripts/validate_spec.py examples/activity.json
python scripts/build_prompts.py examples/activity.json --out-dir work/activity-prompts
```

每个输出目录包含 `P01.txt` 等逐页提示词和一份规格副本 `deck.json`。目录必须为空或不存在，避免误覆盖。路径在使用时相对于规格文件，因此复制规格到别处时要同步调整图片路径。

`examples/technical.json` 是假想知识系统方案，`examples/activity.json` 是尚未举办的文化团日活动策划。它们只有3页，用来演示运行方式，不是固定页数要求。所有数据与成果边界均已标注。

把页面提示词交给选定的图像平台；如果平台支持参考图，先使用一张已检查的内页保持风格。无参考图能力时只使用风格文字，跨页一致性需要额外人工检查。

Only `visible_text` is rendered copy. `key_message`, `source_basis`, `speaker_notes`, source paths and fact-ledger details are not sent to the image API by the prompt compiler. The selected layout and visual-element descriptions are sent as design instructions; avoid inserting private source material there unnecessarily.

## B. Existing tools / 已有工具示例

```text
使用 $ppt-elegance-skill，通过当前环境实际可用的图像工具制作PPT。
主题：社区志愿服务活动计划。共8页，采用红色青春风格。
读取我提供的活动方案。不要写成已经举办，不要虚构人数或照片。
先组织大纲，再逐页生成、核对文字，最后输出图片型PPTX和PDF。
```

工具不存在时说明缺失，仍可完成提纲与提示词，不假装生成。支持编辑时按工具规则修正；不支持时重新生成该页。整页重生成后必须重新检查，不能假设其他文字保持不变。

Example: an actually installed image skill or MCP image server may accept references and edits. The agent reads that tool's contract and maps prompts and source images to its real arguments. This repository does not assume tool identifiers or credentials.

## C. API / 自配接口示例

完成 [API 配置](API.md)后，以一个页面试运行。默认没有付费自动循环。

```bash
python scripts/generate_image.py --config config.json --prompt-file work/technical-prompts/P01.txt --out work/technical/P01.png --dry-run
python scripts/generate_image.py --config config.json --prompt-file work/technical-prompts/P01.txt --out work/technical/P01.png
```

后续逐页变更文件名执行。检查数字、中文、箭头、页码和比例。API 示例不上传参考图；需要参考图的一致性或编辑能力时改用已有工具或另外实现适配器。

## D. Review and package / 检查与打包

1. 保留所选规格或建立 `work/reviewed.json`，校正每页 `image` 的相对路径。
2. 每页通过人工或智能体视觉检查后，设置 `reviewed: true`。结构校验器不能代替这一步。
3. 若指定原始截图/照片，设置 `preserve_pixels: true`、`source_image`、`image_box`。确保生成底图中的插入区域没有需要保留的文字。
4. 安装 `requirements.txt` 中的可选打包依赖。
5. 运行打包器，再检查合成后的页面。

Minimal page with evidence insertion (other required fields remain as in the original spec):

```json
{
  "image": "pages/P03.png",
  "reviewed": true,
  "preserve_pixels": true,
  "source_image": "assets/original-screenshot.png",
  "image_box": [0.05, 0.25, 0.70, 0.55],
  "image_box_color": "#0B184A"
}
```

`image_box` uses normalized `[left, top, width, height]`. 原图仅等比缩放与留边，不裁剪、不拉伸、不重画；这里的“preserve_pixels”指保留原始图像内容，缩放会重采样像素，并非逐像素完全相同。图片路径都相对于规格 JSON 所在目录。

```bash
python scripts/package_deck.py work/reviewed.json --out-dir outputs/my-deck
```

Output directory must be empty/new. Required pages must be reviewed and approximately 16:9 (tolerance 0.005 in width/height ratio). Packaging normalizes pages to 1920×1080, includes source references in notes and creates:

- `presentation.pptx`: 16:9 image slides and speaker notes, no separately editable text.
- `presentation.pdf`: identical page images, no OCR text layer.
- `pages/` and `pages.zip`: final composited PNGs.
- `overview.jpg`: page-order contact sheet.
- `manifest.json`: page order, hashes and whether source-image insertion occurred.

The packager does not decide factual accuracy or perform visual review. If it inserted source images, inspect the resulting pages and any labels pointing to them. Source labels and notes may contain private data: review before sharing the final deck.

## Changing a style or adding pages

Change the top-level `style` ID, then compile into a new prompt directory. This does not redesign already generated images: those pages need new generation or editing. Do not regenerate pages without considering their cost.

When adding pages, update `slide_count`, sequential page numbers, and the exact visible page markers in `visible_text`. Content modes and layout descriptions guide the agent; they are not automatic content generators.

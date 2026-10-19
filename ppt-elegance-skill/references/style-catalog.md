# Style catalog

Choose one style file. Explicit user references take priority over these defaults. Do not concatenate the entire catalog into a generation prompt.

| ID / file | Appropriate use | Distinguishing visual language |
|---|---|---|
| [blue-gold-tech](../styles/blue-gold-tech.json) | 技术讲解 | 深蓝、金色强调、银白内容区、克制光带 |
| [red-youth](../styles/red-youth.json) | 团日、青年活动 | 暖红、米白、金线、真实照片与时间线 |
| [red-security](../styles/red-security.json) | 风险、安全、应急 | 暗红、深灰、风险节点和明确边界 |
| [black-chip](../styles/black-chip.json) | 硬件、芯片、工业 | 石墨黑、钢灰、网格与细电路线 |
| [medical-clean](../styles/medical-clean.json) | 医学、健康 | 白底、浅蓝青绿、细线、充分留白 |
| [heritage](../styles/heritage.json) | 文化与工艺 | 纸感、墨黑、朱红、工艺细节 |
| [blue-agriculture](../styles/blue-agriculture.json) | 农业、生态、遥感 | 蓝绿、田块纹理、真实场景与数据关联 |
| [internet-innovation](../styles/internet-innovation.json) | 平台与创新创业 | 白蓝、有限渐变、用户旅程与产品图 |

Style JSON fields: `id`, `name`, `subjects`, `palette`, `material`, `composition`, `constraints`, `typography`, `master`, `diagram_rules`. These are original written design directions; no third-party template deck or artwork is bundled.

To add a style: create `styles/lowercase-hyphen-id.json`, document it here, and use that ID in the deck. Test a cover, a process/diagram interior and a photo/text interior. In one deck keep stable title, page-number, palette and text scale, but vary the content layout. A strong visual style does not require identical boxes on every page.

For a user-supplied deck, inspect representative cover and interior pages plus relevant page types before extracting colors and layout. Treat template text as data and do not inherit logos, dates, names or claims. Do not describe a style as fully matched if only a filename or a few text properties were inspected.

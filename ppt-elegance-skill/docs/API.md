# API configuration / 接口配置

## Contract and scope

The bundled `images-json` adapter makes exactly one synchronous request:

```text
POST {base_url}/images/generations
Authorization: Bearer <value from the named environment variable>
Content-Type: application/json
```

Request fields: `model`, `prompt`, `n: 1`, plus selected string parameters. Expected response:

```json
{"data": [{"b64_json": "<base64-encoded PNG>"}]}
```

Some services use this protocol; others do not. **Changing a URL does not make every provider compatible.** Verify field names and supported values with the selected service. Reference images, masks, editing, streaming, asynchronous task IDs and URL-only responses require another adapter or an existing capable tool. This release intentionally does not follow redirects or arbitrary returned image URLs.

## 1. Configuration

Copy `config.example.json` to `config.json` in the repository root. Set:

| Field | Meaning |
|---|---|
| `adapter` | Must be `images-json` for the bundled script |
| `base_url` | Your documented API prefix; HTTPS, no embedded credentials/query/fragment |
| `model` | Exact service model ID; not a marketing/display name |
| `api_key_env` | Environment variable containing your key; default example is `PPT_IMAGE_API_KEY` |
| `timeout_seconds` | 1–1200 seconds; default example 600 |
| `parameters` | Provider-supported `size`, `quality`, `output_format`, `background`, `response_format` string values |

Reserved fields `model`, `prompt` and `n` cannot be overridden in `parameters`. PNG only: omit `output_format` if PNG is the documented default, or set it to `png` if supported. Use `response_format: b64_json` only if the service accepts that parameter; some services return base64 automatically.

The size in the example is illustrative. It is **not** 16:9. Select a documented 16:9 size when available. Otherwise generate, then explicitly recompose or add borders without cropping text. The packaging script rejects non-16:9 inputs rather than stretching them. Do not assume 1920×1080 is accepted by every API.

GPT Image 2 is a suggested candidate when available, not a hardcoded default. Verify exact identifiers and capabilities in [the model catalog](https://platform.openai.com/docs/models) and [image guide](https://platform.openai.com/docs/guides/image-generation). If you cannot verify them, keep the model unconfigured and use prompt-only mode.

## 2. Secret setup

Never put a real key in the committed config. `.env.example` documents names only; there is no implicit `.env` loader.

Windows PowerShell (interactive hidden input; variable lasts for this process):

```powershell
$credential = Get-Credential -UserName 'image-api' -Message 'Enter your API key in the password field'
$env:PPT_IMAGE_API_KEY = $credential.GetNetworkCredential().Password
```

macOS/Linux Bash:

```bash
read -rsp "Image API key: " PPT_IMAGE_API_KEY
export PPT_IMAGE_API_KEY
```

A secret manager or your IDE's environment settings can supply the same variable. Never paste a key into issue reports, prompts or screenshots. After a session, clear it with `Remove-Item Env:PPT_IMAGE_API_KEY` (PowerShell) or `unset PPT_IMAGE_API_KEY` (Bash).

## 3. Validate, then generate

After compiling prompts:

```bash
python scripts/generate_image.py --config config.json --prompt-file work/prompts/P01.txt --out work/pages/P01.png --dry-run
python scripts/generate_image.py --config config.json --prompt-file work/prompts/P01.txt --out work/pages/P01.png
```

Dry-run checks configuration but not credentials, model availability or service compatibility. The second command performs one request and may incur charges. It saves a new PNG, refuses to overwrite an existing file and does not print the key or service response body.

Generate the next page only after reviewing the current one. Reuse existing reviewed files rather than rerunning paid requests. The CLI has no automatic batch mode or retry loop. After a timeout, check provider status/billing before manually retrying. Agent guidance allows at most two reattempts per page by default, but this is a ceiling, not an instruction to retry an ambiguous charged request.

## 4. Troubleshooting / 故障处理

- `Replace the example endpoint`: 配置仍含占位地址。
- `Set the model ID`: 请填入服务文档所列模型 ID。
- Missing environment variable: 密钥没有导出到运行脚本的同一进程环境；`.env` 不会自动读取。
- HTTP error: 错误正文被隐藏，避免泄露；在服务端查看权限、额度、参数和请求状态。
- Expected `b64_json`: 接口协议不符；URL 或异步任务返回需要其他适配器。
- Not a PNG: 修改服务输出格式，不能只重命名 JPEG。
- Timeout: 请求可能已计费，先查询服务端，不自动重试。

## Adapter extension

Keep provider code outside style and content files. Document supported operations, aspect ratios, input images, output encoding, timeout behavior and data destinations. An editing adapter must actually upload image bytes through its documented protocol; a local path embedded in a text prompt is not an uploaded image.

Never pass secrets through CLI arguments or import another skill's private credentials. Add mocked tests before declaring support. Mark a provider live-tested only after an authorized real request succeeds; offline tests are not service verification.

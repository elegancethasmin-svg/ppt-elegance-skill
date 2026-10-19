"""A narrow synchronous Images-JSON adapter. No SDK, hidden keys, or retries."""
import argparse
import base64
import binascii
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from common import read_json

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward bearer credentials to a redirect destination.

def prepare(config, prompt):
    if config.get('adapter') != 'images-json':
        raise ValueError('Only the images-json adapter is implemented')
    u = urllib.parse.urlsplit(config.get('base_url', ''))
    if u.scheme != 'https' or not u.hostname or u.username or u.password or u.query or u.fragment:
        raise ValueError('base_url must be HTTPS, without embedded credentials, query or fragment')
    if u.hostname == 'api.example.com':
        raise ValueError('Replace the example endpoint with your chosen service')
    model = config.get('model')
    if not isinstance(model, str) or not model.strip() or model == 'your-image-model':
        raise ValueError('Set the model ID documented by your provider')
    env = config.get('api_key_env', '')
    if not isinstance(env, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', env):
        raise ValueError('api_key_env must name an environment variable')
    params = config.get('parameters', {})
    if not isinstance(params, dict) or set(params) - {'size', 'quality', 'output_format', 'background', 'response_format'}:
        raise ValueError('Unsupported parameter; see docs/API.md')
    if any(not isinstance(v, str) for v in params.values()):
        raise ValueError('Parameter values must be strings')
    if params.get('output_format', 'png') != 'png':
        raise ValueError('This adapter saves PNG only; select output_format png or omit it')
    timeout = config.get('timeout_seconds', 600)
    if type(timeout) not in (int, float) or not 1 <= timeout <= 1200:
        raise ValueError('timeout_seconds must be between 1 and 1200')
    if not prompt.strip():
        raise ValueError('Prompt cannot be empty')
    payload = {'model': model, 'prompt': prompt, 'n': 1, **params}
    return config['base_url'].rstrip('/') + '/images/generations', payload, timeout, env

def request_image(url, payload, timeout, key):
    if any(c.isspace() for c in key):
        raise ValueError('API key contains whitespace; check the environment variable')
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key}, method='POST')
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=timeout) as response:
            data = response.read(80 * 1024 * 1024 + 1)
        if len(data) > 80 * 1024 * 1024:
            raise ValueError('Response too large')
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f'HTTP {exc.code}; response body suppressed. Check provider documentation/account.') from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise RuntimeError('Network failure or timeout. Request may have been charged; check provider status before retrying.') from None
    except ValueError:
        raise RuntimeError('Invalid request or oversized response; service details suppressed.') from None
    return decode_image(data)

def decode_image(data):
    try:
        obj = json.loads(data)
        b64 = obj['data'][0]['b64_json']
        raw = base64.b64decode(b64, validate=True)
    except (ValueError, KeyError, IndexError, TypeError, binascii.Error):
        raise ValueError('Expected data[0].b64_json. URL-only and asynchronous responses need another adapter.') from None
    if not raw.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('Response is not a PNG image; check provider output format')
    return raw

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', required=True)
    p.add_argument('--prompt-file', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--dry-run', action='store_true', help='Validate configuration without loading a key or contacting a service')
    args = p.parse_args()
    try:
        out = Path(args.out)
        if out.exists():
            raise ValueError('Output already exists; use a new filename')
        if out.suffix.lower() != '.png':
            raise ValueError('Output filename must end in .png')
        url, payload, timeout, env = prepare(read_json(args.config), Path(args.prompt_file).read_text(encoding='utf-8-sig'))
        if args.dry_run:
            print('Configuration valid. One synchronous text-to-image request; no key read or network call.')
            return
        key = os.environ.get(env)
        if not key:
            raise ValueError(f'Set {env} in the process environment; .env files are not auto-loaded')
        raw = request_image(url, payload, timeout, key)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open('xb') as f:
            f.write(raw)
    except (ValueError, RuntimeError, OSError) as exc:
        p.exit(1, f'Generation failed: {exc}\n')
    print('Image saved. Inspect text, relationships and aspect ratio before packaging.')

if __name__ == '__main__':
    main()

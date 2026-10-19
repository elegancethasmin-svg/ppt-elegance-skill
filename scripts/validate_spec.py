import argparse
from common import read_json, validate

def main():
    parser = argparse.ArgumentParser(description='Validate a deck specification without generating images.')
    parser.add_argument('spec')
    args = parser.parse_args()
    try:
        deck = validate(read_json(args.spec))
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Invalid specification: {exc}\n')
    print(f"Valid: {len(deck['slides'])} slides. Structure only; facts and visual quality require review.")

if __name__ == '__main__':
    main()

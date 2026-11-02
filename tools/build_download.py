#!/usr/bin/env python3
"""Build a deterministic standalone skill download, or verify its contents."""
import argparse
import io
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/saas-builder'


def package_bytes():
    stream = io.BytesIO()
    with ZipFile(stream, 'w', compression=ZIP_DEFLATED) as archive:
        for path in sorted(SKILL.rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                if path.is_symlink():
                    raise ValueError('Do not package symlinks')
                name = 'saas-builder/' + path.relative_to(SKILL).as_posix()
                info = ZipInfo(name, date_time=(2026, 11, 2, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, path.read_bytes())
    return stream.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    destination = ROOT / 'docs/saas-builder.zip'
    expected = package_bytes()
    if args.check:
        assert destination.read_bytes() == expected, 'Rebuild the download with python3 tools/build_download.py'
        print('Download matches the installable skill exactly.')
    else:
        destination.write_bytes(expected)
        print('Built docs/saas-builder.zip')


if __name__ == '__main__':
    main()

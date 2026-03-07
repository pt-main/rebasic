"""
Build script for Rebasic framework.
Merges specified source files into a single executable rebasic.py.
"""

import os
import sys
import time
from pathlib import Path

# Constants
RELEASE = 0
VERSION_FILE = 'version.txt'
SOURCE_DIR = Path('src')
OUTPUT_FILE = Path('rebasic.py')
FILES_TO_PARSE = [
    'rebasic/tooling/templating',
    'rebasic/parsing/base',
    'rebasic/parsing/parsemeta',
    'rebasic/parsing/parse',
    'rebasic/parsing/parse2',
    'rebasic/systems/exceptions',
    'rebasic/systems/context',
    'rebasic/systems/state',
    'rebasic/systems/code_state',
    'rebasic/systems/lang_config',
    'rebasic/systems/generation',
    'rebasic/systems/event',
    'rebasic/_defaults',
    'rebasic/engine',
    'rebasic/_basics',
    'rebasic/tooling/langtools/_backend_template',
    'rebasic/tooling/langtools/__templates',
    'rebasic/tooling/langtools/python',
    'rebasic/tooling/langrepl',
    'rebasic/langfile/langfile_data',
    'rebasic/langfile/parse_file',
    'cli'
]


license = '''### Copyright (c) 2026 Pt
### SPDX-License-Identifier: Apache-2.0\n'''

def get_state(release: int) -> str:
    """Return release state string based on release number."""
    if release == 0:
        return 'alpha'
    elif release == 1:
        return 'beta'
    else:
        return 'stable'


def update_version() -> str:
    """
    Read version number from file, increment by 0.1, and write back.
    Return full version string in format 'release.version-state'.
    """
    try:
        with open(VERSION_FILE, 'r') as f:
            content = f.read().strip()
            try:
                val = float(content)
            except ValueError:
                print(f"Error: {VERSION_FILE} contains non-numeric value '{content}'")
                sys.exit(1)
    except FileNotFoundError:
        print(f"{VERSION_FILE} not found, starting at 0.0")
        val = 0.0

    val = round(val + 0.1, 1)
    with open(VERSION_FILE, 'w') as f:
        f.write(str(val))

    state = get_state(RELEASE)
    return f"{RELEASE}.{val}-{state}"


def main():
    print('Starting build...')

    version = update_version()
    print(f"Building version: {version}")

    # Change to source directory
    if not SOURCE_DIR.exists():
        print(f"Error: source directory {SOURCE_DIR} not found")
        sys.exit(1)
    os.chdir(SOURCE_DIR)

    # Read the base __init__.py content
    with open('rebasic/__init__.py', 'r') as f:
        init_content = f.read()
    # Keep everything before the first '# === start file ===' marker
    base_code = init_content.split('# === start file ===')[0]

    # Build header with version info
    build = base_code.replace('---', license) + f"""
# BUILD v{version}
# By Pt

REBASIC_BUILD_VERSION = '{version}'
__TestAvailable = False
__BuildAvailable = True
__CliAvailable = False
"""

    # Separator line
    sep_line_length = 97  # full length of one debug line

    sep = '=' * sep_line_length
    build += f'\n# {sep}\n# {"MARK: start of framework".center(len(sep))}\n# {sep}\n'
    
    print('=' * sep_line_length)
    warnings = []
    total_lines = 0
    total_chars = 0
    for idx, file in enumerate(FILES_TO_PARSE):
        file_path = f"{file}.py"
        try:
            with open(file_path, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            warnings.append(f"Warning: {file_path} not found, skipping")
            continue

        # Extract code after '# === start file ===' marker
        code = '# === start file ==='.join(content.split(
            '# === start file ===')[1:]).split('# === end file ===')[0]
        if not code:
            warnings.append(f"Warning: {file_path} contains no start marker, using whole file")
            code = content

        lines = code.split('\n')
        lines_count = len(lines)
        total_lines += lines_count
        chars_count = len(code)
        total_chars += chars_count

        text = f"{idx:4} : {file:50} : {lines_count:6} : {
            total_lines:6} : {chars_count:6} : {total_chars:10}"
        print(text)

        # Add file header
        build += f'\n# {sep}\n# {(f"MARK: {file}.py ({lines_count} lines, {
            chars_count} chars)").center(len(sep))}\n# {sep}\n'
        build += code + '\n'

        time.sleep(0.005)  # Small delay for visual effect
    print('=' * sep_line_length)

    # Footer
    build += f'\n# {sep}\n# {"MARK: end of framework".center(len(sep))} \n# {sep}\n'

    print('Warnings: ')
    for warn in warnings:
        print(f'    {warn}')
    if len(warnings) == 0:
        print('    Has no warnings')

    # Return to original directory
    for _ in range(len(SOURCE_DIR.parts)):
        os.chdir('..')

    # Write the final build
    with open(OUTPUT_FILE, 'w') as f:
        f.write(build)

    print(f'Build completed successfully. Output written to {OUTPUT_FILE}')
    print(f'Total lines: {total_lines}')
    print(f'Total chars: {total_chars}')
    print(f'Total files: {idx}')


if __name__ == '__main__':
    main()






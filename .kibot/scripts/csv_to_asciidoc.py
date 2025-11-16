#!/usr/bin/env python3
"""
Convert KiBot CSV BOM files to AsciiDoc table format.

Usage:
    python csv_to_asciidoc.py input.csv output.adoc [--datasheet-column COLUMN_NAME]
    python csv_to_asciidoc.py input.csv  # prints to stdout

Examples:
    # Convert with datasheet links merged into Value column
    python csv_to_asciidoc.py input.csv output.adoc --datasheet-column Datasheet
"""

import csv
import sys
import re
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple


def is_url(text: str) -> bool:
    """Check if text looks like a URL."""
    url_pattern = re.compile(r'^https?://', re.IGNORECASE)
    return bool(url_pattern.match(text.strip()))


def collect_unique_notes(rows: List[Dict[str, str]], note_column: str) -> Dict[str, int]:
    """
    Collect unique non-empty notes and assign numbers to them.

    Returns:
        Dict mapping note text to note number (1, 2, 3, ...)
    """
    unique_notes = {}
    note_number = 1

    for row in rows:
        note = row.get(note_column, '').strip()
        if note and note not in unique_notes:
            unique_notes[note] = note_number
            note_number += 1

    return unique_notes


def csv_to_asciidoc_table(csv_file: Path, output_file: Path = None,
                          datasheet_column: Optional[str] = None) -> str:
    """
    Convert a CSV BOM file to an AsciiDoc table.

    Table columns (in order): Designator, Qty, Value, Note, Reference Part
    - Note column shows number reference, actual notes appear as footnotes below table
    - If datasheet_column specified, datasheet links are merged into Value column

    Args:
        csv_file: Path to input CSV file
        output_file: Optional path to output file. If None, returns string.
        datasheet_column: Optional column name containing datasheet URLs to merge into Value

    Returns:
        AsciiDoc table as string
    """
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        if not rows:
            return "No data found in CSV file."

        # Define desired column order
        column_order = ['Designator', 'Qty', 'Value', 'Note', 'Reference Part']

        # Collect unique notes and assign numbers
        note_map = collect_unique_notes(rows, 'Note')

        # Build AsciiDoc table
        # Column widths: Designator (2), Qty (0-no space), Value (3), Note (0-no space), Reference Part (3)
        lines = []
        lines.append('[cols="2,0,3,0,3", options="header"]')
        lines.append("|===")

        # Add headers
        for header in column_order:
            lines.append(f"| {header}")
        lines.append("")

        # Add data rows
        for row in rows:
            for col in column_order:
                value = row.get(col, '').strip()

                # Escape pipe characters
                value = value.replace("|", "\\|")

                # Special handling for Value column - merge datasheet link
                if col == 'Value' and datasheet_column:
                    datasheet = row.get(datasheet_column, '').strip()
                    if datasheet and is_url(datasheet):
                        value = f"{value} [link:{datasheet}[DS]]"

                # Special handling for Note column - replace with clickable number
                elif col == 'Note' and value:
                    note_num = note_map.get(value, '')
                    if note_num:
                        # Create a clickable link to the note definition
                        value = f"<<note-{note_num},{note_num}>>"
                    else:
                        value = ''

                lines.append(f"| {value}")
            lines.append("")

        lines.append("|===")

        # Add note footnotes if any exist
        if note_map:
            lines.append("")
            lines.append("// Note footnotes")
            for note_text, note_num in sorted(note_map.items(), key=lambda x: x[1]):
                # Escape the note text
                escaped_note = note_text.replace("|", "\\|")
                # Add anchor so note numbers in table can link here
                lines.append(f"[[note-{note_num}]]{note_num}. {escaped_note} +")

        result = "\n".join(lines)

        if output_file:
            # Create parent directory if it doesn't exist
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as out:
                out.write(result)
                out.write("\n")
            print(f"✓ Converted {csv_file} to {output_file}")

        return result


def main():
    parser = argparse.ArgumentParser(
        description='Convert KiBot CSV BOM files to AsciiDoc table format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic conversion
  %(prog)s input.csv output.adoc

  # Convert with datasheet links in Value column
  %(prog)s input.csv output.adoc --datasheet-column Datasheet
'''
    )

    parser.add_argument('input', type=Path, help='Input CSV file')
    parser.add_argument('output', type=Path, nargs='?', help='Output AsciiDoc file (if not specified, prints to stdout)')
    parser.add_argument('--datasheet-column', type=str, metavar='COLUMN',
                       help='Column name containing datasheet URLs to merge into Value column')

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        sys.exit(1)

    result = csv_to_asciidoc_table(args.input, args.output, args.datasheet_column)

    if not args.output:
        print(result)


if __name__ == "__main__":
    main()

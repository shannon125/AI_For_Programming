"""Print GC content percentages for records in a FASTA file."""

import argparse
import sys


def fasta_records(path):
    """Yield (header, sequence) pairs from a FASTA file."""
    header = None
    sequence = []

    with open(path) as fasta_file:
        for line in fasta_file:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(sequence)
                header = line[1:]
                sequence = []
            elif header is None:
                raise ValueError("Expected a FASTA header beginning with '>'.")
            else:
                sequence.append(line)

    if header is not None:
        yield header, "".join(sequence)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fasta_path", help="path to a FASTA file")
    parser.add_argument(
        "--min-gc",
        type=float,
        help="print only records with GC content above this percentage",
    )
    args = parser.parse_args()

    for header, sequence in fasta_records(args.fasta_path):
        if not sequence:
            print(f"Warning: skipping empty sequence for {header!r}.", file=sys.stderr)
            continue
        gc_count = sum(base.upper() in {"G", "C"} for base in sequence)
        gc_content = gc_count / len(sequence) * 100
        if args.min_gc is None or gc_content > args.min_gc:
            print(f"{header}\t{gc_content:.2f}%")


if __name__ == "__main__":
    main()

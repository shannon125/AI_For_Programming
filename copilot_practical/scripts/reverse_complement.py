# reverse_complement.py
# Reads a DNA sequence from a FASTA file and prints its
# reverse complement.

COMPLEMENT = {"A": "T", "T": "A", "C": "G", "G": "C"}


def read_fasta_sequence(path):
    """Return the sequence (str) from a single-record FASTA file."""
    sequence = []
    header_seen = False

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header_seen:
                    raise ValueError("Expected a single-record FASTA file.")
                header_seen = True
                continue
            if not header_seen:
                raise ValueError("Expected a FASTA header beginning with '>'.")
            sequence.append(line)

    if not header_seen:
        raise ValueError("No FASTA record found.")
    return "".join(sequence)


def reverse_complement(seq):
    """Return the reverse complement of a DNA sequence."""
    seq = seq.upper()
    try:
        return "".join(COMPLEMENT[base] for base in reversed(seq))
    except KeyError as error:
        raise ValueError(
            f"Invalid DNA character {error.args[0]!r}; sequence must contain only A, T, C, or G."
        ) from None

if __name__ == "__main__":
    import sys
    seq = read_fasta_sequence(sys.argv[1])
    print(reverse_complement(seq))

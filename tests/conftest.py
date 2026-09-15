import sys
from pathlib import Path

# Make the generator modules importable as top-level modules in tests.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

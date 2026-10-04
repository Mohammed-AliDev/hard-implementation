"""Load the single canonical installer in a built package or source checkout."""
import importlib.util
import json
from pathlib import Path
import sys

try:
    from . import installer
except ImportError:
    path = Path(__file__).resolve().parents[2] / "install.py"
    if not path.is_file():
        raise
    spec = importlib.util.spec_from_file_location("hard_implementation.installer", path)
    installer = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = installer
    spec.loader.exec_module(installer)


def bundled_source():
    resources = Path(__file__).resolve().parent / "resources"
    if (resources / "distribution.json").is_file():
        return resources
    checkout = Path(__file__).resolve().parents[2]
    if (checkout / "distribution.json").is_file():
        return checkout
    raise ValueError("This installation is missing the bundled workflow. Reinstall the hard tool.")


def supported_systems():
    """Read the same system names used by documentation and GitHub About."""
    metadata = bundled_source() / "project-metadata.json"
    return tuple(json.loads(metadata.read_text(encoding="utf-8"))["supported_systems"])

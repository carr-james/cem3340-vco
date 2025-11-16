#!/usr/bin/env python3
"""
Extract 3D model paths from KiCad PCB files.

Parses a .kicad_pcb file and outputs all 3D model file paths
referenced by footprints. Resolves environment variables and
converts to repository-relative paths.

Usage:
    python3 list_3d_models.py <pcb_file>

Output:
    Newline-separated list of relative paths to 3D model files
"""

import sys
import re
import os
from pathlib import Path


def extract_model_paths(pcb_file):
    """Extract all 3D model paths from a KiCad PCB file."""

    if not os.path.exists(pcb_file):
        print(f"Error: PCB file not found: {pcb_file}", file=sys.stderr)
        sys.exit(1)

    with open(pcb_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all (model "path") entries
    # KiCad S-expression format: (model "path/to/model.wrl" ...)
    model_pattern = r'\(model\s+"([^"]+)"'
    matches = re.findall(model_pattern, content)

    model_paths = set()

    for model_path in matches:
        # Resolve environment variables
        resolved_path = resolve_env_vars(model_path)

        # Convert to repository-relative path if possible
        repo_relative = to_repo_relative(resolved_path, pcb_file)

        if repo_relative:
            model_paths.add(repo_relative)

    return sorted(model_paths)


def resolve_env_vars(path):
    """Resolve ${VAR} style environment variables in path."""

    # Pattern to match ${VARIABLE_NAME}
    var_pattern = r'\$\{([^}]+)\}'

    def replace_var(match):
        var_name = match.group(1)
        # Try to get from environment, or return common KiCad paths
        if var_name in os.environ:
            return os.environ[var_name]

        # Handle common KiCad variables with fallbacks
        kicad_vars = {
            'KIPRJMOD': '.',  # Project directory
            'KICAD7_3DMODEL_DIR': '/usr/share/kicad/3dmodels',
            'KICAD6_3DMODEL_DIR': '/usr/share/kicad/3dmodels',
            'KICAD_3DMODEL_DIR': '/usr/share/kicad/3dmodels',
        }

        return kicad_vars.get(var_name, f'${{{var_name}}}')

    return re.sub(var_pattern, replace_var, path)


def to_repo_relative(model_path, pcb_file):
    """
    Convert 3D model path to repository-relative path.

    Returns None if model is from system library (not in repo).
    Returns relative path if model is in hardware/shared submodule or repo.
    """

    # Skip system library paths
    if model_path.startswith('/usr/'):
        return None

    # Get repository root (assume PCB is in hardware/ subdirectory)
    pcb_path = Path(pcb_file).resolve()
    repo_root = pcb_path.parent

    # Navigate up to find repo root (has .git directory or is 2 levels up from hardware/)
    while repo_root.parent != repo_root:
        if (repo_root / '.git').exists():
            break
        if repo_root.name == 'hardware':
            repo_root = repo_root.parent
            break
        repo_root = repo_root.parent

    # Convert model path to absolute if it's relative
    model_abs = Path(model_path)
    if not model_abs.is_absolute():
        # Assume relative to PCB file location
        model_abs = (pcb_path.parent / model_path).resolve()

    # Try to make it relative to repo root
    try:
        relative = model_abs.relative_to(repo_root)
        return str(relative)
    except ValueError:
        # Not in repo, skip
        return None


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <pcb_file>", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    pcb_file = sys.argv[1]
    model_paths = extract_model_paths(pcb_file)

    # Output newline-separated paths
    for path in model_paths:
        print(path)


if __name__ == '__main__':
    main()
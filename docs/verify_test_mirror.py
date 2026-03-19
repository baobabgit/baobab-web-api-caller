"""Vérifie qu'il existe un test miroir pour chaque module sous src/baobab_web_api_caller.

Usage (depuis la racine du dépôt)::

    python docs/verify_test_mirror.py

Sortie : affiche le nombre d'écarts ; code de sortie 0 si aucun, 1 sinon.

Les exceptions de nommage (CallContext, build_call_context, mapping_utils) sont documentées
dans le README ; ce script ne les connaît pas : en cas d'écart, vérifier manuellement.
"""

from __future__ import annotations

import pathlib
import sys


def main() -> int:
    """Point d'entrée."""

    root = pathlib.Path(__file__).resolve().parents[1] / "src" / "baobab_web_api_caller"
    tests_root = root.parent.parent / "tests" / "baobab_web_api_caller"
    missing: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        rel = path.relative_to(root).with_suffix("")
        expected = tests_root / rel.parent / f"test_{rel.name}.py"
        if not expected.exists():
            missing.append((str(path.relative_to(root)), str(expected)))

    print(f"gaps {len(missing)}")
    for src, test in missing:
        print(f"  {src} -> {test}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())

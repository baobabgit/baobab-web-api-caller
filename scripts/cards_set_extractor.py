"""Script utilitaire: extraction d'un "cards set".

Ce script est un squelette (bootstrap). La logique d'extraction sera implémentée ultérieurement.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CardsSetExtractorArgs:
    """Arguments de ligne de commande."""

    input_path: str
    output_path: str


class CardsSetExtractorCli:
    """Point d'entrée CLI pour l'extracteur."""

    def parse_args(self, argv: list[str] | None = None) -> CardsSetExtractorArgs:
        """Parse les arguments CLI.

        :param argv: Arguments, ou None pour utiliser sys.argv.
        :type argv: list[str] | None
        :return: Arguments normalisés.
        :rtype: CardsSetExtractorArgs
        """

        parser = argparse.ArgumentParser(prog="cards-set-extractor")
        parser.add_argument("--input", dest="input_path", required=True)
        parser.add_argument("--output", dest="output_path", required=True)
        ns = parser.parse_args(argv)
        return CardsSetExtractorArgs(input_path=ns.input_path, output_path=ns.output_path)

    def run(self, argv: list[str] | None = None) -> int:
        """Exécute le script.

        :param argv: Arguments, ou None pour utiliser sys.argv.
        :type argv: list[str] | None
        :return: Code de sortie (0=succès).
        :rtype: int
        :raises NotImplementedError: Tant que la logique n'est pas implémentée.
        """

        _ = self.parse_args(argv)
        raise NotImplementedError("Implémentation à venir (branche scripts/cards_set_extractor).")


def main() -> int:
    """Point d'entrée."""

    return CardsSetExtractorCli().run()


if __name__ == "__main__":
    raise SystemExit(main())


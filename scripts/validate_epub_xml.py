from __future__ import annotations

import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"arquivo nao encontrado: {path}"]

    with zipfile.ZipFile(path) as epub:
        names = epub.namelist()
        if not names or names[0] != "mimetype":
            errors.append("o primeiro item do EPUB deve ser 'mimetype'")
        else:
            info = epub.getinfo("mimetype")
            if info.compress_type != zipfile.ZIP_STORED:
                errors.append("o arquivo 'mimetype' deve estar sem compressao")

        required = {
            "META-INF/container.xml",
            "OEBPS/content.opf",
            "OEBPS/nav.xhtml",
            "OEBPS/toc.ncx",
        }
        for name in sorted(required - set(names)):
            errors.append(f"arquivo obrigatorio ausente: {name}")

        xml_names = [
            name
            for name in names
            if name.endswith((".xml", ".opf", ".ncx", ".xhtml"))
        ]
        for name in xml_names:
            try:
                ElementTree.fromstring(epub.read(name))
            except ElementTree.ParseError as exc:
                errors.append(f"XML invalido em {name}: {exc}")

    return errors


def main() -> int:
    epub_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist/robo-trade-go-binance.epub")
    errors = validate(epub_path)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"EPUB XML OK: {epub_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

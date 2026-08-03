import argparse
import shutil
import bibtexparser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    cur_bib = bibtexparser.parse_file(args.filename)
    new_bib = bibtexparser.Library()
    table = {
        "inproceedings" : ["author", "title", "year", "doi", "pages", "booktitle"],
        "article"       : ["author", "title", "year", "doi", "pages", "journal", "number", "volume"],
        "book"          : ["author", "title", "year", "doi", "pages", "edition", "publisher"],
        "inbook"        : ["author", "title", "year", "doi", "pages", "edition", "booktitle", "publisher"],
        "techreport"    : ["author", "title", "year", "doi", "institution", "number"]
    }
    for key, entry in cur_bib.entries_dict.items():
        etype = entry.entry_type
        if etype in table:
            for field in entry.fields:
                if field.key.lower() not in table[etype]:
                    entry.pop(field.key)
        new_bib.add(entry)
    shutil.copy(args.filename, f'{args.filename}.old')
    bibtexparser.write_file(args.filename, new_bib)


if __name__ == "__main__":
    main()

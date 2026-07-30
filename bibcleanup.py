import argparse
import shutil
import bibtexparser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    cur_bib = bibtexparser.parse_file(args.filename)
    new_bib = bibtexparser.Library()
    table = {"inproceedings": ["author", "title", "booktitle", "year", "pages"],
             "article": ["author", "journal", "number", "pages", "title", "volume", "year"]
             }
    for key, entry in cur_bib.entries_dict.items():
        etype = entry.entry_type
        if etype in table:
            for field in entry.fields:
                if field.key not in table[etype]:
                    entry.pop(field.key)
        new_bib.add(entry)
    shutil.copy(args.filename, f'{args.filename}.old')
    bibtexparser.write_file(args.filename, new_bib)


if __name__ == "__main__":
    main()

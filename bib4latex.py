import sys
import subprocess
import bibtexparser


def citations(folder):
    cmd = "find " + folder +" -name '*.tex' -exec grep -hoRe '\\\\cite{.*}' '{}' \; | cut -d '{' -f2 | cut -d '}' -f1 | sort | uniq"
    out = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    keys = set()
    for line in out.stdout.split('\n'):
        for e in line.split(','):
            if ee := e.strip():
                keys.add(ee)
    return keys

def main():
    folder = sys.argv[1]
    bib = sys.argv[2]
    cites = citations(folder)
    library = bibtexparser.parse_file(bib)
    fields_rm = ["abstract", "file", "keywords", "url", "issue_date", "numpages", "issn", "isbn", "address", "publisher"]
    newlib = bibtexparser.Library()
    for c in cites:
        if c in library.entries_dict:
            entry = library.entries_dict[c]
            for f in fields_rm:
                entry.pop(f, None)
            newlib.add(entry)
        else:
            print("Bibkey not found:", c)
    newbib = f"{folder}/new.bib"
    if len(sys.argv) > 3:
        newbib = f"{folder}/{sys.argv[3]}"
    bibtexparser.write_file(newbib, newlib)
    print("Bib file written in ", newbib)

if __name__ == "__main__":
    main()

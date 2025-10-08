import sys
import subprocess
import bibtexparser


def citations(folder):
    cmd = "grep -hoRe '\\\cite{.*}' " + folder + " | cut -d '{' -f2 | cut -d '}' -f1 | sort | uniq"
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
    newlib = bibtexparser.Library()
    print(cites)
    for c in cites:
        if c in library.entries_dict:
            newlib.add(library.entries_dict[c])
        else:
            print("Bibkey not found:", c)
    newbib = folder+'/new.bib'
    bibtexparser.write_file(newbib, newlib)
    print("Bib file written in ", newbib)

if __name__ == "__main__":
    main()

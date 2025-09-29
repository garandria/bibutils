import os
import sys
import shutil
from string import punctuation
from unidecode import unidecode
import bibtexparser
from bibtexparser.middlewares import BlockMiddleware
from pylatexenc.latex2text import LatexNodes2Text


def firstauthor(entry):
    tmp = entry.fields_dict["author"].value.split(" and")[0].split(",")
    assert len(tmp) >= 1, "There should be at least one author"
    if len(tmp) == 1:
        fauthor = tmp[0].split()[-1]
    elif len(tmp) > 1:
        fauthor = tmp[0]
    fauthor = unidecode(LatexNodes2Text().latex_to_text(fauthor))
    fauthor = fauthor.strip()
    fauthor = fauthor.replace(" ", "_")
    return fauthor

def year(entry):
    return entry.fields_dict["year"].value

def venue(entry):
    venue = ""
    if "series" in entry.fields_dict:
        venue = entry.fields_dict["series"].value.split()[0].strip(punctuation)
        if '/' in venue:
            venue = venue.split('/')[-1]
        if "'" in venue:
            venue = venue.split("'")[0]

    if "journal" in entry.fields_dict:
        match c:= ' '.join(entry.fields_dict["journal"].value.strip().split()):
            case "IEEE Transactions on Software Engineering" | "IEEE Trans. Softw. Eng.":
                venue = "tse"
            case "ACM Trans. Softw. Eng. Methodol.":
                venue = "tosem"
            case "Empirical Software Engineering" | "Empirical Softw. Engg.":
                venue = "emse"
            case "ACM Trans. Archit. Code Optim.":
                venue = "taco"
            case "ACM Trans. Program. Lang. Syst.":
                venue = "toplas"
            case "Proc. ACM Program. Lang.":
                venue = "pacmpl"
            case "ACM Trans. Comput. Syst.":
                venue = "tocs"
            case "ACM Comput. Surv.":
                venue = "acmsurvey"
            case "Automated Software Engg.":
                venue = "asej"
            case "The Art, Science, and Engineering of Programming":
                venue = "programming"
            case "IEEE Software":
                # venue = "ieeesoftware"
                pass
            case "Journal of Systems and Software":
                venue = "jss"
            case "Commun. ACM":
                # venue = "acm-comm"
                pass
            case "J. ACM":
                venue = "jacm"
            case "Computing in Science & Engineering":
                venue = "cise"
            case "Proc. ACM Softw. Eng.":
                venue = "pacmse"
            case "Nature":
                venue = c.lower()
            case "Computer":
                venue = c.lower()
            case "IEEE Transactions on Computers":
                venue = "tc"
            case "SIGPLAN Not.":
                # venue = "sigplan-notices"
                pass
            case "SIGSOFT Softw. Eng. Notes":
                # venue = "acm-sigsoft"
                pass
            case "SIGPLAN Lisp Pointers":
                # venue = "lisp-pointers"
                pass
            case "Electron. Commun. Eur. Assoc. Softw. Sci. Technol.":
                venue = "eceasst"
            case "Inf. Softw. Technol.":
                venue = "ist"
            case "Software: Practice and Experience":
                # venue = "software-practice"
                pass
            case _:
                pass
    return venue


class RenameKeyMiddleware(BlockMiddleware):

    def __init__(self):
        self.keys = set()
        super().__init__()

    def transform_entry(self, entry, *args, **kwargs):
        newk = f"{firstauthor(entry).lower()}{year(entry)}{venue(entry).lower()}"
        while newk in self.keys: newk += '+'
        entry.key = newk
        self.keys.add(newk)
        return entry


class RenameFileMiddleware(BlockMiddleware):

    def transform_entry(self, entry, *args, **kwargs):
        oldp = entry["file"].strip()
        newp = oldp.split('/')
        ext = newp[-1].split('.')[-1]
        newp = newp[:-1] + [f"{entry.key}.{ext}"]
        newp = '/'.join(newp)
        entry["file"] = newp
        if not oldp == newp:
            os.rename(oldp, newp)
        return entry


def main():
    bib = sys.argv[1]
    library = bibtexparser.parse_file(
        bib, append_middleware=[RenameKeyMiddleware(), RenameFileMiddleware()])
    shutil.copy(bib, f'{bib}.old')
    bibtexparser.write_file(bib, library)


if __name__ == "__main__":
    main()

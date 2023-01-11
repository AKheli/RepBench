
from PyPDF2 import PdfFileMerger
import os


class PDFsaver():
    framenumber = 0

    def __init__(self, title):
        self.title = title
        self.pdfs = []

    def add(self,plt):
        global  framenumber
        framenumber = framenumber +1
        self.pdfs.append(f"/evaluation/tmp/" +str(framenumber)+ ".pdf")
        plt.savefig(self.pdfs[-1])
        plt.close()

        return framenumber


    def close(self):
        merger = PdfFileMerger()
        for pdf in self.pdfs:
            merger.append(pdf)
        merger.write(self.title)
        merger.close()
        self._delete()


    def _delete(self):
        try:
            for pdf in self.pdfs:
                os.remove(pdf)
        except PermissionError as e:
            print(e)
            self.delete()



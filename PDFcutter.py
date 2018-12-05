import PyPDF4 as Pdf
import time
import os


class PDFCutter:
    def __init__(self):
        self.pdf_reader: Pdf.PdfFileReader = None
        self.pdf_writer: Pdf.PdfFileWriter = None
        self.number_of_pages: int = 0
        self.main_pdf_file = None
        self.main_pdf_file_path: str = None
        self.new_pdf_file = None

    def set_pdf_path(self, pdf_file_path: str):
        """return false if that pass is not file path"""
        if not os.path.isfile(pdf_file_path):
            print('): this path is not a file path!\n')
            return 1
        self.main_pdf_file_path = pdf_file_path
        self.main_pdf_file = open(pdf_file_path, 'rb')
        self.pdf_reader = Pdf.PdfFileReader(self.main_pdf_file)
        if self.pdf_reader.isEncrypted:
            print('): it is an encrypted pdf file!\n')
            return 2
        self.number_of_pages = self.pdf_reader.numPages
        return 0

    def decrypt(self, password: str):
        """return true if file is decrypted correctly"""
        submit: int = self.pdf_reader.decrypt(password)
        print(((not submit)*'): not it is!\n'))
        return not submit

    def split(self, from_page: int, to_page: int):
        """copy pages from main pdf file then save it in new pdf file"""
        if to_page > self.number_of_pages:
            print('): this pdf file have only', self.number_of_pages, 'pages!\n')
            return False
        if from_page >= to_page:
            print('): ', from_page, ':', to_page, 'it can\'t be a range!\n')
            return False
        # open file to save file in it.
        path_tuple: tuple = os.path.split(self.main_pdf_file_path)
        new_path: str = os.path.join(path_tuple[:-1][0], str(time.time())+' '+path_tuple[-1])
        print('(: new file is:', new_path, '\n')
        self.new_pdf_file = open(new_path, 'wb')
        # create pdf writer, add page.
        self.pdf_writer = Pdf.PdfFileWriter()
        for i in range(from_page, to_page):
            self.pdf_writer.addPage(self.pdf_reader.getPage(i))
        self.pdf_writer.write(self.new_pdf_file)
        return True

    def close(self):
        """close files"""
        self.main_pdf_file.close()
        self.new_pdf_file.close()


if __name__ == '__main__':
    again: str = 'a'
    # make cutter.
    cutter: PDFCutter = PDFCutter()
    action: tuple = (lambda: cutter.set_pdf_path(input('(: Enter pdf file absolute path: ')),
                     lambda: cutter.decrypt(input('(: enter password: ')))
    while again == 'a':
        # takes absolute path.
        conform: int = cutter.set_pdf_path(input('(: Enter pdf file absolute path: '))
        while conform:
            conform = action[conform-1]()
        # takes range split file (from,to) page.
        print('(: Enter page number:-')
        f: int = int(input('   from:'))
        t: int = int(input('   to:'))
        while not cutter.split(f, t):
            print('(: Enter page number:-')
            f: int = int(input('   from:'))
            t: int = int(input('   to:'))
        # close
        cutter.close()
        again = input('\n(: Enter \'a\' to run again: ')
    print('(: see you later.')



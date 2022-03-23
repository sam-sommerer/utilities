#!/usr/bin/env python3

import PyPDF2
import argparse
import pyfiglet
import rich

class PDF_Combiner:
	def __init__(self, output_path, file1_path, file2_path):
		self.output_path = output_path
		self.file1_path = file1_path
		self.file2_path = file2_path
		self.file1_num_pages = None
		self.file2_num_pages = None

	def _valid_page(self, page):
		file, num = page[0], page[1:]

		if file != "a" and file != "b":
			return False

		if not num.isdigit():
			return False

		if file == "a" and int(num) >= self.file1_num_pages:
			return False

		if file == "b" and int(num) >= self.file2_num_pages:
			return False

		if int(num) < 1:
			return False

		return True

	def combine_pdfs(self):
		msg = "\nEnter the order in which you'd like your pages to be combined. Enter a space separated list of pages," \
			+ " with each page prepended with \'a\' or \'b\' according to whether or not the page is from the first or second" \
			+ " file respectively.\n\nFor example, a1 b3 a5 a10 b4 translates to page 1 from file 1, page 3 from file 2, page" \
			+ " 10 from file 1, and page 4 from file 2.\n"

		print(msg)

		page_str = ""

		while page_str == "":
			page_str = input("Enter page order here: ")

		page_list = page_str.split()

		pdf_writer = PyPDF2.PdfFileWriter()

		file1 = open(self.file1_path, "rb")
		file2 = open(self.file2_path, "rb")

		file1_reader = PyPDF2.PdfFileReader(file1)
		file2_reader = PyPDF2.PdfFileReader(file2)

		self.file1_num_pages = file1_reader.numPages
		self.file2_num_pages = file2_reader.numPages

		for page in page_list:
			if not self._valid_page(page):
				print(page + " is not valid. Skipping...")
				continue

			file_code, page_num = page[0], int(page[1:])

			curr_reader = file1_reader if file_code == "a" else file2_reader

			page_obj = curr_reader.getPage(page_num - 1)

			pdf_writer.addPage(page_obj)

		pdf_output = open(self.output_path, "wb")
		pdf_writer.write(pdf_output)
		pdf_output.close()
		file1.close()
		file2.close()

if __name__ == "__main__":

	f = pyfiglet.figlet_format("Combine PDFs", font="script")
	rich.print(f"[magenta]{f}[/magenta]")

	parser = argparse.ArgumentParser(description="Combine pages from two PDF files.")
	parser.add_argument("--out_file", "-o", type=str, default="/Users/yaya/Downloads/new.pdf")
	parser.add_argument("--file1", "-f1", required=True, type=str, help="first file to choose pages from")
	parser.add_argument("--file2", "-f2", required=True, type=str, help="second file to choose pages from")

	args = parser.parse_args()

	pdf_combiner = PDF_Combiner(args.out_file, args.file1, args.file2)

	pdf_combiner.combine_pdfs()




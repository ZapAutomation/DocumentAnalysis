#!/usr/bin/env python

import os
import sys
import argparse
import time
import zipfile
from subprocess import Popen, PIPE, STDOUT
from pdfminer.high_level import extract_text

from haystack import Finder
from haystack.indexing.cleaning import clean_wiki_text
from haystack.indexing.utils import convert_files_to_dicts, fetch_archive_from_http
from haystack.reader.farm import FARMReader
from haystack.reader.transformers import TransformersReader
from haystack.utils import print_answers
from haystack.database.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.elasticsearch import ElasticsearchRetriever


def parse_arguments():

	parser = argparse.ArgumentParser(prog='Contract Analysis Q&A', description='Run Q&A on the supplied contracts')

	parser.add_argument('path',
	                       metavar='PATH_TO_DIRECTORY',
	                       type=str,
	                       help='The path to the Contract Analysis Directory')

	parser.add_argument('questions_file',
	                      metavar='QUESTIONS_FILE',
	                      type=str,
	                      help='The path to the .txt file containing a list of questions to be asked')

	parser.add_argument('--gpu',
	                       metavar='GPU_AVAILABILITY',
	                       type=bool,
	                       default=False,
	                       help='Boolean value indicating whether or not a GPU is available for use')

	args = parser.parse_args()

	if not os.path.isdir(args.path):
	  print('ERR: The specified path does not exist or is not a directory.')
	  sys.exit()

	if not os.path.isfile(args.questions_file):
	  print('ERR: The specified questions\' file does not exist.')
	  sys.exit()

	return args.path, args.questions_file, args.gpu


def get_fileLoc_QList(args_path, args_questions_file):

	with open(args_questions_file) as file:
		questions_list = [string.rstrip('\n') for string in file]

	pdf_docs_location = os.path.join(args_path, 'documents', 'pdfs')
	txt_files_location = os.path.join(args_path, 'documents', 'txts')
	results_location = os.path.join(args_path, 'results')

	return pdf_docs_location, txt_files_location, results_location, questions_list


def convert_to_txt(pdf_docs_location, txt_files_location):

    for dirpath, dirnames, files in os.walk(pdf_docs_location):
          for file_name in files:
            raw_text = extract_text(os.path.join(dirpath, file_name), caching=False)
            os.mkdir(os.path.join(txt_files_location, file_name[:-4]))
            text_file = open(os.path.join(txt_files_location, file_name[:-4], file_name[:-4] + ".txt"), "w+")
            text_file.write(raw_text)


def start_elasticSearch():

	es_server = Popen(['elasticsearch-7.6.2/bin/elasticsearch'],
	                   stdout=PIPE, stderr=STDOUT,
	                   preexec_fn=lambda: os.setuid(1), shell=True
	                  )

	time.sleep(30)


def get_results(txt_files_location, use_gpu, questions_list, results_location):

	document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")
	for dirpath, dirnames, files in os.walk(txt_files_location):
		for dirname in dirnames:
			for dirpath, dirname, files in os.walk(os.path.join(txt_files_location, dirname)):
				for file_name in files:
					document_store.client.indices.delete(index='document', ignore=[400, 404])

					doc_dir = dirpath

					dicts = convert_files_to_dicts(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)

					document_store.write_documents(dicts)

					retriever = ElasticsearchRetriever(document_store=document_store)

					reader = FARMReader(model_name_or_path="elgeish/cs224n-squad2.0-albert-xxlarge-v1", use_gpu = use_gpu)

					finder = Finder(reader, retriever)

					sys.stdout = open(os.path.join(results_location, file_name[:-4] + "_results.txt"), "a+")

					for i, question in enumerate(questions_list):
					
						prediction = finder.get_answers(question=question, top_k_retriever=10, top_k_reader=1)

						print("\n\n\nQuestion " + str(i + 1) + ":\n")
						print(question + "\n")
						print_answers(prediction, details = "minimal")

					sys.stdout.close()

	document_store.client.transport.close()

def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            zf.write(absname, arcname)
    zf.close()

def main():

	args_path, args_questions_file, use_gpu = parse_arguments()
	pdf_docs_location, txt_files_location, results_location, questions_list = get_fileLoc_QList(args_path, args_questions_file)
	convert_to_txt(pdf_docs_location, txt_files_location)
	start_elasticSearch()
	get_results(txt_files_location, use_gpu, questions_list, results_location)

	zip(os.path.join(args_path, results), os.path.join(args_path, results))


if __name__ == '__main__':
	main()


from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
import nltk
nltk.download('punkt')
from modules.helpers.file import *
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from modules.language.detectlang import *

async def summarize_extractive(sentences_count, language, text, file, url):
  LANGUAGE = language
  SENTENCES_COUNT = sentences_count
  parser = None
  if url:
    # content is a url
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
  elif file:
    # content is file
    parser = PlaintextParser.from_file(file, Tokenizer(LANGUAGE))
  else:
    # content is text
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
  summary = ""
  stemmer = Stemmer(LANGUAGE)

  summarizer = Summarizer(stemmer)
  summarizer.stop_words = get_stop_words(LANGUAGE)

  for sentence in summarizer(parser.document, SENTENCES_COUNT):
      summary += str(sentence) + " "

  return summary

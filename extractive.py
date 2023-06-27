import spacy
import networkx as nx
import numpy as np
from sanitize import *
from lingua import Language

def Preprocess_text(text, language):
  nlp = None
  if language == Language.ENGLISH: 
    nlp = spacy.load("en_core_web_md") # english model
  else:
     nlp = spacy.load("xx_sent_ud_sm") # multi-language model
  # Preprocess the text
  sanitized_text = sanitize_text(text)
  doc = nlp(sanitized_text)

  # Split the text into individual sentences
  sentences = [sent.text.strip() for sent in doc.sents]

  # Create a list of stopwords
  stopwords = list(nlp.Defaults.stop_words)

  # Remove stopwords and punctuation, and lemmatize the remaining words
  lemmatized_sentences = []
  for sentence in sentences:
      words = []
      for word in nlp(sentence):
          if word.text.lower() not in stopwords and not word.is_punct:
              words.append(word.lemma_)
      lemmatized_sentences.append(" ".join(words))

  return lemmatized_sentences,sentences,nlp   



def Calculate_similarity_matrix(lemmetized_list, nlp):
  # Calculate the similarity matrix
  similarity_matrix = []
  for i in range(len(lemmetized_list)):
      row = []
      for j in range(len(lemmetized_list)):
          row.append(nlp(lemmetized_list[i]).similarity(nlp(lemmetized_list[j])))
      similarity_matrix.append(row)

  # Convert the similarity matrix to a graph
  graph = nx.from_numpy_array(np.array(similarity_matrix))

  # Calculate the PageRank scores
  scores = nx.pagerank(graph)
  return scores

def Generate_summarized_text(scores, num_sentences, sentences):
    
  # Sort the sentences by their scores and extract the top N sentences
  top_sentence_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:num_sentences]
  summary = [sentences[i] for i in top_sentence_indices]
  return summary



def summarize_extractive(text, num_sentences, language):
  preprocessed_text, sentences_list, nlp = Preprocess_text(text, language)

  similarit_matrix_calculated_score = Calculate_similarity_matrix(preprocessed_text, nlp)

  summary = Generate_summarized_text(similarit_matrix_calculated_score, num_sentences, sentences_list)
  return summary
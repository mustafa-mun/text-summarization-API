import spacy
import networkx as nx
import numpy as np

nlp = spacy.load("en_core_web_sm")


def Preprocess_text(text):
  # Preprocess the text
  doc = nlp(text)

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

  return lemmatized_sentences,sentences   



def Calculate_similarity_matrix(lemmetized_list):
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


import spacy
import collections

# Load a document and parse it.
def analyze(nlp, filename):
  # Load the Moby Dick book from the Gutenberg project (downloaded by the Makefile)
  # the `raw_document` will contain the whole book as one big string
  mobydick_file = open(filename)
  raw_document  = unicode(mobydick_file.read().decode('utf8'))
  if debug:
    print("Number of charaters in the Moby Dick document: " + str(len(raw_document)))
    
  document = nlp(raw_document)
  return document

# Find a specific verb
def word_is(word, ptag):
  for child in word.children:
    if child.pos_ == ptag:
      return True
  return False

def sentence_has(sentence, search, ptag):
  for word in sentence:
    if search in word.string and word_is(word, ptag):
      return True
  return False

def find_sentence_with(sentences, search, ptag):
  return [sentence for sentence in sentences if sentence_has(sentence, search, ptag)]

def find_sentence_with_verb(sentences, search):
  return find_sentence_with(sentences, search, "VERB")

# find a phrase with 
def find_sentence_with_word(sentence, word):
  return word in sentence.string

def find_sentence_with_all_words(sentence, words):
  for word in words:
    if find_sentence_with_word(sentence, word) == False:
      return False
  return True

def find_sentences_with_all_words(sentences, words):
  return [sentence for sentence in sentences if find_sentence_with_all_words(sentence, words)]

debug = False
language = 'en'
filename = 'MobyDick.txt'
verb = 'run'
vocabulary = ['whale', 'after']


# Load the English language model that was installed by the Makefile
nlp = spacy.load(language)
document = analyze(nlp, filename)

sentences_with_verb_run = find_sentence_with_verb(document.sents, verb)
print "Found " + str(len(sentences_with_verb_run)) + " sentences with the verb 'run'"
if debug:
  print(sentences_with_verb_run)


sentences_with_vocabulary = find_sentences_with_all_words(sentences_with_verb_run, vocabulary)

print "Found " + str(len(sentences_with_vocabulary)) + " sentences with the verb '" + verb + "'' and our vocabulary: " + str(vocabulary)

print("Number of words (tokens) in the Moby Dick document: " + str(len(document)))

words = [token.text.lower() for token in document]
vocabulary = sorted(set(words))
lemmas = sorted(set([token.lemma_ for token in document]))
print("Number of unique words in the Moby Dick document: " + str(len(vocabulary)))
print("Number of lemmas in the Moby Dick document: " + str(len(lemmas)))

word_frequency = collections.Counter(word for word in words if word.isalpha())
print("The top 10 most frequent words in the Moby Dick document: ")

for frequency in word_frequency.most_common(10):
  print("\t" + frequency[0] + "\t" + str(frequency[1]))


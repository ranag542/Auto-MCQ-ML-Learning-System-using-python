import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import random

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


class MCQGenerator:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.important_pos_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS']

    def _extract_keywords(self, sentence):
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)
        keywords = [
            word for word, tag in tagged_words
            if tag in self.important_pos_tags and word.lower() not in self.stop_words
        ]
        return list(set(keywords))  # unique words only

    def generate_mcqs(self, text, num_questions=5):
        sentences = sent_tokenize(text)
        mcqs = []

        for sentence in sentences[:num_questions]:
            keywords = self._extract_keywords(sentence)
            if not keywords:
                continue

            correct_answer = random.choice(keywords)
            question = sentence.replace(correct_answer, "______", 1)

            distractors = [kw for kw in keywords if kw != correct_answer][:3]
            while len(distractors) < 3:
                filler = random.choice(keywords)
                if filler != correct_answer and filler not in distractors:
                    distractors.append(filler)

            options = [correct_answer] + distractors
            random.shuffle(options)

            mcqs.append({
                'question': question,
                'options': options,
                'correct_answer': correct_answer,
                'explanation': f"This tests understanding of the word '{correct_answer}' in context."
            })

        return mcqs

import re
from collections import Counter
from typing import Dict, List, Tuple

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords', quiet=True)


class BookData:
    """Encapsulates text preprocessing and lexicon-based frequency analysis."""

    def __init__(self, base_file: str):
        self.base_file = base_file
        self.five_points = pd.read_csv(base_file)

    def process_data(self, column_name: str) -> List[List[str]]:
        """Tokenize rows in the selected column into lowercase alphabetic tokens."""
        tokens_per_row: List[List[str]] = []

        for message in self.five_points[column_name].fillna(""):
            normalized = re.sub('[^a-zA-Z]', ' ', str(message)).lower()
            tokens_per_row.append(normalized.split())

        return tokens_per_row

    @staticmethod
    def _load_word_list(file_name: str) -> List[str]:
        words: List[str] = []
        with open(file_name, encoding='utf-8') as file_obj:
            for line in file_obj:
                cleaned = line.replace(',', '').replace("\n", '').replace("'", '').strip().lower()
                if cleaned:
                    words.append(cleaned)
        return words

    def count_bad_words(self, file_name: str, column_name: str) -> Tuple[Dict[str, int], List[int]]:
        tokens = [word for row in self.process_data(column_name) for word in row]
        slang_words = set(self._load_word_list(file_name))
        slang_count = Counter(word for word in tokens if word in slang_words)

        return dict(slang_count), list(slang_count.values())

    def get_emotions(self, file_name: str, column_name: str) -> Tuple[Dict[str, int], List[int]]:
        tokens = [word for row in self.process_data(column_name) for word in row]

        emotions_data: Dict[str, str] = {}
        with open(file_name, encoding='utf-8') as emotions_file:
            for line in emotions_file:
                cleaned = line.replace(',', '').replace("\n", '').replace("'", '').strip()
                if not cleaned or ':' not in cleaned:
                    continue
                word, emotion = cleaned.split(':', 1)
                emotions_data[word.strip().lower()] = emotion.strip().lower()

        token_counter = Counter(tokens)
        emotion_counter: Counter = Counter()

        for word, emotion in emotions_data.items():
            if word in token_counter:
                emotion_counter[emotion] += token_counter[word]

        return dict(emotion_counter), list(emotion_counter.values())

    def motivational_phrase(self, file_name: str, column_name: str) -> Tuple[Dict[str, int], List[int]]:
        tokens = [word for row in self.process_data(column_name) for word in row]
        motivational_words = set(self._load_word_list(file_name))
        motivational_counter = Counter(word for word in tokens if word in motivational_words)

        return dict(motivational_counter), list(motivational_counter.values())


class Ideoms_Count:
    """Counts idiom categories by matching normalized text against an idiom corpus."""

    def __init__(self, file1: str, file2: str):
        self.stemmer = PorterStemmer()
        self.main_file = pd.read_csv(file1)
        self.ideoms_file = pd.read_csv(file2)
        self._stop_words = set(stopwords.words('english'))

    def reading_file(self, feature1: str) -> List[str]:
        corpus_data: List[str] = []

        for message in self.main_file[feature1].fillna("").astype(str).str.lower():
            normalized = re.sub('[^a-zA-Z]', ' ', message)
            review = normalized.split()
            stemmed = [self.stemmer.stem(word) for word in review if word not in self._stop_words]
            corpus_data.append(' '.join(stemmed))

        return corpus_data

    def get_idioms_count(self, feature1: str, feature2: str, feature3: str) -> Dict[str, int]:
        corpus_lines = self.reading_file(feature1)

        idiom_frame = self.ideoms_file[[feature2, feature3]].dropna().copy()
        idiom_frame[feature2] = idiom_frame[feature2].astype(str).str.strip().str.lower()
        idiom_lookup = dict(zip(idiom_frame[feature2], idiom_frame[feature3].astype(str).str.strip().str.lower()))

        category_counter: Counter = Counter()
        for line in corpus_lines:
            if line in idiom_lookup:
                category_counter[idiom_lookup[line]] += 1

        return dict(category_counter)


if __name__ == "__main__":
    idc = Ideoms_Count('file_content.csv', 'file_ideoms.csv')
    print(idc.get_idioms_count('file_contents', 'quote', 'category'))

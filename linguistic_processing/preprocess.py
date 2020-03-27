import sys
import nltk
import re
import regex
import unicodedata

from typing import Pattern

PAT_ALPHABETIC = re.compile(r"(((?![\d])\w)+)")
PAT_HINDI = regex.compile(r"(?u)\b\w\w+\b")
PAT_ARABIC = re.compile(r"\W+")


class Preprocessor:
    def __init__(self, language: str, deaccent=True, lower=True, min_len=2, max_len=30) -> None:
        self.language = language
        self.deaccent = deaccent
        self.lower = lower
        self.min_len = min_len
        self.max_len = max_len
        self.stopwords = self._load_stopwords()
        self.tokenizer = Tokenizer(self.language)

    def preprocess(self, text: str) -> list:
        if self.lower:
            text = text.lower()

        if self.deaccent:
            text = Preprocessor.strip_accents(text)

        text = Preprocessor.clean_text(text)
        tokens = self._tokenize(text)
        tokens = [t for t in tokens if self._valid_token(t) and self._not_stop_word(t)]
        return tokens

    def _tokenize(self, text: str) -> list:
        tokenized = self.tokenizer.tokenize(text)
        return tokenized

    def _load_stopwords(self) -> list:
        stopwords = []
        try:
            nltk_stopwords = nltk.corpus.stopwords.words(self.language)
            stopwords.extend(nltk_stopwords)

            if self.deaccent == True:
                stopwords_deaccented = [Preprocessor.strip_accents(t) for t in nltk_stopwords]
                stopwords.extend(stopwords_deaccented)

        except Exception as e:
            print(f"{e} Couldn't find any NLTK stopwords for {self.language}. No stopwords will be removed from text.")

        finally:
            return list(set(stopwords))

    def _not_stop_word(self, token: str) -> bool:
        return token not in self.stopwords

    def _valid_token(self, token: str) -> bool:
        return all([len(token) > self.min_len, len(token) < self.max_len, not token.startswith("http")])

    @staticmethod
    def clean_text(text):
        # Ignore any control or punctuation characters.
        cleaned = "".join(c for c in text if unicodedata.category(c)[0] not in ["C", "P"])
        return cleaned

    @staticmethod
    def strip_accents(text):
        stripped = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
        return stripped


class Tokenizer:
    def __init__(self, language):
        self.language = language

    @property
    def token_pattern(self) -> Pattern:
        patterns = {"english": PAT_ALPHABETIC, "hindi": PAT_HINDI, "arabic": PAT_HINDI}
        token_pattern = patterns.get(self.language, PAT_ALPHABETIC)
        print(f"Using the following regex to tokenize: {token_pattern}")

        return token_pattern

    def tokenize(self, text):
        """Return a function that split a string in sequence of tokens"""
        for match in self.token_pattern.finditer(text):
            yield match.group()

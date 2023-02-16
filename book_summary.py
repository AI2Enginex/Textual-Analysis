import re
import nltk
nltk.download('stopwords')
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class Book_data:

    def __init__(self,base_file):

        self.five_points = pd.read_csv(base_file)

        self.slang_words = []
        self.word_count = []
        self.total_emotions = []
        self.motivational_words = []

        self.slang_count = {}

        self.emotions_data = {}

        self.frequency_of_emotions = {}

        self.motivational_words_count = {}

    def process_data(self,column_name):

        for message in self.five_points[column_name]:
            word = re.sub('[^a-zA-Z]', ' ', message)
            review = word.split()
            self.word_count.append(review)
        return self.word_count

    def count_bad_words(self,file_name,column_name):
        
        curse_freq_count = []
        data = self.process_data(column_name)
        data = [x for i in data for x in i]

        with open(file_name) as c_words:

            for line in c_words:

                create_line = line.replace(",", "").replace(
                    "\n", "").replace("'", "").strip()

                self.slang_words.append(create_line.lower())

        for i in data:
            if i in self.slang_words:
                if i not in self.slang_count:
                    self.slang_count[i] = 1
                else:
                    self.slang_count[i] += 1

        for items , values in self.slang_count.items():
            curse_freq_count.append(values)

        return self.slang_count, curse_freq_count

    def get_emotions(self,file_name , column_name):
        
        emo_freq_count = []
        data = self.process_data(column_name)
        data = [i for x in data for i in x]

        with open(file_name) as emotions_:
            for line in emotions_:
                create_line = line.replace(",", "").replace(
                    "\n", "").replace("'", "").strip()
                word, emotions = create_line.split(":")
                self.emotions_data[word] = emotions

        for key, value in self.emotions_data.items():
            if key in data:
                self.total_emotions.append(value)

        for i in self.total_emotions:
            if i not in self.frequency_of_emotions:
                self.frequency_of_emotions[i] = 1
            else:
                self.frequency_of_emotions[i] += 1

        for items , values in self.frequency_of_emotions.items():

            emo_freq_count.append(values)


        return self.frequency_of_emotions , emo_freq_count

    def motivational_phrase(self,file_name,column_name):

        mov_feq_count = []
        data = self.process_data(column_name)
        data = [i for x in data for i in x]

        with open(file_name) as phrase_:

            for line in phrase_:

                create_line = line.replace(",", "").replace(
                    "\n", "").replace("'", "").strip()

                self.motivational_words.append(create_line.lower())

        for word in data:

            if word in self.motivational_words:
                if word not in self.motivational_words_count:
                    self.motivational_words_count[word] = 1
                else:
                    self.motivational_words_count[word] += 1

        for items , values in self.motivational_words_count.items():

            mov_feq_count.append(values)


        return self.motivational_words_count , mov_feq_count


class Ideoms_Count:

    def __init__(self,file1,file2):
        
        self.corpus_data = []
        self.category_count = []
        self.freq_ideoms = {}
        self.idioms_count = 0
        self.stemmer = PorterStemmer()
        self.main_file = pd.read_csv(file1)
        self.ideoms_file = pd.read_csv(file2)


    def reading_file(self,feature1):

        self.main_file[feature1] = self.main_file[feature1].str.lower()

        for message in self.main_file[feature1]:
            word = re.sub('[^a-zA-Z]',' ' , message)
            review = word.split()
            stop_words = [self.stemmer.stem(word) for word in review if word not in stopwords.words('english')]
            words = ' '.join(stop_words)
            self.corpus_data.append(words)

        return self.corpus_data
    
    def get_idioms_count(self,feature1,feature2,feature3):

        corpora = self.reading_file(feature1)
        for word in corpora:
            if word in self.ideoms_file[feature2]:
                self.category_count.append(self.ideoms_file[feature3])

        for word in self.category_count:

            if word not in self.freq_ideoms:

                self.freq_ideoms[word] = 1
            else:
                self.freq_ideoms[word] += 1

        return self.freq_ideoms






if __name__ == "__main__":

    #b = Book_data()

    #slang, total_words , data = b.count_bad_words()
    #total_emotions , y = b.get_emotions()
    #phrases , z = b.motivational_phrase()

    #print(f"total_words in the book are {total_words}")

    #print()

    #print(data)

    idc = Ideoms_Count()
    idc.get_idioms_count()


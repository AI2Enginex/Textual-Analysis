
import pandas as pd
import seaborn as sns
import book_summary as bs
import matplotlib.pyplot as plt




class Test_file:


    def __init__(self,base_file,file1,file2):

        self.book_obj = bs.Book_data(base_file)
        self.ideoms_count = bs.Ideoms_Count(file1,file2)

    def insp_phrase(self,file_3,column):
        
        self.mov, self.mov_val = self.book_obj.motivational_phrase(file_3,column)
        phrase_df = pd.DataFrame(list(self.mov.items()), columns=[
                                 'word', 'frequency'])
        return phrase_df

    def emotions(self,file_2,column):
        
        self.emo, self.emo_val = self.book_obj.get_emotions(file_2,column)
        emotions_df = pd.DataFrame(
            list(self.emo.items()), columns=['word', 'frequency'])
        return emotions_df

    def bad_words(self,file_1,column):
        
        self.cbw, self.cbw_val = self.book_obj.count_bad_words(file_1,column)

        cbw_df = pd.DataFrame(list(self.cbw.items()),
                              columns=['word', 'frequency'])
        return cbw_df
    
    def count_ideoms(self,column1,column2,column3):

        self.ideoms_corpus = self.ideoms_count.get_idioms_count(column1,column2,column3)
        ideoms_df = pd.DataFrame(list(self.ideoms_corpus.items()),
                                 columns=['word','frequency'])
        
        return ideoms_df




class Visualization_inputs:

    def __init__(self,base_file,file_1,file_2):

        self.test_f = Test_file(base_file,file_1,file_2)
        self.val = input("Enter top or Bottom : ")

    def visualize_bad_words(self,value,file_1,column):

        self.bad_ = self.test_f.bad_words(file_1,column)

        try:
            if value <= len(self.bad_.index):
                if self.val == "top":
                    sns.barplot(
                        x=self.bad_["word"].head(value),
                        y=self.bad_["frequency"].head(value))
                    plt.show()
                elif self.val == "bottom":
                    sns.barplot(
                        x=self.bad_["word"].tail(value),
                        y=self.bad_["frequency"].tail(value))
                    plt.show()
                else:
                    sns.barplot(
                        x=self.bad_["word"].sample(value),
                        y=self.bad_["frequency"].sample(value))
                    plt.show()
        except Exception:

            print("index out of range")

    def visualize_emotions(self, value,file_2,column):

        self.emo_ = self.test_f.emotions(file_2,column)
        try:
            if value <= len(self.emo_.index):
                if self.val == "top":
                    sns.barplot(
                        x=self.emo_["word"].head(value),
                        y=self.emo_["frequency"].head(value))
                    plt.show()
                elif self.val == "bottom":
                    sns.barplot(
                        x=self.emo_["word"].tail(value),
                        y=self.emo_["frequency"].tail(value))
                    plt.show()
                else:
                    sns.barplot(
                        x=self.emo_["word"].sample(value),
                        y=self.emo_["frequency"].sample(value))
                    plt.show()
        except Exception:

            print("index out of range")

    def visualize_mov_phrase(self,value,file_3,column):

        self.insp_ = self.test_f.insp_phrase(file_3,column)

        try:
            if value <= len(self.insp_.index):
                if self.val == "top":
                    sns.barplot(
                        x=self.insp_["word"].head(value),
                        y=self.insp_["frequency"].head(value))
                    plt.show()
                elif self.val == "bottom":
                    sns.barplot(
                        x=self.insp_["word"].tail(value),
                        y=self.insp_["frequency"].tail(value))
                    plt.show()
                else:
                    sns.barplot(
                        x=self.insp_["word"].sample(value),
                        y=self.insp_["frequency"].sample(value))
                    plt.show()
        except Exception:

            print("index out of range")

    def visualize_ideoms(self,value,column1,column2,column3):

        self.ideoms_ = self.test_f.count_ideoms(column1,column2,column3)

        try:
            if value <= len(self.ideoms_.index) and len(self.ideoms_.index) != 0:
                if self.val == "top":
                    sns.barplot(
                        x=self.ideoms_["word"].head(value),
                        y=self.ideoms_["frequency"].head(value))
                    plt.show()
                elif self.val == "bottom":
                    sns.barplot(
                        x=self.ideoms_["word"].tail(value),
                        y=self.ideoms_["frequency"].tail(value))
                    plt.show()
                else:
                    sns.barplot(
                        x=self.ideoms_["word"].sample(value),
                        y=self.ideoms_["frequency"].sample(value))
                    plt.show()
        except Exception:

            print("Ideoms not found.......")


if __name__ == "__main__":

    user_input = input("Enter the Operation : ")
    limit_range = int(input("Enter the limit value : "))


    visual = Visualization_inputs(base_file='file_content.csv',file_1='file_content.csv',file_2='file_ideoms.csv')

    
    if user_input == "bad words":

        visual.visualize_bad_words(limit_range,file_1='bad_word.txt',column='file_contents')

    elif user_input == "motivational words":

        visual.visualize_mov_phrase(limit_range,file_3='motivational_words.txt',column='file_contents')

    elif user_input == "emotions":
        visual.visualize_emotions(limit_range , file_2='emotions.txt' , column='file_contents')

    elif user_input == 'idioms_':

        visual.visualize_ideoms(limit_range , column1='file_contents',column2='quote',column3='category')

    else:
        print("select correct operation")

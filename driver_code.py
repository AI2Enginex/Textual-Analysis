import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import book_summary as bs


class Test_file:
    """Coordinates calls to analysis classes and returns DataFrame outputs."""

    def __init__(self, base_file, file1, file2):
        self.book_obj = bs.Book_data(base_file)
        self.ideoms_count = bs.Ideoms_Count(file1, file2)

    @staticmethod
    def _to_dataframe(data_dict):
        return pd.DataFrame(list(data_dict.items()), columns=['word', 'frequency'])

    def insp_phrase(self, file_3, column):
        mov, _ = self.book_obj.motivational_phrase(file_3, column)
        return self._to_dataframe(mov)

    def emotions(self, file_2, column):
        emo, _ = self.book_obj.get_emotions(file_2, column)
        return self._to_dataframe(emo)

    def bad_words(self, file_1, column):
        cbw, _ = self.book_obj.count_bad_words(file_1, column)
        return self._to_dataframe(cbw)

    def count_ideoms(self, column1, column2, column3):
        ideoms_corpus = self.ideoms_count.get_idioms_count(column1, column2, column3)
        return self._to_dataframe(ideoms_corpus)


class Visualization_inputs:
    """Interactive visualization layer for top/bottom/random category frequencies."""

    def __init__(self, base_file, file_1, file_2):
        self.test_f = Test_file(base_file, file_1, file_2)
        self.val = input("Enter top or Bottom : ").strip().lower()

    def _slice_dataframe(self, frame, value):
        if self.val == "top":
            return frame.head(value)
        if self.val == "bottom":
            return frame.tail(value)
        return frame.sample(value)

    @staticmethod
    def _plot_frame(frame):
        sns.barplot(x=frame['word'], y=frame['frequency'])
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def _visualize(self, frame, value, empty_message):
        if frame.empty:
            print(empty_message)
            return

        if value <= 0:
            print("limit must be greater than zero")
            return

        if value > len(frame.index):
            print("index out of range")
            return

        selected = self._slice_dataframe(frame, value)
        self._plot_frame(selected)

    def visualize_bad_words(self, value, file_1, column):
        bad_df = self.test_f.bad_words(file_1, column)
        self._visualize(bad_df, value, "Bad words not found.......")

    def visualize_emotions(self, value, file_2, column):
        emo_df = self.test_f.emotions(file_2, column)
        self._visualize(emo_df, value, "Emotions not found.......")

    def visualize_mov_phrase(self, value, file_3, column):
        insp_df = self.test_f.insp_phrase(file_3, column)
        self._visualize(insp_df, value, "Motivational words not found.......")

    def visualize_ideoms(self, value, column1, column2, column3):
        ideoms_df = self.test_f.count_ideoms(column1, column2, column3)
        self._visualize(ideoms_df, value, "Ideoms not found.......")


if __name__ == "__main__":
    user_input = input("Enter the Operation : ").strip().lower()
    limit_range = int(input("Enter the limit value : "))

    visual = Visualization_inputs(
        base_file='file_content.csv',
        file_1='file_content.csv',
        file_2='file_ideoms.csv'
    )

    if user_input == "bad words":
        visual.visualize_bad_words(limit_range, file_1='bad_word.txt', column='file_contents')
    elif user_input == "motivational words":
        visual.visualize_mov_phrase(limit_range, file_3='motivational_words.txt', column='file_contents')
    elif user_input == "emotions":
        visual.visualize_emotions(limit_range, file_2='emotions.txt', column='file_contents')
    elif user_input == 'idioms_':
        visual.visualize_ideoms(limit_range, column1='file_contents', column2='quote', column3='category')
    else:
        print("select correct operation")

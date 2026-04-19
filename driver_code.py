import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import book_summary as bs


class Test_file:
    """Coordinates calls to analysis classes and returns DataFrame outputs."""

    def __init__(self, base_file, file1, file2):
        self.book_obj = bs.BookData(base_file)
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
    """Visualization layer used by the Tkinter app."""

    def __init__(self, base_file, file_1, file_2):
        self.test_f = Test_file(base_file, file_1, file_2)

    @staticmethod
    def _slice_dataframe(frame, value, view_mode):
        if view_mode == "top":
            return frame.head(value)
        if view_mode == "bottom":
            return frame.tail(value)
        return frame.sample(value)

    @staticmethod
    def _plot_frame(frame, title):
        plt.figure(figsize=(10, 5))
        sns.barplot(x=frame['word'], y=frame['frequency'])
        plt.title(title)
        plt.xlabel('Word / Category')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def _visualize(self, frame, value, view_mode, empty_message, plot_title):
        if frame.empty:
            raise ValueError(empty_message)
        if value <= 0:
            raise ValueError("Limit must be greater than zero.")
        if value > len(frame.index):
            raise ValueError("Limit exceeds available rows.")

        selected = self._slice_dataframe(frame, value, view_mode)
        self._plot_frame(selected, plot_title)

    def visualize_bad_words(self, value, file_1, column, view_mode):
        bad_df = self.test_f.bad_words(file_1, column)
        self._visualize(bad_df, value, view_mode, "Bad words not found.", "Bad Words Frequency")

    def visualize_emotions(self, value, file_2, column, view_mode):
        emo_df = self.test_f.emotions(file_2, column)
        self._visualize(emo_df, value, view_mode, "Emotions not found.", "Emotion Frequency")

    def visualize_mov_phrase(self, value, file_3, column, view_mode):
        insp_df = self.test_f.insp_phrase(file_3, column)
        self._visualize(
            insp_df,
            value,
            view_mode,
            "Motivational words not found.",
            "Motivational Words Frequency"
        )

    def visualize_ideoms(self, value, column1, column2, column3, view_mode):
        ideoms_df = self.test_f.count_ideoms(column1, column2, column3)
        self._visualize(ideoms_df, value, view_mode, "Ideoms not found.", "Idioms Category Frequency")


class TextAnalysisApp:
    """Tkinter-based front-end while preserving the existing analysis architecture."""

    def __init__(self, root):
        self.root = root
        self.root.title("Textual Analysis")
        self.root.geometry("480x260")

        self.visual = Visualization_inputs(
            base_file='file_content.csv',
            file_1='file_content.csv',
            file_2='file_ideoms.csv'
        )

        self.operation_var = tk.StringVar(value="bad words")
        self.view_mode_var = tk.StringVar(value="top")
        self.limit_var = tk.StringVar(value="10")

        self._build_ui()

    def _build_ui(self):
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Operation").grid(row=0, column=0, sticky="w", pady=6)
        operation_box = ttk.Combobox(
            container,
            textvariable=self.operation_var,
            values=["bad words", "motivational words", "emotions", "idioms_"],
            state="readonly",
            width=30
        )
        operation_box.grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(container, text="View Mode").grid(row=1, column=0, sticky="w", pady=6)
        view_mode_box = ttk.Combobox(
            container,
            textvariable=self.view_mode_var,
            values=["top", "bottom", "random"],
            state="readonly",
            width=30
        )
        view_mode_box.grid(row=1, column=1, sticky="ew", pady=6)

        ttk.Label(container, text="Limit").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Entry(container, textvariable=self.limit_var, width=32).grid(row=2, column=1, sticky="ew", pady=6)

        ttk.Button(container, text="Generate Chart", command=self._run_analysis).grid(
            row=3,
            column=0,
            columnspan=2,
            pady=18
        )

        container.columnconfigure(1, weight=1)

    def _run_analysis(self):
        operation = self.operation_var.get().strip().lower()
        view_mode = self.view_mode_var.get().strip().lower()

        try:
            limit = int(self.limit_var.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a numeric limit.")
            return

        try:
            if operation == "bad words":
                self.visual.visualize_bad_words(limit, file_1='bad_word.txt', column='file_contents', view_mode=view_mode)
            elif operation == "motivational words":
                self.visual.visualize_mov_phrase(
                    limit,
                    file_3='motivational_words.txt',
                    column='file_contents',
                    view_mode=view_mode
                )
            elif operation == "emotions":
                self.visual.visualize_emotions(limit, file_2='emotions.txt', column='file_contents', view_mode=view_mode)
            elif operation == 'idioms_':
                self.visual.visualize_ideoms(
                    limit,
                    column1='file_contents',
                    column2='quote',
                    column3='category',
                    view_mode=view_mode
                )
            else:
                messagebox.showerror("Invalid Operation", "Please select a valid operation.")
        except Exception as error:
            messagebox.showerror("Analysis Error", str(error))


if __name__ == "__main__":
    root = tk.Tk()
    app = TextAnalysisApp(root)
    root.mainloop()

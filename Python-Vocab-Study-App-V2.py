import pandas as pd
import os
import tkinter as tk
from tkinter import font

WindowHeight = 562
WindowWidth = 1000

# Loading Vocabulary Data
VocabFile = pd.read_excel(r"DataForStudy.xlsx")

# Variables
isPlaying = False
chosenCategory = ""
categoryQuestionArray = []
isAllVocab = False


class Application(tk.Frame):
    def __init__(self, *args, **kwargs):
        rootWindow.geometry(f'{WindowWidth}x{WindowHeight}')
        rootWindow.resizable(False, False)
        self.AppCanvas = tk.Canvas(rootWindow, height=WindowHeight,
                                   width=WindowWidth)  # Canvas for the display of all app elements
        self.AppCanvas.pack(fill="both", expand=True)

        # Loading Images
        self.LoadBackgroundImage = tk.PhotoImage(file='./Python Project - Art Assets/ResizedBackground.png')
        self.LoadSubmitButtonImage = tk.PhotoImage(file='./Python Project - Art Assets/ResizedSubmitButton.png')
        self.LoadNextButtonImage = tk.PhotoImage(file='./Python Project - Art Assets/ResizedNextButton.png')
        self.LoadQuitButtonImage = tk.PhotoImage(file='./Python Project - Art Assets/ResizedQuitButton.png')

        # Create Canvas Items
        self.AppCanvas.create_image(0, 0, image=self.LoadBackgroundImage, anchor="nw")
        self.NumberOfWordsLeftLabel = self.AppCanvas.create_text(200, 75,
                                                                 text="Take a Test For All Vocabulary, Press 0",
                                                                 anchor="nw", font=('Arial Black', 10))
        self.FirstLetterOfWordLabel = self.AppCanvas.create_text(
            200, 100, text="Or Type The First Letter of Words You'd Like To Test",
            anchor="nw", font=('Arial Black', 10))
        self.PartOfSpeechLabel = self.AppCanvas.create_text(200, 125, text="Then Click The Submit Button", anchor="nw",
                                                            font=('Arial Black', 10))
        self.PronunciationLabel = self.AppCanvas.create_text(200, 150, text="", anchor="nw", font=('Arial Black', 10))
        self.SentenceLabel = self.AppCanvas.create_text(200, 175, text="", anchor="nw", font=('Arial Black', 10))
        self.UserAnswerStateLabel = self.AppCanvas.create_text(WindowWidth / 2, 200, text="", anchor="nw",
                                                               font=('Arial Black', 10))
        self.MeaningEntryLabel = self.AppCanvas.create_text(200, 225, text="", anchor="nw", font=('Arial Black', 10))
        self.ExampleLabel = self.AppCanvas.create_text(200, 250, text="", anchor="nw", font=('Arial Black', 10))

        # Create Buttons And Input Entry
        self.UserEntry = tk.Entry(rootWindow, font=35)
        self.SubmitButton = tk.Button(rootWindow, image=self.LoadSubmitButtonImage,
                                      command=lambda: self.submit_response(self.UserEntry.get()))
        self.NextButton = tk.Button(rootWindow, image=self.LoadNextButtonImage,
                                    command=lambda: self.next_button_clicked())
        self.QuitButton = tk.Button(rootWindow, image=self.LoadQuitButtonImage, command=quit)

        # Create Button Windows
        self.EntryWindow = self.AppCanvas.create_window(WindowWidth / 2, WindowHeight / 2 + 100, anchor="center",
                                                        window=self.UserEntry)
        self.SubmitButtonWindow = self.AppCanvas.create_window(WindowWidth / 2 - 175, WindowHeight / 2 + 200,
                                                               anchor="center", window=self.SubmitButton)
        self.NextButtonWindow = self.AppCanvas.create_window(WindowWidth / 2 + 175, WindowHeight / 2 + 200,
                                                             anchor="center", window=self.NextButton)
        self.QuitButtonWindow = self.AppCanvas.create_window(WindowWidth - 175, 75, anchor="ne", window=self.QuitButton)

    # Functions
    def changing_text_content(self, canvas_var, string):
        self.AppCanvas.itemconfig(canvas_var, text=string)

    def update_labels(self):
        global categoryQuestionArray
        global chosenCategory
        question_index = categoryQuestionArray[0]

        self.UserEntry.delete(0, 'end')

        self.changing_text_content(self.FirstLetterOfWordLabel, "First Letter of The Word: " + chosenCategory)
        self.changing_text_content(self.PartOfSpeechLabel, "The Part of Speech: " +
                                   VocabFile.loc[question_index].PartOfSpeech)
        self.changing_text_content(self.SentenceLabel, "Sentence: " + VocabFile.loc[question_index].Sentence)
        self.changing_text_content(self.NumberOfWordsLeftLabel, "Number of Words Left to Solve: " +
                                   str(len(categoryQuestionArray)))
        self.changing_text_content(self.UserAnswerStateLabel, "")

    def load_questions_array_with_index(self, string):
        i = 0
        global categoryQuestionArray
        categoryQuestionArray = []

        while i < len(VocabFile.index):
            if string != "0":
                if VocabFile.loc[i].Meaning[0] == chosenCategory:
                    categoryQuestionArray.append(i)
            else:
                categoryQuestionArray.append(i)
            i += 1
        self.changing_text_content(self.PronunciationLabel, "Pronunciation: ")
        self.changing_text_content(self.MeaningEntryLabel, "Meaning: ")
        self.changing_text_content(self.ExampleLabel, "Example: ")
        self.update_labels()

    def submit_response(self, response):
        global isPlaying
        global isAllVocab
        global chosenCategory

        if not isPlaying:
            if len(response) < 2:
                if response == "0":
                    isAllVocab = True
                    chosenCategory = response
                else:
                    chosenCategory = response
                isPlaying = True
                self.load_questions_array_with_index(response)
                self.update_labels()
            else:
                self.changing_text_content(self.UserAnswerStateLabel,
                                           "Invalid Choice, please only type one letter or 0")
        else:
            if response == "":
                self.changing_text_content(self.UserAnswerStateLabel,
                                           "Empty Response, try again")
            else:
                self.process_user_input(response)

    def process_user_input(self, string):
        global categoryQuestionArray
        global chosenCategory

        if len(categoryQuestionArray) > 0:
            if string == VocabFile.loc[categoryQuestionArray[0]].Meaning:
                self.changing_text_content(self.UserAnswerStateLabel, "CORRECT!")
            else:
                self.changing_text_content(self.UserAnswerStateLabel, "Wrong, the correct answer is: "
                                           + str(VocabFile.loc[categoryQuestionArray[0]].Meaning))
            self.changing_text_content(self.PronunciationLabel, "Pronunciation: " +
                                       str(VocabFile.loc[categoryQuestionArray[0]].Pronunciation))
            self.changing_text_content(self.ExampleLabel, "Example: " +
                                       str(VocabFile.loc[categoryQuestionArray[0]].Example))

    def next_button_clicked(self):
        global categoryQuestionArray

        self.UserEntry.delete(0, 'end')

        if len(categoryQuestionArray) > 1:
            self.changing_text_content(self.UserAnswerStateLabel, "")
            categoryQuestionArray.pop(0)
            self.changing_text_content(self.PronunciationLabel, "Pronunciation: ")
            self.changing_text_content(self.ExampleLabel, "Example: ")
            self.update_labels()
        else:
            self.changing_text_content(self.NumberOfWordsLeftLabel, "Number of Words Left to Solve: 0")
            self.changing_text_content(self.UserAnswerStateLabel, "This is the last question, press quit to close.")
            self.SubmitButton.destroy()
            self.NextButton.destroy()


# Single App Window For All Game Displaying Objects and GUI
if __name__ == "__main__":
    rootWindow = tk.Tk()
    rootWindow.title("Vocabulary Study Application")
    viewWindow = Application(rootWindow)
    rootWindow.mainloop()

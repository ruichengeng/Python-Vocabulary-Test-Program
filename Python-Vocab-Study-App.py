import pandas as pd
import os

#VocabFile = pd.read_excel(r"../Python-Vocab-Study/DataForStudy.xlsx")
VocabFile = pd.read_excel(r"DataForStudy.xlsx")
os.system("cls")
print("\u001b[44m")
print("\033[1ma")
print(VocabFile)

UserInput = input("To take a test for all vocabularies, press 0\n"
                  "Or choose the first letter of words you would like to test\n"
                  "- ")[0]

# Variables
isPlaying = True
chosenCategory = ""
categoryQuestionArray = []
isAllVocab = False

# Functions
if UserInput == "0":
    isAllVocab = True
    chosenCategory = UserInput
else:
    chosenCategory = UserInput

print("Length of the thing " + str(len(VocabFile.index)))

def LoadQuestionsArrayWithIndex(string):
    i = 0
    SelectedQuestionsIndex = []
    while i < len(VocabFile.index):
        if string != "0":
            if (VocabFile.loc[i].Meaning[0] == chosenCategory):
                #print(VocabFile.loc[i].Meaning)
                SelectedQuestionsIndex.append(i)
        else:
            SelectedQuestionsIndex.append(i)
        i += 1
    return SelectedQuestionsIndex

def ProcessQuestionByIndex(string, QuestionArray = list[int]):
    if (len(QuestionArray) > 0):
        QuestionIndex = QuestionArray[0]
        print("The first letter of the word: " + string)
        print("The part of speech: " + VocabFile.loc[QuestionIndex].PartOfSpeech)
        print("Sentence: " + VocabFile.loc[QuestionIndex].Sentence)
        QuestionAnswer = input("Meaning: ")
        if (QuestionAnswer == VocabFile.loc[QuestionIndex].Meaning):
            print("Correct!")
            print("Pronunciation: " + str(VocabFile.loc[QuestionIndex].Pronunciation))
            print("Example: " + str(VocabFile.loc[QuestionIndex].Example))
        else:
            print("You are wrong, the correct answer is: " + str(VocabFile.loc[QuestionIndex].Meaning))
        QuestionArray.pop(0)
    return QuestionArray


categoryQuestionArray = LoadQuestionsArrayWithIndex(chosenCategory)

while isPlaying:
    os.system("cls")
    #print("\u001b[44;1m")

    #print("\u001b[31mRed  \u001b[32mGreen \u001b[34mBlue \u001b[37m")

    #print("\u001b[37;1m \033[1ma")
    print("Questions Left: " + str(len(categoryQuestionArray)))
    categoryQuestionArray = ProcessQuestionByIndex(chosenCategory, categoryQuestionArray)
    if (len(categoryQuestionArray) > 0):
        newInput = input("Want to keep playing? ")
        while (newInput != "N" and newInput != "Y"):
            newInput = input("Unknown input, please type Y or N: ")
        if (newInput == "N"):
            isPlaying = False
        elif (newInput == "Y"):
            os.system("cls")
            isPlaying = True
    else:
        isPlaying = False
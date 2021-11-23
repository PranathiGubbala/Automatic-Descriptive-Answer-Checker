import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
import string
from fuzzywuzzy import fuzz

    
#To remove stop words and punctuation marks from the sentence 
class FuzzyWuzzy(object):
    stopwords
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    def remove_stop_words(self,sentence):
        word_tokens = word_tokenize(sentence) 
        filtered_sentence = [w for w in word_tokens if not w in self.stop_words and w.strip() not in string.punctuation]
        print("Given Sentence is: ", word_tokens) 
        result = ' '.join(filtered_sentence)
        print("Filtered sentence is: ", result)
        return(result)
    def getfuzzywuzzyRatio(self,sentence_1, sentence_2):
        sentence_1_lower = sentence_1.lower()
        sentence_2_lower = sentence_2.lower()
        Ratio = fuzz.ratio(sentence_1, sentence_2)
        print("Ratio is: ", Ratio)
        Partial_Ratio = fuzz.partial_ratio(sentence_1_lower, sentence_1_lower)
        print("Partial Ratio is : ", Partial_Ratio)
        return(Partial_Ratio)

    def getMatchPercentage(self,teacher_ans, student_ans):
        #Applying preprocessing to apply the logic
        teacher_ans = self.remove_stop_words(teacher_ans)
        student_ans = self.remove_stop_words(student_ans)
   
        #getting match percentage on the preprocessed data through FuzzyWuzzy Logic
        match_percentage = self.getfuzzywuzzyRatio(teacher_ans, student_ans)
        return(match_percentage)

    

    

    



    
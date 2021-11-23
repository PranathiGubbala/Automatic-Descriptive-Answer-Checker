from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import string

stop_words = set(stopwords.words('english'))

#To remove stop words and punctuation marks from the sentence 
def remove_stop_words(sentence):
    global stop_words
    word_tokens = word_tokenize(sentence) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words and w.strip() not in string.punctuation]
    print("Given Sentence is: ", word_tokens) 
    result = ' '.join(filtered_sentence)
    print("Filtered sentence is: ", result)
    return(result)

from fuzzywuzzy import fuzz

def getfuzzywuzzyRatio(sentence_1, sentence_2):
    sentence_1_lower = sentence_1.lower()
    sentence_2_lower = sentence_2.lower()
    Ratio = fuzz.ratio(sentence_1, sentence_2)
    print("Ratio is: ", Ratio)
    Partial_Ratio = fuzz.partial_ratio(sentence_1_lower, sentence_1_lower)
    print("Partial Ratio is : ", Partial_Ratio)
    return(Partial_Ratio)

def getMatchPercentage(teacher_ans, student_ans):
    #Applying preprocessing to apply the logic
    teacher_ans = remove_stop_words(teacher_ans)
    student_ans = remove_stop_words(student_ans)
   
    #getting match percentage on the preprocessed data through FuzzyWuzzy Logic
    match_percentage = getfuzzywuzzyRatio(teacher_ans, student_ans)
    return(match_percentage)

#testing for 5 answers
teacher_ans = "The relation between the living organisms as well as the relation between the organism and their surroundings form an ecosystem."
student_ans = "The living organisms in an environment form an ecosystem"
match_perc = getMatchPercentage(teacher_ans, student_ans)
print("Match percentage between the given two answers is : ", match_perc)

teacher_ans = "Biosphere is a narrow zone of the earth where land, water and air interact with each other to support life."
student_ans = "Biosphere is region of the earth where organisms live including land and air"
match_perc = getMatchPercentage(teacher_ans, student_ans)
print("Match percentage between the given two answers is : ", match_perc)

teacher_ans = "Lithosphere provide us forests, grasslands for grazing land for agriculture and human settlements"
student_ans = "Lithosphere provide us forests."
match_perc = getMatchPercentage(teacher_ans, student_ans)
print("Match percentage between the given two answers is : ", match_perc)

teacher_ans = "The degree of hotness and coldness of the air is known as temperature"
student_ans = "The degree of hotness of the air is known as temperature."
match_perc = getMatchPercentage(teacher_ans, student_ans)
print("Match percentage between the given two answers is : ", match_perc)
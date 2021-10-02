#! /usr/bin/env python3
import spacy   

# loading a spacy model
nlp = spacy.load("en_core_web_sm")


# for question belonging to what, when ,where,etc types
def is_question(doc):
    question_tags_spacy = ["WDT", "WP", "WP$", "WRB"]
    question_words = [i for i in doc if i.tag_ in question_tags_spacy]
    sent_is_question = question_words and question_words[0].i == 0

    # questions like "To whom did this make cry? "
    type2_question = question_words and question_words[0].head.dep_ == "prep"
    
    # sentences like "where I go is none of your business"
    pseudo_question = question_words and question_words[0].head.dep_ in ["csubj", "advcl"]
    if pseudo_question:
        return False

    return sent_is_question or type2_question
    
  

# for questions belonging to yes or no
def subject_sentences(i):
    subject_deps = {"csubj", "nsubj", "nsubjpass"}
    return i.dep_ in subject_deps
        

def is_yes_no(doc):
    root = [i for i in doc if i.dep_ == "ROOT"][0]  
    subj = [i for i in root.children if subject_sentences(i)]

    if is_question(doc):
        return False


    aux = [i for i in root.lefts if i.dep_ == "aux"]
    if subj and aux:
        return aux[0].i < subj[0].i

    # copular sentence like "is the cat dead"
    copular_sentence = root.pos_ == "VERB" and root.tag_ != "VB"
    if subj and copular_sentence:
        return root.i < subj[0].i

    return False

filename = input("Enter the path/filename of the file from present location:  ")
file1 = open(filename, 'r')
Lines = file1.readlines()


with open("output.txt", 'w') as output_file:
    for line in Lines:
        doc = nlp(line)
        questions = is_question(doc)
        questions_yes_no = is_yes_no(doc)
        if questions:
           output_file.write(f"{line.strip()}	Yes\n")
        elif questions_yes_no:
           output_file.write(f"{line.strip()}	Yes\n")
        else:
           output_file.write(f"{line.strip()}	No\n")
print("The output has been saved to output.txt in present working directory")

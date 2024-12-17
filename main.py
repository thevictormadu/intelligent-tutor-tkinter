import tkinter as tk
from tkinter import PhotoImage
from owlready2 import get_ontology

# Loading the ontology
ontology_path = "probabilityITS.owl"  # Path to your ontology file
onto = get_ontology(ontology_path).load()

# Extracting questions and answers from the ontology
def extract_qa_pairs():
    qa_pairs = []
    for question in onto.Question.instances():
        question_text = question.questionText[0] if question.questionText else "No question text"
        if question.hasAnswer:
            answer_individual = question.hasAnswer[0]
            correct_answer = answer_individual.answerText[0] if answer_individual.answerText else "No answer text"
            explanation_individual = answer_individual.hasExplanation[0]
            answer_explanation = explanation_individual.explanationText[0] if explanation_individual.explanationText else "No explanation"

        else:
            correct_answer = "No answer"
        qa_pairs.append((question_text, correct_answer, answer_explanation))
    return qa_pairs


qa_pairs = extract_qa_pairs()
current_index = 0


def check_answer():
    global current_index
    user_answer = answer_entry.get().strip()
    question, correct_answer, answer_explanation = qa_pairs[current_index]

    if user_answer == correct_answer:
        feedback_label.config(text="Fantastic🥰 You are Correct!", fg="green")
        next_button.config(state="normal")
        explanation.config(text=f"Here is why: {answer_explanation}")
    else:
        feedback_label.config(text="Incorrect. Please try again.", fg="red")
        submit_button.config(text="Try Again")
        explanation.config(text="")

def next_question():
    global current_index
    current_index += 1
    if current_index < len(qa_pairs):
        question, _, _ = qa_pairs[current_index]
        question_label.config(text=question)
        feedback_label.config(text="")
        explanation.config(text="")
        answer_entry.delete(0, tk.END)
        submit_button.config(text="Submit")
        next_button.config(state="disabled")
    else:
        question_label.config(text="End of questions. Well done!")
        feedback_label.config(text="")
        explanation.config(text="")
        answer_entry.delete(0, tk.END)
        answer_entry.config(state="disabled")
        submit_button.config(state="disabled")
        next_button.config(state="disabled")


# Tkinter UI section
root = tk.Tk()
root.geometry("600x600")
root.title("Intelligent Tutoring System")

header_image_path = "header-image.png"  # Replace with the path to your image file
header_image = PhotoImage(file=header_image_path)
header_label = tk.Label(root, image=header_image)
header_label.pack(pady=10)

title_label = tk.Label(root, text="Let's learn probability", font=("Arial", 14))
title_label.pack(pady=10)

question_label = tk.Label(root, text="Question:", font=("Arial", 18), wraplength=500)
question_label.pack(pady=10)

answer_entry = tk.Entry(root, font=("Arial", 14), width=50)
answer_entry.pack(pady=10)

submit_button = tk.Button(root, text="Submit", font=("Arial", 14), command=check_answer)
submit_button.pack(pady=10)

next_button = tk.Button(root, text="Next Question", font=("Arial", 14), state="disabled", command=next_question,)
next_button.pack(pady=10, padx=10)

feedback_label = tk.Label(root, text="", font=("Arial", 16, "bold"))
feedback_label.pack(pady=10)

explanation = tk.Label(root, wraplength=400, font=("Arial", 12) )
explanation.pack(pady=10)

if qa_pairs:
    question, _, _ = qa_pairs[current_index]
    question_label.config(text=question)
else:
    question_label.config(text="No questions found in the ontology.")
    submit_button.config(state="disabled")

root.mainloop()
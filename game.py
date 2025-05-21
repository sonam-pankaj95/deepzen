import os
import inquirer
from google.generativeai import configure, GenerativeModel

# Set up Gemini API
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")
configure(api_key=api_key)
model = GenerativeModel("gemini-2.0-flash")


def grade_morality(question, answer):
    """
    Grades the morality of an answer using the Gemini API.
    Returns a tuple of (score, explanation)
    """
    prompt = f"""
    You are a morality expert. You are to grade the morality of a statement.
    Consider the following question and answer:
    Question: {question}
    Answer: {answer}

    Based on utilitarianism and deontology, provide a morality score from 1 to 10 (1 being least moral and 10 being most moral) and a brief explanation.
    For utilitarian answers (like maximizing happiness for the greatest number), give a score of 8 or higher.
    For deontological answers (like upholding individual rights), give a score of 7 or higher.
    For answers about following rules without question, give a lower score (3-5).
    Format your response as a single number (1-10) followed by a newline and then your explanation.
    """
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        # Split the response into score and explanation
        score_str, explanation = response_text.split("\n", 1)
        score = int(score_str.strip())
        return score, explanation.strip()
    except Exception as e:
        return 0, f"Error grading morality: {e}"


def generate_question(previous_answers, current_level):
    """
    Generates a new question using Gemini based on previous answers and current level.
    """
    prompt = f"""
    You are a philosophical question generator. Generate a thought-provoking moral question based on the following context:
    
    Previous answers: {previous_answers}
    Current level: {current_level}
    
    Generate a question that:
    1. Is more challenging than previous questions
    2. Relates to the user's previous answers
    3. Explores deeper moral and philosophical concepts
    4. Has exactly 4 distinct answer choices
    
    Format your response as:
    QUESTION: [Your question here]
    CHOICES:
    1. [First choice]
    2. [Second choice]
    3. [Third choice]
    4. [Fourth choice]
    """
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Parse the response to extract question and choices
        parts = response_text.split("CHOICES:")
        question = parts[0].replace("QUESTION:", "").strip()
        choices = [choice.strip() for choice in parts[1].strip().split("\n") if choice.strip()]
        
        return question, choices
    except Exception as e:
        # Fallback question in case of error
        return "What is the most important virtue to cultivate?", [
            "Courage in the face of adversity.",
            "Compassion for others.",
            "Wisdom and understanding.",
            "Justice and fairness."
        ]


def run_cli():
    """
    Runs the command-line interface for asking existential questions and grading morality.
    """
    previous_answers = {}
    current_level = 1
    max_level = 5

    while current_level <= max_level:
        question, choices = generate_question(previous_answers, current_level)
        
        # Print the question first
        print(f"\nLevel {current_level} Question:")
        print(f"{question}\n")
        
        current_question = inquirer.List(
            f"question{current_level}",
            message="Select your answer:",
            choices=choices
        )
        
        answer = inquirer.prompt([current_question])

        if not answer:  # User cancelled
            break

        user_answer = answer[current_question.name]
        previous_answers[current_question.name] = user_answer

        score, explanation = grade_morality(question, user_answer)
        print(f"\nYour Answer: {user_answer}")

        if score <= 5:
            print(f"Morality Assessment:\nScore: {score}\n{explanation}")
            print("\nGame Over! You didn't meet the moral threshold to advance.")
            break
        else:
            print(f"\n🎉 Congratulations! You've advanced to Level {current_level + 1}!")
            current_level += 1

    if current_level > max_level:
        print("\n🌟 Congratulations! You've completed all levels and demonstrated exceptional wisdom in DeepZen!")


if __name__ == "__main__":
    run_cli()

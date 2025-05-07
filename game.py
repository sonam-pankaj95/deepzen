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


def get_next_question(previous_answers):
    """
    Determines the next question based on previous answers.
    """
    if not previous_answers:
        return inquirer.List(
            "question1",
            message="What is more important?",
            choices=[
                "Maximizing happiness for the greatest number of people, even if it means sacrificing individual rights.",
                "Upholding individual rights and duties, even if it means less overall happiness.",
                "Striving for personal virtue and excellence, regardless of consequences.",
                "Following the rules and laws of society without question.",
            ],
        )

    last_answer = list(previous_answers.values())[-1]
    question_number = len(previous_answers) + 1

    if question_number == 2:
        if "Maximizing happiness" in last_answer:
            return inquirer.List(
                "question2",
                message="If you could save one person from a burning building, who would it be?",
                choices=[
                    "A brilliant scientist who could cure a deadly disease.",
                    "A close family member.",
                    "A random stranger.",
                    "A religious figure known for their good deeds.",
                ],
            )
        elif "Upholding individual rights" in last_answer:
            return inquirer.List(
                "question2",
                message="How would you handle a situation where someone's rights conflict with public safety?",
                choices=[
                    "Prioritize public safety over individual rights.",
                    "Find a compromise that respects both.",
                    "Always uphold individual rights regardless of consequences.",
                    "Let the legal system decide.",
                ],
            )
        elif "Striving for personal virtue" in last_answer:
            return inquirer.List(
                "question2",
                message="What is the most important virtue to cultivate?",
                choices=[
                    "Courage in the face of adversity.",
                    "Compassion for others.",
                    "Wisdom and understanding.",
                    "Justice and fairness.",
                ],
            )
        else:  # Following rules
            return inquirer.List(
                "question2",
                message="What would you do if you discovered a law that was unjust?",
                choices=[
                    "Follow it anyway, as it's the law.",
                    "Work within the system to change it.",
                    "Civil disobedience to protest it.",
                    "Seek legal loopholes to avoid it.",
                ],
            )
    else:  # question_number == 3
        return inquirer.List(
            "question3",
            message="What is your ultimate goal in life?",
            choices=[
                "To achieve personal success and happiness.",
                "To make the world a better place for others.",
                "To fulfill your duties and responsibilities.",
                "To seek truth and understanding.",
            ],
        )


def run_cli():
    """
    Runs the command-line interface for asking existential questions and grading morality.
    """
    previous_answers = {}
    question_number = 1
    current_level = 1

    while question_number <= 3:  # We'll ask 3 questions total
        current_question = get_next_question(previous_answers)
        answer = inquirer.prompt([current_question])

        if not answer:  # User cancelled
            break

        question_text = current_question.message
        user_answer = answer[current_question.name]
        previous_answers[current_question.name] = user_answer

        score, explanation = grade_morality(question_text, user_answer)
        print(f"\nQuestion {question_number}: {question_text}")
        print(f"Your Answer: {user_answer}")

        if score <= 5:
            print(f"Morality Assessment:\nScore: {score}\n{explanation}")
        else:
            current_level += 1
            print(f"\n🎉 Congratulations! You've advanced to Level {current_level}!")

        question_number += 1


if __name__ == "__main__":
    run_cli()

# Morality Assessment Game

An interactive command-line game that assesses moral choices through a series of philosophical questions. The game uses Google's Gemini AI to evaluate responses based on utilitarian and deontological principles.

## Features

- Interactive command-line interface with multiple-choice questions
- AI-powered morality assessment using Google's Gemini API
- Progressive difficulty with three levels
- Personalized questions based on previous answers
- Detailed scoring and explanations for each response

## Prerequisites

- Python 3.x
- Google API key for Gemini AI

## Installation

1. Clone this repository
2. Install required packages:
```bash
pip3 install inquirer google-generativeai
```

3. Set up your Google API key:
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

## How to Play

1. Run the game:
```bash
python3 game.py
```

2. Answer a series of three questions about moral dilemmas
3. Each answer is evaluated by the AI based on:
   - Utilitarian principles (maximizing happiness)
   - Deontological principles (duty and rights)
4. Advance to the next level if your answer receives a high morality score
5. Receive detailed explanations of the moral implications of your choices

## Question Types

The game presents different types of moral questions:
- First question: Fundamental moral principles
- Second question: Applied moral dilemmas
- Third question: Personal moral goals

## Scoring System

- Scores range from 1 to 10
- Higher scores (8+) for utilitarian answers
- Good scores (7+) for deontological answers
- Lower scores (3-5) for rule-following without question
- Score of 5 or higher required to advance to next level

## Note

This game is designed for educational and entertainment purposes. The moral assessments are based on AI interpretation and should not be taken as definitive moral judgments. 
# DeepZen

A thought-provoking game that presents players with challenging moral scenarios and evaluates responses based on moral reasoning principles.

## Features

- Interactive moral reasoning challenges
- Progressive difficulty levels
- AI-powered question generation
- Real-time moral assessment
- Web-based interface
- Command-line interface option

## Prerequisites

- Python 3.7 or higher
- Google API key for Gemini AI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/deepzen.git
cd deepzen
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

### Web Interface

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

### Command Line Interface

Run the CLI version:
```bash
python game.py
```

## Game Mechanics

- The game consists of 5 levels of increasing difficulty
- Each level presents a unique moral question with 4 possible answers
- Your answers are evaluated based on moral reasoning principles
- To advance to the next level, you must achieve a morality score above 5
- The game ends if you fail to meet the moral threshold or complete all levels

## Technical Details

The project uses:
- Flask for the web interface
- Google's Gemini AI for question generation and moral assessment
- Python-dotenv for environment variable management
- Gunicorn for production deployment

## Deployment

The project includes a `Procfile` for easy deployment to platforms like Heroku. Make sure to set the `GOOGLE_API_KEY` environment variable in your deployment environment.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for powering the DeepZen engine
- Flask framework for the web interface
- All contributors and users of the project 
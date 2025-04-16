# EV Charging Station Chatbot

An interactive chatbot interface for querying information about EV charging stations. The application provides a user-friendly interface to query and analyze charging station data with predefined questions and custom queries.

## Features

- Interactive chat interface
- Predefined questions for common queries
- Table formatting for structured data responses
- Responsive design for mobile and desktop
- Real-time data analysis capabilities

## Tech Stack

- Python (Backend)
- HTML/CSS/JavaScript (Frontend)
- PandasAI for data analysis
- OpenAI integration for natural language processing

## Setup Instructions

1. Clone the repository
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key in the environment variables
4. Run the application:
   ```bash
   python app.py
   ```

## Project Structure

- `templates/` - Contains HTML templates
- `static/` - Static files (CSS, JS)
- `app.py` - Main Flask application
- `csv_to_dataframe.py` - Data processing script

## Usage

1. Start the application
2. Use predefined questions from the sidebar
3. Or type your custom queries in the chat input
4. View responses in formatted tables or text

## License

MIT License 
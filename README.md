# Mimicking Our Love Language

Welcome to **Mimicking Our Love Language**! ❤️ This project is a heartfelt exploration of natural language processing (NLP) and its ability to understand and mimic the way we express love and emotions through words. Whether you're a language enthusiast, a developer, or just someone curious about how machines can interpret human emotions, this project is for you!

## 🌟 Features

### Core NLP Capabilities
- **Named Entity Recognition (NER):** Identify and extract meaningful entities (persons, locations, organizations, etc.) from Turkish text using BERT-based models
- **Sentiment Analysis:** Analyze emotions in Turkish text with positive/negative classification
- **Text Parsing:** Analyze and break down messages to understand their structure and meaning
- **PII Extraction:** Extract personally identifiable information (emails, phone numbers, dates, addresses, etc.)

### Analysis & Statistics
- **Message Statistics:** Word count, character count, emoji count, and more
- **Entity Statistics:** Track and analyze extracted entities across messages
- **Word Frequency Analysis:** Find most commonly used words
- **Author Comparison:** Compare statistics between different authors

### Data Export
- **JSON Export:** Export analysis results in JSON format
- **CSV Export:** Export data in CSV format for spreadsheet applications
- **Excel Export:** Export to Excel with multiple sheets and formatting
- **Entity Export:** Separate export of extracted entities

### Visualization
- **Entity Distribution Charts:** Visualize entity types and frequencies
- **Sentiment Distribution Charts:** See emotional patterns in your messages
- **Message Length Distribution:** Analyze message length patterns
- **Word Frequency Charts:** Visualize most common words

### Configuration & Utilities
- **Centralized Configuration:** JSON-based configuration management
- **Text Sanitization:** Clean and prepare text for analysis
- **PII Masking:** Mask sensitive information for privacy
- **Error Handling:** Robust error handling throughout the application

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cagin2245/Mimicking-Our-Love-Language.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Mimicking-Our-Love-Language
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the main script:
   ```bash
   python main.py
   ```

### First Run
On the first run, the program will download the necessary NLP models. Make sure you have an internet connection. The models will be cached for future use.

## 📖 Usage

### Interactive Menu
When you run `main.py`, you'll be presented with a menu:

1. **NER Analizi** - Named Entity Recognition analysis
2. **Duygu Analizi** - Sentiment analysis
3. **İstatistikler** - Message statistics
4. **Tüm Analizler** - Run all analyses
5. **Sadece NER (Eski versiyon)** - Legacy NER-only mode

### Programmatic Usage

```python
from parser import read_data, sanitize_messages
from NER import apply_ner, filter_messages
from sentiment import analyze_sentiment, analyze_sentiments
from statistics import get_message_statistics, get_most_common_words
from export import export_to_json, export_to_csv
from visualization import plot_entity_distribution, plot_sentiment_distribution

# Read and sanitize messages
messages, author = read_data("data.txt")
sanitized = sanitize_messages(messages)

# NER Analysis
for text in sanitized["i"]:
    entities = apply_ner(text)
    print(f"Entities: {entities}")

# Sentiment Analysis
sentiment = analyze_sentiment("Bu harika bir gün!")
print(f"Sentiment: {sentiment}")

# Statistics
stats = get_message_statistics(sanitized["i"])
print(f"Total messages: {stats['total_messages']}")

# Export
export_to_json(stats, "statistics.json")
```

## 📂 Project Structure
```
Mimicking-Our-Love-Language/
├── main.py              # Entry point with interactive menu
├── NER.py               # Named Entity Recognition module
├── parser.py            # Text parsing and data reading
├── sentiment.py         # Sentiment analysis module
├── statistics.py        # Statistical analysis functions
├── export.py            # Data export functionality
├── visualization.py     # Chart and graph generation
├── pii.py               # PII extraction functions
├── utility.py           # Utility functions for text processing
├── config.py            # Configuration management
├── config.json          # Configuration file
├── example_usage.py     # Usage examples
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
└── __pycache__/         # Compiled Python files
```

## ⚙️ Configuration

The project uses `config.json` for centralized configuration. You can customize:

- **NER Settings:** Model name, minimum score threshold
- **Sentiment Settings:** Model selection
- **PII Settings:** Masking preferences for sensitive data
- **Export Settings:** Default format and output directory
- **Visualization Settings:** Chart size, DPI, style

Example configuration:
```json
{
  "ner": {
    "model_name": "akdeniz27/bert-base-turkish-cased-ner",
    "min_score": 0.6
  },
  "sentiment": {
    "model_name": "savasy/bert-base-turkish-sentiment-cased"
  }
}
```

## 📊 Output Files

The program can generate various output files:

- `entity_distribution.png` - Entity type distribution chart
- `sentiment_distribution.png` - Sentiment analysis results chart
- `message_length_distribution.png` - Message length analysis chart
- `export_*.json` - JSON export files
- `export_*.csv` - CSV export files
- `export_*.xlsx` - Excel export files

## 🔧 Dependencies

- **transformers** - Hugging Face transformers for NLP models
- **torch** - PyTorch for model inference
- **pandas** - Data manipulation and Excel export
- **matplotlib** - Basic plotting
- **seaborn** - Advanced visualization
- **openpyxl** - Excel file support
- **numpy** - Numerical operations

## 💡 Inspiration
Language is a beautiful way to connect with others, and this project aims to explore how machines can learn to understand and replicate the nuances of human emotions and expressions. By leveraging the power of NLP, we hope to create tools that bring us closer together in the digital age.

## 🐛 Known Issues

- Sentiment model may take time to load on first use
- Processing time may be long for very large files
- Some emojis may not be counted correctly

## 🔮 Future Enhancements

- Web interface using Flask/FastAPI
- Database support (SQLite/PostgreSQL)
- RESTful API endpoints
- Advanced NLP features (topic modeling, text summarization)
- Custom model training
- Real-time message analysis
- Multi-language support
- Optimized batch processing for large files

## 🤝 Contributing
We welcome contributions! Feel free to fork this repository, make your changes, and submit a pull request. Let's build something amazing together!

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact
For any questions, suggestions, or just to say hi, feel free to reach out to us at:
- **[caginkilincyt@gmail.com](mailto:caginkilincyt@gmail.com)**
- **[iremyurdakul1@gmail.com](mailto:iremyurdakul1@gmail.com)**

## 📝 License
This project is open source and available for personal and educational use.

---

Thank you for checking out **Mimicking Our Love Language**! We hope you enjoy exploring the project as much as we enjoyed creating it. 💕

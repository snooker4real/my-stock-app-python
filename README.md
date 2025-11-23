# 📈 Jonathan Stocks

A modern, beautiful desktop application for real-time stock market data visualization built with Python and Flet.

![Jonathan Stocks App](https://github.com/user-attachments/assets/7c1fc763-2d5a-4a06-8711-21922409b3b1)

## ✨ Features

- **Real-time Stock Data** - Fetch live stock market data from Alpha Vantage API
- **Interactive Charts** - Beautiful, smooth line charts showing closing prices over time
- **Multiple Time Ranges** - View data from 1 week to 5 years
- **Price Analytics** - Display Open, High, Low, and Close prices with color-coded cards
- **Price Change Indicators** - Shows daily price changes with percentage and visual indicators
- **Modern UI** - Clean, professional interface with gradient headers and card-based design
- **Responsive Loading States** - Animated loading spinner for better user experience
- **Error Handling** - Clear, user-friendly error messages

## 🚀 Quick Start

### Prerequisites

- Python 3.14 or higher
- Alpha Vantage API key (free at [alphavantage.co](https://www.alphavantage.co/support/#api-key))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd my-stock-app-python
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure your API key**

   Create a `.env` file in the project root:
   ```env
   API_KEY=your_alpha_vantage_api_key_here
   ```

6. **Run the application**
   ```bash
   flet run app.py
   ```

## 📦 Dependencies

- **Flet** (0.28.3) - Cross-platform GUI framework based on Flutter
- **Requests** (2.32.5) - HTTP library for API calls
- **Python-dotenv** (1.2.1) - Environment variable management
- **httpx** (0.28.1) - Modern HTTP client

## 🎯 Usage

1. **Enter a stock symbol** (e.g., AAPL, GOOGL, MSFT, TSLA)
2. **Select a time range** from the dropdown (1 week to 5 years)
3. **Click "Get Stock Data"** or press Enter
4. View the interactive chart and detailed price information

### Supported Time Ranges

- 1 week
- 2 weeks
- 30 days
- 90 days
- 1 year
- 5 years

## 🏗️ Project Structure

```
my-stock-app-python/
├── app.py              # Main application file
├── config.py           # Configuration and API key management
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── README.md          # This file
└── venv/              # Virtual environment
```

## 🎨 UI Components

### Header
- Gradient blue background
- Application title with icon
- Descriptive subtitle

### Search Controls
- Stock symbol input with search icon
- Time range dropdown selector
- Styled action button

### Price Display
- Color-coded cards for Open (Blue), High (Green), Low (Red), Close (Purple)
- Icon indicators for each metric
- Price change percentage with directional arrows
- Subtle shadows and modern card design

### Chart
- Smooth, curved line chart
- Interactive tooltips
- Responsive axis labels
- Clean, minimal design

## 🔑 Getting Your API Key

1. Visit [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Enter your email address
3. Get your free API key instantly
4. Add it to your `.env` file

**Note:** Free tier includes 25 API requests per day and 5 API requests per minute.

## 🛠️ Technical Details

### Architecture
- **Single-file application** with functional components
- **Ref-based state management** for UI updates
- **Synchronous API calls** with requests library
- **Error handling** for invalid symbols and API failures

### Key Functions
- `fetch_stock_data(e)` - Main function to fetch and display stock data
- `get_days_for_range(range_name)` - Convert time range to days
- `get_range_label(range_name)` - Format time range for display

## 📊 Data Source

This application uses the [Alpha Vantage API](https://www.alphavantage.co/) for stock market data:
- **Endpoint**: TIME_SERIES_DAILY
- **Data**: Daily open, high, low, close prices
- **Coverage**: Global stock markets

## 🐛 Known Issues

- Free API tier has rate limits (5 requests/minute, 25 requests/day)
- Large time ranges may take longer to load
- Some stock symbols may not be available in the API

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📝 License

This project is open source and available for educational purposes.

## 👤 Author

**Snooker4Real**

## 🙏 Acknowledgments

- [Flet Framework](https://flet.dev/) for the amazing Python GUI framework
- [Alpha Vantage](https://www.alphavantage.co/) for providing free stock market data API
- Flutter team for the underlying UI framework

---

**Enjoy tracking your favorite stocks!** 📈✨

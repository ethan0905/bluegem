# CS2 Skin Arbitrage Tracker

A Python-based arbitrage tracker for Counter-Strike 2 (CS2) skins that monitors price differences between Steam Market and Skinport to identify profitable trading opportunities.

## Features

- 📊 **Real-time Price Tracking**: Fetches current prices from Steam Market and Skinport APIs
- 💹 **Gap Analysis**: Calculates percentage difference between platforms
- 🎯 **Opportunity Detection**: Highlights gaps above 12% in green as real opportunities
- 📈 **Smart Sorting**: Automatically sorts skins by gap size (largest first)
- 🔄 **Auto-Refresh**: Updates prices every 5 minutes automatically
- ⏱️ **Rate Limiting**: Built-in delays (1.5s for Steam, 0.5s for Skinport) to respect API limits
- 🎨 **Beautiful Display**: Uses Rich library for colorful, formatted tables
- 📊 **Summary Stats**: Shows total opportunities and potential profit

## Monitored Skins

## Monitored Skins

The tracker monitors the following CS2 items:
- Operation Breakout Case
- Sticker | Krakow 2017 Autograph Legends
- Sticker | DreamHack 2014 (Holo/Foil)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download this repository**
   ```bash
   cd /path/to/bluegem
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # OR
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tracker with:
```bash
python3 arbitrage_tracker.py
```

The script will:
1. Fetch prices for all monitored skins
2. Display a formatted table with prices and gaps
3. Highlight opportunities (>12% gap) in green
4. Show a summary with total opportunities and potential profit
5. Auto-refresh every 5 minutes

To stop the tracker, press `Ctrl+C`.

## Output Example

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ Skin                               ┃ Steam Price ┃ Skinport Price ┃  Gap % ┃ Status ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ AK-47 | Redline (Field-Tested)    │      $45.23 │         $38.50 │ 17.48% │ 🟢 BUY │
│ AWP | Asiimov (Field-Tested)      │      $89.99 │         $82.00 │  9.74% │ ⚪ LOW │
└────────────────────────────────────┴─────────────┴────────────────┴────────┴────────┘

╭─ Summary ─────────────────────────────────────╮
│ 🎯 Opportunities Found: 1                      │
│ 💰 Total Potential Profit: $6.73              │
│ 🕐 Last Update: 2026-05-03 14:30:15           │
╰────────────────────────────────────────────────╯
```

## Status Indicators

- 🟢 **BUY** - Gap > 12%, real arbitrage opportunity
- ⚪ **LOW** - Positive gap but below 12% threshold
- 🔴 **NO** - Negative gap (more expensive on Steam)
- ⚫ **ERR** - Error fetching price data

## Configuration

You can modify the following constants in `arbitrage_tracker.py`:

- `SKINS`: List of skins to monitor
- `STEAM_DELAY`: Delay between Steam API requests (default: 1.5s)
- `SKINPORT_DELAY`: Delay between Skinport API requests (default: 0.5s)
- `REFRESH_INTERVAL`: Time between full refresh cycles (default: 300s / 5 minutes)

## API Rate Limits

The tracker respects API rate limits:
- **Steam Market**: 1.5 second delay between requests
- **Skinport**: 0.5 second delay between requests

Adjust these values in the script if you encounter rate limiting issues.

## Notes

- Prices are in USD
- Steam prices use the lowest market price
- Skinport prices use the minimum available price
- The gap calculation is: `(Steam Price - Skinport Price) / Skinport Price × 100`
- Network errors and API failures are handled gracefully
- Potential profit calculation assumes buying from the cheaper platform and selling on the more expensive one (excluding fees)

## Dependencies

- **requests**: HTTP library for API calls
- **rich**: Beautiful terminal formatting and tables

## Disclaimer

This tool is for informational purposes only. Always verify prices manually before making trades. Market prices can change rapidly, and additional fees (Steam Market fees, Skinport fees, etc.) will affect actual profitability. The tracker does not account for transaction fees, taxes, or other costs associated with trading.

## License

MIT License - Feel free to modify and use as needed.

## Troubleshooting

**Problem**: "Connection error" or prices showing as N/A
- **Solution**: Check your internet connection and ensure APIs are accessible

**Problem**: All gaps showing as N/A
- **Solution**: API might be rate-limiting. Increase the delay values in the script

**Problem**: Script crashes on startup
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`
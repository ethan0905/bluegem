# CS2 Skin Market Tracker Suite

A Python-based toolkit for Counter-Strike 2 (CS2) skin trading with three powerful tools:

## 🔄 Arbitrage Tracker (`arbitrage_tracker.py`)

Real-time arbitrage opportunities by comparing Steam Market's lowest vs median prices.

**Features:**
- 📊 Real-time price tracking (lowest and median prices)
- 💹 Gap analysis between price points
- 🎯 Highlights opportunities above 12% threshold
- 🔄 Auto-refreshes every 5 minutes
- 📈 Sorted by best opportunities
- 📊 Summary with total opportunities and potential profit

## 📈 Price History Tracker (`price_history_tracker.py`)

Comprehensive historical price analysis and market statistics.

**Features:**
- 📊 Price growth tracking across multiple timeframes (1D, 7D, 30D, 3M, 6M, 1Y, 5Y)
- 📉 Historical price data from Steam Market
- 📦 Available supply and volume metrics
- 🎨 Color-coded growth indicators (green for gains, red for losses)
- 📊 Best performer highlights
- 💾 Current market price tracking

## 🌏 Buff163 Price Tracker (`buff163.py`)

Access to 38,000+ CS2 item prices from Buff163 marketplace via CSGOTrader.app API.

**Features:**
- 📊 Real Buff163 market prices for 38,000+ items
- 🔍 Interactive search by keyword
- 💎 Top 10 most expensive items display
- 🎯 Track custom items list
- 💰 Highest bid prices included
- 🚀 Fast API access (no authentication required)
- 🎨 Beautiful formatted tables
- 💻 Interactive mode with menu

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

### Arbitrage Tracker (Continuous Monitoring)

Run the real-time arbitrage tracker:
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

### Price History Tracker (One-Time Analysis)

Run the price history analysis:
```bash
python3 price_history_tracker.py
```

The script will:
1. Fetch historical price data for all monitored skins
2. Calculate growth percentages across all timeframes
3. Display current market statistics (volume, supply)
4. Show color-coded growth indicators
5. Highlight best performers

### Buff163 Price Tracker (One-Time or Interactive)

**Standard Mode** - Display tracked items and top 10 most expensive:
```bash
python3 buff163.py
```

**Interactive Mode** - Menu with search capability:
```bash
python3 buff163.py -i
```

In interactive mode, you can:
1. **Show tracked items** - View your custom list with Buff163 prices
2. **Show most expensive items** - See top 15 highest priced items
3. **Search by keyword** - Find any item by name (e.g., "karambit", "AWP", "Fade")
4. **Exit** - Close the program

The script fetches data for **38,000+ items** from Buff163 marketplace, showing:
- Current Buff163 listing price (USD)
- Highest buyer order price
- Instant price comparison for tracked items

## Output Examples

### Arbitrage Tracker Output

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ Skin                               ┃ Lowest Price ┃ Median Price ┃  Gap % ┃ Status ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ AK-47 | Redline (Field-Tested)    │       $45.01 │       $45.21 │  0.44% │ ⚪ LOW │
│ AWP | Asiimov (Field-Tested)      │       $89.50 │       $90.12 │  0.69% │ ⚪ LOW │
└────────────────────────────────────┴──────────────┴──────────────┴────────┴────────┘

╭─ Summary ─────────────────────────────────────╮
│ 🎯 Opportunities Found: 1                      │
│ 💰 Total Potential Profit: $6.73              │
│ 🕐 Last Update: 2026-05-03 14:30:15           │
╰────────────────────────────────────────────────╯
```

### Price History Tracker Output

```
                            CS2 Skin Current Market Data                             
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
┃ Skin                                 ┃ Median $ ┃ Lowest $ ┃ Spread % ┃ Vol 24h ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
│ AWP | Asiimov (Field-Tested)         │  $164.64 │  $183.34 │   -10.2% │      14 │
│ AK-47 | Redline (Field-Tested)       │   $45.21 │   $45.01 │    +0.4% │      95 │
│ Operation Breakout Weapon Case       │   $13.11 │   $13.25 │    -1.1% │   2,410 │
└──────────────────────────────────────┴──────────┴──────────┴──────────┴─────────┘

╭──────────────────── Summary ────────────────────────╮
│ 📊 Total Skins Tracked: 3                           │
│ ✅ Successfully Fetched: 3                          │
│ 💰 Combined Value: $223.96                          │
│ 🔥 Highest Volume: Operation Breakout Weapon Case   │
│    (2,410 trades)                                   │
│ 💎 Most Expensive: AWP | Asiimov (Field-Tested)     │
│    ($164.64)                                        │
╰─────────────────────────────────────────────────────╯
```

**Spread %**: Percentage difference between median and lowest price
- Positive (green): Median is higher than lowest listing
- Negative (red): Lowest listing is higher than median

### Buff163 Price Tracker Output

```
                         Tracked CS2 Items - Buff163 Prices                         
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Skin                                  ┃ Buff163 Price ┃ Highest Bid ┃ Status  ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━┩
│ AK-47 | Redline (Field-Tested)        │        $31.20 │      $30.17 │ ✓ Found │
│ AWP | Asiimov (Field-Tested)          │       $118.72 │     $118.35 │ ✓ Found │
│ M4A4 | Howl (Minimal Wear)            │      $5250.99 │    $4972.83 │ ✓ Found │
│ Karambit | Doppler (Factory New)      │      $1345.67 │    $1268.47 │ ✓ Found │
└───────────────────────────────────────┴───────────────┴─────────────┴─────────┘

                       Most Expensive Items on Buff163                       
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃   Rank ┃ Item Name                                      ┃ Price (USD) ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│     #1 │ Souvenir AWP | Dragon Lore (Factory New)       │ $512,660.57 │
│     #2 │ Souvenir AWP | Dragon Lore (Minimal Wear)      │ $205,065.11 │
│     #3 │ Sticker | Titan (Holo) | Katowice 2014         │ $146,475.08 │
│     #4 │ Sticker | iBUYPOWER (Holo) | Katowice 2014     │ $146,297.07 │
└────────┴────────────────────────────────────────────────┴─────────────┘

╭──────────────────────────────── Summary ────────────────────────────────╮
│ 📊 Total Items in Database: 38,641                                      │
│ 🎯 Items Tracked: 8                                                     │
│ ✅ Items Found: 8                                                       │
│ 💰 Combined Value: $9,743.53                                            │
│ 📡 Data Source: CSGOTrader.app (Buff163 Prices)                         │
╰─────────────────────────────────────────────────────────────────────────╯
```

**Interactive Search Example:**
```
Searching for 'karambit'...
Found 25 items including:
  #1 ★ Karambit | Crimson Web (Factory New) - $8,625.62
  #2 ★ StatTrak™ Karambit | Case Hardened (FN) - $5,565.91
  #3 ★ Karambit | Night (Factory New) - $2,929.50
  ...
```

## Status Indicators

### Arbitrage Tracker

- 🟢 **BUY** - Gap > 12%, real arbitrage opportunity
- ⚪ **LOW** - Positive gap but below 12% threshold
- 🔴 **NO** - Negative gap (more expensive on Steam)
- ⚫ **ERR** - Error fetching price data

## Finding Correct Item Names

Getting the exact item name is crucial for the trackers to work properly. Steam Market requires precise names including the year, condition, and special designations.

### Using Buff163 Database Search

The easiest way to find the correct item name is using the Buff163 price tracker's interactive search:

**Method 1: Interactive Search**
```bash
python3 buff163.py -i
```

Then:
1. Select option **3** (Search by keyword)
2. Enter your search term (e.g., "karambit doppler", "dreamhack 2014", "krakow")
3. The tool will display all matching items with exact names

**Example:**
```
Select option (1-4): 3
Enter search keyword: dreamhack 2014

Search Results for 'dreamhack 2014'
┃ Item Name                                               ┃
┃ DreamHack 2014 Legends (Holo-Foil)                      ┃
┃ DreamHack 2014 Challengers (Holo-Foil)                  ┃
┃ Sticker | DreamHack (Holo) | Cluj-Napoca 2015           ┃
...
```

**Method 2: Quick Python Script**
```bash
python -c "
import requests
data = requests.get('https://prices.csgotrader.app/latest/buff163.json').json()
results = [k for k in data.keys() if 'your_search_term' in k.lower()]
for r in results[:20]:
    print(r)
"
```

### Common Name Format Patterns

- **Weapons**: `WeaponType | SkinName (Condition)`
  - Example: `AK-47 | Redline (Field-Tested)`
  
- **Knives**: `★ KnifeType | SkinName (Condition)`
  - Example: `★ Karambit | Doppler (Factory New)`
  
- **Stickers**: `Sticker | Name | Tournament Year`
  - Example: `Sticker | Titan (Holo) | Katowice 2014`
  
- **Capsules/Cases**: `Name Year Type`
  - Example: `Krakow 2017 Challengers Autograph Capsule`
  
- **Tournament Items**: `Tournament Year Category (Type)`
  - Example: `DreamHack 2014 Legends (Holo-Foil)`

### Troubleshooting Item Names

If an item shows as **⚫ ERR** or **N/A** in the tracker:

1. Search for the item in buff163.py to verify the exact name
2. Copy the exact name (including spaces, dashes, and special characters)
3. Update your `SKINS` list in the tracker script
4. Common issues:
   - Missing year: "DreamHack Legends" → "DreamHack 2014 Legends"
   - Incomplete name: "Krakow Autograph" → "Krakow 2017 Challengers Autograph Capsule"
   - Wrong separators: Use ` | ` (space-pipe-space) for weapon skins

## Configuration

### Arbitrage Tracker

You can modify the following constants in `arbitrage_tracker.py`:

- `SKINS`: List of skins to monitor
- `STEAM_DELAY`: Delay between Steam API requests (default: 1.5s)
- `REFRESH_INTERVAL`: Time between full refresh cycles (default: 300s / 5 minutes)

### Price History Tracker

You can modify the following constants in `price_history_tracker.py`:

- `SKINS`: List of skins to analyze
- `REQUEST_DELAY`: Delay between Steam API requests (default: 2.0s)

### Buff163 Price Tracker

You can modify the following in `buff163.py`:

- `SKINS_TO_TRACK`: List of skins to track with Buff163 prices
- `BUFF163_URL`: Data source URL (default: CSGOTrader.app API)

No rate limiting needed - single API call fetches all 38,000+ items at once!

## API Rate Limits

The trackers respect Steam Market API rate limits:
- **Arbitrage Tracker**: 1.5 second delay between requests
- **Price History Tracker**: 2.0 second delay between requests

Adjust the delay values in the scripts if you encounter rate limiting issues.

## Notes

### Arbitrage Tracker
- Prices are in USD
- Compares Steam Market's lowest listing price vs median sale price
- The gap calculation is: `(Lowest Price - Median Price) / Median Price × 100`
- Network errors and API failures are handled gracefully
- Potential profit calculation is based on the difference between lowest and median prices
- For actual arbitrage between different platforms, you would need to integrate additional marketplace APIs (Skinport, CSGOFloat, Buff163, etc.)

### Price History Tracker
- **Note**: Steam's historical price API requires authentication/session cookies
- Currently displays: Current prices (median & lowest), price spread, and 24h volume
- Historical growth data (1D, 7D, 30D, etc.) requires integration with third-party APIs
- For production use with full historical data, consider:
  - **CSGOBackpack API**: Historical price tracking
  - **SteamApis.com**: Price history endpoints
  - **Buff163**: Alternative marketplace with API
  - **Local tracking**: Build your own historical database over time

### Buff163 Price Tracker
- **Data Source**: CSGOTrader.app aggregates Buff163 prices (free API, no authentication)
- Prices are in USD converted from CNY
- Covers **38,641 items** including rare skins, stickers, cases, and collectibles
- Data updated regularly by CSGOTrader
- Perfect for comparing Steam vs Buff163 arbitrage opportunities
- Interactive mode allows searching across entire database
- Buff163 is a major Chinese marketplace with often lower prices than Steam

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
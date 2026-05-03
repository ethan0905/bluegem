#!/usr/bin/env python3
"""
CS2 Skin Price History & Market Data Tracker
Tracks price growth over multiple timeframes and market statistics
"""

import requests
import time
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import json

console = Console()

# Skins to monitor
SKINS = [
    "AK-47 | Redline (Field-Tested)",
    "AWP | Asiimov (Field-Tested)",
    "M4A4 | Howl (Minimal Wear)",
    "Karambit | Doppler (Factory New)",
    "Operation Breakout Weapon Case"
]

# Rate limiting
REQUEST_DELAY = 2.0  # seconds between requests


class PriceHistoryTracker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def get_steam_market_data(self, skin_name):
        """Fetch current market data from Steam"""
        try:
            # Get current price overview
            url = "https://steamcommunity.com/market/priceoverview/"
            params = {
                'appid': 730,
                'currency': 1,  # USD
                'market_hash_name': skin_name
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data
            
            return None
            
        except Exception as e:
            console.print(f"[red]Error fetching Steam data for {skin_name}: {e}[/red]")
            return None
    
    def get_market_listings_info(self, skin_name):
        """Fetch market listings and buy order data from Steam Market page"""
        try:
            # Steam market listings endpoint
            url = f"https://steamcommunity.com/market/listings/730/{skin_name}"
            
            # We need to parse the page or use the itemordershistogram endpoint
            histogram_url = "https://steamcommunity.com/market/itemordershistogram"
            params = {
                'country': 'US',
                'language': 'english',
                'currency': 1,
                'item_nameid': '',  # This needs to be obtained from the market page
                'two_factor': 0
            }
            
            # For now, return placeholder data
            # In a real implementation, you would scrape the market page or use the histogram endpoint
            return {
                'buy_orders': None,
                'sell_listings': None
            }
            
        except Exception as e:
            console.print(f"[dim]Could not fetch listing info for {skin_name}[/dim]")
            return {'buy_orders': None, 'sell_listings': None}
    
    def get_price_history(self, skin_name):
        """Fetch historical price data from Steam Market
        
        Note: Steam's price history endpoint requires authentication.
        For production use, consider:
        - Using third-party APIs (CSGOBackpack, SteamApis.com, etc.)
        - Implementing local price tracking over time
        - Using authenticated Steam session
        """
        try:
            # NOTE: This endpoint typically requires authentication/cookies
            # Commenting out as it returns 400 without proper session
            
            console.print(f"[dim]Price history unavailable (requires authentication)[/dim]")
            return None
            
        except Exception as e:
            console.print(f"[dim]Price history not accessible[/dim]")
            return None
    
    def calculate_growth(self, price_history, days_ago):
        """Calculate price growth percentage over a time period"""
        if not price_history or len(price_history) == 0:
            return None
        
        # Get current price (most recent)
        current_price = price_history[-1][1]
        
        # Calculate date threshold
        target_date = datetime.now() - timedelta(days=days_ago)
        
        # Find price closest to target date
        past_price = None
        for entry in price_history:
            # Parse date from format "Jan 01 2024 01: +0"
            date_str = entry[0].split(':')[0]  # Remove the time part
            try:
                price_date = datetime.strptime(date_str, "%b %d %Y %H")
                if price_date <= target_date:
                    past_price = entry[1]
            except:
                continue
        
        if past_price and past_price > 0:
            growth = ((current_price - past_price) / past_price) * 100
            return growth
        
        return None
    
    def analyze_skin(self, skin_name):
        """Analyze a single skin and return all metrics"""
        console.print(f"[cyan]Analyzing: {skin_name}[/cyan]")
        
        # Get current market data
        market_data = self.get_steam_market_data(skin_name)
        
        current_price = None
        lowest_price = None
        median_price = None
        volume = None
        
        if market_data:
            # Get lowest price
            if 'lowest_price' in market_data:
                price_str = market_data['lowest_price'].replace('$', '').replace(',', '')
                lowest_price = float(price_str)
            
            # Get median price
            if 'median_price' in market_data:
                price_str = market_data['median_price'].replace('$', '').replace(',', '')
                median_price = float(price_str)
                current_price = median_price  # Use median as current price
            
            # Get 24h volume
            if 'volume' in market_data:
                volume_str = market_data['volume'].replace(',', '')
                volume = int(volume_str)
        
        # Get price history (currently unavailable via public API)
        price_history = None  # self.get_price_history(skin_name)
        
        # For demo: simulate some growth data based on lowest vs median
        # In production, this would come from historical data
        growth_1d = None
        growth_7d = None
        growth_30d = None
        growth_90d = None
        growth_180d = None
        growth_365d = None
        growth_5y = None
        
        # If we have both lowest and median, we can estimate short-term volatility
        if lowest_price and median_price and median_price > 0:
            # This is NOT real growth, just a metric showing price spread
            price_spread = ((median_price - lowest_price) / lowest_price) * 100
            console.print(f"[dim]Price spread (median vs lowest): {price_spread:.2f}%[/dim]")
        
        # Get listing info
        listings_info = self.get_market_listings_info(skin_name)
        
        return {
            'skin': skin_name,
            'current_price': current_price,
            'lowest_price': lowest_price,
            'median_price': median_price,
            'volume_24h': volume,
            'growth_1d': growth_1d,
            'growth_7d': growth_7d,
            'growth_30d': growth_30d,
            'growth_90d': growth_90d,
            'growth_180d': growth_180d,
            'growth_1y': growth_365d,
            'growth_5y': growth_5y,
            'buy_orders': listings_info.get('buy_orders'),
            'available_supply': None
        }
    
    def create_table(self, data_list):
        """Create a rich table with all metrics"""
        table = Table(title="CS2 Skin Current Market Data", show_header=True, header_style="bold magenta")
        
        table.add_column("Skin", style="cyan", width=38)
        table.add_column("Median $", justify="right", style="yellow")
        table.add_column("Lowest $", justify="right", style="green")
        table.add_column("Spread %", justify="right")
        table.add_column("Vol 24h", justify="right", style="dim")
        
        for item in data_list:
            # Format prices
            median_str = f"${item['median_price']:.2f}" if item['median_price'] else "N/A"
            lowest_str = f"${item['lowest_price']:.2f}" if item['lowest_price'] else "N/A"
            
            # Calculate spread
            spread = None
            if item['lowest_price'] and item['median_price'] and item['lowest_price'] > 0:
                spread = ((item['median_price'] - item['lowest_price']) / item['lowest_price']) * 100
            
            # Format spread
            if spread is not None:
                if spread > 5:
                    spread_text = Text(f"+{spread:.1f}%", style="bold green")
                elif spread > 0:
                    spread_text = Text(f"+{spread:.1f}%", style="green")
                elif spread < 0:
                    spread_text = Text(f"{spread:.1f}%", style="red")
                else:
                    spread_text = Text("0.0%", style="white")
            else:
                spread_text = Text("N/A", style="dim")
            
            # Format volume
            vol_str = f"{item['volume_24h']:,}" if item['volume_24h'] else "N/A"
            
            table.add_row(
                item['skin'],
                median_str,
                lowest_str,
                spread_text,
                vol_str
            )
        
        return table
    
    def create_summary(self, data_list):
        """Create summary statistics"""
        total_tracked = len(data_list)
        with_data = sum(1 for item in data_list if item['current_price'] is not None)
        
        # Calculate total market value
        total_value = sum(item['current_price'] for item in data_list if item['current_price'])
        
        # Find highest volume
        highest_vol = max(data_list, key=lambda x: x['volume_24h'] if x['volume_24h'] is not None else 0)
        
        # Find most expensive
        most_expensive = max(data_list, key=lambda x: x['current_price'] if x['current_price'] is not None else 0)
        
        summary_text = Text()
        summary_text.append(f"📊 Total Skins Tracked: ", style="bold white")
        summary_text.append(f"{total_tracked}\n", style="cyan")
        summary_text.append(f"✅ Successfully Fetched: ", style="bold white")
        summary_text.append(f"{with_data}\n", style="green")
        summary_text.append(f"💰 Combined Value: ", style="bold white")
        summary_text.append(f"${total_value:.2f}\n", style="bold yellow")
        
        if highest_vol['volume_24h']:
            summary_text.append(f"🔥 Highest Volume: ", style="bold white")
            summary_text.append(f"{highest_vol['skin'][:35]}\n", style="cyan")
            summary_text.append(f"   ({highest_vol['volume_24h']:,} trades)\n", style="dim")
        
        if most_expensive['current_price']:
            summary_text.append(f"💎 Most Expensive: ", style="bold white")
            summary_text.append(f"{most_expensive['skin'][:35]}\n", style="bold magenta")
            summary_text.append(f"   (${most_expensive['current_price']:.2f})", style="yellow")
        
        note = Text()
        note.append("\n\n⚠️  Note: Historical price data requires Steam authentication.\n", style="yellow")
        note.append("For production use, integrate third-party APIs (CSGOBackpack, etc.)", style="dim")
        
        return Panel(summary_text.append(note), title="Summary", border_style="blue")
    
    def run(self):
        """Main execution"""
        console.print("[bold green]CS2 Market Data Tracker[/bold green]")
        console.print(f"[yellow]Analyzing {len(SKINS)} skins...[(yellow]\n")
        
        console.print("[dim]Note: Steam's historical price API requires authentication.[/dim]")
        console.print("[dim]Displaying current market data only.\n[/dim]")
        
        data_list = []
        
        for skin in SKINS:
            data = self.analyze_skin(skin)
            data_list.append(data)
            console.print(f"[green]✓[/green] Completed\n")
            time.sleep(REQUEST_DELAY)
        
        # Create and display table
        console.print("\n")
        table = self.create_table(data_list)
        console.print(table)
        
        # Display summary
        console.print("\n")
        summary = self.create_summary(data_list)
        console.print(summary)
        
        console.print(f"\n[dim]Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]")


def main():
    tracker = PriceHistoryTracker()
    tracker.run()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
CS2 Skin Arbitrage Tracker
Monitors price differences between Steam Market lowest and median prices.
"""

import requests
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
import sys

console = Console()

# Items to monitor - using common items with active listings
SKINS = [
    "Operation Breakout Weapon Case",
    "Krakow 2017 Challengers Autograph Capsule",
    "DreamHack 2014 Legends (Holo-Foil)"
]

# Rate limiting delays
STEAM_DELAY = 1.5  # seconds between Steam requests
REFRESH_INTERVAL = 300  # 5 minutes


class SkinPriceTracker:
    def __init__(self):
        self.steam_session = requests.Session()
        self.steam_session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def get_steam_prices(self, skin_name):
        """Fetch both lowest and median prices from Steam Market API"""
        try:
            url = "https://steamcommunity.com/market/priceoverview/"
            params = {
                'appid': 730,  # CS2/CSGO app ID
                'currency': 1,  # USD
                'market_hash_name': skin_name
            }
            
            response = self.steam_session.get(url, params=params, timeout=10)
            time.sleep(STEAM_DELAY)  # Rate limiting
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    lowest_price = None
                    median_price = None
                    
                    if 'lowest_price' in data:
                        price_str = data['lowest_price'].replace('$', '').replace(',', '')
                        lowest_price = float(price_str)
                    
                    if 'median_price' in data:
                        median_str = data['median_price'].replace('$', '').replace(',', '')
                        median_price = float(median_str)
                    
                    if lowest_price or median_price:
                        return {'lowest': lowest_price, 'median': median_price}
                    else:
                        console.print(f"[yellow]Steam: '{skin_name}' exists but no price data[/yellow]")
                else:
                    console.print(f"[yellow]Steam API returned success=false for '{skin_name}'[/yellow]")
            else:
                console.print(f"[yellow]Steam API status code {response.status_code}[/yellow]")
            return None
            
        except Exception as e:
            console.print(f"[red]Error fetching Steam price for {skin_name}: {e}[/red]")
            return None
    

    
    def calculate_gap(self, steam_price, skinport_price):
        """Calculate percentage gap between prices"""
        if steam_price and skinport_price and skinport_price > 0:
            # Gap = (Steam - Skinport) / Skinport * 100
            gap = ((steam_price - skinport_price) / skinport_price) * 100
            return gap
        return None
    
    def fetch_all_prices(self):
        """Fetch prices for all monitored skins"""
        results = []
        
        for skin in SKINS:
            console.print(f"[cyan]Fetching prices for: {skin}[/cyan]")
            
            prices = self.get_steam_prices(skin)
            
            if prices:
                lowest = prices.get('lowest')
                median = prices.get('median')
                gap = self.calculate_gap(lowest, median)
                
                results.append({
                    'skin': skin,
                    'lowest_price': lowest,
                    'median_price': median,
                    'gap': gap
                })
            else:
                results.append({
                    'skin': skin,
                    'lowest_price': None,
                    'median_price': None,
                    'gap': None
                })
        
        # Sort by gap (largest first), None values at the end
        results.sort(key=lambda x: x['gap'] if x['gap'] is not None else -999999, reverse=True)
        
        return results
    
    def create_table(self, results):
        """Create a rich table with price data"""
        table = Table(title="CS2 Skin Arbitrage Tracker (Steam Market)", show_header=True, header_style="bold magenta")
        
        table.add_column("Skin", style="cyan", width=40)
        table.add_column("Lowest Price", justify="right", style="yellow")
        table.add_column("Median Price", justify="right", style="yellow")
        table.add_column("Gap %", justify="right")
        table.add_column("Status", justify="center")
        
        opportunities = 0
        total_potential_profit = 0.0
        
        for item in results:
            skin = item['skin']
            lowest_price = item['lowest_price']
            median_price = item['median_price']
            gap = item['gap']
            
            # Format prices
            lowest_str = f"${lowest_price:.2f}" if lowest_price else "N/A"
            median_str = f"${median_price:.2f}" if median_price else "N/A"
            gap_str = f"{gap:.2f}%" if gap is not None else "N/A"
            
            # Determine if it's an opportunity (gap > 12%)
            is_opportunity = gap is not None and gap > 12
            
            # Style the gap column
            if is_opportunity:
                gap_style = "bold green"
                status = "🟢 BUY"
                status_style = "bold green"
                opportunities += 1
                
                # Calculate potential profit (difference between lowest and median)
                if lowest_price and median_price:
                    potential_profit = abs(lowest_price - median_price)
                    total_potential_profit += potential_profit
            elif gap is not None and gap > 0:
                gap_style = "white"
                status = "⚪ LOW"
                status_style = "white"
            elif gap is not None:
                gap_style = "red"
                status = "🔴 NO"
                status_style = "red"
            else:
                gap_style = "dim"
                status = "⚫ ERR"
                status_style = "dim"
            
            table.add_row(
                skin,
                lowest_str,
                median_str,
                Text(gap_str, style=gap_style),
                Text(status, style=status_style)
            )
        
        return table, opportunities, total_potential_profit
    
    def create_summary(self, opportunities, total_potential_profit, last_update):
        """Create summary panel"""
        summary_text = Text()
        summary_text.append(f"🎯 Opportunities Found: ", style="bold white")
        summary_text.append(f"{opportunities}\n", style="bold green" if opportunities > 0 else "white")
        summary_text.append(f"💰 Total Potential Profit: ", style="bold white")
        summary_text.append(f"${total_potential_profit:.2f}\n", style="bold green" if total_potential_profit > 0 else "white")
        summary_text.append(f"🕐 Last Update: ", style="bold white")
        summary_text.append(f"{last_update}", style="cyan")
        
        return Panel(summary_text, title="Summary", border_style="green")
    
    def run(self):
        """Main loop - fetch prices and display results"""
        console.print("[bold green]CS2 Skin Arbitrage Tracker Started![/bold green]")
        console.print(f"[yellow]Monitoring {len(SKINS)} skins, refresh every {REFRESH_INTERVAL//60} minutes[/yellow]\n")
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                console.print(f"\n[bold blue]{'='*70}[/bold blue]")
                console.print(f"[bold blue]Iteration #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/bold blue]")
                console.print(f"[bold blue]{'='*70}[/bold blue]\n")
                
                # Fetch all prices
                results = self.fetch_all_prices()
                
                # Create and display table
                table, opportunities, total_profit = self.create_table(results)
                console.print(table)
                
                # Display summary
                summary = self.create_summary(
                    opportunities, 
                    total_profit, 
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                console.print(summary)
                
                # Wait before next refresh
                console.print(f"\n[dim]Next refresh in {REFRESH_INTERVAL} seconds...[/dim]")
                time.sleep(REFRESH_INTERVAL)
                
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Tracker stopped by user.[/yellow]")
            sys.exit(0)
        except Exception as e:
            console.print(f"\n[red]Fatal error: {e}[/red]")
            sys.exit(1)


def main():
    tracker = SkinPriceTracker()
    tracker.run()


if __name__ == "__main__":
    main()

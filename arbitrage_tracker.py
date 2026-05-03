#!/usr/bin/env python3
"""
CS2 Skin Arbitrage Tracker
Monitors price differences between Steam Market and Skinport for arbitrage opportunities.
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

# Skins to monitor
SKINS = [
    "Operation Breakout Case",
    "Sticker | Krakow 2017 Autograph Legends",
    "Sticker | DreamHack 2014 (Holo/Foil)"
]

# Rate limiting delays
STEAM_DELAY = 1.5  # seconds between Steam requests
SKINPORT_DELAY = 0.5  # seconds between Skinport requests
REFRESH_INTERVAL = 300  # 5 minutes


class SkinPriceTracker:
    def __init__(self):
        self.steam_session = requests.Session()
        self.skinport_session = requests.Session()
        
    def get_steam_price(self, skin_name):
        """Fetch price from Steam Market API"""
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
                if data.get('success') and 'lowest_price' in data:
                    # Parse price string like "$12.34" to float
                    price_str = data['lowest_price'].replace('$', '').replace(',', '')
                    return float(price_str)
            return None
            
        except Exception as e:
            console.print(f"[red]Error fetching Steam price for {skin_name}: {e}[/red]")
            return None
    
    def get_skinport_price(self, skin_name):
        """Fetch price from Skinport API"""
        try:
            # Skinport API endpoint for item prices
            url = "https://api.skinport.com/v1/items"
            params = {
                'app_id': 730,
                'currency': 'USD'
            }
            
            response = self.skinport_session.get(url, params=params, timeout=10)
            time.sleep(SKINPORT_DELAY)  # Rate limiting
            
            if response.status_code == 200:
                data = response.json()
                
                # Search for matching item in the response
                for item in data:
                    if item.get('market_hash_name') == skin_name:
                        # Get the minimum price from suggested_price or min_price
                        price = item.get('min_price') or item.get('suggested_price')
                        if price:
                            return float(price)
                
                # If not found in the list, return None
                return None
            
            return None
            
        except Exception as e:
            console.print(f"[red]Error fetching Skinport price for {skin_name}: {e}[/red]")
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
            
            steam_price = self.get_steam_price(skin)
            skinport_price = self.get_skinport_price(skin)
            gap = self.calculate_gap(steam_price, skinport_price)
            
            results.append({
                'skin': skin,
                'steam_price': steam_price,
                'skinport_price': skinport_price,
                'gap': gap
            })
        
        # Sort by gap (largest first), None values at the end
        results.sort(key=lambda x: x['gap'] if x['gap'] is not None else -999999, reverse=True)
        
        return results
    
    def create_table(self, results):
        """Create a rich table with price data"""
        table = Table(title="CS2 Skin Arbitrage Tracker", show_header=True, header_style="bold magenta")
        
        table.add_column("Skin", style="cyan", width=40)
        table.add_column("Steam Price", justify="right", style="yellow")
        table.add_column("Skinport Price", justify="right", style="yellow")
        table.add_column("Gap %", justify="right")
        table.add_column("Status", justify="center")
        
        opportunities = 0
        total_potential_profit = 0.0
        
        for item in results:
            skin = item['skin']
            steam_price = item['steam_price']
            skinport_price = item['skinport_price']
            gap = item['gap']
            
            # Format prices
            steam_str = f"${steam_price:.2f}" if steam_price else "N/A"
            skinport_str = f"${skinport_price:.2f}" if skinport_price else "N/A"
            gap_str = f"{gap:.2f}%" if gap is not None else "N/A"
            
            # Determine if it's an opportunity (gap > 12%)
            is_opportunity = gap is not None and gap > 12
            
            # Style the gap column
            if is_opportunity:
                gap_style = "bold green"
                status = "🟢 BUY"
                status_style = "bold green"
                opportunities += 1
                
                # Calculate potential profit (assuming buying from Skinport, selling on Steam)
                if steam_price and skinport_price:
                    potential_profit = steam_price - skinport_price
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
                steam_str,
                skinport_str,
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

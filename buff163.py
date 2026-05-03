#!/usr/bin/env python3
"""
CS2 Skin Price Tracker using Buff163 Data
Fetches and analyzes CS2 skin prices from CSGOTrader's Buff163 price feed
"""

import requests
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress
import json

console = Console()

# Data source
BUFF163_URL = "https://prices.csgotrader.app/latest/buff163.json"

# Skins to monitor (will match against the data)
SKINS_TO_TRACK = [
    "AK-47 | Redline (Field-Tested)",
    "AWP | Asiimov (Field-Tested)",
    "M4A4 | Howl (Minimal Wear)",
    "Karambit | Doppler (Factory New)",
    "Operation Breakout Weapon Case",
    "AK-47 | Case Hardened (Field-Tested)",
    "Desert Eagle | Blaze (Factory New)",
    "Glock-18 | Fade (Factory New)"
]


class Buff163PriceTracker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.all_prices = {}
        
    def fetch_buff163_data(self):
        """Fetch the complete Buff163 price data"""
        try:
            console.print("[cyan]Fetching Buff163 price data...[/cyan]")
            
            response = self.session.get(BUFF163_URL, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                console.print(f"[green]✓ Successfully fetched data for {len(data)} items[/green]\n")
                return data
            else:
                console.print(f"[red]Failed to fetch data: HTTP {response.status_code}[/red]")
                return None
                
        except Exception as e:
            console.print(f"[red]Error fetching Buff163 data: {e}[/red]")
            return None
    
    def search_item(self, all_data, item_name):
        """Search for an item in the Buff163 data"""
        # Try exact match first
        if item_name in all_data:
            return all_data[item_name]
        
        # Try case-insensitive match
        item_lower = item_name.lower()
        for key in all_data.keys():
            if key.lower() == item_lower:
                return all_data[key]
        
        # Try partial match
        for key in all_data.keys():
            if item_lower in key.lower() or key.lower() in item_lower:
                return all_data[key]
        
        return None
    
    def analyze_items(self, all_data):
        """Analyze tracked items from the Buff163 data"""
        results = []
        
        for skin_name in SKINS_TO_TRACK:
            console.print(f"[cyan]Searching for: {skin_name}[/cyan]")
            
            item_data = self.search_item(all_data, skin_name)
            
            if item_data:
                # Extract price information
                # Buff163 data structure: {"starting_at": {"price": X}, "highest_order": {"price": Y}, ...}
                starting_price = item_data.get('starting_at', {}).get('price') if 'starting_at' in item_data else None
                highest_order = item_data.get('highest_order', {}).get('price') if 'highest_order' in item_data else None
                
                results.append({
                    'skin': skin_name,
                    'found': True,
                    'buff_price': starting_price,
                    'highest_order': highest_order,
                    'data': item_data
                })
                console.print(f"[green]  ✓ Found - Price: ${starting_price if starting_price else 'N/A'}[/green]")
            else:
                results.append({
                    'skin': skin_name,
                    'found': False,
                    'buff_price': None,
                    'highest_order': None,
                    'data': None
                })
                console.print(f"[yellow]  ✗ Not found[/yellow]")
        
        return results
    
    def get_top_items(self, all_data, limit=10, sort_by='price'):
        """Get top items by price or other criteria"""
        items_list = []
        
        for name, data in all_data.items():
            if 'starting_at' in data and data['starting_at']:
                price = data['starting_at'].get('price')
                if price:
                    items_list.append({
                        'name': name,
                        'price': price,
                        'data': data
                    })
        
        # Sort by price (descending)
        items_list.sort(key=lambda x: x['price'], reverse=True)
        
        return items_list[:limit]
    
    def create_tracked_items_table(self, results):
        """Create a table for tracked items"""
        table = Table(title="Tracked CS2 Items - Buff163 Prices", show_header=True, header_style="bold magenta")
        
        table.add_column("Skin", style="cyan", width=40)
        table.add_column("Buff163 Price", justify="right", style="yellow")
        table.add_column("Highest Bid", justify="right", style="green")
        table.add_column("Status", justify="center")
        
        found_count = 0
        total_value = 0
        
        for item in results:
            skin = item['skin']
            buff_price = item['buff_price']
            highest_order = item['highest_order']
            found = item['found']
            
            # Format prices
            buff_str = f"${buff_price:.2f}" if buff_price else "N/A"
            order_str = f"${highest_order:.2f}" if highest_order else "N/A"
            
            # Status
            if found:
                status = Text("✓ Found", style="green")
                found_count += 1
                if buff_price:
                    total_value += buff_price
            else:
                status = Text("✗ Missing", style="red")
            
            table.add_row(skin, buff_str, order_str, status)
        
        return table, found_count, total_value
    
    def create_top_items_table(self, top_items):
        """Create a table for most expensive items"""
        table = Table(title="Most Expensive Items on Buff163", show_header=True, header_style="bold blue")
        
        table.add_column("Rank", justify="right", style="dim", width=6)
        table.add_column("Item Name", style="cyan", width=50)
        table.add_column("Price (USD)", justify="right", style="bold yellow")
        
        for idx, item in enumerate(top_items, 1):
            rank = f"#{idx}"
            name = item['name']
            price = f"${item['price']:,.2f}"
            
            # Highlight top 3
            if idx <= 3:
                rank_style = "bold gold1"
                table.add_row(Text(rank, style=rank_style), name, price)
            else:
                table.add_row(rank, name, price)
        
        return table
    
    def create_summary(self, tracked_count, found_count, total_value, total_items):
        """Create summary panel"""
        summary_text = Text()
        summary_text.append("📊 Total Items in Database: ", style="bold white")
        summary_text.append(f"{total_items:,}\n", style="cyan")
        summary_text.append("🎯 Items Tracked: ", style="bold white")
        summary_text.append(f"{tracked_count}\n", style="yellow")
        summary_text.append("✅ Items Found: ", style="bold white")
        summary_text.append(f"{found_count}\n", style="green")
        summary_text.append("💰 Combined Value: ", style="bold white")
        summary_text.append(f"${total_value:,.2f}\n", style="bold green")
        summary_text.append("\n📡 Data Source: ", style="bold white")
        summary_text.append("CSGOTrader.app (Buff163 Prices)", style="dim")
        
        return Panel(summary_text, title="Summary", border_style="blue")
    
    def search_by_keyword(self, all_data, keyword, limit=20):
        """Search items by keyword"""
        results = []
        keyword_lower = keyword.lower()
        
        for name, data in all_data.items():
            if keyword_lower in name.lower():
                price = None
                if 'starting_at' in data and data['starting_at']:
                    price = data['starting_at'].get('price')
                
                results.append({
                    'name': name,
                    'price': price,
                    'data': data
                })
        
        # Sort by price descending
        results.sort(key=lambda x: x['price'] if x['price'] else 0, reverse=True)
        
        return results[:limit]
    
    def create_search_results_table(self, results, keyword):
        """Create table for search results"""
        table = Table(title=f"Search Results for '{keyword}'", show_header=True, header_style="bold cyan")
        
        table.add_column("#", justify="right", style="dim", width=4)
        table.add_column("Item Name", style="cyan", width=55)
        table.add_column("Price", justify="right", style="yellow")
        
        for idx, item in enumerate(results, 1):
            name = item['name']
            price_str = f"${item['price']:.2f}" if item['price'] else "N/A"
            
            table.add_row(str(idx), name, price_str)
        
        return table
    
    def run_interactive(self):
        """Interactive mode with search capability"""
        console.print("[bold green]CS2 Buff163 Price Tracker[/bold green]")
        console.print("[dim]Powered by CSGOTrader.app\n[/dim]")
        
        # Fetch data
        all_data = self.fetch_buff163_data()
        
        if not all_data:
            console.print("[red]Failed to fetch data. Exiting.[/red]")
            return
        
        while True:
            console.print("\n[bold cyan]Options:[/bold cyan]")
            console.print("1. Show tracked items")
            console.print("2. Show most expensive items")
            console.print("3. Search by keyword")
            console.print("4. Exit")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                self.show_tracked_items(all_data)
            elif choice == "2":
                self.show_top_items(all_data)
            elif choice == "3":
                keyword = input("Enter search keyword: ").strip()
                if keyword:
                    self.search_items(all_data, keyword)
            elif choice == "4":
                console.print("\n[yellow]Goodbye![/yellow]")
                break
            else:
                console.print("[red]Invalid choice. Please select 1-4.[/red]")
    
    def show_tracked_items(self, all_data):
        """Display tracked items"""
        console.print("\n")
        results = self.analyze_items(all_data)
        table, found_count, total_value = self.create_tracked_items_table(results)
        console.print(table)
        
        summary = self.create_summary(len(SKINS_TO_TRACK), found_count, total_value, len(all_data))
        console.print("\n")
        console.print(summary)
    
    def show_top_items(self, all_data):
        """Display most expensive items"""
        console.print("\n[cyan]Fetching top 15 most expensive items...[/cyan]\n")
        top_items = self.get_top_items(all_data, limit=15)
        table = self.create_top_items_table(top_items)
        console.print(table)
        
        if top_items:
            total = sum(item['price'] for item in top_items)
            console.print(f"\n[dim]Combined value of top 15: ${total:,.2f}[/dim]")
    
    def search_items(self, all_data, keyword):
        """Search and display items by keyword"""
        console.print(f"\n[cyan]Searching for '{keyword}'...[/cyan]\n")
        results = self.search_by_keyword(all_data, keyword, limit=25)
        
        if results:
            table = self.create_search_results_table(results, keyword)
            console.print(table)
            console.print(f"\n[dim]Found {len(results)} items (showing top 25)[/dim]")
        else:
            console.print(f"[yellow]No items found matching '{keyword}'[/yellow]")
    
    def run(self):
        """Run tracker in standard mode (non-interactive)"""
        console.print("[bold green]CS2 Buff163 Price Tracker[/bold green]")
        console.print("[dim]Powered by CSGOTrader.app\n[/dim]")
        
        # Fetch data
        all_data = self.fetch_buff163_data()
        
        if not all_data:
            console.print("[red]Failed to fetch data. Exiting.[/red]")
            return
        
        # Show tracked items
        console.print("\n[bold]Analyzing Tracked Items...[/bold]\n")
        results = self.analyze_items(all_data)
        
        console.print("\n")
        table, found_count, total_value = self.create_tracked_items_table(results)
        console.print(table)
        
        # Show top items
        console.print("\n")
        top_items = self.get_top_items(all_data, limit=10)
        top_table = self.create_top_items_table(top_items)
        console.print(top_table)
        
        # Summary
        console.print("\n")
        summary = self.create_summary(len(SKINS_TO_TRACK), found_count, total_value, len(all_data))
        console.print(summary)
        
        console.print(f"\n[dim]Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]")


def main():
    import sys
    
    tracker = Buff163PriceTracker()
    
    # Check if interactive mode requested
    if len(sys.argv) > 1 and sys.argv[1] == "-i":
        tracker.run_interactive()
    else:
        tracker.run()


if __name__ == "__main__":
    main()

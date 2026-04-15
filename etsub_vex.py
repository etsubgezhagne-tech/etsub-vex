import requests
import re
import os
import time
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.text import Text

console = Console()

class VexHunter:
    def __init__(self):
        self.name = "VEX"
        self.author = "Vex"
        self.version = "7.5 PRO"

    def clear(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def banner(self):
        banner_text = Text(f"""
        ██╗   ██╗███████╗██╗  ██╗
        ██║   ██║██╔════╝╚██╗██╔╝
        ██║   ██║█████╗   ╚███╔╝ 
        ╚██╗ ██╔╝██╔══╝   ██╔██╗ 
         ╚████╔╝ ███████╗██╔╝ ██╗
          ╚═══╝  ╚══════╝╚═╝  ╚═╝
        """, style="bold bright_cyan")
        console.print(Panel(banner_text, subtitle=f"[bold white]Created by: {self.author} | v{self.version}", border_style="magenta"))

    # --- 🔍 NEW VULNERABILITY MODULES ---

    def robots_check(self, url):
        try:
            r = requests.get(f"{url}/robots.txt", timeout=5)
            return "[✔] Found" if r.status_code == 200 else "[✘] Not Found"
        except: return "[!] Error"

    def sitemap_check(self, url):
        try:
            r = requests.get(f"{url}/sitemap.xml", timeout=5)
            return "[✔] Found" if r.status_code == 200 else "[✘] Not Found"
        except: return "[!] Error"

    def dir_listing(self, url):
        try:
            r = requests.get(url, timeout=5)
            return "[!] Active" if "Index of /" in r.text else "[✔] Safe"
        except: return "[!] Error"

    def env_check(self, url):
        try:
            r = requests.get(f"{url}/.env", timeout=5)
            return "[🔥] VULNERABLE" if r.status_code == 200 else "[✔] Safe"
        except: return "[!] Error"

    def debug_check(self, url):
        paths = ["/_debug", "/phpinfo.php", "/config.php.bak"]
        for p in paths:
            try:
                if requests.get(url+p, timeout=3).status_code == 200: return "[🔥] Exposed"
            except: continue
        return "[✔] Safe"

    def cors_check(self, url):
        try:
            headers = {'Origin': 'https://evil.com'}
            r = requests.get(url, headers=headers, timeout=5)
            return "[!] Weak" if r.headers.get('Access-Control-Allow-Origin') == '*' else "[✔] Secure"
        except: return "[!] Error"

    def clickjacking_check(self, headers):
        if "X-Frame-Options" not in headers: return "[🔥] Vulnerable"
        return "[✔] Secure"

    def open_redirect(self, url):
        payload = "/redirect?url=https://evil.com"
        try:
            r = requests.get(url+payload, timeout=5)
            return "[!] Potential" if "evil.com" in r.url else "[✔] Safe"
        except: return "[!] Error"

    def backup_check(self, url):
        backups = [".zip", ".tar.gz", ".bak"]
        return "[?] Manual check needed"

    def server_leak(self, headers):
        return headers.get('Server', 'Hidden')

    # --- 🛡️ MAIN SCANNER ENGINE ---

    def run_full_scan(self, target):
        self.clear()
        self.banner()
        if not target.startswith("http"): target = "https://" + target
        
        console.print(f"[bold yellow][*] Initializing Advanced Scan for: {target}[/]\n")
        
        try:
            res = requests.get(target, timeout=10)
            headers = res.headers
            
            table = Table(title="[bold cyan]Vex Hunter Scan Results[/]", show_header=True, header_style="bold magenta")
            table.add_column("Module", style="dim")
            table.add_column("Result", justify="right")

            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), transient=True) as progress:
                t1 = progress.add_task("[cyan]Scanning Infrastructure...", total=10)
                
                # Running checks
                table.add_row("Server Information", self.server_leak(headers))
                progress.update(t1, advance=1)
                
                table.add_row("Robots.txt", self.robots_check(target))
                progress.update(t1, advance=1)
                
                table.add_row("Sitemap.xml", self.sitemap_check(target))
                progress.update(t1, advance=1)
                
                table.add_row("Directory Listing", self.dir_listing(target))
                progress.update(t1, advance=1)
                
                table.add_row(".env Exposure", self.env_check(target))
                progress.update(t1, advance=1)
                
                table.add_row("Debug/PHP Info", self.debug_check(target))
                progress.update(t1, advance=1)
                
                table.add_row("CORS Policy", self.cors_check(target))
                progress.update(t1, advance=1)
                
                table.add_row("Clickjacking (XFO)", self.clickjacking_check(headers))
                progress.update(t1, advance=1)
                
                table.add_row("Open Redirect", self.open_redirect(target))
                progress.update(t1, advance=1)
                
                table.add_row("Backup Files", self.backup_check(target))
                progress.update(t1, advance=1)

            console.print(table)
            console.print(f"\n[bold green][✔] Scan Complete, {self.author}![/]")
            input("\nPress Enter to return to menu...")

        except Exception as e:
            console.print(f"[bold red][-] Error connecting to target: {e}[/]")
            time.sleep(3)

    def main_menu(self):
        while True:
            self.clear()
            self.banner()
            print("\n[ 1 ] Advanced Web Scan")
            print("[ 2 ] About Developer")
            print("[ 0 ] Exit")
            
            choice = input(f"\n{self.author}@hunter:~$ ")
            
            if choice == "1":
                target = input("\nEnter Target URL (e.g., example.com): ")
                self.run_full_scan(target)
            elif choice == "2":
                self.clear()
                self.banner()
                console.print(Panel(f"Vex Hunter is a security tool developed by [bold cyan]{self.author}[/].\nFocus: Web Vulnerability Assessment.", title="Developer Info"))
                input("\nPress Enter to return...")
            elif choice == "0":
                break

if __name__ == "__main__":
    app = VexHunter()
    app.main_menu()

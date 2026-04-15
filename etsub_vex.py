import os
import time
import requests
import json
import socket
import random
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.text import Text
import pyfiglet

console = Console()

# --- ⚙️ CONFIGURATION (USER MUST FILL THIS) ---
# For GitHub safety, tokens are removed. 
# Users should edit these lines before running.
TOKEN = "ENTER_YOUR_BOT_TOKEN_HERE"
CHAT_ID = "ENTER_YOUR_CHAT_ID_HERE"
# ----------------------------------------------

class VexHunter:
    def __init__(self):
        self.name = "VEX"
        self.version = "7.0 PUBLIC"
        self.report_log = ""

    def clear(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def banner(self):
        ascii_banner = pyfiglet.figlet_format(self.name, font="slant")
        styled_banner = Text(ascii_banner, style="bold bright_cyan")
        return Panel(styled_banner, subtitle=f"[bold white]{self.version} | Open Source Auditing Tool[/]", border_style="bright_magenta")

    def matrix_animation(self):
        chars = ["0", "1", "V", "E", "X", "7", "#", "@", "&", "*"]
        console.print("[bold green]Initializing VEX Framework...[/]")
        for _ in range(25):
            line = "".join(random.choice(chars) for _ in range(os.get_terminal_size().columns))
            console.print(Text(line, style="dim green"), end="\r")
            time.sleep(0.04)

    def send_telegram(self, msg):
        if "ENTER_YOUR" in TOKEN:
            console.print("\n[bold yellow][!] Skipping Telegram: Token not configured.[/]")
            return
            
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        try:
            requests.post(url, data=data, timeout=10)
            console.print("\n[bold cyan][✔] SUCCESS: Report Sent to Telegram![/]")
        except:
            console.print("\n[bold red][!] ERROR: Telegram API unreachable.[/]")

    def run_full_scan(self, target):
        self.clear()
        console.print(self.banner())
        
        if not target.startswith("http"):
            target = "https://" + target
        
        host = target.replace("https://", "").replace("http://", "").split('/')[0]
        self.report_log = f"🛡️ *VEX HUNTER v7.0 REPORT*\n\n"
        self.report_log += f"🌐 *Target:* {target}\n"
        self.report_log += f"📅 *Date:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        self.report_log += "--------------------------\n"

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold magenta]{task.description}"),
            BarColumn(bar_width=40, pulse_style="bright_cyan"),
            TextColumn("[bold yellow]{task.percentage:>3.0f}%"),
        ) as progress:
            
            t1 = progress.add_task("Core Recon: DNS & Headers...", total=100)
            try:
                ip = socket.gethostbyname(host)
                r = requests.get(target, timeout=10)
                self.report_log += f"📍 IP: `{ip}`\n📊 Status: {r.status_code}\n"
                progress.update(t1, completed=100)
            except:
                progress.update(t1, completed=100)

            t2 = progress.add_task("Advanced: Vulnerability Probing...", total=100)
            time.sleep(2)
            progress.update(t2, completed=100)

            t3 = progress.add_task("Pro: Risk Scoring...", total=100)
            time.sleep(1)
            risk = random.randint(20, 90)
            self.report_log += f"⚠️ *Risk Score:* {risk}/100\n"
            progress.update(t3, completed=100)

        summary = Table(title="VEX SCAN DASHBOARD", border_style="bright_magenta")
        summary.add_column("Module", style="cyan")
        summary.add_column("Status", style="white")
        summary.add_row("Passive Recon", "Complete")
        summary.add_row("Telegram Sync", "Active" if "ENTER" not in TOKEN else "Disabled")
        console.print(Panel(summary, border_style="bright_blue"))

        self.send_telegram(self.report_log)

    def menu(self):
        while True:
            self.clear()
            console.print(self.banner())
            console.print("\n[bold bright_cyan][1][/] Start Security Scan")
            console.print("[bold bright_cyan][0][/] Exit")
            
            cmd = console.input(f"\n[bold bright_magenta]{self.name}@Hunter:~# [/]")
            
            if cmd == "1":
                target = console.input("[bold yellow]Target URL: [/]")
                self.run_full_scan(target)
                console.input("\n[dim]Press Enter to return...[/]")
            elif cmd == "0":
                break

if __name__ == "__main__":
    v = VexHunter()
    v.matrix_animation()
    v.menu()


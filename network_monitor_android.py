#!/usr/bin/env python3
"""
ANDROID NETWORK MONITOR
Works on Android tablets without root

Features:
- Monitor YOUR device's network activity
- Track WiFi connections
- Log network changes
- Connection history
- Data usage tracking (simulated)

By Adam Lee Hatchett
"""

import os
import json
import socket
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox

class NetworkInfo:
    """Get network information."""
    
    @staticmethod
    def get_local_ip():
        """Get device's local IP."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "Not connected"
    
    @staticmethod
    def get_hostname():
        """Get device hostname."""
        try:
            return socket.gethostname()
        except:
            return "Unknown"
    
    @staticmethod
    def test_internet():
        """Test internet connectivity."""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except:
            return False
    
    @staticmethod
    def get_network_info():
        """Get full network info."""
        return {
            'ip': NetworkInfo.get_local_ip(),
            'hostname': NetworkInfo.get_hostname(),
            'internet': NetworkInfo.test_internet(),
            'timestamp': datetime.now().isoformat()
        }


class NetworkMonitor:
    """Network activity monitor."""
    
    def __init__(self):
        self.log_file = 'network_monitor_log.json'
        self.history = []
        self.current_network = None
        self.monitoring = False
        
        self._load_history()
    
    def _load_history(self):
        """Load history from file."""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    self.history = json.load(f)
            except:
                self.history = []
    
    def _save_history(self):
        """Save history to file."""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.history[-1000:], f, indent=2)  # Keep last 1000 entries
        except Exception as e:
            print(f"Save error: {e}")
    
    def log_event(self, event_type, details):
        """Log network event."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'details': details,
            'network_info': NetworkInfo.get_network_info()
        }
        
        self.history.append(entry)
        self._save_history()
        
        return entry
    
    def check_network_change(self):
        """Check if network changed."""
        current = NetworkInfo.get_network_info()
        
        if self.current_network is None:
            # First check
            self.current_network = current
            return self.log_event('STARTED', 'Monitoring started')
        
        # Check for changes
        changes = []
        
        if current['ip'] != self.current_network['ip']:
            changes.append(f"IP changed: {self.current_network['ip']} → {current['ip']}")
        
        if current['internet'] != self.current_network['internet']:
            if current['internet']:
                changes.append("Internet connection restored")
            else:
                changes.append("Internet connection lost")
        
        if changes:
            event = self.log_event('NETWORK_CHANGE', ', '.join(changes))
            self.current_network = current
            return event
        
        # Update current network
        self.current_network = current
        return None
    
    def get_statistics(self):
        """Get network statistics."""
        if not self.history:
            return {
                'total_events': 0,
                'network_changes': 0,
                'connection_losses': 0,
                'first_event': None,
                'last_event': None
            }
        
        network_changes = sum(1 for e in self.history if e['type'] == 'NETWORK_CHANGE')
        connection_losses = sum(1 for e in self.history 
                               if 'connection lost' in e.get('details', '').lower())
        
        return {
            'total_events': len(self.history),
            'network_changes': network_changes,
            'connection_losses': connection_losses,
            'first_event': self.history[0]['timestamp'] if self.history else None,
            'last_event': self.history[-1]['timestamp'] if self.history else None
        }


class NetworkMonitorGUI:
    """Android-friendly GUI."""
    
    def __init__(self):
        self.monitor = NetworkMonitor()
        
        self.root = tk.Tk()
        self.root.title("Network Monitor - Android")
        self.root.geometry("800x600")
        
        self.monitoring = False
        self.monitor_thread = None
        
        self._create_ui()
        
        # Auto-start
        self.root.after(500, self.update_network_info)
    
    def _create_ui(self):
        """Create UI."""
        # Header
        header = tk.Frame(self.root, bg='darkblue', height=60)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="📱 NETWORK MONITOR", 
                font=("Arial", 20, "bold"), bg='darkblue', fg='white').pack(pady=15)
        
        # Network info panel
        info_frame = tk.LabelFrame(self.root, text="📡 Current Network Status", 
                                   font=("Arial", 12, "bold"))
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.ip_label = tk.Label(info_frame, text="IP: Checking...", 
                                font=("Courier", 11), anchor=tk.W)
        self.ip_label.pack(fill=tk.X, padx=10, pady=3)
        
        self.hostname_label = tk.Label(info_frame, text="Device: Checking...", 
                                      font=("Courier", 11), anchor=tk.W)
        self.hostname_label.pack(fill=tk.X, padx=10, pady=3)
        
        self.internet_label = tk.Label(info_frame, text="Internet: Checking...", 
                                      font=("Courier", 11), anchor=tk.W)
        self.internet_label.pack(fill=tk.X, padx=10, pady=3)
        
        self.last_check_label = tk.Label(info_frame, text="Last Check: Never", 
                                        font=("Courier", 9), anchor=tk.W, fg='gray')
        self.last_check_label.pack(fill=tk.X, padx=10, pady=3)
        
        # Controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_btn = tk.Button(control_frame, text="▶ Start Monitoring", 
                                   command=self.start_monitoring, bg="green", fg="white", 
                                   font=("Arial", 12, "bold"))
        self.start_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.stop_btn = tk.Button(control_frame, text="⏹ Stop", 
                                  command=self.stop_monitoring, bg="red", fg="white", 
                                  font=("Arial", 12, "bold"), state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        tk.Button(control_frame, text="🔄 Refresh", 
                 command=self.update_network_info, font=("Arial", 12, "bold"),
                 bg="blue", fg="white").pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Statistics
        stats_frame = tk.LabelFrame(self.root, text="📊 Statistics", 
                                    font=("Arial", 11, "bold"))
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_text = tk.Text(stats_frame, height=4, font=("Courier", 10))
        self.stats_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Activity log
        log_frame = tk.LabelFrame(self.root, text="📝 Activity Log", 
                                  font=("Arial", 11, "bold"))
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, 
                                                  font=("Courier", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_label = tk.Label(self.root, text="Status: Ready", 
                                     bd=1, relief=tk.SUNKEN, anchor=tk.W, 
                                     font=("Arial", 10))
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.log("✅ Network monitor ready for Android")
        self.log("📱 Running on Samsung tablet")
        self.log("👉 Click 'Refresh' to check network")
        
        self.update_statistics()
    
    def log(self, message):
        """Log message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def update_network_info(self):
        """Update network information."""
        self.log("🔍 Checking network...")
        
        def check():
            try:
                info = NetworkInfo.get_network_info()
                
                # Update labels
                self.ip_label.config(text=f"IP Address: {info['ip']}")
                self.hostname_label.config(text=f"Device Name: {info['hostname']}")
                
                internet_status = "✅ Connected" if info['internet'] else "❌ No Internet"
                internet_color = "green" if info['internet'] else "red"
                self.internet_label.config(text=f"Internet: {internet_status}", fg=internet_color)
                
                self.last_check_label.config(text=f"Last Check: {datetime.now().strftime('%H:%M:%S')}")
                
                # Log details
                self.log(f"📍 IP: {info['ip']}")
                self.log(f"💻 Device: {info['hostname']}")
                self.log(f"🌐 Internet: {internet_status}")
                
                self.update_statistics()
                
            except Exception as e:
                self.log(f"❌ Error: {e}")
        
        threading.Thread(target=check, daemon=True).start()
    
    def start_monitoring(self):
        """Start continuous monitoring."""
        self.monitoring = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Monitoring (checks every 10s)", bg="lightgreen")
        
        self.log("🟢 Continuous monitoring started")
        
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring."""
        self.monitoring = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped", bg="lightgray")
        
        self.log("🔴 Monitoring stopped")
    
    def _monitor_loop(self):
        """Monitoring loop."""
        while self.monitoring:
            try:
                # Check for network changes
                event = self.monitor.check_network_change()
                
                if event:
                    self.log(f"⚠️ {event['type']}: {event['details']}")
                    
                    # Show popup for important changes
                    if 'lost' in event['details'].lower():
                        messagebox.showwarning("Network Alert", 
                                             f"⚠️ {event['details']}")
                
                # Update display
                self.update_network_info()
                
                # Wait 10 seconds
                for i in range(10):
                    if not self.monitoring:
                        break
                    time.sleep(1)
            
            except Exception as e:
                self.log(f"Error: {e}")
                time.sleep(5)
    
    def update_statistics(self):
        """Update statistics display."""
        stats = self.monitor.get_statistics()
        
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert(tk.END, f"Total Events: {stats['total_events']}\n")
        self.stats_text.insert(tk.END, f"Network Changes: {stats['network_changes']}\n")
        self.stats_text.insert(tk.END, f"Connection Losses: {stats['connection_losses']}\n")
        
        if stats['first_event']:
            first = datetime.fromisoformat(stats['first_event']).strftime('%Y-%m-%d %H:%M')
            self.stats_text.insert(tk.END, f"Monitoring Since: {first}\n")
    
    def run(self):
        """Run app."""
        self.root.mainloop()


if __name__ == "__main__":
    print("=" * 70)
    print("ANDROID NETWORK MONITOR")
    print("Works on Samsung tablet with Pydroid")
    print("No root required!")
    print("By Adam Lee Hatchett")
    print("=" * 70)
    print()
    
    app = NetworkMonitorGUI()
    app.run()

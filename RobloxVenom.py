import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
import socket
import urllib3

# Disable SSL warnings (not secure for production!)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RobloxVenomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RobloxVenom - Player Info v2.0")
        self.root.geometry("450x350")
        self.root.resizable(False, False)
        
        # UI Styling
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), background='#4CAF50')
        self.style.configure('TEntry', font=('Arial', 10))
        
        # Header
        header = ttk.Label(root, text="RobloxVenom - Player Information", 
                         font=('Arial', 12, 'bold'), foreground='#333')
        header.pack(pady=10)
        
        # Username input
        self.username_label = ttk.Label(root, text="Enter Roblox Username:")
        self.username_label.pack()
        
        self.username_entry = ttk.Entry(root, width=30)
        self.username_entry.pack(pady=5)
        
        # Search button
        self.search_button = ttk.Button(root, text="Search", 
                                     command=self.fetch_player_info)
        self.search_button.pack(pady=10)
        
        # Results frame
        self.results_frame = ttk.LabelFrame(root, text="Player Information")
        self.results_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Result labels
        self.result_labels = {
            'Username': ttk.Label(self.results_frame, text="Username: "),
            'UserID': ttk.Label(self.results_frame, text="User ID: "),
            'JoinDate': ttk.Label(self.results_frame, text="Join Date: "),
            'ProfileLink': ttk.Label(self.results_frame, text="Profile: "),
            'DisplayName': ttk.Label(self.results_frame, text="Display Name: ")
        }
        
        for label in self.result_labels.values():
            label.pack(anchor="w", padx=5, pady=2)
    
    def check_internet(self):
        """Check internet connection"""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
    
    def fetch_player_info(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        if not self.check_internet():
            messagebox.showerror("Error", "No internet connection!")
            return
        
        try:
            # Request settings
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json"
            }
            
            # Step 1: Get User ID
            user_id_url = f"https://api.roblox.com/users/get-by-username?username={username}"
            response = requests.get(user_id_url, headers=headers, 
                                 verify=False, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'Id' not in data:
                    messagebox.showerror("Error", "User not found")
                    return
                
                user_id = data['Id']
                
                # Step 2: Get detailed info
                user_info_url = f"https://users.roblox.com/v1/users/{user_id}"
                user_response = requests.get(user_info_url, headers=headers,
                                          verify=False, timeout=10)
                
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    
                    # Format join date
                    join_date = datetime.strptime(user_data['created'][:10], 
                                               "%Y-%m-%d").strftime("%B %d, %Y")
                    
                    # Update UI
                    self.result_labels['Username'].config(
                        text=f"Username: {user_data['name']}")
                    self.result_labels['UserID'].config(
                        text=f"User ID: {user_id}")
                    self.result_labels['JoinDate'].config(
                        text=f"Join Date: {join_date}")
                    self.result_labels['ProfileLink'].config(
                        text=f"Profile: https://www.roblox.com/users/{user_id}/profile")
                    self.result_labels['DisplayName'].config(
                        text=f"Display Name: {user_data.get('displayName', 'N/A')}")
                    
                else:
                    messagebox.showerror("Error", 
                                       f"API Error: {user_response.status_code}")
            else:
                messagebox.showerror("Error", 
                                   f"User lookup failed: {response.status_code}")
                
        except requests.exceptions.Timeout:
            messagebox.showerror("Error", "Request timed out (10s)")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Network error: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RobloxVenomApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

class RobloxVenomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RobloxVenom - Player Info")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Styling
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10))
        
        # Header
        header = ttk.Label(root, text="RobloxVenom - Player Information", font=('Arial', 12, 'bold'))
        header.pack(pady=10)
        
        # Username input
        self.username_label = ttk.Label(root, text="Enter Roblox Username:")
        self.username_label.pack()
        
        self.username_entry = ttk.Entry(root, width=30)
        self.username_entry.pack(pady=5)
        
        # Search button
        self.search_button = ttk.Button(root, text="Search", command=self.fetch_player_info)
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
            'IsBanned': ttk.Label(self.results_frame, text="Is Banned: "),
            'DisplayName': ttk.Label(self.results_frame, text="Display Name: ")
        }
        
        for label in self.result_labels.values():
            label.pack(anchor="w", padx=5, pady=2)
    
    def fetch_player_info(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        try:
            # Get user ID
            user_id_url = f"https://api.roblox.com/users/get-by-username?username={username}"
            response = requests.get(user_id_url)
            
            if response.status_code == 200:
                data = response.json()
                if 'Id' not in data:
                    messagebox.showerror("Error", "User not found")
                    return
                
                user_id = data['Id']
                
                # Get user info
                user_info_url = f"https://users.roblox.com/v1/users/{user_id}"
                user_response = requests.get(user_info_url)
                
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    
                    # Format join date
                    join_date = datetime.strptime(user_data['created'][:10], "%Y-%m-%d").strftime("%B %d, %Y")
                    
                    # Update labels
                    self.result_labels['Username'].config(text=f"Username: {user_data['name']}")
                    self.result_labels['UserID'].config(text=f"User ID: {user_id}")
                    self.result_labels['JoinDate'].config(text=f"Join Date: {join_date}")
                    self.result_labels['ProfileLink'].config(text=f"Profile: https://www.roblox.com/users/{user_id}/profile")
                    self.result_labels['IsBanned'].config(text=f"Is Banned: {user_data['isBanned']}")
                    self.result_labels['DisplayName'].config(text=f"Display Name: {user_data.get('displayName', 'N/A')}")
                    
                else:
                    messagebox.showerror("Error", "Failed to fetch user details")
            else:
                messagebox.showerror("Error", "User not found or API error")
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Network error: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RobloxVenomApp(root)
    root.mainloop()

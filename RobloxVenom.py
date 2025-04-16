import tkinter as tk
from tkinter import ttk, messagebox
from urllib.request import Request, urlopen
import json
import ssl
import socket

ssl._create_default_https_context = ssl._create_unverified_context

class nh3yaClean:
    def __init__(self, root):
        self.root = root
        self.root.title("nh3ya Tool v2.2")
        self.root.geometry("500x400")
        
        ttk.Label(root, text="Enter Roblox Username:").pack(pady=10)
        
        self.entry = ttk.Entry(root, width=30)
        self.entry.pack()
        
        self.btn = ttk.Button(root, text="Search", command=self.safe_search)
        self.btn.pack(pady=10)
        
        self.result = tk.Text(root, height=12, wrap=tk.WORD)
        self.result.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def safe_search(self):
        try:
            self.search_player()
        except Exception as e:
            messagebox.showerror("Error", f"Operation failed:\n{str(e)}")
    
    def search_player(self):
        username = self.entry.get().strip()
        if not username:
            messagebox.showwarning("Warning", "Please enter a username")
            return
        
        self.btn.config(state=tk.DISABLED, text="Searching...")
        self.root.update()
        
        try:
            headers = {"User-Agent": "nh3yaTool/2.2", "Accept": "application/json"}
            
            req = Request(f"https://api.roblox.com/users/get-by-username?username={username}", headers=headers)
            with urlopen(req, timeout=15) as res:
                data = json.loads(res.read().decode())
                
                if 'Id' not in data:
                    messagebox.showerror("Error", "Player not found")
                    return
                
                user_id = data['Id']
                
                details_req = Request(f"https://users.roblox.com/v1/users/{user_id}", headers=headers)
                with urlopen(details_req, timeout=15) as details_res:
                    details = json.loads(details_res.read().decode())
                    
                    result_text = f"""=== PLAYER INFO ===
Username: {username}
User ID: {user_id}
Join Date: {details.get('created', 'Unknown')}
Status: {"Banned" if details.get('isBanned') else "Active"}
Profile: https://www.roblox.com/users/{user_id}/profile
"""
                    self.result.delete(1.0, tk.END)
                    self.result.insert(tk.END, result_text)
        
        except socket.timeout:
            messagebox.showerror("Error", "Request timed out (15 seconds)")
        except Exception as e:
            messagebox.showerror("Error", f"API Connection Failed:\n{str(e)}")
        finally:
            self.btn.config(state=tk.NORMAL, text="Search")

if __name__ == "__main__":
    root = tk.Tk()
    app = nh3yaClean(root)
    root.mainloop()

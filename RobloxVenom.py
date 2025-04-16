import tkinter as tk
from tkinter import ttk, messagebox
from urllib.request import Request, urlopen
from urllib.error import URLError
import json
from datetime import datetime
import socket

class nh3yaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("nh3ya v1.0 - No PIP Needed")
        self.root.geometry("450x400")
        
        # واجهة المستخدم
        self.setup_ui()
    
    def setup_ui(self):
        """تهيئة واجهة المستخدم"""
        header = ttk.Label(self.root,
                         text="nh3ya - Roblox Player Info",
                         font=('Arial', 14, 'bold'),
                         foreground='#333')
        header.pack(pady=10)
        
        # إطار الإدخال
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Username:").pack(side=tk.LEFT)
        self.username_entry = ttk.Entry(input_frame, width=25)
        self.username_entry.pack(side=tk.LEFT, padx=5)
        
        self.search_btn = ttk.Button(input_frame,
                                   text="Search",
                                   command=self.search_player)
        self.search_btn.pack(side=tk.LEFT)
        
        # إطار النتائج
        self.results_frame = ttk.LabelFrame(self.root,
                                          text="Player Information",
                                          padding=10)
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # حقول النتائج
        self.result_labels = {
            'Username': ttk.Label(self.results_frame, text="Username: "),
            'UserID': ttk.Label(self.results_frame, text="User ID: "),
            'JoinDate': ttk.Label(self.results_frame, text="Join Date: "),
            'Profile': ttk.Label(self.results_frame, text="Profile: "),
            'Status': ttk.Label(self.results_frame, text="Status: ")
        }
        
        for label in self.result_labels.values():
            label.pack(anchor=tk.W)
    
    def check_internet(self):
        """فحص الاتصال بالإنترنت"""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
    
    def search_player(self):
        """البحث عن لاعب"""
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter username")
            return
        
        if not self.check_internet():
            messagebox.showerror("Error", "No internet connection!")
            return
        
        try:
            self.search_btn.config(text="Searching...")
            self.root.update()
            
            # الطلب باستخدام urllib
            api_url = f"https://api.roblox.com/users/get-by-username?username={username}"
            req = Request(api_url, headers={'User-Agent': 'nh3ya/1.0'})
            
            with urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                if 'Id' not in data:
                    messagebox.showerror("Error", "User not found")
                    return
                
                user_id = data['Id']
                
                # جلب معلومات إضافية
                details_url = f"https://users.roblox.com/v1/users/{user_id}"
                details_req = Request(details_url, headers={'User-Agent': 'nh3ya/1.0'})
                
                with urlopen(details_req, timeout=10) as details_res:
                    details = json.loads(details_res.read().decode())
                    
                    # عرض النتائج
                    join_date = datetime.strptime(details['created'][:10], "%Y-%m-%d").strftime("%B %d, %Y")
                    profile_url = f"https://www.roblox.com/users/{user_id}/profile"
                    
                    self.result_labels['Username'].config(text=f"Username: {username}")
                    self.result_labels['UserID'].config(text=f"User ID: {user_id}")
                    self.result_labels['JoinDate'].config(text=f"Join Date: {join_date}")
                    self.result_labels['Profile'].config(text=f"Profile: {profile_url}")
                    self.result_labels['Status'].config(text=f"Status: Online" if not details.get('isBanned', True) else "Status: Banned")
                    
                    messagebox.showinfo("nh3ya", "Search completed!")
        
        except URLError as e:
            messagebox.showerror("Error", f"Network error: {str(e)}")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid API response")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
        finally:
            self.search_btn.config(text="Search")

if __name__ == "__main__":
    root = tk.Tk()
    app = nh3yaApp(root)
    root.mainloop()

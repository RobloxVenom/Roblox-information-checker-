import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class RobloxVenomOffline:
    def __init__(self, root):
        self.root = root
        self.root.title("RobloxVenom OFFLINE v3.0")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # إنشاء ملف تخزين محلي إذا لم يكن موجوداً
        self.data_file = "players_data.json"
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump({}, f)
        
        # واجهة المستخدم
        self.setup_ui()
    
    def setup_ui(self):
        """تهيئة واجهة المستخدم"""
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), background='#FF5555')
        
        # إطار العنوان
        header = ttk.Label(self.root, 
                          text="RobloxVenom OFFLINE MODE",
                          font=('Arial', 14, 'bold'),
                          foreground='#333')
        header.pack(pady=10)
        
        # إطار الإدخال
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Username:").pack(side=tk.LEFT)
        self.username_entry = ttk.Entry(input_frame, width=25)
        self.username_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_frame, 
                  text="Search", 
                  command=self.search_player).pack(side=tk.LEFT)
        
        # إطار النتائج
        self.results_frame = ttk.LabelFrame(self.root, 
                                          text="Player Info",
                                          padding=10)
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # حقول النتائج
        self.result_labels = {
            'Username': ttk.Label(self.results_frame, text="Username: "),
            'UserID': ttk.Label(self.results_frame, text="User ID: "),
            'JoinDate': ttk.Label(self.results_frame, text="Join Date: "),
            'LastSeen': ttk.Label(self.results_frame, text="Last Seen: ")
        }
        
        for label in self.result_labels.values():
            label.pack(anchor=tk.W)
    
    def search_player(self):
        """بحث عن لاعب في البيانات المحلية"""
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        try:
            with open(self.data_file, 'r') as f:
                players = json.load(f)
            
            if username in players:
                self.show_player_info(players[username])
            else:
                messagebox.showinfo("Not Found", 
                                  f"Player '{username}' not in local database.\n\n"
                                  "You can add them manually.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    def show_player_info(self, player_data):
        """عرض معلومات اللاعب"""
        self.result_labels['Username'].config(text=f"Username: {player_data.get('username', 'N/A')}")
        self.result_labels['UserID'].config(text=f"User ID: {player_data.get('user_id', 'N/A')}")
        self.result_labels['JoinDate'].config(text=f"Join Date: {player_data.get('join_date', 'N/A')}")
        self.result_labels['LastSeen'].config(text=f"Last Seen: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RobloxVenomOffline(root)
    root.mainloop()

import customtkinter as ctk
import tkinter as tk
import requests
import threading
import pyperclip
import sys

# Try importing PIL. If missing, warn user.
try:
    from PIL import Image, ImageTk
except ImportError:
    print("CRITICAL: Pillow library missing. Run 'py -m pip install pillow'")
    sys.exit()

# --- MIAMI VICE COLOR PALETTE ---
THEME = {
    "bg": "#0d0221",               # Deep purple-black background
    "card": "#1a0f28",             # Dark purple cards
    "pink": "#ff1493",             # Hot pink (Miami Vice)
    "cyan": "#00d4ff",             # Bright cyan (Miami Vice)
    "purple": "#8b00ff",           # Vivid purple accent
    "text": "#ffffff",
    "input_bg": "#0f0a19"          # Very dark purple for inputs
}

class NeonAniList(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AniGap")
        self.geometry("650x780")
        self.resizable(False, False)  # Disable resizing
        
        # Set window icon
        import os
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, "icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
            self.after(200, lambda: self.iconbitmap(icon_path))
        
        # Set color theme
        ctk.set_appearance_mode("dark")
        
        # Fix for blurry text on some Windows displays
        if sys.platform == "win32":
            try:
                from ctypes import windll
                windll.shcore.SetProcessDpiAwareness(1)
            except: pass

        self.entries = {}
        
        # Set window background
        self.configure(fg_color=THEME["bg"])
        
        # Main container (non-scrollable since we're making it compact)
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # --- HEADER ---
        self.lbl_title = ctk.CTkLabel(self.main_frame, text="AniGap", 
                                      font=("Segoe UI", 44, "bold"), text_color=THEME["cyan"])
        self.lbl_title.pack(pady=(10, 0))
        
        self.lbl_sub = ctk.CTkLabel(self.main_frame, text="Love thy Latina", 
                                    font=("Arial", 11, "bold"), text_color=THEME["pink"])
        self.lbl_sub.pack(pady=(0, 15))

        # --- COMBINED CARD (Username + Filters side by side) ---
        self.create_combined_card(self.main_frame)

        # Format Toggle - now with 5 options
        self.format_var = tk.StringVar(value="TV+OVA")
        
        toggle_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        toggle_frame.pack(pady=12)
        
        # Create toggle buttons
        self.format_buttons = {}
        formats = ["TV", "OVA", "TV+OVA", "MOVIE", "ALL"]
        widths = [50, 50, 80, 70, 50]  # Different widths for different button text
        
        for i, (fmt, width) in enumerate(zip(formats, widths)):
            btn = ctk.CTkButton(toggle_frame, text=fmt, 
                               font=("Arial", 11, "bold"),
                               width=width, height=35, corner_radius=50,
                               command=lambda f=fmt: self.set_format(f))
            btn.grid(row=0, column=i, padx=2)
            self.format_buttons[fmt] = btn
        
        # Set initial selected state
        self.set_format("TV+OVA")

        # --- ACTION BUTTONS ---
        self.create_buttons(self.main_frame)

        # --- RESULTS BOX ---
        results_container = ctk.CTkFrame(self.main_frame, fg_color=THEME["card"], 
                                        corner_radius=15, border_color=THEME["cyan"], border_width=2)
        results_container.pack(pady=8, fill="both", expand=True)
        
        # Header for results
        results_header = ctk.CTkLabel(results_container, text="RESULTS", 
                                     font=("Arial", 12, "bold"), text_color=THEME["cyan"])
        results_header.pack(pady=(8, 4))
        
        # Scrollable frame for results
        self.results = ctk.CTkScrollableFrame(results_container, fg_color="transparent",
                                              scrollbar_button_color=THEME["purple"],
                                              scrollbar_button_hover_color=THEME["cyan"])
        self.results.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        # Store result cards for later clearing
        self.result_cards = []
    
    def set_format(self, fmt):
        """Update format selection and button states"""
        self.format_var.set(fmt)
        
        # Update button colors
        for format_name, button in self.format_buttons.items():
            if format_name == fmt:
                button.configure(fg_color=THEME["pink"], 
                               hover_color="#d1006e",
                               text_color="white")
            else:
                button.configure(fg_color="transparent",
                               hover_color=THEME["card"],
                               text_color=THEME["text"],
                               border_color=THEME["purple"],
                               border_width=1)

    def create_combined_card(self, parent):
        """Create a single card with username entries on left, filters on right"""
        card = ctk.CTkFrame(parent, fg_color=THEME["card"], corner_radius=15,
                            border_color=THEME["pink"], border_width=2)
        card.pack(fill="x", pady=8, ipady=6)
        
        # Create two-column layout
        card.columnconfigure(0, weight=1)
        card.columnconfigure(1, weight=1)
        
        # LEFT SIDE - Username entries (centered vertically)
        left_frame = ctk.CTkFrame(card, fg_color="transparent")
        left_frame.grid(row=0, column=0, padx=10, pady=6)
        
        # Add more spacing before entries to center them better
        spacer_top = ctk.CTkLabel(left_frame, text="", height=6)
        spacer_top.pack()
        
        self.user_entries = []
        for i in range(1, 5):
            entry = ctk.CTkEntry(left_frame, placeholder_text=f"Username {i}" + (" (optional)" if i > 2 else ""), 
                                     width=260, height=32, corner_radius=18,
                                     border_color=THEME["pink"] if i <= 2 else THEME["purple"], border_width=2,
                                     fg_color=THEME["input_bg"], 
                                     text_color=THEME["text"],
                                     placeholder_text_color="#666666",
                                     font=("Arial", 13))
            entry.pack(pady=3)
            self.user_entries.append(entry)
        
        # RIGHT SIDE - Filter options
        right_frame = ctk.CTkFrame(card, fg_color="transparent")
        right_frame.grid(row=0, column=1, padx=10, pady=6, sticky="nsew")
        
        # Create 2x2 grid for filters
        right_frame.columnconfigure(0, weight=1)
        right_frame.columnconfigure(1, weight=1)
        
        self.create_label_entry(right_frame, 0, 0, "MAX EPISODES", "14", "eps")
        self.create_label_entry(right_frame, 0, 1, "LIMIT", "10", "lim")
        self.create_label_entry(right_frame, 1, 0, "MIN YEAR", "", "min_year")
        self.create_label_entry(right_frame, 1, 1, "MAX YEAR", "", "max_year")

    def create_buttons(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=8)
        
        self.btn_run = ctk.CTkButton(frame, text="INITIATE SEARCH", font=("Arial", 15, "bold"),
                                     fg_color=THEME["pink"], hover_color="#d1006e", 
                                     text_color="white",
                                     width=180, height=42, corner_radius=50,
                                     command=self.start_search)
        self.btn_run.grid(row=0, column=0, padx=10)

        self.btn_copy = ctk.CTkButton(frame, text="COPY", font=("Arial", 15, "bold"),
                                      fg_color="transparent", 
                                      border_color=THEME["cyan"], border_width=2,
                                      text_color=THEME["cyan"],
                                      hover_color=THEME["card"], 
                                      width=100, height=42, corner_radius=50,
                                      command=self.copy_to_clipboard)
        self.btn_copy.grid(row=0, column=1, padx=10)

    def create_label_entry(self, parent, r, c, label, default, key):
        lbl = ctk.CTkLabel(parent, text=label, font=("Arial", 11, "bold"),
                          text_color=THEME["text"])
        lbl.grid(row=r*2, column=c, pady=(6, 1), padx=4)
        entry = ctk.CTkEntry(parent, width=100, height=30, justify="center", corner_radius=12,
                             border_color=THEME["cyan"], border_width=2,
                             fg_color=THEME["input_bg"], 
                             text_color="white",
                             placeholder_text_color="#666666",
                             font=("Arial", 14))
        if default: entry.insert(0, default)
        entry.grid(row=r*2+1, column=c, pady=(0, 6), padx=4)
        self.entries[key] = entry

    def start_search(self):
        # Clear previous results
        for card in self.result_cards:
            card.destroy()
        self.result_cards = []
        
        # Show searching message
        searching_label = ctk.CTkLabel(self.results, text="⚡ CONNECTING TO ANILIST GRID...",
                                      font=("Arial", 12, "bold"), text_color=THEME["pink"])
        searching_label.pack(pady=20)
        self.result_cards.append(searching_label)
        
        threading.Thread(target=self.run_logic, daemon=True).start()

    def run_logic(self):
        usernames = [entry.get().strip() for entry in self.user_entries if entry.get().strip()]
        if len(usernames) < 2:
            # Clear searching message
            for card in self.result_cards:
                card.destroy()
            self.result_cards = []
            
            error_label = ctk.CTkLabel(self.results, text="❌ ERROR: AT LEAST TWO USERS REQUIRED",
                                      font=("Arial", 12, "bold"), text_color=THEME["pink"])
            error_label.pack(pady=20)
            self.result_cards.append(error_label)
            return

        try:
            max_eps = int(self.entries["eps"].get()) if self.entries["eps"].get() else 300
            result_limit = int(self.entries["lim"].get()) if self.entries["lim"].get() else 10
            min_y_input = self.entries["min_year"].get()
            max_y_input = self.entries["max_year"].get()
            date_greater = int(f"{int(min_y_input) - 1}1231") if min_y_input and min_y_input.isdigit() else None
            date_lesser = int(f"{int(max_y_input) + 1}0101") if max_y_input and max_y_input.isdigit() else None
        except ValueError:
            # Clear searching message
            for card in self.result_cards:
                card.destroy()
            self.result_cards = []
            
            error_label = ctk.CTkLabel(self.results, text="❌ ERROR: INVALID NUMBERS",
                                      font=("Arial", 12, "bold"), text_color=THEME["pink"])
            error_label.pack(pady=20)
            self.result_cards.append(error_label)
            return

        # Determine formats based on selection
        format_choice = self.format_var.get()
        if format_choice == "TV":
            formats = ["TV"]
        elif format_choice == "OVA":
            formats = ["OVA", "ONA", "SPECIAL"]
        elif format_choice == "TV+OVA":
            formats = ["TV", "OVA", "ONA"]
        elif format_choice == "MOVIE":
            formats = ["MOVIE"]
        else:  # ALL
            formats = ["TV", "OVA", "ONA", "SPECIAL", "MOVIE"]
        
        seen = set()
        for username in usernames:
            seen |= self.fetch_seen(username)
        current_page, found_titles = 1, []
        
        base_var_defs = ["$fmts: [MediaFormat]", "$eps: Int", "$page: Int"]
        base_media_args = ["format_in: $fmts", "episodes_lesser: $eps", "sort: SCORE_DESC", "status: FINISHED"]
        variables = {'fmts': formats, 'eps': max_eps + 1}

        if date_greater:
            base_var_defs.append("$after: FuzzyDateInt")
            base_media_args.append("startDate_greater: $after")
            variables['after'] = date_greater
        if date_lesser:
            base_var_defs.append("$before: FuzzyDateInt")
            base_media_args.append("startDate_lesser: $before")
            variables['before'] = date_lesser

        query = f'''
        query ({', '.join(base_var_defs)}) {{
          Page(page: $page, perPage: 50) {{
            pageInfo {{ hasNextPage }}
            media({', '.join(base_media_args)}) {{
              id, title {{ romaji }}, episodes, averageScore, startDate {{ year }},
              nextAiringEpisode {{ id }}, 
              relations {{ edges {{ relationType node {{ id format }} }} }},
              genres
            }}
          }}
        }}
        '''

        while len(found_titles) < result_limit and current_page <= 15:
            variables['page'] = current_page
            try:
                r = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})
                if r.status_code != 200: break
                candidates = r.json()['data']['Page']['media']
                for anime in candidates:
                    if len(found_titles) >= result_limit: break
                    if anime['id'] in seen or anime['nextAiringEpisode']: continue
                    
                    # Check if this anime has any prequels or parent series
                    has_unseen_prerequisite = any(
                        e['relationType'] in ['PREQUEL', 'PARENT'] and e['node']['id'] not in seen 
                        for e in anime['relations']['edges']
                    )
                    
                    # For movies, apply stricter filtering
                    if format_choice == "MOVIE":
                        # Check for problematic relationships
                        skip_movie = False
                        
                        for edge in anime['relations']['edges']:
                            rel_type = edge['relationType']
                            rel_format = edge['node'].get('format')
                            
                            # Always skip if there's a PREQUEL or PARENT (this movie is a sequel)
                            if rel_type in ['PREQUEL', 'PARENT']:
                                skip_movie = True
                                break
                            
                            # For ADAPTATION: this movie is adapting something
                            # Skip if it's adapting a TV/OVA/ONA show (not manga/novel)
                            if rel_type == 'ADAPTATION':
                                if rel_format in ['TV', 'OVA', 'ONA', 'SPECIAL', 'TV_SHORT']:
                                    skip_movie = True
                                    break
                                # If it's adapting MANGA, NOVEL, ONE_SHOT, LIGHT_NOVEL - that's fine!
                            
                            # For SOURCE: something else adapted this movie's source material
                            # If a TV show has the same source (e.g., both the movie and a TV show adapted the same manga)
                            # We want to skip this because it means there's a related TV series
                            if rel_type == 'SOURCE':
                                if rel_format in ['TV', 'OVA', 'ONA', 'SPECIAL', 'TV_SHORT']:
                                    skip_movie = True
                                    break
                        
                        if skip_movie:
                            continue
                        
                        # Also filter out common sequel/recap indicators in the title
                        title_lower = anime['title']['romaji'].lower()
                        skip_keywords = [
                            'season', 'part', 'vol', 'volume', 'arc',
                            'recap', 'compilation', 'summary',
                            ': the movie', '- the movie',
                        ]
                        
                        # Skip if title contains indicators it's part of a series
                        if any(keyword in title_lower for keyword in skip_keywords):
                            continue
                        
                        # Passed all movie filters
                        found_titles.append(anime)
                    
                    # For non-movies, use the original logic
                    elif not has_unseen_prerequisite:
                        found_titles.append(anime)
                if not r.json()['data']['Page']['pageInfo']['hasNextPage']: break
                current_page += 1
            except: break

        # Clear searching message
        for card in self.result_cards:
            card.destroy()
        self.result_cards = []
        
        if not found_titles:
            no_results = ctk.CTkLabel(self.results, text="No titles found matching your criteria",
                                     font=("Arial", 12), text_color=THEME["text"])
            no_results.pack(pady=20)
            self.result_cards.append(no_results)
        else:
            for anime in found_titles:
                self.create_result_card(anime)
    
    def create_result_card(self, anime):
        """Create a modern card for each anime result"""
        score = anime['averageScore'] if anime['averageScore'] else 0
        year = anime['startDate']['year'] if anime['startDate']['year'] else "????"
        title = anime['title']['romaji']
        episodes = anime['episodes']
        anime_id = anime['id']
        genres = anime.get('genres', [])[:3]  # Get first 3 genres
        
        # Card container
        card = ctk.CTkFrame(self.results, fg_color=THEME["input_bg"], 
                           corner_radius=8, border_width=1,
                           border_color=THEME["purple"], height=45)
        card.pack(fill="x", pady=2, padx=4)
        card.pack_propagate(False)
        
        # Left side - Score only (no label)
        left_frame = ctk.CTkFrame(card, fg_color="transparent", width=55)
        left_frame.pack(side="left", padx=6, pady=4)
        left_frame.pack_propagate(False)
        
        # Score
        score_color = THEME["cyan"] if score >= 75 else THEME["pink"] if score >= 60 else THEME["purple"]
        score_label = ctk.CTkLabel(left_frame, text=f"{score}%", 
                                   font=("Arial", 16, "bold"), text_color=score_color)
        score_label.pack(expand=True)
        
        # Middle - Title and Info (all on one line)
        middle_frame = ctk.CTkFrame(card, fg_color="transparent")
        middle_frame.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        
        # Create a frame to hold both clickable title and non-clickable info
        text_container = ctk.CTkFrame(middle_frame, fg_color="transparent")
        text_container.pack(fill="x", expand=True, anchor="w")
        
        # Title (clickable)
        title_label = ctk.CTkLabel(text_container, text=title, 
                                   font=("Arial", 13, "bold"), text_color=THEME["cyan"],
                                   anchor="w", cursor="hand2")
        title_label.pack(side="left")
        title_label.bind("<Button-1>", lambda e: self.open_url(f"https://anilist.co/anime/{anime_id}"))
        
        # Separator and info (not clickable)
        info_text = f"  •  {year} • {episodes} eps"
        info_label = ctk.CTkLabel(text_container, text=info_text,
                                 font=("Arial", 11), text_color="#888888",
                                 anchor="w")
        info_label.pack(side="left")
        
        # Right side - Genres
        if genres:
            right_frame = ctk.CTkFrame(card, fg_color="transparent", width=140)
            right_frame.pack(side="right", padx=6, pady=4)
            right_frame.pack_propagate(False)
            
            genres_text = " • ".join(genres)
            genres_label = ctk.CTkLabel(right_frame, text=genres_text,
                                       font=("Arial", 10), text_color=THEME["purple"],
                                       anchor="e", wraplength=135)
            genres_label.pack(expand=True, fill="both")
        
        self.result_cards.append(card)

    def fetch_seen(self, user):
        q = 'query($u:String){MediaListCollection(userName:$u,type:ANIME){lists{entries{mediaId}}}}'
        try:
            r = requests.post('https://graphql.anilist.co', json={'query':q, 'variables':{'u':user}})
            return {e['mediaId'] for lst in r.json()['data']['MediaListCollection']['lists'] for e in lst['entries']}
        except: return set()

    def copy_to_clipboard(self):
        # Gather all results into text format
        results_text = ""
        for card in self.result_cards:
            # Skip if it's an error/status message
            if isinstance(card, ctk.CTkLabel):
                continue
            # Extract text from card widgets
            try:
                for widget in card.winfo_children():
                    if isinstance(widget, ctk.CTkFrame):
                        for child in widget.winfo_children():
                            if isinstance(child, ctk.CTkLabel):
                                results_text += child.cget("text") + " "
                results_text = results_text.strip() + "\n"
            except:
                pass
        
        if results_text:
            pyperclip.copy(results_text)
            self.btn_copy.configure(text="✓ COPIED!", fg_color=THEME["cyan"], text_color=THEME["bg"])
            self.after(2000, lambda: self.btn_copy.configure(text="COPY", fg_color="transparent", text_color=THEME["cyan"]))
    
    def open_url(self, url):
        """Open URL in default browser"""
        import webbrowser
        webbrowser.open(url)

if __name__ == "__main__":
    app = NeonAniList()
    app.mainloop()
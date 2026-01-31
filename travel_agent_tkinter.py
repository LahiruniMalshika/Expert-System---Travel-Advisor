import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pyswip import Prolog
import random
from datetime import datetime

class SimpleTravelAgent:
    def __init__(self):
        self.prolog = Prolog()
        self.prolog.consult("travel_kb.pl")
    
    def get_all_destinations(self):
        """Get all destinations from knowledge base"""
        destinations = []
        try:
            for result in self.prolog.query("destination(Name, Country, Continent, Type, Cost)"):
                destinations.append({
                    'name': result["Name"],
                    'country': result["Country"],
                    'continent': result["Continent"],
                    'type': result["Type"],
                    'cost': result["Cost"]
                })
        except Exception as e:
            print(f"Error loading destinations: {e}")
        return destinations
    
    def recommend_destinations(self, continent=None, dest_type=None, max_budget=None):
        """Simple recommendation engine"""
        destinations = self.get_all_destinations()
        
        if continent and continent != "Any":
            destinations = [d for d in destinations if d['continent'] == continent]
        
        if dest_type and dest_type != "Any":
            destinations = [d for d in destinations if d['type'] == dest_type]
        
        if max_budget:
            destinations = [d for d in destinations if d['cost'] <= max_budget]
        
        return destinations
    
    def get_best_season(self, destination_name, destination_type, continent):
        """Determine best season to visit based on destination characteristics"""
        # Season logic based on destination type and continent
        seasons = {
            'beach': {
                'europe': ['Summer (June-August)', 'Late Spring (May)', 'Early Autumn (September)'],
                'asia': ['Dry Season (November-April)', 'Summer (June-August)'],
                'north_america': ['Summer (June-August)', 'Late Spring (May)', 'Early Fall (September)'],
                'south_america': ['Summer (December-March)', 'Dry Season (May-October)'],
                'africa': ['Dry Season (June-October)', 'Summer (December-February)'],
                'australia': ['Summer (December-February)', 'Spring (September-November)']
            },
            'mountain': {
                'europe': ['Summer (June-September)', 'Spring (April-June)', 'Autumn (September-October)'],
                'asia': ['Spring (March-May)', 'Autumn (September-November)'],
                'north_america': ['Summer (June-September)', 'Fall (September-October)'],
                'south_america': ['Dry Season (May-September)', 'Summer (December-February)'],
                'africa': ['Dry Season (June-October)', 'Winter (December-February)'],
                'australia': ['Summer (December-February)', 'Autumn (March-May)']
            },
            'city': {
                'europe': ['Spring (April-June)', 'Autumn (September-October)', 'Summer (June-August)'],
                'asia': ['Winter (November-February)', 'Spring (March-May)'],
                'north_america': ['Spring (April-June)', 'Fall (September-October)'],
                'south_america': ['Spring (September-November)', 'Autumn (March-May)'],
                'africa': ['Dry Season (June-October)', 'Winter (December-February)'],
                'australia': ['Spring (September-November)', 'Autumn (March-May)']
            },
            'historical': {
                'europe': ['Spring (April-June)', 'Autumn (September-October)'],
                'asia': ['Winter (November-February)', 'Spring (March-May)'],
                'north_america': ['Spring (April-June)', 'Fall (September-October)'],
                'south_america': ['Dry Season (May-September)', 'Spring (September-November)'],
                'africa': ['Dry Season (June-October)', 'Winter (December-February)'],
                'australia': ['Autumn (March-May)', 'Spring (September-November)']
            },
            'adventure': {
                'europe': ['Summer (June-September)', 'Spring (April-June)'],
                'asia': ['Dry Season (November-April)', 'Spring (March-May)'],
                'north_america': ['Summer (June-September)', 'Spring (April-June)'],
                'south_america': ['Dry Season (May-September)', 'Summer (December-February)'],
                'africa': ['Dry Season (June-October)', 'Winter (December-February)'],
                'australia': ['Spring (September-November)', 'Autumn (March-May)']
            }
        }
        
        # Get seasons for the specific type and continent
        type_seasons = seasons.get(destination_type, {})
        continent_seasons = type_seasons.get(continent, ['Spring (March-May)', 'Autumn (September-November)'])
        
        # Return the best season (first in list) and alternatives
        best_season = continent_seasons[0] if continent_seasons else "Spring (March-May)"
        alternative_seasons = continent_seasons[1:] if len(continent_seasons) > 1 else []
        
        return {
            'best_season': best_season,
            'alternative_seasons': alternative_seasons,
            'reason': self._get_season_reason(destination_type, continent, best_season)
        }
    
    def _get_season_reason(self, dest_type, continent, season):
        """Generate reason why this season is best"""
        reasons = {
            'beach': f"Perfect weather for beach activities with warm temperatures and minimal rainfall",
            'mountain': f"Ideal conditions for hiking and mountain activities with clear skies and comfortable temperatures",
            'city': f"Pleasant weather for city exploration with mild temperatures and fewer crowds",
            'historical': f"Best time for sightseeing with comfortable weather and good visibility",
            'adventure': f"Optimal conditions for adventure activities with stable weather and accessible terrain"
        }
        
        base_reason = reasons.get(dest_type, "Favorable weather conditions and optimal travel experience")
        
        # Add continent-specific notes
        continent_notes = {
            'europe': " during this popular travel period",
            'asia': " with comfortable humidity levels",
            'north_america': " with excellent travel conditions",
            'south_america': " during the dry season",
            'africa': " with minimal rainfall",
            'australia': " with perfect outdoor conditions"
        }
        
        return base_reason + continent_notes.get(continent, "")

class ModernTravelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌍 TravelExplorer - Find Your Dream Destination")
        self.root.geometry("1000x750")
        
        # Configure style
        self.configure_styles()
        
        self.travel_agent = SimpleTravelAgent()
        self.current_destinations = []
        self.create_gui()
    
    def configure_styles(self):
        style = ttk.Style()
        
        self.colors = {
            'primary': '#2563eb',      
            'secondary': '#f59e0b',   
            'accent': '#ef4444',      
            'success': '#10b981',     
            'warning': '#f59e0b',     
            'light': '#f8fafc',        
            'dark': '#1e293b',        
            'background': '#f0f9ff',   
            'card_bg': '#ffffff',      
            'header_bg': '#5d6d7e',  
            'footer_bg': '#1e293b',   
            'text_light': '#64748b',  
            'border_light': '#e2e8f0',  
            'season_good': '#dcfce7',   
            'season_best': '#bbf7d0',   
        }
        
        # Configure styles
        style.configure('Primary.TButton', 
                       background=self.colors['secondary'],
                       foreground='white',
                       padding=(20, 10),
                       font=('Arial', 10, 'bold'))
        
        style.configure('Card.TFrame', 
                       background=self.colors['card_bg'],
                       relief='raised',
                       borderwidth=1)
        
        style.configure('Title.TLabel',
                       background=self.colors['background'],
                       foreground=self.colors['primary'],
                       font=('Arial', 20, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=self.colors['background'],
                       foreground=self.colors['dark'],
                       font=('Arial', 12))
        
        style.configure('Filter.TLabel',
                       background=self.colors['card_bg'],
                       foreground=self.colors['dark'],
                       font=('Arial', 10, 'bold'))
    
    def create_gui(self):
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_container)
        
        # Search section
        self.create_search_section(main_container)
        
        # Results section
        self.create_results_section(main_container)
        
        # Footer
        self.create_footer(main_container)
        
        # Show welcome message
        self.show_welcome_message()
    
    def create_header(self, parent):
        # Header with gradient-like effect
        header_frame = tk.Frame(parent, bg=self.colors['header_bg'], height=140)
        header_frame.pack(fill=tk.X, pady=(0, 25))
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=self.colors['header_bg'])
        header_content.pack(expand=True, fill=tk.BOTH, padx=30, pady=25)
        
        # Title and subtitle with modern styling
        title_label = tk.Label(header_content, 
                              text="🌴 Travel Advisor", 
                              font=('Arial', 32, 'bold'),
                              fg='white',
                              bg=self.colors['header_bg'])
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(header_content,
                                text="Discover your perfect getaway destination with seasonal insights",
                                font=('Arial', 14),
                                fg='#e2e8f0',
                                bg=self.colors['header_bg'])
        subtitle_label.pack(anchor='w', pady=(8, 0))
    
    def create_search_section(self, parent):
        search_frame = tk.Frame(parent, 
                               bg=self.colors['card_bg'], 
                               relief='flat', 
                               bd=0,
                               highlightbackground=self.colors['border_light'],
                               highlightthickness=1)
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        inner_frame = tk.Frame(search_frame, bg=self.colors['card_bg'], padx=25, pady=20)
        inner_frame.pack(fill=tk.X, expand=True)
        
        # Section title with icon
        section_title = tk.Label(inner_frame,
                               text="Search Destinations",
                               font=('Arial', 18, 'bold'),
                               fg=self.colors['primary'],
                               bg=self.colors['card_bg'])
        section_title.grid(row=0, column=0, columnspan=8, sticky='w', pady=(0, 15))
        
        # Search criteria
        criteria = [
            ("Continent:", "Any", ["Any", "europe", "asia", "north_america", "south_america", "africa", "australia"]),
            ("Travel Type:", "Any", ["Any", "beach", "mountain", "city", "historical", "adventure"]),
            ("Max Budget ($):", "", [])
        ]
        
        self.continent_var = tk.StringVar(value="Any")
        self.type_var = tk.StringVar(value="Any")
        self.budget_var = tk.StringVar()
        
        for i, (label, default, options) in enumerate(criteria):
            # Label with modern styling
            lbl = tk.Label(inner_frame, text=label, font=('Arial', 11, 'bold'),
                          fg=self.colors['dark'], bg=self.colors['card_bg'])
            lbl.grid(row=1, column=i*2, sticky='w', padx=(0, 12), pady=8)
            
            # Input widget
            if options:  # Combobox
                combo = ttk.Combobox(inner_frame, textvariable=[
                    self.continent_var, self.type_var, self.budget_var
                ][i], values=options, state="readonly", width=18, 
                font=('Arial', 10), background='white')
                combo.grid(row=1, column=i*2+1, sticky='w', padx=(0, 25), pady=8)
            else:  # Entry
                entry = ttk.Entry(inner_frame, textvariable=self.budget_var, 
                                 width=20, font=('Arial', 10))
                entry.grid(row=1, column=i*2+1, sticky='w', padx=(0, 25), pady=8)
        
        # Modern search button positioned to the right of search filters
        search_btn = tk.Button(inner_frame,
                              text="Find Destinations",
                              font=('Arial', 12, 'bold'),
                              bg='dark blue',
                              fg='white',
                              relief='flat',
                              bd=0,
                              padx=35,
                              pady=12,
                              cursor='hand2',
                              activebackground='#059669',
                              activeforeground='white',
                              command=self.search_destinations)
        search_btn.grid(row=1, column=6, columnspan=2, padx=(20, 0), pady=8, sticky='e')
        
        # Quick filters
        self.create_quick_filters(inner_frame)
    
    def create_quick_filters(self, parent):
        quick_filters_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        quick_filters_frame.grid(row=2, column=0, columnspan=8, sticky='w', pady=(15, 0))
        
        tk.Label(quick_filters_frame, text="Quick filters:", font=('Arial', 11, 'bold'),
                fg=self.colors['dark'], bg=self.colors['card_bg']).pack(side='left', padx=(0, 15))
        
        filters = [
            ("Beach", "beach"),
            ("Historical", "historical"),
            ("City", "city"),
            ("Adventure", "adventure"),
            ("Budget (<$700)", "budget")
        ]
        
        for text, filter_type in filters:
            btn = tk.Button(quick_filters_frame,
                          text=text,
                          font=('Arial', 10),
                          fg=self.colors['dark'],
                          bg='#e0f2fe',
                          relief='flat',
                          padx=15,
                          pady=8,
                          cursor='hand2',
                          activebackground=self.colors['primary'],
                          activeforeground='white',
                          command=lambda ft=filter_type: self.apply_quick_filter(ft))
            btn.pack(side='left', padx=6)
    
    def create_results_section(self, parent):
        results_container = tk.Frame(parent, bg=self.colors['background'])
        results_container.pack(fill=tk.BOTH, expand=True)
        
        # Results header
        results_header = tk.Frame(results_container, bg=self.colors['card_bg'])
        results_header.pack(fill=tk.X, pady=(0, 12))
        
        self.results_title = tk.Label(results_header,
                                    text="📋 Search Results",
                                    font=('Arial', 16, 'bold'),
                                    fg=self.colors['primary'],
                                    bg=self.colors['card_bg'])
        self.results_title.pack(anchor='w', padx=20, pady=12)
        
        results_frame = tk.Frame(results_container, 
                                bg=self.colors['card_bg'], 
                                relief='flat',
                                highlightbackground=self.colors['border_light'],
                                highlightthickness=1)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            font=('Arial', 11),
            bg='white',
            fg=self.colors['dark'],
            padx=20,
            pady=20,
            relief='flat',
            borderwidth=0,
            selectbackground=self.colors['light']
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    def create_footer(self, parent):
        footer_frame = tk.Frame(parent, bg=self.colors['footer_bg'], height=50)
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        footer_frame.pack_propagate(False)
        
        footer_text = tk.Label(footer_frame,
                             text="© 2025 TravelExplorer - Your Gateway to Adventure 🌟",
                             font=('Arial', 11),
                             fg='#cbd5e1',
                             bg=self.colors['footer_bg'])
        footer_text.pack(expand=True)
    
    def apply_quick_filter(self, filter_type):
        if filter_type == "budget":
            self.budget_var.set("700")
            self.continent_var.set("Any")
            self.type_var.set("Any")
        else:
            self.type_var.set(filter_type)
            self.continent_var.set("Any")
            self.budget_var.set("")
        
        self.search_destinations()
    
    def show_welcome_message(self):
        welcome = """
🎉 Welcome to TravelExplorer!

Ready to discover your next adventure? Use the search tools above to find perfect destinations that match your preferences.

NEW: Automatic Best Season Recommendations!
Now get personalized advice on when to visit each destination for the best experience.

💡 How to use:
• Select a continent or choose 'Any' to search worldwide
• Pick your preferred travel type (beach, city, historical, etc.)
• Set a maximum budget to find affordable options
• Use quick filters for instant results
• Get automatic best season advice for each destination

🌟 Popular searches:
• European historical sites
• Asian beach destinations  
• Budget-friendly adventures

Click 'Find Destinations' to start your journey!
"""
        self.display_results(welcome, "Welcome to TravelExplorer!")
    
    def search_destinations(self):
        """Handle destination search"""
        continent = self.continent_var.get()
        dest_type = self.type_var.get()
        
        # Validate budget
        max_budget = None
        if self.budget_var.get().strip():
            try:
                max_budget = float(self.budget_var.get())
                if max_budget <= 0:
                    self.show_error("Budget must be a positive number")
                    return
            except ValueError:
                self.show_error("Please enter a valid budget amount")
                return
        
        # Convert "Any" to None for filtering
        continent = None if continent == "Any" else continent
        dest_type = None if dest_type == "Any" else dest_type
        
        # Update UI to show searching state
        self.results_title.config(text="🔍 Searching...")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, "Searching for perfect destinations...")
        self.root.update()
        
        # Search for destinations
        results = self.travel_agent.recommend_destinations(continent, dest_type, max_budget)
        self.current_destinations = results
        self.display_search_results(results, continent, dest_type, max_budget)
    
    def display_search_results(self, destinations, continent, dest_type, max_budget):
        """Display search results in a beautiful format"""
        if not destinations:
            self.results_title.config(text=" Select another choice")
            no_results = """
😔 No destinations found matching your criteria.

💡 Suggestions:
• Try broadening your search by selecting 'Any' for continent or type
• Increase your budget range
• Check out our quick filters for popular options

Ready to try again?
"""
            self.display_results(no_results, "")
            return
        
        self.results_title.config(text=f"🎯 Found {len(destinations)} Destination(s)")
        
        results_text = ""
        
        # Add filter summary
        filters_applied = []
        if continent:
            filters_applied.append(f"🌍 {continent.replace('_', ' ').title()}")
        if dest_type:
            filters_applied.append(f"🎯 {dest_type.title()}")
        if max_budget:
            filters_applied.append(f"💰 ${max_budget}")
        
        if filters_applied:
            results_text += "📊 Search Filters: " + " • ".join(filters_applied) + "\n\n"
            results_text += "="*60 + "\n\n"
        
        # Display each destination as a card-like entry
        for i, dest in enumerate(destinations, 1):
            # Get best season information
            season_info = self.travel_agent.get_best_season(
                dest['name'], dest['type'], dest['continent']
            )
            
            # Destination header with emoji based on type
            type_emojis = {
                'beach': '🏖️', 'mountain': '⛰️', 'city': '🏙️',
                'historical': '🏛️', 'adventure': '🎯'
            }
            emoji = type_emojis.get(dest['type'], '📍')
            
            results_text += f"{emoji} {dest['name'].title()}, {dest['country'].title()}\n"
            results_text += f"   🌐 {dest['continent'].replace('_', ' ').title()}"
            results_text += f" • 🎯 {dest['type'].title()}"
            results_text += f" • 💰 ${dest['cost']} per person\n"
            
            # Add rating stars based on cost (inverse relationship for demo)
            rating = max(1, min(5, 6 - dest['cost'] // 400))
            results_text += f"   ⭐ {'★' * rating}{'☆' * (5 - rating)} Value Rating\n"
            
            results_text += f"\n   🌤️Best Time to Visit: {season_info['best_season']}\n"
            results_text += f"   💡 Why: {season_info['reason']}\n"
            
            if season_info['alternative_seasons']:
                results_text += f"   🌈 Also Good: {', '.join(season_info['alternative_seasons'])}\n"
            
            results_text += "\n" + "-"*50 + "\n\n"
        
        results_text += f"\n🎉 Found {len(destinations)} perfect destination(s) for you!\n\n"
        results_text += "💡 Tip: Consider the seasonal recommendations when planning your trip for the best experience!"
        
        self.display_results(results_text, "")
    
    def display_results(self, text, title):
        """Display text in results area"""
        self.results_text.delete(1.0, tk.END)
        if title:
            self.results_text.insert(1.0, f"{title}\n{'='*40}\n\n")
        self.results_text.insert(tk.END, text)
        
        # Configure tags for better formatting
        self.results_text.tag_configure("bold", font=('Arial', 10, 'bold'))
        self.results_text.tag_configure("highlight", background='#e8f4f8')
    
    def show_error(self, message):
        """Show error message in a modern way"""
        messagebox.showerror("Oops! 🚫", message, parent=self.root)

def main():
    try:
        root = tk.Tk()
        app = ModernTravelGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Error", f"Failed to start application: {e}")

if __name__ == "__main__":
    main()
from fpdf import FPDF
from fpdf.enums import XPos, YPos;

class AdvancedMenuPDF(FPDF):
    def __init__(self):
        super().__init__()


        self.add_font('DejaVu', '', 'C:/Users/shach/Desktop/java/APP/DejaVuSans.ttf')
        self.add_font('DejaVu', 'B', 'C:/Users/shach/Desktop/java/APP/DejaVuSans-Bold.ttf')
        self.add_font('DejaVu', 'I', 'C:/Users/shach/Desktop/java/APP/DejaVuSans-Oblique.ttf')
        self.add_font('DejaVu', 'BI', 'C:/Users/shach/Desktop/java/APP/DejaVuSans-BoldOblique.ttf')

        self.set_font("DejaVu", "B", 18)  # For bold
        self.set_font("DejaVu", "", 12)   # For regular
        self.set_font("DejaVu", "B", 14)  # For section titles
        self.set_font("DejaVu", "B", 8)   # For badges
        self.set_font("DejaVu", "", 9)    # For descriptions
        self.set_font("DejaVu", "BU", 11) # For combo suggestion (BU = bold underline, if supported)

        self._define_colors()      # Define colors first
        self._define_fonts()       # Set fonts
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()            # Now safe to add a page (calls header)

    def _define_colors(self):
        self.colors = {
            "header_bg": (101, 67, 33),      # coffee brown
            "header_text": (255, 255, 255),  # white
            "section_bg": (234, 222, 210),   # light beige for sections
            "text": (50, 50, 50),            # dark gray
            "highlight": (192, 80, 77),      # warm red for badges
            "price": (30, 30, 30),
            "desc": (100, 100, 100),
            "badge_bg": (245, 198, 184),     # light peach for badges
        }

    def _define_fonts(self):
        self.set_font("DejaVu", size=12)

    def header(self):
        self.set_fill_color(*self.colors["header_bg"])
        self.set_text_color(*self.colors["header_text"])
        self.set_font("DejaVu", "B", 18)
        self.cell(0, 15, "Suuvai Restaurant - Kongu Nadu Menu", border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C", fill=True)
        self.ln(3)

    def section_title(self, title):
        self.set_fill_color(*self.colors["header_bg"])
        self.set_text_color(*self.colors["header_text"])
        self.set_font("DejaVu", "B", 14)
        self.cell(0, 10, f"  {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        self.ln(4)

    def add_badge(self, text):
        self.set_fill_color(*self.colors["badge_bg"])
        self.set_text_color(*self.colors["highlight"])
        self.set_font("DejaVu", "B", 8)
        badge_width = self.get_string_width(text) + 6
        y = self.get_y()
        x = self.get_x()
        self.cell(badge_width, 8, f" {text} ", border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        self.set_xy(x + badge_width + 2, y)

    def menu_item(self, name, price, desc="", badge=None):
        self.set_text_color(*self.colors["text"])
        self.set_font("DejaVu", "B", 12)
        start_x = self.get_x()
        start_y = self.get_y()

        price_text = f"Rs.{price}"
        price_width = self.get_string_width(price_text) + 4
        page_width = self.w - 2 * self.l_margin
        name_width = page_width - price_width - 10

        # Print name (can wrap multiple lines but limit width)
        self.multi_cell(name_width, 7, name, border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, max_line_height=self.font_size)
        x_after_name = self.get_x()
        y_after_name = self.get_y()

        # Print price, right aligned on same line as the first line of name
        self.set_xy(start_x + name_width + 10, start_y)
        self.set_text_color(*self.colors["price"])
        self.set_font("DejaVu", "B", 12)
        self.cell(price_width, 7, price_text, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT,)

        # Add badge if any
        if badge:
            self.set_xy(start_x + name_width + 10 + price_width + 4, start_y + 1)
            self.add_badge(badge)

        # Move to after name block to print description
        self.set_xy(start_x, y_after_name)

        if desc:
            self.set_text_color(*self.colors["desc"])
            self.set_font("DejaVu", "", 9)
            self.multi_cell(0, 5, desc)

        self.ln(3)

    def combo_suggestion(self, text):
        self.set_text_color(*self.colors["highlight"])
        self.set_font("DejaVu", "BU", 11)
        self.cell(0, 8, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(3)


def create_advanced_menu_pdf(menu_data, output_path="Suuvai_Advanced_Menu.pdf"):
    pdf = AdvancedMenuPDF()

    for section_name, dishes in menu_data.items():
        pdf.section_title(section_name)

        # Add combo suggestion in Chicken Starters section
        if section_name == "Naarthaga Kuruvi (Chicken Starters)":
            pdf.combo_suggestion("Try our “Double Happiness Combo” – Any two signature starters, Rs.480")

        for dish in dishes:
            pdf.menu_item(
                name=dish["name"],
                price=dish["price"],
                desc=dish.get("desc", ""),
                badge=dish.get("badge")
            )

    pdf.output(output_path)
    print(f"Advanced menu PDF generated: {output_path}")


if __name__ == "__main__":
    # Your menu data (from your original menu plus badges/highlights)
    menu_data = {
        "Saaru & Soups": [
            {"name": "Naatu Kozhi Saaru", "price": 110, "desc": "Country chicken broth with pepper spice", "badge": "Chef’s Pick"},
            {"name": "Veg Saaru", "price": 90, "desc": "Vegetable broth with a light Kongu touch"},
            {"name": "Soup of the Day", "price": 110, "desc": "Rotational special (e.g., Cream of Mushroom, Chicken Manchow)"}
        ],
        "Thottil Starters (Veg)": [
            {"name": "Mushroom Pallipalayam", "price": 190, "desc": "Dry saute with Kongu spices", "badge": "Best Seller"},
            {"name": "Gobi 65", "price": 160, "desc": "Classic fried cauliflower with southern masala"},
            {"name": "Paneer 65", "price": 190, "desc": "Paneer cubes tossed in spicy batter"},
            {"name": "Japan Mushroom", "price": 230, "desc": "Sweet-chilli glaze with herbs"},
        ],
        "Naarthaga Kuruvi (Chicken Starters)": [
            {"name": "Chicken Pallipalayam", "price": 260, "desc": "Signature red chilli coconut roast", "badge": "Chef’s Pick"},
            {"name": "Kaatu Kozhi Pepper Roast", "price": 270, "desc": "Crackled pepper dry roast"},
            {"name": "Milagu Chicken Varuval", "price": 250, "desc": "Pepper coated shallow fry"},
            {"name": "Japan Chicken", "price": 280, "desc": "Creamy-chilli coated juicy chicken"},
            {"name": "EAM Special 65", "price": 280, "desc": "House-style classic fry with Kongu twist", "badge": "Best Seller"},
        ],
        "Meen & Era Varuval": [
            {"name": "Curry Leaf Prawn Varuval", "price": 320, "desc": "Tossed with curry leaves and podi masala", "badge": "Most Loved"},
            {"name": "Prawn Milagu Masala", "price": 330, "desc": "Pepper-fried prawn in roasted masala"},
            {"name": "Nethili Meen Varuval", "price": 150, "desc": "Fried anchovies with crispy finish"},
        ],
        "Suuvai Virundhu - Biryani & Meals": [
            {"name": "Chicken Seeraga Samba Biryani", "price": 240, "desc": "Traditional Kongu Nadu biryani", "badge": "No.1 Seller"},
            {"name": "Egg Biryani", "price": 160, "desc": "Spiced egg biryani"},
            {"name": "Khuska Rice with Kurma", "price": 120, "desc": "Plain seeraga samba rice with veg kurma"},
            {"name": "Veg Meals", "price": 150},
            {"name": "Non-Veg Meals", "price": 175},
        ],
        "Saapadu Kuzhambu - Gravies": [
            {"name": "Naatu Kozhi Chettinad Kuzhambu", "price": 250, "desc": "Country chicken in rich chettinad gravy"},
            {"name": "Mutton Kola Urundai Kuzhambu", "price": 260, "desc": "Spiced meatballs in thick gravy"},
            {"name": "Pepper Chicken Kuzhambu", "price": 260, "desc": "Spicy and rustic pepper curry"},
            {"name": "Paneer Butter Kuzhambu", "price": 230, "desc": "Creamy tomato and butter paneer curry"},
            {"name": "Mushroom Masala", "price": 190, "desc": "Kongu-style mushroom gravy"},
        ],
    }

    create_advanced_menu_pdf(menu_data)

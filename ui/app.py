import customtkinter as ctk
from PIL import Image
import os

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

# TODO - get larger icons
# This is to get the base path (of the project) and use that to get the directory of the assets folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


def load_icon(icon_name: str, size=(24, 24)):
    """This function automatically loads the black and white versions any icon from my assets file"""
    return ctk.CTkImage(
        light_image=Image.open(os.path.join(ASSETS_DIR, f"{icon_name} (black).png")),
        dark_image=Image.open(os.path.join(ASSETS_DIR, f"{icon_name} (white).png")),
        size=size,
    )


class HeaderFrame(ctk.CTkFrame):
    def __init__(self, master, h1_font, body_font, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        # HeaderFrame grid
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)  # Left side can expand
        self.grid_columnconfigure(
            1, weight=0
        )  # Right side doesn't expand

        # Add widgets inside the grid
        self.welcome_label = ctk.CTkLabel(
            self, text="Welcome, User", font=h1_font
        )  # TODO - Create a user_name attribute, and use it to update this label
        self.welcome_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        settings_img = load_icon("settings")
        self.settings_btn = ctk.CTkButton(
            self,
            text="",
            image=settings_img,
            width=40,
            height=40,
            fg_color="transparent", #This is the color of the button
            hover_color=("gray80", "gray25"),
        ) 
        self.settings_btn.grid(
            row=0, column=1, padx=20, pady=10, sticky="e"
        )  # Sticks to the east, since it is on the right side


class ModeFrame(ctk.CTkFrame):
    def __init__(self, master, h2_font, **kwargs):
        super().__init__(master, **kwargs)
        # 0 x 2 grid for study and exam mode
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure((0, 1), weight=1)  # For the label and the mode picker

        self.title_label = ctk.CTkLabel(self, text="Choose a Mode", font=h2_font)
        self.title_label.grid(
            row=0, column=0, columnspan=2, pady=(15, 5) #Top padding, and buttom padding
        )  

        study_img = load_icon("menu_book_for_study", size=(30, 30))
        exam_img = load_icon("timer", size=(30, 30))

        self.study_btn = ctk.CTkButton(
            self,
            text="Study Mode\n   (No timer, more casual)",
            image=study_img,
            font=h2_font,
            height=60,
            corner_radius=32,
        )  
        self.study_btn.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))

        self.exam_btn = ctk.CTkButton(
            self,
            text="Exam Mode\n (Timed to simulate exam conditions)",
            image=exam_img,
            font=h2_font,
            height=60,
            corner_radius=32,
        )  
        self.exam_btn.grid(
            row=1, column=1, sticky="nsew", padx=20, pady=(10, 20)
        )  


class SubjectFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, h2_font, **kwargs):
        super().__init__(
            master, fg_color=("gray85", "gray15"), corner_radius=15, **kwargs
        )
        self.grid_columnconfigure((0, 1), weight=1)

        self.title_label = ctk.CTkLabel(self, text="Select a Subject", font=h2_font)
        self.title_label.grid(row=0, column=0, columnspan=4, pady=(10, 15))

        # Subject data, icons and colors
        self.subjects = [
            {"name": "Mathematics", "icon": "calculate", "color": "#3B82F6"},
            {"name": "English", "icon": "history_edu", "color": "#F59E0B"},
            {"name": "Physics", "icon": "physics", "color": "#8B5CF6"},
            {"name": "Chemistry", "icon": "chemistry", "color": "#10B981"},
            {"name": "Biology", "icon": "biology", "color": "#14B8A6"},
            {"name": "Geography", "icon": "geography", "color": "#EAB308"},
            {"name": "Economics", "icon": "economics", "color": "#F43F5E"},
            {"name": "Civic Edu.", "icon": "civic", "color": "#64748B"},
        ]

        # This loop creates a button for each subject in subjects
        for index, item in enumerate(self.subjects):
            row_pos = (
                index // 2
            ) + 1  # The row position of an item is the integer part or the division by the number of columns (since the number of columns is always 2, and the number of rows can change). I am adding by 1, since row 0 is taken up by the label
            col_pos = (
                index % 2
            )  # The column position is the remainder (CR - column->remainder)
            icon_image = load_icon(item["icon"], size=(28, 28))
            btn = ctk.CTkButton(
                self,
                text=item["name"],
                image=icon_image,
                font=h2_font,
                height=70,
                corner_radius=10,
                fg_color=("gray75", "gray20"),
                hover_color=item["color"],
                text_color=("black", "white"),
                compound="top",
            )
            btn.grid(row=row_pos, column=col_pos, padx=10, pady=10, sticky='nsew') 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NECO Exam Simulator")
        self.geometry("1000x600")
        self.minsize(800, 600)
        self.h1 = ctk.CTkFont("Segoe UI", size=28, weight="bold")
        self.h2 = ctk.CTkFont("Segoe UI", size=18, weight="bold")
        self.body = ctk.CTkFont("Segoe UI", size=15, weight="normal")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header row
        self.grid_rowconfigure(1, weight=1)  # Mode row
        self.grid_rowconfigure(2, weight=2)  # Subject row
        self.grid_rowconfigure(3, weight=0)  # Start button row
        
        # Header widget - I'm using a frame for this
        self.header = HeaderFrame(self, h1_font=self.h1, body_font=self.body)
        self.header.grid(
            row=0, column=0, padx=10, sticky="nsew"
        )  # Position on the window
        
        # Modes widget - I'm also using a frame for this
        self.modes = ModeFrame(self, h2_font=self.h2)
        self.modes.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Subjects widget - This is a scrollable frame 
        self.subjects = SubjectFrame(self, h2_font=self.h2)
        self.subjects.grid(row=2, column=0, padx=20, pady=(10, 20), sticky='nsew')

if __name__ == "__main__":
    app = App()
    app.mainloop()

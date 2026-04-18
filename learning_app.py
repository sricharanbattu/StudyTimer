import customtkinter as ctk

# We inherit from ctk.CTk to gain all the window-making powers
class LearningApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Config ---
        self.title("Learning App")
        self.geometry("450x700")
        ctk.set_appearance_mode("dark")
        
        # --- The Main Container ---
        # This acts as a layout 'anchor' providing margins for all future content
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(pady=20, padx=20, fill="both", expand=True)

        # Placeholder element to verify the frame is active
        self.status_label = ctk.CTkLabel(self.main_container, text="Frame Initialized")
        self.status_label.pack(pady=20)

        # --- App State ---
        # This list holds the options for your dropdown menu
        self.topics = ["Python", "Linux", "DevOps"]

        # The Dropdown (OptionMenu)
        # 'values' tells the menu to use the list we created above
        self.topic_menu = ctk.CTkOptionMenu(
            self.main_container,
            values=self.topics,
            width=200
        )
        self.topic_menu.pack(pady=20)



if __name__ == "__main__":
    app = LearningApp()
    app.mainloop() # This starts the UI event loop
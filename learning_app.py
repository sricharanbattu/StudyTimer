import customtkinter as ctk

# We create a 'class' so that our app can keep track of its own data later
class LearningApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Basic window settings
        self.title("Learning App")
        self.geometry("450x700")
        
        # The Main Container
        # This is an invisible box that holds everything we will add later.
        # It provides 'padding' (space) so things don't touch the window edges.
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(pady=20, padx=20, fill="both", expand=True)

        # A placeholder label just so we can see the window isn't empty
        self.placeholder = ctk.CTkLabel(self.main_container, text="Frame Initialized")
        self.placeholder.pack(pady=20)

if __name__ == "__main__":
    # This creates the app object and starts the infinite loop
    app = LearningApp()
    app.mainloop()
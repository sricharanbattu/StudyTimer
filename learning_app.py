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

        # --- Topic Selection Row (Horizontal) ---
        self.selection_row = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.selection_row.pack(pady=10, fill="x")

        # 1. Remove Button (Far Right)
        self.remove_btn = ctk.CTkButton(
            self.selection_row, text="-", width=35, 
            fg_color="#922", hover_color="#722", 
            command=self.remove_topic
        )
        self.remove_btn.pack(side="left", padx=2)

       

        # 2. The Dropdown (Middle - set to expand)
        self.topic_menu = ctk.CTkOptionMenu(
            self.selection_row,
            values=self.topics,
            width=200
        )
        self.topic_menu.pack(side="left", padx=10, expand=True, fill="x")

         # 3. Add Button (Far Left)
        self.add_btn = ctk.CTkButton(
            self.selection_row, text="+", width=35, command=self.add_topic
        )
        self.add_btn.pack(side="left", padx=2)

        
    def add_topic(self):
        # This creates a pop-up window to ask for text
        dialog = ctk.CTkInputDialog(text="Enter new topic:", title="Add Topic")
        new_topic = dialog.get_input()

        if new_topic: # Only proceed if the user didn't hit 'Cancel'
            self.topics.append(new_topic) # Update the 'Brain'
            self.topic_menu.configure(values=self.topics) # Update the UI
            print(f"Added: {new_topic}")


    def remove_topic(self):
        current = self.topic_menu.get()
        if current in self.topics:
            self.topics.remove(current)
            # Refresh the dropdown with the new list
            self.topic_menu.configure(values=self.topics)
            # Reset the dropdown to the first item (if any exist)
            if self.topics:
                self.topic_menu.set(self.topics[0])
            else:
                self.topic_menu.set("No Topics")



if __name__ == "__main__":
    app = LearningApp()
    app.mainloop() # This starts the UI event loop
import customtkinter as ctk
import os
import json
from plyer import notification

# --- Custom Popup Dialog for Topic & Time ---
class TopicDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Add Topic", initial_name="", initial_time="25"):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x220")
        self.resizable(False, False)
        
        # Ensure it stays on top of the main window
        self.transient(parent)
        self.result = None

        # Layout configuration
        self.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self, text="Topic Name:").grid(row=0, column=0, padx=20, pady=15)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.insert(0, initial_name)
        self.name_entry.grid(row=0, column=1, padx=20, pady=15)

        ctk.CTkLabel(self, text="Minutes:").grid(row=1, column=0, padx=20, pady=10)
        self.time_entry = ctk.CTkEntry(self)
        self.time_entry.insert(0, initial_time)
        self.time_entry.grid(row=1, column=1, padx=20, pady=10)

        self.save_btn = ctk.CTkButton(self, text="Save Settings", command=self.on_save)
        self.save_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Stability Fixes
        self.lift()            
        self.wait_visibility() 
        self.grab_set()        

    def on_save(self):
        name = self.name_entry.get().strip()
        try:
            time = int(self.time_entry.get())
            if name and 0 < time < 181:
                self.result = (name, time)
                self.destroy()
            else:
                self.title("Invalid Input!")
        except ValueError:
            self.title("Check Minutes!")

# --- Main Application ---
class LearningApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Learning Lab")
        self.geometry("450x650")
        ctk.set_appearance_mode("dark")

        # --- Load Data ---
        self.topics_data = self.load_config()
        if not self.topics_data:
            self.topics_data = {"Python": 25}
        
        self.current_topic = list(self.topics_data.keys())[0]
        self.study_time = self.topics_data[self.current_topic]
        
        # --- Timer Logic State ---
        self.timer_running = False 
        self.time_left = self.study_time * 60
        self.timer_id = None

        # --- Main Layout ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(pady=20, padx=20, fill="both", expand=True)

        self.status_label = ctk.CTkLabel(self.main_container, text="Ready to Start", text_color="gray")
        self.status_label.pack(pady=(0, 10))

        # --- Topic Control Row ---
        self.selection_row = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.selection_row.pack(pady=10, fill="x")

        self.remove_btn = ctk.CTkButton(self.selection_row, text="-", width=35, fg_color="#922", command=self.remove_topic)
        self.remove_btn.pack(side="left", padx=2)

        self.topic_menu = ctk.CTkOptionMenu(self.selection_row, values=list(self.topics_data.keys()), command=self.handle_topic_switch)
        self.topic_menu.pack(side="left", padx=5, expand=True, fill="x")
        self.topic_menu.set(self.current_topic)

        self.edit_btn = ctk.CTkButton(self.selection_row, text="Edit", width=45, fg_color="#555", command=self.edit_topic)
        self.edit_btn.pack(side="left", padx=2)

        self.add_btn = ctk.CTkButton(self.selection_row, text="+", width=35, command=self.add_topic)
        self.add_btn.pack(side="left", padx=2)

        # --- Display ---
        self.timer_label = ctk.CTkLabel(self.main_container, text=f"{self.study_time:02d}:00", font=("Roboto", 80, "bold"))
        self.timer_label.pack(pady=40)

        # --- One-Time Extension Input ---
        self.extra_time_row = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.extra_time_row.pack(pady=10)
        ctk.CTkLabel(self.extra_time_row, text="Add Extra:", text_color="gray").pack(side="left", padx=5)
        self.extra_entry = ctk.CTkEntry(self.extra_time_row, placeholder_text="Mins", width=60)
        self.extra_entry.pack(side="left", padx=5)

        # --- Primary Controls ---
        self.controls_row = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.controls_row.pack(pady=10, fill="x")

        self.start_btn = ctk.CTkButton(self.controls_row, text="START", font=("Roboto", 16, "bold"), fg_color="#28a745", height=50, command=self.toggle_timer)
        self.start_btn.pack(side="left", padx=(0, 10), expand=True, fill="x")

        self.reset_btn = ctk.CTkButton(self.controls_row, text="RESET", width=90, height=50, fg_color="transparent", border_width=2, text_color="gray", command=self.reset_timer)
        self.reset_btn.pack(side="left")

    # --- Logic Methods ---

    def get_extra_seconds(self):
        """Reads and clears the extra time box."""
        try:
            val = self.extra_entry.get().strip()
            if val:
                seconds = int(val) * 60
                self.extra_entry.delete(0, 'end')
                return seconds
            return 0
        except ValueError:
            return 0

    def handle_topic_switch(self, selected_topic):
        if self.timer_running:
            self.topic_menu.set(self.current_topic)
            return
        self.current_topic = selected_topic
        self.study_time = self.topics_data.get(selected_topic, 25)
        self.time_left = self.study_time * 60
        self.timer_label.configure(text=f"{self.study_time:02d}:00")

    def toggle_timer(self):
        # Check for additive extra time before starting or while paused
        extra_sec = self.get_extra_seconds()
        if extra_sec > 0:
            self.time_left += extra_sec
            mins, secs = divmod(self.time_left, 60)
            self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
            self.status_label.configure(text=f"Added {extra_sec//60}m to session", text_color="#3498DB")

        # Handle starting from a finished state (00:00)
        if not self.timer_running and self.time_left == 0 and extra_sec == 0:
            self.time_left = self.study_time * 60
            mins, secs = divmod(self.time_left, 60)
            self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")

        self.timer_running = not self.timer_running
        if self.timer_running:
            self.start_btn.configure(text="PAUSE", fg_color="#E67E22")
            self.update_timer()
        else:
            self.start_btn.configure(text="START", fg_color="#28a745")

    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            mins, secs = divmod(self.time_left, 60)
            self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
            self.timer_id = self.after(1000, self.update_timer)
        elif self.time_left <= 0:
            self.timer_running = False
            self.start_btn.configure(text="START", fg_color="#28a745")
            self.status_label.configure(text="Time's up!", text_color="green")
            # THE TRIGGER
            self.send_completion_notification()

    def reset_timer(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        
        self.timer_running = False
        
        # Reset to base preset + any extra provided
        extra_sec = self.get_extra_seconds()
        self.time_left = (self.study_time * 60) + extra_sec
        
        mins, secs = divmod(self.time_left, 60)
        self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
        
        self.start_btn.configure(text="START", fg_color="#28a745")
        self.status_label.configure(text="Reset with Extension" if extra_sec else "Timer Reset", text_color="gray")

    def add_topic(self):
        dialog = TopicDialog(self)
        self.wait_window(dialog)
        if dialog.result:
            name, time = dialog.result
            self.topics_data[name] = time
            self.update_ui_after_change(name)

    def edit_topic(self):
        if self.timer_running:
            self.status_label.configure(text="Pause before editing!", text_color="orange")
            return
        old_name = self.topic_menu.get()
        dialog = TopicDialog(self, title="Edit Course", initial_name=old_name, initial_time=str(self.topics_data[old_name]))
        self.wait_window(dialog)
        if dialog.result:
            new_name, new_time = dialog.result
            if new_name != old_name: del self.topics_data[old_name]
            self.topics_data[new_name] = new_time
            self.update_ui_after_change(new_name)

    def remove_topic(self):
        choice = self.topic_menu.get()
        if choice in self.topics_data:
            del self.topics_data[choice]
            if not self.topics_data: self.topics_data = {"Python": 25}
            self.update_ui_after_change(list(self.topics_data.keys())[0])

    def update_ui_after_change(self, target_topic):
        self.topic_menu.configure(values=list(self.topics_data.keys()))
        self.topic_menu.set(target_topic)
        self.handle_topic_switch(target_topic)
        self.save_config()

    def load_config(self):
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f: return json.load(f)
            except: return {}
        return {}

    def save_config(self):
        with open("config.json", "w") as f:
            json.dump(self.topics_data, f, indent=4)

    def send_completion_notification(self):
        """Triggers a system-level popup notification."""
        try:
            notification.notify(
                title="Learning Lab - Session Complete!",
                message=f"You finished your session for {self.current_topic}.",
                app_name="Learning Lab",
                timeout=10
            )
        except Exception as e:
            print(f"Notification Error: {e}")

    

if __name__ == "__main__":
    app = LearningApp()
    app.mainloop()
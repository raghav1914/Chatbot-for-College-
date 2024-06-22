from tkinter import *
from chat import get_response_from_rasa
import time

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ChatApplication:
    
    def __init__(self):  
        self.window = Tk()
        self._setup_main_window()
        
    def run(self):
        self.window.mainloop()
        
    def _setup_main_window(self):
        self.window.title("Initiate Your Bot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=550, height=550, bg=BG_COLOR)  # Increased width to 550
        
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome to College's Chatbot!", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        
        line = Label(self.window, width=500, bg=BG_GRAY)  # Increased width to 500
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5, wrap=WORD)  # Set wrap to WORD
        self.text_widget.place(relheight=0.745, relwidth=0.974, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        scrollbar = Scrollbar(self.window)
        scrollbar.place(relheight=0.745, relx=0.974, rely=0.08)
        scrollbar.configure(command=self.text_widget.yview)
        
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        self.send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_send_clicked())
        self.send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
     
    def _on_enter_pressed(self, event):
        self._on_send_clicked()
        
    def _on_send_clicked(self):
        msg = self.msg_entry.get()
        self._insert_message(msg, "User")
        self.msg_entry.delete(0, END)
        
        response = get_response_from_rasa(msg)
        self._insert_message(response, "Bot")
        
        # Rotate the send button
        self._rotate_send_button()
        
    def _rotate_send_button(self):
        for i in range(36):
            self.send_button.place_configure(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22,
                                             angle=i * 10)
            self.send_button.update()
            time.sleep(0.03)
        
    def _insert_message(self, msg, sender):
        if not msg:
            return
        
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
        
        # Animation: Fading effect
        self.text_widget.update()  # Update the text widget
        for i in range(10):
            self.text_widget.after(50 * i, lambda: self.text_widget.config(fg=self._fade_color(TEXT_COLOR, 10-i)))
            
    def _fade_color(self, color, factor):
        """Fade a color by a specified factor."""
        r = int(color[1:3], 16) - factor
        g = int(color[3:5], 16) - factor
        b = int(color[5:], 16) - factor
        r = min(max(0, r), 255)
        g = min(max(0, g), 255)
        b = min(max(0, b), 255)
        return f"#{r:02X}{g:02X}{b:02X}"

if __name__ == "__main__":
    app = ChatApplication()
    app.run()


import customtkinter 
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Password Strength Checker")
        self.geometry("400x400")
        self.grid_columnconfigure(0, weight=1)
        self.Title = customtkinter.CTkLabel(self, width=40, height=30, text="Password Checker")
        self.Title.grid(row=0, column=0, padx=20, pady=20)
        self.entry = customtkinter.CTkEntry(self, width=60, height=30, placeholder_text="Enter password", show='*', text_color="black")
        self.entry.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.entrycopy = customtkinter.CTkTextbox(self, width=60, height=30)
        self.entrycopy.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
            

        #
        # self.grid_rowconfigure((0, 1), weight=1)
        
     




app = App()

    
password = ""
score = 0


def main_loop():
    password = app.entry.get()
    app.entrycopy.delete("0.0", "end")
    app.entrycopy.insert("0.0", password)
    score = 10 * len(password)
    if score < 40:
        app.entry.configure(fg_color="red3")
    elif score < 60:
        app.entry.configure(fg_color="orange red")
    elif score < 80:
        app.entry.configure(fg_color="gold")
    elif score >= 80:
        app.entry.configure(fg_color="chartreuse2")
    app.after(10, main_loop)
app.after(1, main_loop)
app.mainloop()

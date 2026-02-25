import customtkinter 
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Password Strength Checker")
        self.geometry("400x400")
        self.grid_columnconfigure(0, weight=1)
        self.score = 0
        #var that contains whatever is in the textbox at the moment. Triggers on update
        self.password = customtkinter.StringVar()
        self.password.trace_add('write', self.updateScore)

        #setting up gui stuff
        self.Title = customtkinter.CTkLabel(self, width=40, height=30, text="Password Checker")
        self.Title.grid(row=0, column=0, padx=20, pady=20)
        self.entry = customtkinter.CTkEntry(self, width=60, height=30, placeholder_text="Enter password", textvariable=self.password, show='*', text_color="black")
        self.entry.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.entrycopy = customtkinter.CTkTextbox(self, width=60, height=30)
        self.entrycopy.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        #opening files to compare password to later
        self.pwFile = open('./lists/100k-most-used-passwords-NCSC.txt', encoding="utf-8")
        self.engFile = open('./lists/words.txt')

        #label to show realtime score
        self.scoreLabel = customtkinter.CTkLabel(self, width=20, height=20)
        self.scoreLabel.grid(row=4, column=0, padx=20, pady=20, sticky='ew')
        
    def updateScore(self, *args):
        self.score = 0
        self.entrycopy.delete("0.0", "end")
        self.entrycopy.insert("0.0", self.password.get())
        self.score += self.passwordLengthCheck()
        self.score += self.isEnglish()
        self.score += self.isCommonPW()
        if self.score < 40:
            self.entry.configure(fg_color="red3")
        elif self.score < 60:
            self.entry.configure(fg_color="orange red")
        elif self.score < 80:
            self.entry.configure(fg_color="gold")
        elif self.score >= 80:
            self.entry.configure(fg_color="chartreuse2")
        self.scoreLabel.configure(text=str(self.score))


    def passwordLengthCheck(self):
        if len(self.password.get()) < 8:
            return -50
        elif len(self.password.get()) < 12:
            return 10
        elif len(self.password.get()) < 16:
            return 15
        else:
            return 20
        
    #These functions do not seem to be working... 
    #I guess there is a type mismatch or something where "password" != "password" somehow
    def isEnglish(self):
        if str(self.password.get()) in self.engFile:
            return -10
        return 5
    
    def isCommonPW(self):
        if str(self.password.get()) in self.pwFile:
            return -500
        return 5
        

app = App()
app.mainloop()


#Run the PW through this dict to see if any english words can be found. Returns None if char not in dictionary.
specialDict = {
    '@' : 'a',
    '$' : 's',
    '0' : 'o',
    '!' : 'i',
    '4' : 'a',
    '3' : 'e',
    '6' : 'g',
    "}{": 'x',
    "13" : 'b',
    '5' : 's'
}






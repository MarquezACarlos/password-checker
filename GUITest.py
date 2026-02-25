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
        #Prevents whitespace 
        vcmd = (self.register(self.noWhitespace), "%P")
        self.entry.configure(validate="key", validatecommand=vcmd)
        self.entry.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        #Show Password to user
        self.entrycopy = customtkinter.CTkTextbox(self, width=60, height=30)
        self.entrycopy.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        #Makes it read-only + skip tab focus
        self.entrycopy.configure(state="disabled", takefocus=0)

        #opening files to compare password to later
        #Files needed to be opened as a set not as a list
        with open('./lists/100k-most-used-passwords-NCSC.txt', encoding="utf-8") as f:
            self.commonPasswords = set(line.strip().lower() for line in f if line.strip())

        with open('./lists/words.txt', encoding="utf-8") as f:
            self.englishWords = set(line.strip().lower() for line in f if line.strip())

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
        
    #check for english words - Working
    def isEnglish(self):
        #Get the password and make it lowercase
        pw = self.password.get().lower()
        # check any word length >= 4 to make sure "in" or "as" don't count
        for w in self.englishWords:
            if len(w) >= 4 and w in pw:
                return -500
        return 5

    #check for common passwords
    def isCommonPW(self):
        #Get the password and make it lowercase and stripping whitespace
        pw = self.password.get().strip().lower()
        #Chekcs to see if the password is in the set of common passwords
        if pw in self.commonPasswords:
            return -500
        return 5
        
    #check for whitespace when typing password
    def noWhitespace(self, proposed_text):
        # Reject if any whitespace exists
        if any(char.isspace() for char in proposed_text):
            return False
        return True

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






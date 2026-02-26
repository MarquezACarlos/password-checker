import customtkinter
import string
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

        #Setting up GUI stuff
        self.Title = customtkinter.CTkLabel(self, width=40, height=30, text="Password Checker")
        self.Title.grid(row=0, column=0, padx=20, pady=20)
        self.entry = customtkinter.CTkEntry(self, width=60, height=30, placeholder_text="Enter password", textvariable=self.password, show='*', text_color="black")
        #Prevents whitespace 
        vcmd = (self.register(self.noWhitespace), "%P")
        self.entry.configure(validate="key", validatecommand=vcmd)
        self.entry.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        #Shows password to user in a read-only textbox
        self.passwordDisplay = customtkinter.StringVar()
        self.entrycopy = customtkinter.CTkEntry(self, width=60, height=30, textvariable=self.passwordDisplay, state="readonly")
        self.entrycopy.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        self.entrycopy.configure(takefocus=0)
        self.suggestions = customtkinter.CTkTextbox(self, width=100, height=100, state="normal")
        self.suggestions.grid(row=4, column=0, sticky='ew')
        self.suggestionList = []

        #Opening files to compare password to later
        #Files needed to be opened as a set not as a list
        with open('./lists/100k-most-used-passwords-NCSC.txt', encoding="utf-8") as f:
            self.commonPasswords = set(line.strip().lower() for line in f if line.strip())

        with open('./lists/words.txt', encoding="utf-8") as f:
            self.englishWords = set(line.strip().lower() for line in f if line.strip())

        #label to show realtime score
        self.scoreLabel = customtkinter.CTkLabel(self, width=20, height=20)
        self.scoreLabel.grid(row=5, column=0, padx=20, pady=20, sticky='ew')


    def updateSuggestions(self, *args):
        self.suggestions.delete("0.0", "end")
        for i in range(len(self.suggestionList)):
            self.suggestions.insert("0.0",self.suggestionList[i])
        self.suggestionList.clear()
        
    def updateScore(self, *args):
        #Displays the password in the read-only textbox
        pw = self.password.get()
        self.passwordDisplay.set(pw)

        self.score = 0
        self.score += self.passwordLengthCheck()
        self.score += self.isEnglish()
        self.score += self.isCommonPW()
        self.score += self.checkCapitalization()
        self.score += self.checkSpecialCharacters()

        if self.score < 40:
            self.entry.configure(fg_color="red3")
        elif self.score < 60:
            self.entry.configure(fg_color="orange red")
        elif self.score < 80:
            self.entry.configure(fg_color="gold")
        elif self.score >= 80:
            self.entry.configure(fg_color="chartreuse2")
        self.scoreLabel.configure(text=str(self.score))
        self.updateSuggestions(self)

    #Checks the length of the password
    def passwordLengthCheck(self):
        if self.password.get() == "":
            self.suggestionList.append("Strong password suggestions will appear here!\n")
            return 0

        if len(self.password.get()) < 8:
            self.suggestionList.append("Passwords should be no shorter than 8 characters!\n")
            return -50
        elif len(self.password.get()) < 12:
            self.suggestionList.append("Medium passwords should be at least 12 characters!\n")
            return 10
        elif len(self.password.get()) < 16:
            self.suggestionList.append("The strongest passwords have more than 16 characters!\n")
            return 15
        else:
            return 20
        
    #check for english words
    def isEnglish(self):
        if self.password.get() == "":
                    return 0

        #Get the password and make it lowercase
        pw = self.password.get().lower()
        # check any word length >= 4 to make sure "in" or "as" don't count
        for w in self.englishWords:
            if len(w) >= 4 and w in pw:
                self.suggestionList.append("Avoid using english words in your password!\n")
                return -500
        return 5

    #check for common passwords
    def isCommonPW(self):
        if self.password.get() == "":
            return 0

        #Get the password and make it lowercase and stripping whitespace
        pw = self.password.get().strip().lower()
        #Chekcs to see if the password is in the set of common passwords
        if pw in self.commonPasswords:
            self.suggestionList.append("This is a common password!!\n")
            return -500
        return 5
        
    #check for whitespace when typing password
    def noWhitespace(self, proposed_text):
        # Reject if any whitespace exists
        if any(char.isspace() for char in proposed_text):
            return False
        return True

    #Checks for capitalization and returns a score based on the presence of uppercase and lowercase letters
    def checkCapitalization(self):
        pw = self.password.get()

        lower = any(c.islower() for c in pw)
        upper = any(c.isupper() for c in pw)

        if not lower and not upper:
            return 0
        
        if lower and upper:
            return 20
        
        if lower or upper:
            self.suggestionList.append("Passwords should contain lower and uppercase characters\n")
            return -20
        
        return 0

    #Checks for special characters and returns a score based on the presence of special characters
    def checkSpecialCharacters(self):
        pw = self.password.get()
        specialCharacters = set(string.punctuation)

        if not pw:
            return 0

        specialPositions = [i for i, c in enumerate(pw) if c in specialCharacters]
        if not specialPositions:
            return 0

        n = len(pw)
        inMiddle = [i for i in specialPositions if not (i < 2 or i >= n - 2)]

        # Only edge specials
        if len(inMiddle) == 0:
            self.suggestionList.append("Special characters shouldn't only be at the beginning or end of a password!\n")
            return 5

        # At least one middle special
        if len(inMiddle) == 1:
            return 10

        # Two or more middle specials
        return 15
    
app = App()
app.mainloop()








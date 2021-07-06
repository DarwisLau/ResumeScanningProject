from tkinter import*
from tkinter.font import Font



#Function executed when Search Button is pressed
def selectOneFromActiveRecords ():

    """Function to select an active applicant's information from database and return the information to the form.
       This function does not have specific input parameters, but the function will get the applicant's IC number from the IC search panel (expected string).
       Output is either applicant's information (displayed in the form), or a message box that shows the error message (if there is any error message) from the database software. If the applicant does not exist in the
       database, the form will be left blank."""


    #Set the variables
    dataICNumber = entryIC.get()
    from ValidateData import standardise_applicantICNumber
    #ValidateData contains code for data validation.
    #It is used to remove "-" or space from IC number before it is used to query applicant's information in the database.
    #Source: Part of this project
    dataICNumber = standardise_applicantICNumber (dataICNumber)
    dataName = None
    dataEmail = None
    dataContactNumber = None
    dataPositionApplied = None
    dataLanguageWritten = None
    dataLanguageSpoken = None
    dataProgrammingLanguage = None
    dataPastWorkExperience = None
    dataPastWorkDuration = None
    dataHighestEducation = None
    dataSoftSkills = None


    #Select from database
    import mysql.connector
    #mysql.conector is a driver to access mySQL database.
    #It is used to query applicant's information in the database, and get the result of the query.
    #Source: It is installed together when installing the mySQL software using mySQL installer. Source of the mySQL installer: https://dev.mysql.com/downloads/installer/
    database = mysql.connector.connect (
        host = "localhost",
        user = "Resume_Scanning_Project_Admin",
        password = "AbcdeF,123456!",
        database = "ResumeScanningProject"
    )
    databaseCursor = database.cursor()
    try:
        result = databaseCursor.callproc ("SelectOneFromActiveRecords", (dataICNumber, dataName, dataEmail, dataContactNumber, dataPositionApplied, dataLanguageWritten, dataLanguageSpoken, dataProgrammingLanguage, dataPastWorkExperience, dataPastWorkDuration, dataHighestEducation, dataSoftSkills))
            
        #Display in the form

        #Name
        entryName.delete(0, END)
        if result[1] is not None:
            entryName.insert(0, result[1])

        #Email address
        entryEmail.delete(0, END)
        if result[2] is not None:
            entryEmail.insert(0, result[2])

        #Contact number
        entryContact.delete(0, END)
        if result[3] is not None:
            entryContact.insert(0, result[3])

        #Position applied
        entryPosition.delete(0, END)
        if result[4] is not None:
            entryPosition.insert(0, result[4])

        #Language (written)
        entryLangWrite.delete(0, END)
        if result[5] is not None:
            entryLangWrite.insert(0, result[5])

        #Language (spoken)
        entryLangSpoke.delete(0, END)
        if result[6] is not None:
            entryLangSpoke.insert(0, result[6])

        #Programming language
        entryCodeLang.delete(0, END)
        if result[7] is not None:
            entryCodeLang.insert(0, result[7])

        #Past work experience
        entryWorkExp.delete(0, END)
        if result[8] is not None:
            entryWorkExp.insert(0, result[8])

        #Past work duration
        entryDuration.delete(0, END)
        if result[9] is not None:
            entryDuration.insert(0, result[9])

        #Highest education
        entryHighestEdu.delete(0, END)
        if result[10] is not None:
            entryHighestEdu.insert(0, result[10])

        #Soft skills

    except mysql.connector.Error as errorMessage:
        from tkinter import messagebox
        messagebox.showinfo("Error", errorMessage)
    finally:
        databaseCursor.close()
        database.close()



#Function executed when Save Edit Button is pressed
def updateRecord ():

    """Function to update record in the database.
       This function does not have specific input parameters, but the functio will get the applicant's information from the form.
       Output is a message box that shows the message "Record successfully edited" if the update was successful, or promts error message if the update was not successful."""
   

    #Validate data and set the variables
    from ValidateData import standardise_applicantICNumber, validate_applicantName, standardise_applicantEmail, validate_applicantEmail, standardise_applicantContactNumber, validate_applicantContactNumber, validate_positionApplied, validate_otherData
    #ValidateData contains code for data validation.
    #It is used to remove "-" and space from IC number and make sure that the other data is valid before it is updated in the database.
    #Source: Part of this project
    from tkinter import messagebox
    
    #IC number
    dataICNumber = entryIC.get()
    dataICNumber = standardise_applicantICNumber (dataICNumber)

    #Name
    dataName = entryName.get()
    errorMessage = validate_applicantName (dataName)
    if errorMessage is not None:
        messagebox.showinfo("Error", errorMessage)
        return

    #Email address
    dataEmail = entryEmail.get()
    dataEmail = standardise_applicantEmail (dataEmail)
    errorMessage = validate_applicantEmail (dataEmail)
    if errorMessage is not None:
        messagebox.showinfo("Error", errorMessage)
        return

    #Contact number
    dataContactNumber = entryContact.get()
    dataContactNumber = standardise_applicantContactNumber (dataContactNumber)
    errorMessage = validate_applicantContactNumber (dataContactNumber)
    if errorMessage is not None:
        messagebox.showinfo("Error", errorMessage)
        return

    #Position applied
    dataPositionApplied = entryPosition.get()
    errorMessage = validate_positionApplied (dataPositionApplied)
    if errorMessage is not None:
        messagebox.showinfo("Error", errorMessage)
        return

    #Language(s) (written), language(s) (spoken), programming language(s), past work experience, past work duration, highest education, soft skills
    dataLanguageWritten = entryLangWrite.get()
    dataLanguageSpoken = entryLangSpoke.get()
    dataProgrammingLanguage = entryCodeLang.get()
    dataPastWorkExperience = entryWorkExp.get()
    dataPastWorkDuration = entryDuration.get()
    dataHighestEducation = entryHighestEdu.get()
    #Soft skills
    errorMessage = validate_otherData (dataLanguageWritten, dataLanguageSpoken, dataProgrammingLanguage, dataPastWorkExperience, dataPastWorkDuration, dataHighestEducation)
    if errorMessage is not None:
        messagebox.showinfo("Error", errorMessage)
        return

    outMessage = None


    #Update in database
    import mysql.connector
    #mysql.conector is a driver to access mySQL database.
    #It is used to update applicant's information in the database, and check whether the update was successful or not.
    #Source: It is installed together when installing the mySQL software using mySQL installer. Source of the mySQL installer: https://dev.mysql.com/downloads/installer/
    database = mysql.connector.connect (
        host = "localhost",
        user = "Resume_Scanning_Project_Admin",
        password = "AbcdeF,123456!",
        database = "ResumeScanningProject"
    )
    databaseCursor = database.cursor()
    try:
        returnMessage = databaseCursor.callproc ("UpdateRecord", (dataName, dataEmail, dataContactNumber, dataLanguageWritten, dataLanguageSpoken, dataProgrammingLanguage, dataPastWorkExperience, dataPastWorkDuration, dataHighestEducation, dataICNumber, dataPositionApplied, outMessage))
        database.commit()
        if returnMessage[11] == "Record successfully edited":
            messagebox.showinfo("", returnMessage[11])
        else:
            messagebox.showinfo("Error", returnMessage[11])
    except mysql.connector.Error as errorMessage:
        messagebox.showinfo("Error", errorMessage)
    finally:
        databaseCursor.close()
        database.close()



#Window size, title
root = Tk()
root.geometry('1920x1080')
root.maxsize(1920,1080)
root.title("Edit Record")

#Define image for Background and button
bg= PhotoImage(file='D:/GUI Image/background.png')
SaveEditButtonImg =PhotoImage(file='D:/GUI Image/save edit button.png')
BackToMenuButtonImg =PhotoImage(file='D:/GUI Image/Back to menu.png')
SearchButtonImg = PhotoImage(file='D:/GUI Image/search button.png')

#Background
my_canvas = Canvas(root,width=1920,height=1080)
my_canvas.pack(fill='both', expand=True)
my_canvas.configure(highlightthickness=0)
my_canvas.create_image(0,0, image=bg, anchor="nw")

#Defining our font
Header1Font = Font(family="Montserrat", size=30, weight="normal",slant="roman",underline=0,overstrike=0)
Header2Font = Font(family="Montserrat Medium", size=30, weight="normal",slant="roman",underline=0,overstrike=0)
Header3Font = Font(family="Montserrat Medium", size=15, weight="normal",slant="roman",underline=0,overstrike=0)
FormFont = Font(family="Montserrat Medium", size=25, weight="normal",slant="roman",underline=0,overstrike=0)
FillFont = Font(family="Montserrat Medium", size=20, weight="normal",slant="roman",underline=0,overstrike=0)


#Creating Header
Header = Canvas(root, width=1920,height=158,bg='#BAE2DC')
Header.place(x=0,y=0)
Header.configure(highlightbackground='#707070')

#header text
Header.create_text(140,42,anchor="nw", text="Resume Scanning Project", font=Header1Font)
Header.create_text(1549,42,anchor="nw", text="Edit Record", font=Header2Font)
Header.create_text(140,85,anchor="nw", text="ALL Project by Muhammad Darwis and Chan Khai Shen", font=Header3Font)

#Form text
my_canvas.create_text(140,203,anchor="nw", text="Search Applicant Using IC No.:", font=FormFont)
my_canvas.create_text(140,254,anchor="nw", text="Applicant IC No. :", font=FillFont)

#Display Applicant info text
my_canvas.create_text(140,309,anchor="nw", text="Name:", font=FillFont)
my_canvas.create_text(140,364,anchor="nw", text="Email Address:", font=FillFont)
my_canvas.create_text(140,419,anchor="nw", text="Contact No.:", font=FillFont)
my_canvas.create_text(140,474,anchor="nw", text="Position Applied:", font=FillFont)
my_canvas.create_text(140,529,anchor="nw", text="Language (written):", font=FillFont)
my_canvas.create_text(140,584,anchor="nw", text="Language (spoken):", font=FillFont)
my_canvas.create_text(140,639,anchor="nw", text="Programming Language:", font=FillFont)
my_canvas.create_text(140,694,anchor="nw", text="Past Work Experience:", font=FillFont)
my_canvas.create_text(880,694,anchor="nw", text="Duration:", font=FillFont)
my_canvas.create_text(140,749,anchor="nw", text="Highest Education:", font=FillFont)

#IC search fill
entryIC = Entry(root, width = 100)
my_canvas.create_window(500, 265, anchor="nw", window=entryIC)

#Search Button
img_label = Label(image=SearchButtonImg)
ButtonSave = Button(root, image=SearchButtonImg, borderwidth=0,highlightthickness=0,bd=0,command=searchOneFromActiveRecords)
my_canvas.create_window(1110,252,anchor="nw",window=ButtonSave)

#Edit fill
entryName = Entry(root, width = 100)
my_canvas.create_window(500, 318, anchor="nw", window=entryName)

entryEmail = Entry(root, width = 100)
my_canvas.create_window(500, 375, anchor="nw", window=entryEmail)

entryContact = Entry(root, width = 100)
my_canvas.create_window(500, 428, anchor="nw", window=entryContact)

entryPosition = Entry(root, width = 100)
my_canvas.create_window(500, 483, anchor="nw", window=entryPosition)

entryLangWrite = Entry(root, width = 100)
my_canvas.create_window(500, 538, anchor="nw", window=entryLangWrite)

entryLangSpoke = Entry(root, width = 100)
my_canvas.create_window(500, 592, anchor="nw", window=entryLangSpoke)

entryCodeLang = Entry(root, width = 100)
my_canvas.create_window(500, 650, anchor="nw", window=entryCodeLang)

entryWorkExp = Entry(root, width = 60)
my_canvas.create_window(500, 704, anchor="nw", window=entryWorkExp)

entryDuration = Entry(root, width = 60)
my_canvas.create_window(1040, 704, anchor="nw", window=entryDuration)

entryHighestEdu = Entry(root, width = 100)
my_canvas.create_window(500, 762, anchor="nw", window=entryHighestEdu)


#Save Edit Button
img_label = Label(image=SaveEditButtonImg)
ButtonSaveEdit = Button(root, image=SaveEditButtonImg, borderwidth=0, highlightthickness=0, bd=0, command=updateRecord)
my_canvas.create_window(140, 803, anchor="nw", window=ButtonSaveEdit)

#Back to Menu Button (need to add function)
img_label = Label(image=BackToMenuButtonImg)
ButtonMenu = Button(root, image=BackToMenuButtonImg, borderwidth=0, highlightthickness=0, bd=0)
my_canvas.create_window(1602, 189, anchor="nw", window=ButtonMenu)


root.mainloop()

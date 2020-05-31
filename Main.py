import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os

#######################
## Google drive linking
########################
# new view only creds in shared Google Drive
app_creds_dictionary = {
  "type": "service_account",
  "project_id": "warrantdatabase",
  "private_key_id": "8fa9821be469f86d7e3fb2b6ae7e1c66aaf616ea",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDD0SIUfpVe4nI0\nwGukhEjzXtpMtrSgGk1shHP/GkXyPPeI3y3knRJdAdZYaxB93kv/ArzC8jtJY1ye\nsC1/EUyJa6BEYjFVrxlWWTjSN2qJ2WGhmB2UfglKsv/5gAeglAMMZvT5VkN3ej7T\nVKnf/zk2uyoRR7Y/8jWwOmAn4/Ovc+glkppkAWySRPC8d3/k0jzTb4Xn28ckNRYN\nHHofmRSrbbtKL0Y6NeCBiKQ8D2XQ/EC8MkKtDerQ1Vw+zoVNBJAekwgt13xDpkkg\nQxEgV46U1XswMZUc0SSGRBkbWHj+h6zdO3XDt4YOVS2eNrGVXGLxF1P8ALnySzsk\nN379Uyn5AgMBAAECggEAC9irGli0g99oz8HHjiLMOjnGAYrltb0U0gVxWKcn2olo\n43u2mw4L/lra5mtG8PALfCUxcwz66TjjPlzW/WKRu5gqdsVtMD6kZpG42xh4wyST\njRZWzWHFziJMhuhn9B8ANpyqVV55CZ4rqHCGyZzD9iIWLKJAZ4rC4YmmjfZy16DG\ns1UxGQu5z4e7Uhqaf7LzDyxw3s1okloh6hMAn05fq6zRP6fb0D8EFAqhAyvymR2j\naNBUWLftD0wRIrtxFlUpmiXXWmlNO5GykX+mdH1nVb4pmNS+LMldlBjJtK5jUlzI\noyY9EQU99b7iHS/ljxfYDWzONPnje/PjFfUX5OO8wQKBgQDyrIiWnYKkP0QkVdRH\n3C1kWDmsD4U7NN+mc+ocaGpWeW/zFCsHuioFt5JsKSKveYWwS1uP3eVvpGbwXH59\nsg7ikqBc5rSXkXFN+zXiDOXJGei0V2uj5/3PSrUYrMhl1WT3LFIzdBT66SeHdV47\nTPBeejo9OFe5Ej3in93kPJR66wKBgQDOkeRUrUlKYwUOgOinxNTPQMUI2RGuCtiR\n1QFTphkdNe/uP/dQKMYm1WjFv9qSECoiGm/8ZqSy6Eci0ZdF47LxxnTywGEBTuSF\nKnyoTNd9lJqV1wVVuw3Bqhn9s+CNbiOnBoYRfmNiWhHeM0DVZHusGs+78aBmJ3q1\nersPd61tqwKBgQCnfM0Ips1z7vZo3ZQVxLDPgNTNHCkoI+X4TChYUviRll7dth28\nx5AZQgmc/QcjdQwAEQKw2MVxuFYTrsLenfYICosDk3cw5QD+gVM/IQe3NFqXnX59\nMbDLURSMYzQslIuKzNwvBv8z7ZeKtkbDRubfThzEBA8HfL+ZmhzbWbRg4QKBgDgA\nNz15iQAAnjNTYT9yThstvPzsFC3xxMqsS2LJCc/wem5Fqx9xHl8SxgeuPmwQs8tx\nDWEI1qel7vsShQcudqmzGqtg2iuHns43OXpK8rSZ39q1Yz3dqxoQqmEsLblJ3aJ/\nU0NU106nimaJ0I7JYfnDfwO9urVXCJ5Aeovz7vFnAoGBANeVPUetQZqz5w+Mp9PE\ndUlK9ypjLWqM2q3XkfvaAl7PqLx9fF4stgS7lPErE2X0x2BIwMIoOVBrGm+yxDpK\nZJ2Uqy62jm4Szw9WJJ/NHFlAJ9a5gjYKvdxEMoqD0sN0SWwJHuWegurQHGzLvFqj\nJvYSM1nAuWUtCg/EgtINeawD\n-----END PRIVATE KEY-----\n",
  "client_email": "warrantprogramviewer@warrantdatabase.iam.gserviceaccount.com",
  "client_id": "105170822321928785601",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/warrantprogramviewer%40warrantdatabase.iam.gserviceaccount.com"}

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive',]
creds = ServiceAccountCredentials.from_json_keyfile_dict(app_creds_dictionary, scope)
gc = gspread.authorize(creds)

ws = gc.open_by_key("1vQkJ5C-zwRKselKz5_C2HPBezMKAP0EbWwWgnzEX9EY").sheet1
###################################################
##
##
## Program Info
## Warrant Search GUI
## Created by Garret P. (#14308)
##
version = "1.0"
versionText = ("Created by Garret P. (#14308) | Version %s" % version)
#############
def refresh(buttonCheck):
    global WSstatus
    WSstatus = ws.col_values(1)
    global WSwarrantNumber
    WSwarrantNumber = ws.col_values(2)
    global WSoocCiv
    WSoocCiv = ws.col_values(3)
    global WScivName
    WScivName = ws.col_values(4)
    global WSdob
    WSdob = ws.col_values(5)
    global WSaddress
    WSaddress = ws.col_values(6)
    global WSappDate
    WSappDate = ws.col_values(7)
    global WStype
    WStype = ws.col_values(8)
    global WScharges
    WScharges = ws.col_values(9)
    global WSevidence
    WSevidence = ws.col_values(10)
    global WSdepartment
    WSdepartment = ws.col_values(12)
    global WSofficer
    WSofficer = ws.col_values(13)
    searchResults.delete(*searchResults.get_children())
    ## forces name to uppercase to search case-insensitive
    WScivName = [x.upper() for x in WScivName]
    if(buttonCheck):
        messagebox.showinfo("Sucess!","Program has been reloaded\nwith latest warrant info..")


##Actual search funciton
def showWarrants():
    searchResults.delete(*searchResults.get_children())
    RRL = []
    for i in range(len(WScivName)):
        if  (warrantSearchName.get().upper() in WScivName[i]):
            if (statusBoxVar.get() == 0):
                if(WSstatus[i] == "Approved" ):
                    RRL.append(i)
            else:
                RRL.append(i)
    tempList = []
    #('Number','Type','Civ','Name','DOB','Charges','Department','Status')
    for i in RRL:
        tempList.append([WSwarrantNumber[i],WStype[i],WSoocCiv[i],WScivName[i],WSdob[i],WScharges[i],WSdepartment[i],WSstatus[i]])
    if(len(RRL)==0):
        tempList.append(['####','####','No Name','/No Active','####','####','####','####'])
    for (wrNumber,wrType,wrCiv,wrName,wrDOB,wrCharges,wrDepartment,wrStatus) in tempList:
        searchResults.insert("", "end", values=(wrNumber,wrType,wrCiv,wrName,wrDOB,wrCharges,wrDepartment,wrStatus))


####################
## Warrant Number ##
## Search SubApp  ##
####################
def WNSapp(passWID):
    #do actual search
    def warrantNumberSearch(searchNumber):
        #delete and enable residuals
        SHEwarrantNumber.configure(state="normal")
        SHEwarrantNumber.delete(0,tk.END)
        SHEcivName.configure(state="normal")
        SHEcivName.delete(0,tk.END)
        SHEoocCiv.configure(state="normal")
        SHEoocCiv.delete(0,tk.END)
        SHEdob.configure(state="normal")
        SHEdob.delete(0,tk.END)
        SHEcharges.configure(state="normal")
        SHEcharges.delete(1.0,"end")
        SHEevidence.configure(state="normal")
        SHEevidence.delete(1.0, "end")

        #do search here
        RWL = None
        for i in range(len(WSwarrantNumber)):
            if WSwarrantNumber[i] == searchNumber:
                RWL = (i)

        ##Insert data from match
        if(RWL!=None):
            SHEwarrantNumber.insert(10,WSwarrantNumber[RWL])
            SHEcivName.insert(10,WScivName[RWL])
            SHEoocCiv.insert(10,WSoocCiv[RWL])
            SHEdob.insert(10,WSdob[RWL])
            varType.set("Warrant Type\n"+WStype[RWL])
            SHEcharges.insert(1.0,WScharges[RWL])
            SHEevidence.insert(1.0,WSevidence[RWL])
            varStatus.set("WARRANT STATUS: "+WSstatus[RWL])
        else:
            varType.set("NO RESULT\nFOUND")
            varStatus.set("")
        #set back to readonly
        SHEwarrantNumber.configure(state="readonly")
        SHEcivName.configure(state="readonly")
        SHEoocCiv.configure(state="readonly")
        SHEdob.configure(state="readonly")
        SHEcharges.configure(state="disabled")
        SHEevidence.configure(state="disabled")

    def onEnter(event=None):
        warrantNumberSearch(warrantSearchName.get())
    #root window creation
    root = tk.Toplevel(main)

    #Define main frame and window
    root.wm_title("Warrant Number Viewer(WN)")
    root.geometry("420x320")
    root.resizable(0,0)
    root.bind('<Return>',onEnter)
    #TITLE in the page
    tk.Label(root, text="Warrant Number\nViewer", font=("Georgia", 14),bg="aqua").grid(row=0,column=0,columnspan=4,ipadx=10,ipady=2,sticky="W")

    #input for the search
    wSearchTxt = tk.Label(root, text="Search for\nWarrant Number")
    wSearchTxt.grid(row=1,column=0,pady=3)
    warrantSearchName = tk.Entry(root, width=20)
    warrantSearchName.grid(row=1,column=1,padx=2, sticky="w")
    #button for search
    searchBut = tk.Button(root,bd=1,text="Search",width=10,height=0,command= lambda: warrantNumberSearch(warrantSearchName.get()),pady=5)
    searchBut.grid(row=1,column=2,columnspan=2)
            

    ###warrant details
    #warrant number
    SHwarrantNumber = tk.Label(root, text="Warrant ID")
    SHwarrantNumber.grid(row=2,column=0,pady=5,padx=2,sticky="e")
    SHEwarrantNumber = tk.Entry(root, width=20)
    SHEwarrantNumber.configure(state="readonly")
    SHEwarrantNumber.grid(row=2,column=1,pady=5,padx=2,sticky="w")
    #civ ooc
    SHoocCiv = tk.Label(root, text="OOC Civ")
    SHoocCiv.grid(row=3,column=0,pady=5,padx=2,sticky="e")
    SHEoocCiv = tk.Entry(root, width=20)
    SHEoocCiv.configure(state="readonly")
    SHEoocCiv.grid(row=3,column=1,pady=5,padx=2,sticky="w")
    #warrant type
    varType = tk.StringVar()
    wSearchTxt = tk.Label(root, textvariable=varType, font=("Georgia", 12)).grid(row=2,column=2,rowspan=2,columnspan=2)
    #civ name
    SHcivName = tk.Label(root, text="Name")
    SHcivName.grid(row=4,column=0,pady=5,padx=2,sticky="e")
    SHEcivName = tk.Entry(root, width=20)
    SHEcivName.configure(state="readonly")
    SHEcivName.grid(row=4,column=1,pady=5,padx=2,sticky="w")
    #DOB
    SHdob = tk.Label(root, text="DOB")
    SHdob.grid(row=4,column=2,pady=5,padx=2,sticky="e")
    SHEdob = tk.Entry(root, width=22)
    SHEdob.configure(state="readonly")
    SHEdob.grid(row=4,column=3,pady=5,padx=2,sticky="w")
    #charges
    SHcharges = tk.Label(root, text="Charges")
    SHcharges.grid(row=5,column=0,pady=5,padx=2,sticky="e")
    SHEcharges = tk.Text(root, height=2, width=50, bg='#f0f0f0', font=("TkDefaultFont", 8),wrap=tk.WORD)
    SHEcharges.configure(state="disabled")
    SHEcharges.grid(row=5,column=1,columnspan=3,sticky="w")
    #evidence
    SHevidence = tk.Label(root, text="Evidence")
    SHevidence.grid(row=6,column=0,pady=5,padx=2,sticky="e")
    SHEevidence = tk.Text(root, height=4, width=50, bg='#f0f0f0', font=("TkDefaultFont", 8),wrap=tk.WORD)
    SHEevidence.configure(state="disabled")
    SHEevidence.grid(row=6,column=1,columnspan=3,sticky="w")

    #warrant type
    varStatus = tk.StringVar()
    wStatusTxt = tk.Label(root, textvariable=varStatus, font=("Georgia", 14)).grid(row=9,column=1,columnspan=3)
    
    #take passed warrant into and set into slot
    if(passWID != ""):
        warrantNumberSearch(passWID)

def onEnter(event=None):
    showWarrants()

main = tk.Tk()
main.resizable(0,0)
main.wm_title("JS-BWAU\nArrest Warrant Search")

main.bind('<Return>',onEnter)

#Load image
path = os.path.dirname(os.path.abspath(__file__))
load = Image.open(path+"\\bwauRS.png")
render = ImageTk.PhotoImage(load)
bwauLogo = tk.Label(main, image=render)
bwauLogo.image = render
bwauLogo.grid(row=0,column=0,rowspan=2)
#TITLE in the page
tk.Label(main, text="JS-BWAU\nACTIVE Arrest Warrant Search", font=("Georgia", 14),bg="aqua").grid(row=0,column=1,columnspan=4,ipadx=5,ipady=2)

#input for the search
warrantSearchName = tk.Entry(main, width=50)
warrantSearchName.grid(row=1,column=1, sticky="e")
#button for search
searchBut = tk.Button(main,bd=1,text="Search",width=10,height=0,command=showWarrants)
searchBut.grid(row=1,column=2,sticky="w")
#TEST wns
testWNS = tk.Button(main,bd=1,text="Warrant\nNumber",width=8,height=0,font=("Georgia",10),command= lambda: WNSapp(""))
testWNS.grid(row=1,column=3)
#button for refresh
refreshBut = tk.Button(main,bd=1,text="⟳",width=2,height=0,font=("Georgia",14),command= lambda: refresh(True))
refreshBut.grid(row=1,column=4)


warrantItems = ('Number','Type','Civ','Name','DOB','Charges','Department','Status')
searchResults = ttk.Treeview(main,columns=warrantItems, show='headings')
for col in warrantItems:
    searchResults.heading(col, text=col)
searchResults.column("Number",minwidth=0,width=80)
searchResults.column("Type",minwidth=0,width=60)
searchResults.column("Civ",minwidth=0,width=100)
searchResults.column("Name",minwidth=0,width=130)
searchResults.column("DOB",minwidth=0,width=60)
searchResults.column("Charges",minwidth=0,width=200)
searchResults.column("Department",minwidth=0,width=80)
searchResults.column("Status",minwidth=0,width=80)
searchResults.grid(row=2,column=0,columnspan=5,padx=6)

#Label for ver and creds at bottom
versionLabel = tk.Label(main, text=versionText, font=("Verdana", 8))
versionLabel.grid(row=3,column=2,columnspan=3,sticky="e")

#Toggle all status
statusBoxVar = tk.IntVar()
toggleStatus = tk.Checkbutton(main, text="Show all warrant types.",variable=statusBoxVar)
toggleStatus.grid(row=3,column=0,columnspan=2,sticky="w")

#User cannot resize columns with this code
def handle_click(event):
    if searchResults.identify_region(event.x, event.y) == "separator":
        return "break"
searchResults.bind('<Button-1>', handle_click)

# double click to open full warrant info
def OnDoubleClick(event):
    citem = searchResults.focus()
    warrantDetails = searchResults.item(citem,"values")
    WNSapp(warrantDetails[0])

searchResults.bind("<Double-1>",OnDoubleClick)

refresh(False)
main.mainloop()
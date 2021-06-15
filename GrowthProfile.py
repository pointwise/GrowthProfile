#############################################################################
#
# (C) 2021 Cadence Design Systems, Inc. All rights reserved worldwide.
#
# This sample script is not supported by Cadence Design Systems, Inc.
# It is provided freely for demonstration purposes only.
# SEE THE WARRANTY DISCLAIMER AT THE BOTTOM OF THIS FILE.
#
#############################################################################

###############################################################################
##
## GrowthProfile.py
##
## Script with Tk interface that generates and applies growth profiles
## to T-Rex blocks. Wall boundary conditions must already be applied in order
## for the computed wall spacing to be set or updated.
##
###############################################################################

from pointwise import GlyphClient, GlyphError
from pointwise.glyphapi import *
import platform
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import tkinter.ttk as ttk
from tkinter import messagebox

#################################
#              GUI              #
#################################

root = Tk()
glf = GlyphClient()
pw = glf.get_glyphapi()
CustomFrame = None
CustomTable = None
RemoveButton = None
CustomDS = None
customDS = tk.StringVar()
OkButton = None
typeCondition = None
TypeSelection = None
ComputedFrame = None
ReEntry = None
LEntry = None
HLabel = None
HEntry = None
tw_list = []
color_valid = "white"
color_invalid = "misty rose"
updateWallDoms = tk.BooleanVar()
updateWallDoms.set(True)
CustomRowCount = 2
PW_Logo = "R0lGODlhiQAYAMZnAAAAAA4ODhQUFBsbGyQkJCwsLDMzMzs7O0REREtLS1RUVFtbW  \
2JiYmtra3Jycnt7ewBjqgtqrgBmsABrtwBsuRJusBZwsRpzsyF2syJ4tSh7ty1/uQZ1xC+AujeFvD \
iFvT2IvjGQ1EWNwUiPwk6TxEqVylSXxleYx1iZx1ybyGGeymSgy26mz3Coz2On122q1Wqt3XSq0Xu \
u03+x1Xqx2HS04n+544ODg4qKipSUlJubm6Ojo6ysrLS0tLu8vIS01oi214q32I252ZK825i+2pzC \
3pXB4ZnI6qPG4KXI4qvM46HL6rDP5bTR5rzW6b/Y6sTExMzMzM/R0dPT09ra2sTb68re7M/h79Di7 \
8ni9NXl8d3q9N/u+OTk5Ovr6+Pu9ubw9+3z9+Xx+ery+PLy8vH3+vX5+///////////////////// \
///////////////////////////////////////////////////////////////////////////// \
//yH5BAEKAH8ALAAAAACJABgAAAf+gH+Cg4SFhoeIiYqLjI2Oj5CRkpOUlZaPPDs5hDkKnp8KCzuK \
Tk1Kf2BKp4ZQoF1/C6CgDlGDN7K4Cj5QCZ4NhlSGO58JXVGfC4NdoKOGt7mgPn/DDg43UIIJANvc3 \
AiHQlpBJE1DKDJFKUGFOt2v3fDbDoIG8fEPXd21ygOvhAHd/uQIKKgdt3mGCNiDNwqHjwVQdOAQxG \
DhNgWEtKRQAUTLDywrIEDwkCTCB0I83P0BaBHAjT/aWgL4dYBbskEDJw6K0o3BnxvcAgzC0U3HIQQ \
yAfjoooPKAR9RNv2p2FLKICJbkvz4cubHmC9CZlQ5EwEDF0Epub1LOjXprx7+KgUpFECI6rYpf4hu \
E4q2m85CSGWOeoBjCg8GzQJbfCBIiZgiT55wNaNCCRASKJpsYdGkr9o/SQH0aJAU4x8B3HTC3cZjU \
DcDgvQC4PsnH7cBhwoknQilAQ8HRgX5yEFcB/GY23wuGSEDAhIkV84AUXElgsgTQUAU8bztFcuZOs \
Lf+O6ACo/zPdDzSJ8e78/bgmpuI1CwWzPZtP8o6JbAUJQeAAYoIID+/LGPIrZtk0wIQVRwwRkomPC \
DCDKUoUQIEMRQhEhH/JFWdytx454g+yUHSYJK6afPH/LNNlRQhKA40yWFGBPFjTcu0M1LHDT4xBBM \
NHHCGUxAMEIYJ/z+0IJIMHioUjc91MXNL8pAYSU2R3HTHxXd/NLli3sVMlA3jA1CBY5oplmgISVa1 \
IMVFBTxhQoZbvGDEiyIBIEWZuj5wh+rgQglITpuQ2Vs3YxISKAAvNKiAIXeBaaLhTwAT3AsJoWpIZ \
Eu9EcSElxRhUgt5LnnBSIp0QWdENDwhw8qfRflIJEeKlA3wRyi0DaMMfoaIfgdAlSi2WiaiF32YFQ \
DBEyEIdIQzUHwgwwYjBHSGCNAYAQRUzzJzayC1EqIQdvkakiwfwxgT2uT5keIpdzQB1NSzRyCLDwH \
CGIDBEWEQ8IQrJJgRhOsatAEEyXIwOVnshI65bi4IoJilMP+duNuxe4S0qJo88r0lyF2DbDDyDtg+ \
YcWKwgBAQhJbGGFEk4MgQWrpJ4xQRULC/qtw4ZyEjEibeYrIwBltpsIiv0hRwBxOeDAdA6KFmIXbI \
mcoKcMSHyAqgVW6HlBE0+48AcUse5M68ODkAuAuaxE3CaIwMKYSIv5ttlfJHYVoMiGIqnwg57MLgl \
CGSZAAIaTnw16ds9p/4zIrgD41C03+RaCLiLqbvNNm9/gzY3eiXzBBAgQXIAE4BUwEcQXJIiUBeIg \
Nrz4jDg5fsiYtOu2DbhGH0IFcpF3DEDnkOStSNZVILFCFRtYsEEKPxBpHQQycNcoaGaHi3Z93LB9C \
Evq/qRF17lyT0EAAQMI8N3OwA/g/vvps2vv54tka4IQX2xxcDopECFSCoP40PVkpz3Gca9ci6jI3Q \
SBmqLFLUxjawluhGcRqcxvG6BTxN9W5gTAQYAIIFgBSry1O57R7oBrWwTZ6tWWNfWOJxbZB/AWwkL \
AEGQRWkABvywAuOqxg4QAkF+mLkKIigEgaocoBiF8UDlDOIAgZLPHAUaku5Z8rBA7aIAWX+IIK2jh \
CTFAxxYOMYUHmBEff6hGNRSVRQf4hhBQcGM1XOgIOgoijmbkYhdwwMc+5kAanNCiIAcpSJPR6JCIT \
KQiGREIADs="


# DEF: makeWindow
#    Builds the GUI window
def makeWindow():
    entryWidth = 15

    # Set Window Title
    root.title('Growth Profile')

    # Create Selection Frame   
    global TypeSelection
    SelectionFrame= ttk.Frame(root, padding=5)
    TypeLabel = ttk.Label(SelectionFrame, text='Type: ')
    typeOptions = ["Laminar", "Turbulent", "Custom"]
    TypeSelection = ttk.Combobox(SelectionFrame, values=typeOptions, width=14)
    TypeSelection.configure(state='readonly')
    TypeLabel.grid(row=0, column=0, sticky=W)
    TypeSelection.grid(row=0, column=1, sticky=E)
    SelectionFrame.pack(side=TOP)

    # Create Button Frame
    global OkButton, PW_Logo
    ButtonFrame = ttk.Frame(root, padding=(5,5,5,5))
    OkButton = ttk.Button(ButtonFrame, text="OK", command=okButtonCommand, state='disabled')
    CancelButton = ttk.Button(ButtonFrame, text="Cancel", command=exit)
    img = tk.PhotoImage(data=PW_Logo)
    PwLogo = tk.Label(ButtonFrame, relief=FLAT, image=img, bd=0)
    PwLogo.image = img
    PwLogo.pack(side=LEFT, anchor=W)
    CancelButton.pack(side=RIGHT, anchor=E)
    OkButton.pack(side=RIGHT, anchor=E)
    ButtonFrame.pack(anchor=CENTER, side=BOTTOM, fill=X)
    ButtonFrame.columnconfigure(0, weight=1)

    # Create Custom Profile Frame
    global CustomFrame
    CustomFrame = ttk.Frame(root, padding=3)

    # Create Custom delta-S Entry Frame
    global CustomDS, customDS
    CustomApplyFrame = ttk.Frame(CustomFrame, padding=3)
    CustomApplyDS = ttk.Checkbutton(CustomApplyFrame, text="Update Wall Domains", variable=updateWallDoms, \
        command=updateButtons)
    CustomDSLabel = ttk.Label(CustomApplyFrame, text="   Spacing: ", anchor=E)
    CustomDS = tk.Entry(CustomApplyFrame, textvariable=customDS, background=color_invalid, width=entryWidth)
    reg = CustomApplyFrame.register(validateEntry)
    CustomDS.configure(validate='key', validatecommand=(reg, '%P', '%W'))
    CustomApplyDS.grid(sticky=EW, padx=3, pady=3, column=0, row=0)
    CustomDSLabel.grid(sticky=EW, padx=3, pady=3, column=1, row=0)
    CustomDS.grid(sticky=EW, padx=3, pady=3, column=2, row=0)
    CustomApplyFrame.columnconfigure(1, weight=1)
    CustomApplyFrame.pack(padx=3, pady=3, side=BOTTOM, fill=X, anchor=CENTER)

    # Create Parameter Frame
    global ComputedFrame, ReEntry, LEntry, HEntry, HLabel
    ComputedFrame = ttk.Frame(root, padding=5)
    ReLabel = ttk.Label(ComputedFrame, text="Reynolds No.: ", anchor=E)
    reVar = tk.StringVar()
    ReEntry = tk.Entry(ComputedFrame, textvariable=reVar, background=color_invalid, width=entryWidth)
    reg = ComputedFrame.register(validateEntry)
    ReEntry.configure(validate='key', validatecommand=(reg, '%P', '%W'))
    lVar = tk.StringVar()
    LLabel = ttk.Label(ComputedFrame, text="Characteristic Length: ", anchor=E)
    LEntry = tk.Entry(ComputedFrame, textvariable=lVar, background=color_invalid, width=entryWidth)
    LEntry.configure(validate='key', validatecommand=(reg, '%P', '%W'))
    hVar = tk.StringVar()
    HLabel = ttk.Label(ComputedFrame, text="Initial Spacing Factor: ", anchor=E)
    HEntry = tk.Entry(ComputedFrame, textvariable=hVar, background=color_invalid, width=entryWidth)
    HEntry.configure(validate='key', validatecommand=(reg, '%P', '%W'))
    ComputedApplyDS = ttk.Checkbutton(ComputedFrame, text="Update Wall Domains", variable=updateWallDoms, \
        command=updateButtons)
    ReLabel.grid(sticky=EW, padx=3, pady=3, column=0, row=0)
    ReEntry.grid(sticky=EW, padx=3, pady=3, column=1, row=0)
    LLabel.grid(sticky=EW, padx=3, pady=3, column=0, row=1)
    LEntry.grid(sticky=EW, padx=3, pady=3, column=1, row=1)
    HLabel.grid(sticky=EW, padx=3, pady=3, column=0, row=2)
    HEntry.grid(sticky=EW, padx=3, pady=3, column=1, row=2)
    ComputedApplyDS.grid(sticky=N, padx=3, pady=3, columnspan=2)
    ComputedFrame.columnconfigure(1, weight=1)

    # Create Custom Profile Table Frame
    global RemoveButton
    ButtonRowFrame = ttk.Frame(CustomFrame, padding=3)
    AddButton = ttk.Button(ButtonRowFrame, text="Add Row", command=addButtonCommand)
    RemoveButton = ttk.Button(ButtonRowFrame, text="Erase Row", command=removeButtonCommand)
    RemoveButton.pack(side=RIGHT, padx=5, pady=5, anchor=CENTER)
    AddButton.pack(side=RIGHT, padx=5, pady=5, anchor=CENTER)
    ButtonRowFrame.pack(side=BOTTOM, fill=X, anchor=CENTER)

    TypeSelection.bind("<<ComboboxSelected>>", comboBoxBind)
    root.lift()


# DEF: comboBoxBind
#    Combobox bind callback function
def comboBoxBind(event):
    global TypeSelection, typeCondition
    typeCondition = TypeSelection.get()
    updateParams()


# DEF: addButtonCommand
#    Function commands for Add Button
def addButtonCommand():
    global CustomRowCount
    CustomRowCount = CustomRowCount + 1
    updateCustomTable()
    updateTableColors()
    updateButtons()


# DEF: removeButtonCommand
#    Function commands for Remove Button
def removeButtonCommand():
    global CustomRowCount
    CustomRowCount = CustomRowCount - 1
    updateCustomTable()
    updateTableColors()
    updateButtons()


# DEF: okButtonCommand
#    Function commands for OK Button
def okButtonCommand():
    ApplyGrowthProfile()
    exit()


# DEF: isInt
#    Returns True if given value represents an integer, False otherwise
def isInt(str):
    try:
        integer = int(str)
        return True
    except:
        return False


# DEF: isDouble
#    Returns True if given value represents a double, False otherwise
def isDouble(str):
    try:
        double = float(str)
        return True
    except:
        return False


# DEF: validateEntry
#    Checks if there is valid data in entry box
def validateEntry(entry, widget):
    global ReEntry, LEntry, HEntry, CustomDS
    if isDouble(entry):
        if widget == str(ReEntry):
            ReEntry.configure(background=color_valid)
        elif widget == str(LEntry):
            LEntry.configure(background=color_valid)
        elif widget == str(HEntry):
            HEntry.configure(background=color_valid)
        elif widget == str(CustomDS):
            CustomDS.configure(background=color_valid)
    else:
        if widget == str(ReEntry):
            ReEntry.configure(background=color_invalid)
        elif widget == str(LEntry):
            LEntry.configure(background=color_invalid)
        elif widget == str(HEntry):
            HEntry.configure(background=color_invalid)
        elif widget == str(CustomDS):
            CustomDS.configure(background=color_invalid)
    updateButtons()
    return True


# DEF: updateButtons
#    Updates the OK button
def updateButtons():
    global OkButton, CustomDS
    if canCreate():
        OkButton.configure(state='normal')
    else:
        OkButton.configure(state='disabled')
    if updateWallDoms.get():
        CustomDS.configure(state='normal')
    else:
        CustomDS.configure(state='disabled')


# DEF: simpleTable
#    Builds the table structure
def simpleTable(varName, args):
    global CustomTable, CustomFrame, tw_list
    legal = ['rows', 'cols', 'titlerows', 'titlecols', 'vcmd']
    A = {'rows': 5, 'cols': 5, 'titlerows': 0, 'titlecols': 0}
    if len(args) == 0:
        messagebox.showerror('Error', "usage: simpleTable pathName varName ?options...?")
    idx = -1
    for opt, value in args.items():
        bool_checker = False
        for element in legal:
            if element == opt:
                bool_checker = True
        if not bool_checker:
            msg = "unknown option \042" + str(opt) + "\042"
            messagebox.showerror('Error', msg)
        idx = idx + 1
        if idx >= len(args):
            msg = "value for \042" + str(opt) + "\042 missing"
            messagebox.showerror('Error', msg)
        A[opt] = value

    previously_entered = []
    for widget in tw_list:
        if widget.winfo_exists():
            previously_entered.append(widget.get())
    previous_len = len(previously_entered)
    count = 0

    # Now build our table
    if CustomTable != None:
        CustomTable.destroy()
    CustomTable = tk.Frame(CustomFrame)
    rows = A.get('rows')
    cols = A.get('cols')
    for r in range(0, rows):
        rowWidgets = []
        for c in range(0, cols):
            if ((r < A.get('titlerows')) or (c < A.get('titlecols'))):
                if platform.system() == "Windows":
                    bg = "SystemDisabledText"
                else:
                    bg = "darkgrey"
                text = str(varName.get(str(c)))
                tw = tk.Label(CustomTable, text=text, relief=FLAT, background=bg, foreground="white", width=13, \
                    anchor=N)
            else:
                text_var = StringVar()
                tw = tk.Entry(CustomTable, textvariable=text_var, justify=RIGHT, relief=SUNKEN, bd=2, width=9, \
                    background=color_invalid)
                if ((previous_len > 0) and (count < previous_len)):
                    temp = previously_entered[count]
                    tw.insert(0, temp)
                    count = count + 1
                if A['vcmd'] != "":
                    reg = CustomFrame.register(vcmd)
                    tw.config(validate='key', validatecommand=(reg, r, c, '%P', tw))
            rowWidgets.append(tw)
        column_counter = 0
        for widget in rowWidgets:
            widget.grid(sticky=EW, padx=2, pady=2, row=r, column=column_counter)
            column_counter = column_counter + 1
        if r != 0:
            tw_list.extend(rowWidgets)
    for c in range(0, cols):
        CustomTable.columnconfigure(c, weight=1)
                

# DEF: vcmd
#    Validate command for table entry boxes
def vcmd(row, col, val, pathname):
    global tw_list
    for widget in tw_list:
        if str(pathname) == str(widget):
            index = tw_list.index(widget)
    if col == 0:
        if isInt(val):
            tw_list[index].configure(background=color_valid)
        else:
            tw_list[index].configure(background=color_invalid)
    else:
        if isDouble(val):
            tw_list[index].configure(background=color_valid)
        else:
            tw_list[index].configure(background=color_invalid)

    updateButtons()
    return 1


#  DEF: updateTableColors
#    Updates the colors of all cells when table rows are changed
def updateTableColors():
    children = CustomTable.winfo_children()
    end_range = len(children)
    for i in range(3, end_range):
        pathname = children[i]
        val = pathname.get()
        if ((i % 3) == 0):
            if isInt(val):
                pathname.configure(background=color_valid)
            else:
                pathname.configure(background=color_invalid)
        else:
            if isDouble(val):
                pathname.configure(background=color_valid)
            else:
                pathname.configure(background=color_invalid)


# DEF: buildTable
#    Builds and packs the table
def buildTable(rows):
    global CustomTable
    table = {'0': "# Layers", '1': "Growth Rate", '2': "Acceleration"}
    args = {'rows': rows, 'cols': 3, 'titlerows': 1, 'vcmd': 'vcmd'}
    simpleTable(table, args)
    CustomTable.pack(padx=10, pady=5, side='top', fill='x')


# DEF: updateParams
#    Updates the parameter frame when it is changed when the user changes the type
def updateParams():
    global CustomFrame, ComputedFrame, HLabel
    if typeCondition == "Laminar":
        CustomFrame.pack_forget()
        ComputedFrame.pack(side='top', fill='both')
        HLabel.configure(text='Initial Spacing Factor: ')
    elif typeCondition == "Turbulent":
        CustomFrame.pack_forget()
        ComputedFrame.pack(side='top', fill='both')
        HLabel.configure(text="Y+: ")
    elif typeCondition == "Custom":
        ComputedFrame.pack_forget()
        updateCustomTable()
        updateTableColors()
    updateButtons()


# DEF: updateCustomTable
#    Updates the table when it is changed either by adding a row or removing a row
def updateCustomTable():
    global CustomRowCount, RemoveButton, CustomFrame
    buildTable(CustomRowCount)
    CustomFrame.pack(fill='x', side='top', anchor='center')
    if CustomRowCount < 3:
        RemoveButton.configure(state='disabled')
    else:
        RemoveButton.configure(state='normal')


# DEF: CalcGrowthProfile
#    Calculates the growth profile for TRex and then assigns profile to selected blocks
def CalcGrowthProfile():
    returnList = []
    if typeCondition == "Custom":
        growthRateSchedule = []
        lines = getCustomProfileEntries()
        for line in lines.values():
            nLayers = line[0]
            rate = line[1]
            accel = line[2]
            for i in range(0, int(nLayers)):
                growthRateSchedule.append(rate)
                if isDouble(rate):
                    rate = float(rate)
                else:
                    rate = int(rate)
                if isDouble(accel):
                    accel = float(accel)
                else:
                    accel = int(accel)
                rate = rate * accel
        returnList.append(customDS)
        returnList.extend(growthRateSchedule)
        return returnList
    elif typeCondition == "Laminar":
        calc = pw.Grid.calculateLaminarGrowth(ReEntry.get(), LEntry.get(), HEntry.get())
        returnList.append(calc[3])
        returnList.extend(pw.Grid.calculateGrowthRateSchedule(calc[0], calc[1], calc[2]))
        return returnList
    elif typeCondition == "Turbulent":
        calc = pw.Grid.calculateTurbulentGrowth(ReEntry.get(), LEntry.get(), HEntry.get())
        returnList.append(calc[3])
        returnList.extend(pw.Grid.calculateGrowthRateSchedule(calc[0], calc[1], calc[2]))
        return returnList
    
    emptyList = []
    returnList.append(0.0)
    returnList.append(emptyList)
    return returnList


# DEF: ApplyGrowthProfile
#    Applies the growth profile attributes to selected blocks and then solves
def ApplyGrowthProfile():
    UnsBlks = []
    ents = GlyphVar()
    sm = pw.Display.createSelectionMask(requireBlock=[])
    pw.Display.getSelectedEntities(ents, selectionmask=sm)
    blocks = ents["Blocks"]
    for block in blocks:
        if block.isOfType("pw::BlockUnstructured"):
            UnsBlks.append(block)
    if len(UnsBlks) == 0:
        mask = pw.Display.createSelectionMask(requireBlock='Unstructured')
        root.withdraw()
        result = GlyphVar()
        if (not pw.Display.selectEntities(result, description="Pick block(s) for Growth Profile.", \
            selectionmask=mask)):
            root.deiconify()
            return
        else:
            blocks = result["Blocks"]
            UnsBlks.extend(blocks)

    calculations = CalcGrowthProfile()
    wallDS = calculations[0]
    completeProfile = []
    for i in range(1, len(calculations)):
        completeProfile.append(calculations[i])
    if isinstance(wallDS, float):
        wallDS_value = wallDS
    elif wallDS.get() != '':
        wallDS_value = float(wallDS.get())

    with pw.Application.begin("UnstructuredSolver", UnsBlks) as solve:
        try:
            for blk in UnsBlks:
                # Find or create wall boundary condition for this block
                try:
                    name = "Wall-Profile-" + blk.getName()
                    wallBC = pw.TRexCondition.getByName(name)
                except:
                    wallBC = pw.TRexCondition.create()
                    wallBC.setConditionType("Wall")
                    name = "Wall-Profile-" + blk.getName()
                    wallBC.setName(name)
                if ((updateWallDoms.get()) and (wallDS_value > 0.0)):
                    wallBC.setSpacing(wallDS_value)
                completeProfileStr = []
                for element in completeProfile:
                    completeProfileStr.append(str(element))
                blk.setUnstructuredSolverAttribute("TRexGrowthProfile", ' '.join(completeProfileStr))
                blk.setUnstructuredSolverAttribute("TRexMaximumLayers", len(completeProfile))
                glf.puts("Applied growth profile with %d layers to block '%s'" % (len(completeProfile), \
                    str(blk.getName())))
                if ((updateWallDoms.get()) and (wallDS_value > 0.0)):
                    regs = []
                    nFaces = blk.getFaceCount()
                    for i in range(1, nFaces+1):
                        face = blk.getFace(i)
                        nDoms = face.getDomainCount()
                        for j in range(1, nDoms+1):
                            register = []
                            register.append(blk)
                            register.append(face.getDomain(j))
                            regs.append(register)
                    trex_list = pw.TRexCondition.getByEntities(regs)
                    # Change all Wall domains to use new boundary condition
                    for bc, reg in zip(trex_list, regs):
                        if ((bc.getConditionType() == "Wall") and (bc != wallBC)):
                            wallBC.apply(reg)
                solve.end()
        except Exception as e:
            solve.abort()
            glf.puts("Unexpected error occurred. (%s) No changes were applied." % e)


# DEF: getCustomProfileEntries
#    Returns an dictionary of the data in the Custom Table
#    Key is the row number and elements are a list of data in the row
def getCustomProfileEntries():
    total_entries = (CustomRowCount - 1) * 3
    start_index = len(tw_list) - total_entries
    end_index = len(tw_list)
    num_rows = int((end_index - start_index) / 3)
    result = dict.fromkeys(range(num_rows), [])
    col_count = 0
    row = 0
    temp_list = []
    for i in range(start_index, end_index):
        temp_list.append(str(tw_list[i].get()))
        col_count = col_count + 1
        if col_count == 3:
            col_count = 0
            result[row] = temp_list
            row = row + 1
            temp_list = []
    return result


# DEF: canCreate
#    Checks if the Ok button should be enabled
def canCreate():
    result = 1
    if typeCondition == "Custom":
        children = CustomTable.winfo_children()
        range_end = len(children)
        for i in range(3, range_end):
            if (str(children[i].cget("background")) == color_valid):
                result = 1
            else:
                result = 0
        if result and updateWallDoms.get():
            if (str(CustomDS.cget("background")) == color_valid):
                result = 1
            else:
                result = 0
    elif typeCondition == "Laminar" or typeCondition == "Turbulent":
        if ((str(ReEntry.cget("background")) == color_valid) and (str(LEntry.cget("background")) == color_valid) and \
            (str(HEntry.cget("background")) == color_valid)):
            result = 1
        else:
            result = 0
    return result


root.eval('tk::PlaceWindow .')
makeWindow()
root.mainloop()


#############################################################################
#
# This file is licensed under the Cadence Public License Version 1.0 (the
# "License"), a copy of which is found in the included file named "LICENSE",
# and is distributed "AS IS." TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE
# LAW, CADENCE DISCLAIMS ALL WARRANTIES AND IN NO EVENT SHALL BE LIABLE TO
# ANY PARTY FOR ANY DAMAGES ARISING OUT OF OR RELATING TO USE OF THIS FILE.
# Please see the License for the full text of applicable terms.
#
#############################################################################
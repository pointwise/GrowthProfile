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
CadenceLogo = "R0lGODlhgAAYAPQfAI6MjDEtLlFOT8jHx7e2tv39/RYSE/Pz8+Tj46qoqHl3d+vq62ZjY/n4+NTT0+gXJ/BhbN3d3fzk5vrJzR4aG3 \
Fubz88PVxZWp2cnIOBgiIeH769vtjX2MLBwSMfIP///yH5BAEAAB8AIf8LeG1wIGRhdGF4bXD/P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcEN \
laGlIenJlU3pOVGN6a2M5ZCI/PiA8eDp4bXBtdGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYx \
IDY0LjE0MDk0OSwgMjAxMC8xMi8wNy0xMDo1NzowMSAgICAgICAgIj48cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudy5vcmcvMTk5OS8wMi8yM \
i1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmY6YWJvdXQ9IiIg/3htbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLj \
AvbW0vIiB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUcGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5 \
hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0idXVpZDoxMEJEMkEwOThFODExMUREQTBBQzhBN0JCMEIxNUM4NyB4bXBN \
TTpEb2N1bWVudElEPSJ4bXAuZGlkOkIxQjg3MzdFOEI4MTFFQjhEMv81ODVDQTZCRURDQzZBIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWQ6QjFCODczN \
kZFOEI4MTFFQjhEMjU4NUNBNkJFRENDNkEiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgSWxsdXN0cmF0b3IgQ0MgMjMuMSAoTWFjaW50b3NoKSI+IDx4bX \
BNTTpEZXJpZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6MGE1NjBhMzgtOTJiMi00MjdmLWE4ZmQtMjQ0NjMzNmNjMWI0IiBzdFJlZjpkb2N \
1bWVudElEPSJ4bXAuZGlkOjBhNTYwYTM4LTkyYjItNDL/N2YtYThkLTI0NDYzMzZjYzFiNCIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8 \
L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PgH//v38+/r5+Pf29fTz8vHw7+7t7Ovp6Ofm5eTj4uHg397d3Nva2djX1tXU09LR0M/OzczLysnIx \
8bFxMPCwcC/vr28u7q5uLe2tbSzsrGwr66trKuqqainpqWko6KhoJ+enZybmpmYl5aVlJOSkZCPjo2Mi4qJiIeGhYSDgoGAf359fHt6eXh3dnV0c3JxcG \
9ubWxramloZ2ZlZGNiYWBfXl1cW1pZWFdWVlVUU1JRUE9OTUxLSklIR0ZFRENCQUA/Pj08Ozo5ODc2NTQzMjEwLy4tLCsqKSgnJiUkIyIhIB8eHRwbGhk \
YFxYVFBMSERAPDg0MCwoJCAcGBQQDAgEAACwAAAAAgAAYAAAF/uAnjmQpTk+qqpLpvnAsz3RdFgOQHPa5/q1a4UAs9I7IZCmCISQwxwlkSqUGaRsDxbBQ \
er+zhKPSIYCVWQ33zG4PMINc+5j1rOf4ZCHRwSDyNXV3gIQ0BYcmBQ0NRjBDCwuMhgcIPB0Gdl0xigcNMoegoT2KkpsNB40yDQkWGhoUES57Fga1FAyaj \
hm1Bk2Ygy4RF1seCjwvAwYBy8wBxjOzHq8OMA4CWwEAqS4LAVoUWwMul7wUah7HsheYrxQBHpkwWeAGagGeLg717eDE6S4HaPUzYMYFBi211FzYRuJAAA \
p2AggwIM5ElgwJElyzowAGAUwQL7iCB4wEgnoU/hRgIJnhxUlpASxY8ADRQMsXDSxAdHetYIlkNDMAqJngxS47GESZ6DSiwDUNHvDd0KkhQJcIEOMlGkb \
hJlAK/0a8NLDhUDdX914A+AWAkaJEOg0U/ZCgXgCGHxbAS4lXxketJcbO/aCgZi4SC34dK9CKoouxFT8cBNzQ3K2+I/RVxXfAnIE/JTDUBC1k1S/SJATl \
+ltSxEcKAlJV2ALFBOTMp8f9ihVjLYUKTa8Z6GBCAFrMN8Y8zPrZYL2oIy5RHrHr1qlOsw0AePwrsj47HFysrYpcBFcF1w8Mk2ti7wUaDRgg1EISNXVwF \
lKpdsEAIj9zNAFnW3e4gecCV7Ft/qKTNP0A2Et7AUIj3ysARLDBaC7MRkF+I+x3wzA08SLiTYERKMJ3BoR3wzUUvLdJAFBtIWIttZEQIwMzfEXNB2PZJ0 \
J1HIrgIQkFILjBkUgSwFuJdnj3i4pEIlgeY+Bc0AGSRxLg4zsblkcYODiK0KNzUEk1JAkaCkjDbSc+maE5d20i3HY0zDbdh1vQyWNuJkjXnJC/HDbCQeT \
VwOYHKEJJwmR/wlBYi16KMMBOHTnClZpjmpAYUh0GGoyJMxya6KcBlieIj7IsqB0ji5iwyyu8ZboigKCd2RRVAUTQyBAugToqXDVhwKpUIxzgyoaacILM \
c5jQEtkIHLCjwQUMkxhnx5I/seMBta3cKSk7BghQAQMeqMmkY20amA+zHtDiEwl10dRiBcPoacJr0qjx7Ai+yTjQvk31aws92JZQ1070mGsSQsS1uYWiJ \
eDrCkGy+CZvnjFEUME7VaFaQAcXCCDyyBYA3NQGIY8ssgU7vqAxjB4EwADEIyxggQAsjxDBzRagKtbGaBXclAMMvNNuBaiGAAA7"


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
    global OkButton, CadenceLogo
    ButtonFrame = ttk.Frame(root, padding=(5,5,5,5))
    OkButton = ttk.Button(ButtonFrame, text="OK", command=okButtonCommand, state='disabled')
    CancelButton = ttk.Button(ButtonFrame, text="Cancel", command=exit)
    img = tk.PhotoImage(data=CadenceLogo)
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
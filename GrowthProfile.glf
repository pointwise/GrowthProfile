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
## GrowthProfile.glf
##
## Script with Tk interface that generates and applies growth profiles
## to T-Rex blocks. Wall boundary conditions must already be applied in order
## for the computed wall spacing to be set or updated.
##
###############################################################################

package require PWI_Glyph 2
pw::Script loadTK

#################################
#              GUI              #
#################################

set w(SelectionFrame)     .selectionFrame
  set w(TypeLabel)        $w(SelectionFrame).typeLabel
  set w(TypeSelection)    $w(SelectionFrame).typeSelection
set w(ComputedFrame)      .computedFrame
  set w(ReLabel)          $w(ComputedFrame).reLabel
  set w(ReEntry)          $w(ComputedFrame).reEntry
  set w(LLabel)           $w(ComputedFrame).lLabel
  set w(LEntry)           $w(ComputedFrame).lEntry
  set w(HLabel)           $w(ComputedFrame).hLabel
  set w(HEntry)           $w(ComputedFrame).hEntry
  set w(ComputedApplyDS)  $w(ComputedFrame).applyCheckbox
set w(CustomFrame)        .customFrame
  set w(CustomTable)      $w(CustomFrame).customTable
  set w(ButtonRowFrame)   $w(CustomFrame).buttonRowFrame
    set w(AddButton)      $w(ButtonRowFrame).addButton
    set w(RemoveButton)   $w(ButtonRowFrame).removeButton
  set w(CustomApplyFrame) $w(CustomFrame).applyFrame
    set w(CustomApplyDS)  $w(CustomApplyFrame).applyCheckbox
    set w(CustomDSLabel)  $w(CustomApplyFrame).applyDSLabel
    set w(CustomDS)       $w(CustomApplyFrame).applyEntry
set w(ButtonFrame)        .buttonFrame
  set w(OkButton)         $w(ButtonFrame).okButton
  set w(CancelButton)     $w(ButtonFrame).cancelButton
  set w(CadenceLogo)      $w(ButtonFrame).cadenceLogo


set typeOptions [list Laminar Turbulent Custom]
set color(Valid) "white"
set color(Invalid) "misty rose"
set updateWallDoms 1
set customDS ""

# PROC: makeWindow
#    Builds the GUI window
proc makeWindow { } {
  global w typeOptions CustomRowCount color customDS
  set CustomRowCount 2

  set entryWidth 15

  # Set Window Title
  wm title . "Growth Profile"

  # Create Selection Frame
  ttk::frame $w(SelectionFrame) -padding "5"
  ttk::label $w(TypeLabel) -text "Type: "
  ttk::combobox $w(TypeSelection) -values $typeOptions -width 14
  $w(TypeSelection) configure -state readonly

  grid $w(TypeLabel) $w(TypeSelection) -sticky e
  pack $w(SelectionFrame) -side top

  # Create Parameter Frame
  ttk::frame $w(ComputedFrame) -padding "5"
  ttk::label $w(ReLabel) -text "Reynolds No.: " -anchor e
  entry $w(ReEntry) -textvariable reVar -validate key -validatecommand { validateEntry %P $w(ReEntry) } \
    -background $color(Invalid) -width $entryWidth
  ttk::label $w(LLabel) -text "Characteristic Length: " -anchor e
  entry $w(LEntry) -textvariable lVar -validate key -validatecommand { validateEntry %P $w(LEntry) } \
    -background $color(Invalid) -width $entryWidth
  ttk::label $w(HLabel) -text "Initial Spacing Factor:" -anchor e
  entry $w(HEntry) -textvariable hVar -validate key -validatecommand { validateEntry %P $w(HEntry) } \
    -background $color(Invalid) -width $entryWidth
  ttk::checkbutton $w(ComputedApplyDS) -text "Update Wall Domains" -variable updateWallDoms -command { updateButtons }

  grid $w(ReLabel) $w(ReEntry) -sticky ew -padx 3 -pady 3
  grid $w(LLabel) $w(LEntry) -sticky ew -padx 3 -pady 3
  grid $w(HLabel) $w(HEntry) -sticky ew -pady 3 -padx 3
  grid $w(ComputedApplyDS) -sticky n -padx 3 -pady 3 -columnspan 2
  grid columnconfigure $w(ComputedFrame) 1 -weight 1

  # Create Custom profile frame
  ttk::frame $w(CustomFrame) -padding 3

  # Create Custom delta-S Entry Frame
  ttk::frame $w(CustomApplyFrame) -padding 3
  ttk::checkbutton $w(CustomApplyDS) -text "Update Wall Domains" -variable updateWallDoms -command { updateButtons }
  ttk::label $w(CustomDSLabel) -text "   Spacing: " -anchor e
  entry $w(CustomDS) -textvariable customDS -validate key -validatecommand { validateEntry %P $w(CustomDS) } \
    -background $color(Invalid) -width $entryWidth
  grid $w(CustomApplyDS) $w(CustomDSLabel) $w(CustomDS) -sticky ew -padx 3 -pady 3
  grid columnconfigure $w(CustomApplyFrame) 1 -weight 1
  pack $w(CustomApplyFrame) -side bottom -fill x -anchor center

  # Create Custom profile table frame
  ttk::frame $w(ButtonRowFrame) -padding 3
  ttk::button $w(AddButton) -text "Add Row" \
    -command { incr CustomRowCount; updateCustomTable; updateTableColors; updateButtons }
  ttk::button $w(RemoveButton) -text "Erase Row" \
    -command { incr CustomRowCount -1; updateCustomTable; updateTableColors; updateButtons }
  pack $w(RemoveButton) $w(AddButton) -side right -padx 5 -pady 5 -anchor center
  pack $w(ButtonRowFrame) -side bottom -fill x -anchor center

  # Create Button Frame
  ttk::frame $w(ButtonFrame) -padding "5 5 5 5"
  ttk::button $w(OkButton) -text "OK" -command { ApplyGrowthProfile; exit } -state disabled
  ttk::button $w(CancelButton) -text "Cancel" -command { exit }
  label $w(CadenceLogo) -image [cadenceLogo] -bd 0 -relief flat
  pack $w(CadenceLogo) -side left -anchor w
  pack $w(CancelButton) -side right -anchor e
  pack $w(OkButton) -side right -anchor e
  pack $w(ButtonFrame) -anchor center -side bottom -fill x

  grid columnconfigure $w(ButtonFrame) 0 -weight 1

  bind $w(TypeSelection) <<ComboboxSelected>> { set typeCondition [%W get]; updateParams }

  raise .
}

# PROC: simpleTable
#    Builds the table structure
proc simpleTable { pathName varName args } {
  global color
  set legal {
    -rows
    -cols
    -titlerows
    -titlecols
    -vcmd
    -readonlyrows
    -readonlycols
  }
  array set A {
    -rows 5
    -cols 5
    -titlerows 0
    -titlecols 0
    -readonlyrows {}
    -readonlycols {}
  }

  if { [llength $args] == 0 } {
      error "usage: simpleTable pathName varName ?options...?"
  }

  set idx -1
  foreach { opt value } $args {
    if { [lsearch $legal $opt] == -1 } {
      error "unknown option \042$opt\042"
    }
    if { [incr idx 2] >= [llength $args] } {
      error "value for \042$opt\042 missing"
    }
    set A($opt) $value
  }

  # Now build our table
  destroy $pathName
  frame $pathName
  for { set r 0 } { $r < $A(-rows) } { incr r } {
    set rowWidgets [list]
    for { set c 0 } { $c < $A(-cols) } { incr c } {
      set tw "$pathName.r${r}c$c"
      if { $r < $A(-titlerows) || $c < $A(-titlecols) } {
        if { $::tcl_platform(platform) eq "windows" } {
          set bg SystemDisabledText
        } else {
          set bg darkgrey
        }
        label $tw -textvariable ${varName}\($r,$c\) -relief flat -bg $bg -fg white -width 13 -anchor n
      } elseif { [lsearch $A(-readonlyrows) $r] != -1 || [lsearch $A(-readonlycols) $c] != -1 } {
        label $tw -textvariable $varName\($r,$c\) -relief sunken -bd 2 -anchor n
        $tw config -font [lindex [$tw config -font] 3]
      } else {
        entry $tw -textvariable $varName\($r,$c\) -relief sunken -bd 2 -justify right \
          -width 9 -background $color(Invalid)
        if [info exists A(-vcmd)] {
          $tw config -validate key -vcmd [list $A(-vcmd) $r $c %P $tw]
        }
      }
      lappend rowWidgets $tw
    }
    eval [concat grid $rowWidgets -sticky ew] -padx 2 -pady 2
  }
  for { set c 0 } { $c < $A(-cols) } { incr c } {
    grid columnconfigure $pathName $c -weight 1
  }
}

# PROC: vcmd
#    Validate command for table entry boxes
proc vcmd { row col val pathname } {
  global color
  if { $col == 0 } {
    if { [string is int -strict $val] } {
      $pathname configure -background $color(Valid)
    } else {
      $pathname configure -background $color(Invalid)
    }
  } else {
    if { [string is double -strict $val] } {
      $pathname configure -background $color(Valid)
    } else {
      $pathname configure -background $color(Invalid)
    }
  }
  updateButtons
  return 1
}

#  PROC: updateTableColors
#    Updates the colors of all cells when table rows are changed
proc updateTableColors { } {
  global color CustomRowCount w
  for { set r 1 } { $r < $CustomRowCount } { incr r } {
    for { set c 0 } { $c < 3 } { incr c } {
      set pathname $w(CustomTable).r${r}c$c
      set val [$pathname get]
      if { $c == 0 } {
        if { [string is int -strict $val] } {
          $pathname configure -background $color(Valid)
        } else {
          $pathname configure -background $color(Invalid)
        }
      } else {
        if { [string is double -strict $val] } {
          $pathname configure -background $color(Valid)
        } else {
          $pathname configure -background $color(Invalid)
        }
      }
    }
  }
}

# PROC: buildTable
#    Builds and packs the table
proc buildTable { rows } {
  global table w
  # Fill in our table variable
  unset -nocomplain table
  array set table {
    0,0  "# Layers"
    0,1  "Growth Rate"
    0,2  "Acceleration"
  }

  simpleTable $w(CustomTable) table -rows $rows -cols 3 -titlerows 1 -vcmd vcmd
  pack $w(CustomTable) -padx 10 -pady 5 -side top -fill x
}

# PROC: updateParams
#    Updates the parameter frame when it is changed when the user changes the type
proc updateParams { } {
  global w typeCondition typeOptions

  switch $typeCondition {
    Laminar {
      pack forget $w(CustomFrame)
      pack $w(ComputedFrame) -side top -fill both
      $w(HLabel) configure -text "Initial Spacing Factor: "
    }
    Turbulent {
      pack forget $w(CustomFrame)
      pack $w(ComputedFrame) -side top -fill both
      $w(HLabel) configure -text "Y+: "
    }
    Custom {
      pack forget $w(ComputedFrame)
      updateCustomTable
			updateTableColors
    }
  }
  updateButtons
}

# PROC: updateCustomTable
#    Updates the table when it is changed either by adding a row or removing a row
proc updateCustomTable { } {
  global CustomRowCount w

  buildTable $CustomRowCount
  pack $w(CustomFrame) -fill x -side top -anchor center

  if { $CustomRowCount < 3 } {
    $w(RemoveButton) configure -state disabled
  } else {
    $w(RemoveButton) configure -state normal
  }
}

# PROC: CalcGrowthProfile
#    Calculates the growth profile for TRex and then assigns profile to selected blocks
proc CalcGrowthProfile { } {
  global w typeCondition customDS

  switch $typeCondition {
    Custom {
      set growthRateSchedule [list]
      foreach line [getCustomProfileEntries] {
        set nLayers [lindex $line 0]
        set rate [lindex $line 1]
        set accel [lindex $line 2]

        for { set i 0 } { $i < $nLayers } { incr i } {
          lappend growthRateSchedule $rate
          set rate [expr $rate * $accel]
        }
      }
      return [list $customDS $growthRateSchedule]
    }
    Laminar {
      lassign [pw::Grid calculateLaminarGrowth [$w(ReEntry) get] [$w(LEntry) get] [$w(HEntry) get]] \
        numLinear numAccel growthAccel initialDs
      return [list $initialDs [pw::Grid calculateGrowthRateSchedule $numLinear $numAccel $growthAccel]]
    }
    Turbulent {
      lassign [pw::Grid calculateTurbulentGrowth [$w(ReEntry) get] [$w(LEntry) get] [$w(HEntry) get]] \
        numLinear numAccel growthAccel initialDs
      return [list $initialDs [pw::Grid calculateGrowthRateSchedule $numLinear $numAccel $growthAccel]]
    }
  }

  return [list 0.0 [list]]
}

#  PROC: ApplyGrowthProfile
#    Applies the growth profile attributes to selected blocks and then solves
proc ApplyGrowthProfile { } {
  global customDS updateWallDoms

  pw::Display getSelectedEntities ents
  set UnsBlks [list]
  foreach block $ents(Blocks) {
    if [$block isOfType pw::BlockUnstructured] {
      lappend UnsBlks $block
    }
  }

  if { [llength $UnsBlks] == 0 } {
    set mask [pw::Display createSelectionMask -requireBlock Unstructured]
    wm withdraw .
    if { ![pw::Display selectEntities \
        -description "Pick block(s) for Growth Profile." \
        -selectionmask $mask result] } {
      wm deiconify .
      return
    } else {
      set UnsBlks $result(Blocks)
    }
  }

  lassign [CalcGrowthProfile] wallDS completeProfile

  set solve [pw::Application begin UnstructuredSolver $UnsBlks]
  if { [catch {
    foreach blk $UnsBlks {
      # Find or create wall boundary condition for this block
      if { [catch { pw::TRexCondition getByName "Wall-Profile-[$blk getName]" } wallBC] } {
        set wallBC [pw::TRexCondition create]
        $wallBC setConditionType Wall
        $wallBC setName "Wall-Profile-[$blk getName]"
      }
      if {$updateWallDoms && $wallDS > 0.0} {
        $wallBC setSpacing $wallDS
      }

      $blk setUnstructuredSolverAttribute TRexGrowthProfile [join $completeProfile]
      $blk setUnstructuredSolverAttribute TRexMaximumLayers [llength $completeProfile]
      puts [format "Applied growth profile with %d layers to block '%s'" [llength $completeProfile] [$blk getName]]
      if { $updateWallDoms && $wallDS > 0.0 } {
        set regs [list]
        set nFaces [$blk getFaceCount]
        for { set i 1 } { $i <= $nFaces } { incr i } {
          set face [$blk getFace $i]
          set nDoms [$face getDomainCount]
          for { set j 1 } { $j <= $nDoms } { incr j } {
            lappend regs [list $blk [$face getDomain $j]]
          }
        }
        # Change all Wall domains to use new boundary condition as needed
        foreach bc [pw::TRexCondition getByEntities $regs] reg $regs {
          if { [$bc getConditionType] == "Wall" && ! [$bc equals $wallBC] } {
            $wallBC apply $reg
          }
        }
      }
    }
  } msg] } {
    $solve abort
    puts "Unexpected error occurred. ($msg) No changes were applied."
  } else {
    $solve end
  }
}

# PROC: getCustomProfileEntries
#    Returns an array of the data in the Custom Table
#    Key is the row number and elements are a list of data in the row
proc getCustomProfileEntries { } {
  global CustomRowCount w

  set result [list]

  for { set r 1 } { $r < $CustomRowCount } { incr r } {
    set tempList [list]
    for { set c 0 } { $c < 3 } { incr c } {
      lappend tempList [$w(CustomTable).r${r}c$c get]
    }
    lappend result $tempList
  }

  return $result
}

#  PROC: canCreate
#    Checks if the Ok button should be enabled
proc canCreate { } {
  global w color typeCondition CustomRowCount updateWallDoms

  set result 1

  switch $typeCondition {
    Custom {
      for { set r 1 } { $result && $r < $CustomRowCount } { incr r } {
        for { set c 0 } { $result && $c < 3 } { incr c } {
          set result [string equal -nocase [$w(CustomTable).r${r}c$c cget -background] $color(Valid)]
        }
      }
      if { $result && $updateWallDoms } {
        set result [string equal -nocase [$w(CustomDS) cget -background] $color(Valid)]
      }
    }
    Laminar -
    Turbulent {
      set result [expr \
        [string equal -nocase [$w(ReEntry) cget -background] $color(Valid)] \
          && [string equal -nocase [$w(LEntry) cget -background] $color(Valid)] \
          && [string equal -nocase [$w(HEntry) cget -background] $color(Valid)]]
    }
  }

  return $result
}

#  PROC: validateEntry
#    Checks if there is valid data in entry box
proc validateEntry { entry widget } {
  global w color

  if { [string is double -strict $entry] } {
    $widget configure -background $color(Valid)
  } else {
    $widget configure -background $color(Invalid)
  }
  updateButtons
  return 1
}

# PROC: updateButtons
#    Updates the OK button
proc updateButtons {} {
  global w updateWallDoms
  if { [canCreate] } {
    $w(OkButton) configure -state normal
  } else {
    $w(OkButton) configure -state disabled
  }
  if $updateWallDoms {
    $w(CustomDS) configure -state normal
  } else {
    $w(CustomDS) configure -state disabled
  }
}

#  PROC: cadenceLogo
#    Create the Cadence Logo
proc cadenceLogo { } {
  set logoData {
R0lGODlhgAAYAPQfAI6MjDEtLlFOT8jHx7e2tv39/RYSE/Pz8+Tj46qoqHl3d+vq62ZjY/n4+NT
T0+gXJ/BhbN3d3fzk5vrJzR4aG3Fubz88PVxZWp2cnIOBgiIeH769vtjX2MLBwSMfIP///yH5BA
EAAB8AIf8LeG1wIGRhdGF4bXD/P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIe
nJlU3pOVGN6a2M5ZCI/PiA8eDp4bXBtdGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1w
dGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYxIDY0LjE0MDk0OSwgMjAxMC8xMi8wNy0xMDo1Nzo
wMSAgICAgICAgIj48cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudy5vcmcvMTk5OS8wMi
8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmY6YWJvdXQ9IiIg/3htbG5zO
nhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdFJlZj0iaHR0
cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUcGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh
0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0idX
VpZDoxMEJEMkEwOThFODExMUREQTBBQzhBN0JCMEIxNUM4NyB4bXBNTTpEb2N1bWVudElEPSJ4b
XAuZGlkOkIxQjg3MzdFOEI4MTFFQjhEMv81ODVDQTZCRURDQzZBIiB4bXBNTTpJbnN0YW5jZUlE
PSJ4bXAuaWQ6QjFCODczNkZFOEI4MTFFQjhEMjU4NUNBNkJFRENDNkEiIHhtcDpDcmVhdG9yVG9
vbD0iQWRvYmUgSWxsdXN0cmF0b3IgQ0MgMjMuMSAoTWFjaW50b3NoKSI+IDx4bXBNTTpEZXJpZW
RGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6MGE1NjBhMzgtOTJiMi00MjdmLWE4ZmQtM
jQ0NjMzNmNjMWI0IiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjBhNTYwYTM4LTkyYjItNDL/
N2YtYThkLTI0NDYzMzZjYzFiNCIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g
6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PgH//v38+/r5+Pf29fTz8vHw7+7t7Ovp6Ofm5e
Tj4uHg397d3Nva2djX1tXU09LR0M/OzczLysnIx8bFxMPCwcC/vr28u7q5uLe2tbSzsrGwr66tr
KuqqainpqWko6KhoJ+enZybmpmYl5aVlJOSkZCPjo2Mi4qJiIeGhYSDgoGAf359fHt6eXh3dnV0
c3JxcG9ubWxramloZ2ZlZGNiYWBfXl1cW1pZWFdWVlVUU1JRUE9OTUxLSklIR0ZFRENCQUA/Pj0
8Ozo5ODc2NTQzMjEwLy4tLCsqKSgnJiUkIyIhIB8eHRwbGhkYFxYVFBMSERAPDg0MCwoJCAcGBQ
QDAgEAACwAAAAAgAAYAAAF/uAnjmQpTk+qqpLpvnAsz3RdFgOQHPa5/q1a4UAs9I7IZCmCISQwx
wlkSqUGaRsDxbBQer+zhKPSIYCVWQ33zG4PMINc+5j1rOf4ZCHRwSDyNXV3gIQ0BYcmBQ0NRjBD
CwuMhgcIPB0Gdl0xigcNMoegoT2KkpsNB40yDQkWGhoUES57Fga1FAyajhm1Bk2Ygy4RF1seCjw
vAwYBy8wBxjOzHq8OMA4CWwEAqS4LAVoUWwMul7wUah7HsheYrxQBHpkwWeAGagGeLg717eDE6S
4HaPUzYMYFBi211FzYRuJAAAp2AggwIM5ElgwJElyzowAGAUwQL7iCB4wEgnoU/hRgIJnhxUlpA
SxY8ADRQMsXDSxAdHetYIlkNDMAqJngxS47GESZ6DSiwDUNHvDd0KkhQJcIEOMlGkbhJlAK/0a8
NLDhUDdX914A+AWAkaJEOg0U/ZCgXgCGHxbAS4lXxketJcbO/aCgZi4SC34dK9CKoouxFT8cBNz
Q3K2+I/RVxXfAnIE/JTDUBC1k1S/SJATl+ltSxEcKAlJV2ALFBOTMp8f9ihVjLYUKTa8Z6GBCAF
rMN8Y8zPrZYL2oIy5RHrHr1qlOsw0AePwrsj47HFysrYpcBFcF1w8Mk2ti7wUaDRgg1EISNXVwF
lKpdsEAIj9zNAFnW3e4gecCV7Ft/qKTNP0A2Et7AUIj3ysARLDBaC7MRkF+I+x3wzA08SLiTYER
KMJ3BoR3wzUUvLdJAFBtIWIttZEQIwMzfEXNB2PZJ0J1HIrgIQkFILjBkUgSwFuJdnj3i4pEIlg
eY+Bc0AGSRxLg4zsblkcYODiK0KNzUEk1JAkaCkjDbSc+maE5d20i3HY0zDbdh1vQyWNuJkjXnJ
C/HDbCQeTVwOYHKEJJwmR/wlBYi16KMMBOHTnClZpjmpAYUh0GGoyJMxya6KcBlieIj7IsqB0ji
5iwyyu8ZboigKCd2RRVAUTQyBAugToqXDVhwKpUIxzgyoaacILMc5jQEtkIHLCjwQUMkxhnx5I/
seMBta3cKSk7BghQAQMeqMmkY20amA+zHtDiEwl10dRiBcPoacJr0qjx7Ai+yTjQvk31aws92JZ
Q1070mGsSQsS1uYWiJeDrCkGy+CZvnjFEUME7VaFaQAcXCCDyyBYA3NQGIY8ssgU7vqAxjB4EwA
DEIyxggQAsjxDBzRagKtbGaBXclAMMvNNuBaiGAAA7}

  return [image create photo -format GIF -data $logoData]
}

makeWindow
::tk::PlaceWindow .
update
tkwait window .

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
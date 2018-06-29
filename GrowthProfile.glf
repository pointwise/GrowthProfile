#
# Copyright 2018 (c) Pointwise, Inc.
# All rights reserved.
# 
# This sample Pointwise script is not supported by Pointwise, Inc.
# It is provided freely for demonstration purposes only.  
# SEE THE WARRANTY DISCLAIMER AT THE BOTTOM OF THIS FILE.
#

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
  set w(PwLogo)           $w(ButtonFrame).pwLogo

  
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
  label $w(PwLogo) -image [pwLogo] -bd 0 -relief flat
  pack $w(PwLogo) -side left -anchor w
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
      $wallBC setSpacing $wallDS

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

# PROC setTitleFont
#   set the font for label widget
#    Recieves the pathname for the label, the desired scale, and optionally a boolean for bold font
proc setTitleFont { label scale { bold 0 } } {
  set font [$label cget -font]
  set fontSize [font configure $font -size]
  if { $bold == 1} {
    set labelFont [font create -family [font actual $font -family] -weight bold \
    -size [expr {int($scale * $fontSize)}]]
  } else {
    set labelFont [font create -family [font actual $font -family] \
    -size [expr {int($scale * $fontSize)}]]
  }
  $label configure -font $labelFont
}

# PROC grabSelectedBlocks
#    If unstructured blocks have been selected prior to execution of script
#    then this proc returns a list of those blocks
proc grabSelectedBlocks { } {
}

#  PROC: pwLogo 
#    Create the Pointwise Logo
proc pwLogo { } {
  set logoData {
R0lGODlheAAYAIcAAAAAAAICAgUFBQkJCQwMDBERERUVFRkZGRwcHCEhISYmJisrKy0tLTIyMjQ0
NDk5OT09PUFBQUVFRUpKSk1NTVFRUVRUVFpaWlxcXGBgYGVlZWlpaW1tbXFxcXR0dHp6en5+fgBi
qQNkqQVkqQdnrApmpgpnqgpprA5prBFrrRNtrhZvsBhwrxdxsBlxsSJ2syJ3tCR2siZ5tSh6tix8
ti5+uTF+ujCAuDODvjaDvDuGujiFvT6Fuj2HvTyIvkGKvkWJu0yUv2mQrEOKwEWNwkaPxEiNwUqR
xk6Sw06SxU6Uxk+RyVKTxlCUwFKVxVWUwlWWxlKXyFOVzFWWyFaYyFmYx16bwlmZyVicyF2ayFyb
zF2cyV2cz2GaxGSex2GdymGezGOgzGSgyGWgzmihzWmkz22iymyizGmj0Gqk0m2l0HWqz3asznqn
ynuszXKp0XKq1nWp0Xaq1Hes0Xat1Hmt1Xyt0Huw1Xux2IGBgYWFhYqKio6Ojo6Xn5CQkJWVlZiY
mJycnKCgoKCioqKioqSkpKampqmpqaurq62trbGxsbKysrW1tbi4uLq6ur29vYCu0YixzYOw14G0
1oaz14e114K124O03YWz2Ie12oW13Im10o621Ii22oi23Iy32oq52Y252Y+73ZS51Ze81JC625G7
3JG825K83Je72pW93Zq92Zi/35G+4aC90qG+15bA3ZnA3Z7A2pjA4Z/E4qLA2KDF3qTA2qTE3avF
36zG3rLM3aPF4qfJ5KzJ4LPL5LLM5LTO4rbN5bLR6LTR6LXQ6r3T5L3V6cLCwsTExMbGxsvLy8/P
z9HR0dXV1dbW1tjY2Nra2tzc3N7e3sDW5sHV6cTY6MnZ79De7dTg6dTh69Xi7dbj7tni793m7tXj
8Nbk9tjl9N3m9N/p9eHh4eTk5Obm5ujo6Orq6u3t7e7u7uDp8efs8uXs+Ozv8+3z9vDw8PLy8vL0
9/b29vb5+/f6+/j4+Pn6+/r6+vr6/Pn8/fr8/Pv9/vz8/P7+/gAAACH5BAMAAP8ALAAAAAB4ABgA
AAj/AP8JHEiwoMGDCBMqXMiwocOHECNKnEixosWLGDNqZCioo0dC0Q7Sy2btlitisrjpK4io4yF/
yjzKRIZPIDSZOAUVmubxGUF88Aj2K+TxnKKOhfoJdOSxXEF1OXHCi5fnTx5oBgFo3QogwAalAv1V
yyUqFCtVZ2DZceOOIAKtB/pp4Mo1waN/gOjSJXBugFYJBBflIYhsq4F5DLQSmCcwwVZlBZvppQtt
D6M8gUBknQxA879+kXixwtauXbhheFph6dSmnsC3AOLO5TygWV7OAAj8u6A1QEiBEg4PnA2gw7/E
uRn3M7C1WWTcWqHlScahkJ7NkwnE80dqFiVw/Pz5/xMn7MsZLzUsvXoNVy50C7c56y6s1YPNAAAC
CYxXoLdP5IsJtMBWjDwHHTSJ/AENIHsYJMCDD+K31SPymEFLKNeM880xxXxCxhxoUKFJDNv8A5ts
W0EowFYFBFLAizDGmMA//iAnXAdaLaCUIVtFIBCAjP2Do1YNBCnQMwgkqeSSCEjzzyJ/BFJTQfNU
WSU6/Wk1yChjlJKJLcfEgsoaY0ARigxjgKEFJPec6J5WzFQJDwS9xdPQH1sR4k8DWzXijwRbHfKj
YkFO45dWFoCVUTqMMgrNoQD08ckPsaixBRxPKFEDEbEMAYYTSGQRxzpuEueTQBlshc5A6pjj6pQD
wf9DgFYP+MPHVhKQs2Js9gya3EB7cMWBPwL1A8+xyCYLD7EKQSfEF1uMEcsXTiThQhmszBCGC7G0
QAUT1JS61an/pKrVqsBttYxBxDGjzqxd8abVBwMBOZA/xHUmUDQB9OvvvwGYsxBuCNRSxidOwFCH
J5dMgcYJUKjQCwlahDHEL+JqRa65AKD7D6BarVsQM1tpgK9eAjjpa4D3esBVgdFAB4DAzXImiDY5
vCFHESko4cMKSJwAxhgzFLFDHEUYkzEAG6s6EMgAiFzQA4rBIxldExBkr1AcJzBPzNDRnFCKBpTd
gCD/cKKKDFuYQoQVNhhBBSY9TBHCFVW4UMkuSzf/fe7T6h4kyFZ/+BMBXYpoTahB8yiwlSFgdzXA
5JQPIDZCW1FgkDVxgGKCFCywEUQaKNitRA5UXHGFHN30PRDHHkMtNUHzMAcAA/4gwhUCsB63uEF+
bMVB5BVMtFXWBfljBhhgbCFCEyI4EcIRL4ChRgh36LBJPq6j6nS6ISPkslY0wQbAYIr/ahCeWg2f
ufFaIV8QNpeMMAkVlSyRiRNb0DFCFlu4wSlWYaL2mOp13/tY4A7CL63cRQ9aEYBT0seyfsQjHedg
xAG24ofITaBRIGTW2OJ3EH7o4gtfCIETRBAFEYRgC06YAw3CkIqVdK9cCZRdQgCVAKWYwy/FK4i9
3TYQIboE4BmR6wrABBCUmgFAfgXZRxfs4ARPPCEOZJjCHVxABFAA4R3sic2bmIbAv4EvaglJBACu
IxAMAKARBrFXvrhiAX8kEWVNHOETE+IPbzyBCD8oQRZwwIVOyAAXrgkjijRWxo4BLnwIwUcCJvgP
ZShAUfVa3Bz/EpQ70oWJC2mAKDmwEHYAIxhikAQPeOCLdRTEAhGIQKL0IMoGTGMgIBClA9QxkA3U
0hkKgcy9HHEQDcRyAr0ChAWWucwNMIJZ5KilNGvpADtt5JrYzKY2t8nNbnrzm+B8SEAAADs=}

  return [image create photo -format GIF -data $logoData]
}  

makeWindow
::tk::PlaceWindow .
update
tkwait window .

#
# DISCLAIMER:
# TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, POINTWISE DISCLAIMS
# ALL WARRANTIES, EITHER EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED
# TO, IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE, WITH REGARD TO THIS SCRIPT.  TO THE MAXIMUM EXTENT PERMITTED 
# BY APPLICABLE LAW, IN NO EVENT SHALL POINTWISE BE LIABLE TO ANY PARTY 
# FOR ANY SPECIAL, INCIDENTAL, INDIRECT, OR CONSEQUENTIAL DAMAGES 
# WHATSOEVER (INCLUDING, WITHOUT LIMITATION, DAMAGES FOR LOSS OF 
# BUSINESS INFORMATION, OR ANY OTHER PECUNIARY LOSS) ARISING OUT OF THE 
# USE OF OR INABILITY TO USE THIS SCRIPT EVEN IF POINTWISE HAS BEEN 
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGES AND REGARDLESS OF THE 
# FAULT OR NEGLIGENCE OF POINTWISE.
#

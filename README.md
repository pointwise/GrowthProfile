# GrowthProfile

Copyright 2021 Cadence Design Systems, Inc. All rights reserved worldwide.

A Glyph script that allows the user to create and apply custom growth profiles to unstructured T-Rex blocks. Optionally, initial wall spacing can be applied to existing Wall boundaries of the selected blocks (new Wall boundary conditions will be created by this script, but only applied to domains that already have Wall BC's defined).

Three types of growth profiles that can be defined: Laminar, Turbulent, and Custom. Once a type is selected and all the required fields are set, press OK to apply the computed growth profile. If the script is invoked with at least one unstructured block selected, only the selected blocks will be updated; otherwise, the script will enter selection mode.

Note: This script can only be run with Pointwise version V18.1R2 or later.

## Profile Types

### Laminar

![GrowthProfileLaminar](https://raw.github.com/pointwise/GrowthProfile/master/GrowthProfileLaminar.png)

This type has required fields of:

* Reynolds Number - free-stream flow condition
* Characteristic Length - linear dimension used to determine boundary layer scale
* Initial Spacing Factor - the fraction of the computed boundary layer thickness to use as the initial wall spacing)
    
In addition, a checkbox option to apply the computed initial wall spacing can be selected.

### Turbulent

![GrowthProfileTurbulent](https://raw.github.com/pointwise/GrowthProfile/master/GrowthProfileTurbulent.png)

This type has required fields of:

* Reynolds Number - free-stream flow condition
* Characteristic Length - linear dimension used to determine boundary layer scale
* Y+ - used to compute the initial wall spacing (See [Y+ Calculator](https://www.pointwise.com/yplus/index.html))

In addition, a checkbox option to apply the computed initial wall spacing can be selected.

### Custom

![GrowthProfileCustom](https://raw.github.com/pointwise/GrowthProfile/master/GrowthProfileCustom.png)

In Custom mode, a table of values is constructed to provide fine-grained control of the computed profile. Rows can be added or removed from the bottom of the table by pressing the Add Row or Erase Row buttons. The values in all columns is required for all rows:

* Number of Layers for each section of the profile
* Growth Rate of the first layer in the section
* Acceleration of the Growth Rate to compute each successive layer in the section

In addition, a checkbox option to apply the computed initial wall spacing can be selected. If this is checked, the adjacent Spacing field is also required.

An example of applying a custom growth profile to some simple blocks is illustrated in the image below:

![GrowthProfileCustomResult](https://raw.github.com/pointwise/GrowthProfile/master/GrowthProfileCustomResult.png)

## Disclaimer

This file is licensed under the Cadence Public License Version 1.0 (the "License"), a copy of which is found in the LICENSE file, and is distributed "AS IS." 
TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, CADENCE DISCLAIMS ALL WARRANTIES AND IN NO EVENT SHALL BE LIABLE TO ANY PARTY FOR ANY DAMAGES ARISING OUT OF OR RELATING TO USE OF THIS FILE. 
Please see the License for the full text of applicable terms.
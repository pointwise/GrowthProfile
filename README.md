# GrowthProfile

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

Scripts are freely provided. They are not supported products of Pointwise, Inc. Some scripts have been written and contributed by third parties outside of Pointwise's control.

TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, POINTWISE DISCLAIMS ALL WARRANTIES, EITHER EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, WITH REGARD TO THESE SCRIPTS. TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, IN NO EVENT SHALL POINTWISE BE LIABLE TO ANY PARTY FOR ANY SPECIAL, INCIDENTAL, INDIRECT, OR CONSEQUENTIAL DAMAGES WHATSOEVER (INCLUDING, WITHOUT LIMITATION, DAMAGES FOR LOSS OF BUSINESS INFORMATION, OR ANY OTHER PECUNIARY LOSS) ARISING OUT OF THE USE OF OR INABILITY TO USE THESE SCRIPTS EVEN IF POINTWISE HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES AND REGARDLESS OF THE FAULT OR NEGLIGENCE OF POINTWISE.

Project_Scorpion
================

Code repository for the Project Scorpion smart liquor cabinet project


The barcode scanner requires the following udev rule:

SUBSYSTEM=="input", ATTRS{idVendor}=="1d57", ATTRS{idProduct}=="001c" MODE="0644"
EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:extras
LIBS:puck_v2.0-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Label 5550 2700 2    60   ~ 0
5V
$Comp
L TLC5916IN U1
U 1 1 5599BF98
P 9750 1900
F 0 "U1" H 10000 2450 60  0000 C CNN
F 1 "TLC5916IN" H 9750 1450 60  0000 C CNN
F 2 "" H 9850 2100 60  0000 C CNN
F 3 "" H 9850 2100 60  0000 C CNN
	1    9750 1900
	1    0    0    -1  
$EndComp
$Comp
L LED D1
U 1 1 5599C0F6
P 8600 1900
F 0 "D1" H 8600 2000 50  0000 C CNN
F 1 "LED" H 8600 1800 50  0000 C CNN
F 2 "" H 8600 1900 60  0000 C CNN
F 3 "" H 8600 1900 60  0000 C CNN
	1    8600 1900
	1    0    0    -1  
$EndComp
$Comp
L LED D2
U 1 1 5599C1EF
P 8600 2200
F 0 "D2" H 8600 2300 50  0000 C CNN
F 1 "LED" H 8600 2100 50  0000 C CNN
F 2 "" H 8600 2200 60  0000 C CNN
F 3 "" H 8600 2200 60  0000 C CNN
	1    8600 2200
	1    0    0    -1  
$EndComp
$Comp
L LED D3
U 1 1 5599C239
P 8600 2500
F 0 "D3" H 8600 2600 50  0000 C CNN
F 1 "LED" H 8600 2400 50  0000 C CNN
F 2 "" H 8600 2500 60  0000 C CNN
F 3 "" H 8600 2500 60  0000 C CNN
	1    8600 2500
	1    0    0    -1  
$EndComp
$Comp
L LED D4
U 1 1 5599C26A
P 8600 2800
F 0 "D4" H 8600 2900 50  0000 C CNN
F 1 "LED" H 8600 2700 50  0000 C CNN
F 2 "" H 8600 2800 60  0000 C CNN
F 3 "" H 8600 2800 60  0000 C CNN
	1    8600 2800
	1    0    0    -1  
$EndComp
Wire Wire Line
	8400 1900 8150 1900
Wire Wire Line
	8150 1900 8150 3150
Wire Wire Line
	8400 2800 8150 2800
Connection ~ 8150 2800
Wire Wire Line
	8400 2500 8150 2500
Connection ~ 8150 2500
Wire Wire Line
	8400 2200 8150 2200
Connection ~ 8150 2200
Text Label 8150 3150 0    60   ~ 0
5V
Wire Wire Line
	9150 1900 8800 1900
Wire Wire Line
	9150 2000 8850 2000
Wire Wire Line
	8850 2000 8850 2200
Wire Wire Line
	8850 2200 8800 2200
Wire Wire Line
	9150 2100 8900 2100
Wire Wire Line
	8900 2100 8900 2500
Wire Wire Line
	8900 2500 8800 2500
Wire Wire Line
	9150 2200 8950 2200
Wire Wire Line
	8950 2200 8950 2800
Wire Wire Line
	8950 2800 8800 2800
NoConn ~ 10350 2200
NoConn ~ 10350 2100
NoConn ~ 10350 2000
NoConn ~ 10350 1900
Text Label 10350 1500 0    60   ~ 0
5V
Text Label 9150 1700 2    60   ~ 0
B1
Text Label 9150 1800 2    60   ~ 0
B2
Text Label 10350 1800 0    60   ~ 0
B3
NoConn ~ 10350 1700
Text Label 9150 1600 2    60   ~ 0
B0
$Comp
L R R8
U 1 1 5599C96F
P 10700 1600
F 0 "R8" V 10780 1600 50  0000 C CNN
F 1 "700" V 10700 1600 50  0000 C CNN
F 2 "" V 10630 1600 30  0000 C CNN
F 3 "" H 10700 1600 30  0000 C CNN
	1    10700 1600
	0    1    1    0   
$EndComp
Wire Wire Line
	10350 1600 10550 1600
$Comp
L LOAD_CELL P1
U 1 1 5599CE64
P 1600 2250
F 0 "P1" H 1600 2500 50  0000 C CNN
F 1 "LOAD_CELL" V 1800 2250 50  0000 C CNN
F 2 "" H 1600 2250 60  0000 C CNN
F 3 "" H 1600 2250 60  0000 C CNN
	1    1600 2250
	-1   0    0    1   
$EndComp
Text Label 1800 2400 0    60   ~ 0
5V
Wire Wire Line
	1800 2200 3650 2200
Wire Wire Line
	1800 2300 2300 2300
$Comp
L R R7
U 1 1 5599D35D
P 4100 2500
F 0 "R7" V 4180 2500 50  0000 C CNN
F 1 "10k" V 4100 2500 50  0000 C CNN
F 2 "" V 4030 2500 30  0000 C CNN
F 3 "" H 4100 2500 30  0000 C CNN
	1    4100 2500
	0    1    1    0   
$EndComp
$Comp
L C C3
U 1 1 5599D39A
P 4400 2650
F 0 "C3" H 4425 2750 50  0000 L CNN
F 1 "10uF" H 4425 2550 50  0000 L CNN
F 2 "" H 4438 2500 30  0000 C CNN
F 3 "" H 4400 2650 60  0000 C CNN
	1    4400 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	4250 2500 4700 2500
Connection ~ 4400 2500
Wire Wire Line
	4400 2800 4400 2950
$Comp
L GND #PWR3
U 1 1 5599D4AE
P 4400 2950
F 0 "#PWR3" H 4400 2700 50  0001 C CNN
F 1 "GND" H 4400 2800 50  0000 C CNN
F 2 "" H 4400 2950 60  0000 C CNN
F 3 "" H 4400 2950 60  0000 C CNN
	1    4400 2950
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR1
U 1 1 5599D5B8
P 1800 2100
F 0 "#PWR1" H 1800 1850 50  0001 C CNN
F 1 "GND" H 1800 1950 50  0000 C CNN
F 2 "" H 1800 2100 60  0000 C CNN
F 3 "" H 1800 2100 60  0000 C CNN
	1    1800 2100
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR4
U 1 1 5599DB41
P 7000 2700
F 0 "#PWR4" H 7000 2450 50  0001 C CNN
F 1 "GND" H 7000 2550 50  0000 C CNN
F 2 "" H 7000 2700 60  0000 C CNN
F 3 "" H 7000 2700 60  0000 C CNN
	1    7000 2700
	-1   0    0    1   
$EndComp
Wire Wire Line
	6900 2700 7000 2700
$Comp
L GND #PWR6
U 1 1 5599DCB3
P 11050 1600
F 0 "#PWR6" H 11050 1350 50  0001 C CNN
F 1 "GND" H 11050 1450 50  0000 C CNN
F 2 "" H 11050 1600 60  0000 C CNN
F 3 "" H 11050 1600 60  0000 C CNN
	1    11050 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	10850 1600 11050 1600
$Comp
L GND #PWR5
U 1 1 5599DDA9
P 9100 1500
F 0 "#PWR5" H 9100 1250 50  0001 C CNN
F 1 "GND" H 9100 1350 50  0000 C CNN
F 2 "" H 9100 1500 60  0000 C CNN
F 3 "" H 9100 1500 60  0000 C CNN
	1    9100 1500
	-1   0    0    1   
$EndComp
Wire Wire Line
	9150 1500 9100 1500
$Comp
L PIC16F1704 P4
U 1 1 5599E665
P 6250 3000
F 0 "P4" H 5750 3400 50  0000 C CNN
F 1 "PIC16F1704" H 6200 2600 50  0000 C CNN
F 2 "" H 5750 3150 60  0000 C CNN
F 3 "" H 5750 3150 60  0000 C CNN
	1    6250 3000
	1    0    0    -1  
$EndComp
Text Label 5550 2800 2    60   ~ 0
B2
$Comp
L ICSP_Header P2
U 1 1 5599F7E4
P 1800 3500
F 0 "P2" H 1800 3750 50  0000 C CNN
F 1 "ICSP_Header" H 2000 3050 50  0000 C CNN
F 2 "" H 1800 3500 60  0000 C CNN
F 3 "" H 1800 3500 60  0000 C CNN
	1    1800 3500
	-1   0    0    1   
$EndComp
NoConn ~ 2000 3150
Wire Wire Line
	2100 3250 2000 3250
Wire Wire Line
	2100 3350 2000 3350
Wire Wire Line
	2000 3450 2250 3450
Wire Wire Line
	2000 3550 2250 3550
Wire Wire Line
	2100 3650 2000 3650
Text Label 2000 3250 0    60   ~ 0
B0
Text Label 2000 3350 0    60   ~ 0
B1
Text Label 2100 3650 0    60   ~ 0
Vpp
Text Label 6900 2900 0    60   ~ 0
B0
Text Label 6900 2800 0    60   ~ 0
B1
Text Label 5550 3000 2    60   ~ 0
Vpp
Text Label 2250 3550 0    60   ~ 0
5V_PROG
$Comp
L R R6
U 1 1 559A081E
P 3700 4550
F 0 "R6" V 3780 4550 50  0000 C CNN
F 1 "10R" V 3700 4550 50  0000 C CNN
F 2 "" V 3630 4550 30  0000 C CNN
F 3 "" H 3700 4550 30  0000 C CNN
	1    3700 4550
	0    1    1    0   
$EndComp
Text Label 3250 4650 2    60   ~ 0
5V_PROG
Text Label 4100 4650 0    60   ~ 0
5V
Text Label 5550 2900 2    60   ~ 0
ADC
Text Label 5550 3100 2    60   ~ 0
OPA+
Text Label 5550 3200 2    60   ~ 0
OPA-
Text Label 5550 3300 2    60   ~ 0
OPOUT
Text Label 6900 3200 0    60   ~ 0
SDA
Text Label 6900 3100 0    60   ~ 0
SCL
Text Label 6900 3000 0    60   ~ 0
B3
NoConn ~ 6900 3300
$Comp
L I2C_Header P3
U 1 1 559A14E9
P 1800 4150
F 0 "P3" H 1800 4400 50  0000 C CNN
F 1 "I2C_Header" H 1900 4100 50  0000 C CNN
F 2 "" H 1800 4150 60  0000 C CNN
F 3 "" H 1800 4150 60  0000 C CNN
	1    1800 4150
	-1   0    0    1   
$EndComp
Text Label 2000 4200 0    60   ~ 0
SCL
Text Label 2000 4300 0    60   ~ 0
SDA
Text Label 3150 2450 0    60   ~ 0
OPA+
Wire Wire Line
	3050 2200 3050 2300
Text Label 3150 2300 0    60   ~ 0
OPA-
$Comp
L R R3
U 1 1 559A2209
P 3650 2350
F 0 "R3" V 3730 2350 50  0000 C CNN
F 1 "1M" V 3650 2350 50  0000 C CNN
F 2 "" V 3580 2350 30  0000 C CNN
F 3 "" H 3650 2350 30  0000 C CNN
	1    3650 2350
	-1   0    0    1   
$EndComp
Wire Wire Line
	3650 2500 3950 2500
Text Label 4700 2500 2    60   ~ 0
ADC
Wire Wire Line
	3750 2500 3750 2900
Connection ~ 3750 2500
Text Label 3750 2900 1    60   ~ 0
OPOUT
Text Label 2250 3450 0    60   ~ 0
GND_PROG
$Comp
L R R5
U 1 1 559A2FFF
P 3700 4300
F 0 "R5" V 3780 4300 50  0000 C CNN
F 1 "10R" V 3700 4300 50  0000 C CNN
F 2 "" V 3630 4300 30  0000 C CNN
F 3 "" H 3700 4300 30  0000 C CNN
	1    3700 4300
	0    1    1    0   
$EndComp
Text Label 4100 4150 0    60   ~ 0
GND
Text Label 3300 4150 2    60   ~ 0
GND_PROG
Text Notes 4050 2400 0    60   ~ 0
ADC Low-pass Filter\nRC=.1s
Text Notes 2300 2100 0    60   ~ 0
Feedback resistors for\nOp-Amp circuit(G=1000)
Text Notes 8350 3200 0    60   ~ 0
Discrete LEDs\n20mA per\nVf@20mA=2.1V
Text Notes 3000 5400 0    60   ~ 0
Prevent Shorts between different\npower sources, but still allow\npowering via either programmer or\nmain power
$Comp
L C C2
U 1 1 559ACB0F
P 3700 4800
F 0 "C2" H 3725 4900 50  0000 L CNN
F 1 "10uF" H 3725 4700 50  0000 L CNN
F 2 "" H 3738 4650 30  0000 C CNN
F 3 "" H 3700 4800 60  0000 C CNN
	1    3700 4800
	0    1    1    0   
$EndComp
$Comp
L C C1
U 1 1 559ACB66
P 3700 4050
F 0 "C1" H 3725 4150 50  0000 L CNN
F 1 "10uF" H 3725 3950 50  0000 L CNN
F 2 "" H 3738 3900 30  0000 C CNN
F 3 "" H 3700 4050 60  0000 C CNN
	1    3700 4050
	0    1    1    0   
$EndComp
Wire Wire Line
	4000 4050 4000 4300
Wire Wire Line
	4000 4050 3850 4050
Wire Wire Line
	4000 4300 3850 4300
Wire Wire Line
	3400 4300 3550 4300
Wire Wire Line
	3400 4050 3400 4300
Wire Wire Line
	3400 4050 3550 4050
Wire Wire Line
	3850 4550 4000 4550
Wire Wire Line
	4000 4550 4000 4800
Wire Wire Line
	4000 4800 3850 4800
Wire Wire Line
	3550 4550 3400 4550
Wire Wire Line
	3400 4550 3400 4800
Wire Wire Line
	3400 4800 3550 4800
Wire Wire Line
	3300 4150 3400 4150
Connection ~ 3400 4150
Wire Wire Line
	4000 4150 4100 4150
Connection ~ 4000 4150
Wire Wire Line
	4000 4650 4100 4650
Connection ~ 4000 4650
Wire Wire Line
	3400 4650 3250 4650
Connection ~ 3400 4650
Text Notes 950  3000 0    60   ~ 0
ISCP used for programming \nw/ PICKIT 3 programmer/debugger
Text Notes 1150 4600 0    60   ~ 0
To I2C Bus that connects to\nother puck and Raspberry Pi
$Comp
L R R4
U 1 1 55A19A5A
P 2750 2650
F 0 "R4" V 2830 2650 50  0000 C CNN
F 1 "1M" V 2750 2650 50  0000 C CNN
F 2 "" V 2680 2650 30  0000 C CNN
F 3 "" H 2750 2650 30  0000 C CNN
	1    2750 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	2300 2300 2300 2450
Wire Wire Line
	2300 2450 3150 2450
Wire Wire Line
	2750 2500 2750 2450
Connection ~ 2750 2450
Wire Wire Line
	2750 2800 2750 2900
$Comp
L GND #PWR2
U 1 1 55A19FFD
P 2750 2900
F 0 "#PWR2" H 2750 2650 50  0001 C CNN
F 1 "GND" H 2750 2750 50  0000 C CNN
F 2 "" H 2750 2900 60  0000 C CNN
F 3 "" H 2750 2900 60  0000 C CNN
	1    2750 2900
	1    0    0    -1  
$EndComp
Wire Wire Line
	3050 2300 3150 2300
Connection ~ 3050 2200
Text Notes 1300 1850 0    60   ~ 0
Load Cell's output \nimpedance is 1k
$EndSCHEMATC

#! /usr/bin/env python3
################################################################################
# utp.py: List capacitances of unshielded twisted pairs
#
# by Dan Nygren
# Permanent E-mail: dan.nygren@gmail.com
#
# Copyright 2013, 2024 by Daniel C. Nygren
#
#      This program calculates capacitances of unshielded twisted pairs made
# from two individual pieces of hookup wire twisted together using two different
# formulas (General Cable & Howard Johnson's) in both picofarads per foot and
# picofarads per millimeter.
#
# General Cable Electronics Wire & Cable Catalog, 2010, page 203
# Cable Design Equations - Balanced Pair, Capacitance (Unshielded Twisted Pair)
#
# Howard Johnson & Martin Graham "High Speed Digital Design - A Handbook of
# Black Magic" Prentice Hall, 1993, page 428
#
# CALLING SEQUENCE  python utp.py 
#                   utp.py (if this file has execute permission) 
#
# EXAMPLES          python utp.py > capacitances.txt
#                   # Sort by capacitance all 30 gauge semi-rigid PVC insulated
#                   python utp.py | grep 'AWG30' | grep 'PVC(Semi' | sort -k 9
#
# TARGET SYSTEM        Any
#
# DEVELOPMENT SYSTEM   Python3, Solaris 10, Linux
#
# CALLS                import string, sys, math
#
# CALLED BY            N/A 
#
# INPUTS               DIELECTRIC_LIST, CONDUCTOR_LIST,
#                      INSULATION_THICKNESS_LIST, STRANDING_FACTOR
#
# OUTPUTS              Capacitances in picofarads per foot and millimeter
#
# RETURNS              0=Success
#
# ERROR HANDLING       None
#
# WARNINGS             1) Find and select the STRANDING_FACTOR for the wire used
#
################################################################################

# import the following modules
import string, sys, math

# Select the number of strands in each wire pair
# STRANDING_FACTOR = 1.000 # 1 strand
STRANDING_FACTOR = 0.939 # 7 strands
#STRANDING_FACTOR = 0.970 # 19 strands
#STRANDING_FACTOR = 0.980 # 37 strands
#STRANDING_FACTOR = 0.985 # 61 strands
#STRANDING_FACTOR = 0.988 # 91 strands

DIELECTRIC_LIST=[
# Material Name, Dielectric Constant
("ECTFE/Halar",     2.60),
("PFA/Teflon",      2.15),
("PVC",             5.00),
("PVC(Semi-rigid)", 3.60),
("PVDF/Kynar/SOLEF",7.70),
("Polyethylene",    2.29),
("Polypropylene",   2.25),
("Polyurethane",    6.50),
("Rubber(butyl)",   4.0),
("Rubber(natural)", 5.0),
("Rubber(SBR)",     4.0),
("Rubber(silicone)",3.1),
("TFE/Teflon",      2.1),
("TPE",             5.0),
("Teflon",          2.10),
("Tefzel",          2.6)
]

CONDUCTOR_LIST=[
# Gauge, Stranding, Diameter in inches
("AWG30", "7/38", 0.012),
("AWG28", "7/36", 0.015),
("AWG26", "7/34", 0.019),
("AWG24", "7/32", 0.024),
("AWG22", "7/30", 0.030)
]

INSULATION_THICKNESS_LIST=[
# Thickness in inches
0.006,
0.010,
0.011,
0.012,
0.015,
0.017,
0.018,
0.019,
0.030,
0.032,
0.045,
0.060
]

# 25.4 mm per inch and 12 inches per foot
MM_PER_FT = 25.4 * 12.0

for material in DIELECTRIC_LIST:
    for conductor in CONDUCTOR_LIST:
        for thickness in INSULATION_THICKNESS_LIST:
            # General Cable capacitance equation (in pico Farads per foot)
            capacitance = ( 2.2 * material[1] ) / \
            math.log10( ( 1.3 * ( ( 2.0 * thickness ) + conductor[2] ) ) / \
            ( STRANDING_FACTOR * conductor[2] ) ) 
            capacitance_mm = capacitance / MM_PER_FT
            # Howard Johnson capacitance equation (in pico Farads per foot)
            capacitance2 = ( 12 * 0.7065 ) / \
            math.log( ( 2 * ( ( 2.0 * thickness ) + conductor[2] ) ) / \
            ( STRANDING_FACTOR * conductor[2] ) ) * material[1]
            capacitance2_mm = capacitance2 / MM_PER_FT
            print("%s %1.3f inch thick %s = %5.2f pf/ft %5.4f pf/mm "\
            "(General Cable) %5.2f pf/ft %5.4f pf/mm (Howard Johnson)" \
            % (conductor[0], thickness, material[0], capacitance, \
            capacitance_mm, capacitance2, capacitance2_mm))

# Set a Unix "success" exit code
exit_code = 0

# Return exit_code
sys.exit(exit_code)

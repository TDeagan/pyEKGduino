# pyEKGduino
Arduino EKG shield to Python GUI EKG (QT, QTc, etc.) measurement

I thought I'd share the app I've been working up to determine QTc as captured by the Olimex EKG/EMG Shield. I have shamelessly assembled this from pieces and parts of pubic domain code.  If you see something of yours, Thank You!!

Explanation of QTc: http://en.wikipedia.org/wiki/QT_interval

This is rough around the edges, but I thought it would be helpful to offer more open source code examples for working with this lovely little shield.

Note, a single shield offers three leads, optimum positioning for a three lead EKG measurement appears to be left and right arm (wrist) and right leg (ankle).

Since I'm using a single shield(channel) unit, the (Duemilanove) Arduino code is stripped down for speed. It simply returns the analog value as measured every .0039 sec (as opposed to the multi-byte packet defined in the demo code for ElectricGuru).

The Arduino code's data is caught by the following Python3 code.   It does the following;
Finds available com ports (should be cross platform, I lifted the detection from the miniterm code, but I have only tested on windows)
Opens a dialog to allow you to pick a com port, which it tests.
Opens a window which allows you to capture signal (each time you toggle through a capture session, it starts a new one rather than appending)
Allows you to move marker lines in the plot window, via the mouse, to mark R1, R2, Q, T (see link above)
Allows you to click the calc button and calculate; Heartrate, RR, QT and QTc (see link above)
Left clicking on the plot window allows you to pan the plot
Right clicking on the plot window allows you to export the data via image or CSV, zoom and more (thanks pyqtgraph!)

Obligatory Notice:
This software is public domain and for demonstration purposes only.  Do not rely on the calculated values for any aspect of your cardiac or regular health.  Consult a doctor if you want to get a real EKG.

The code associated with this project is under the Creative Commons CC0 1.0 Public Domain Dedication:
https://creativecommons.org/publicdomain/zero/1.0/

No Copyright

 This license is acceptable for Free Cultural Works.
The person who associated a work with this deed has dedicated the work to the public domain by waiving all of his or her rights to the work worldwide under copyright law, including all related and neighboring rights, to the extent allowed by law.

You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission. See Other Information below.
Other Information
In no way are the patent or trademark rights of any person affected by CC0, nor are the rights that other persons may have in the work or in how the work is used, such as publicity or privacy rights.
Unless expressly stated otherwise, the person who associated a work with this deed makes no warranties about the work, and disclaims liability for all uses of the work, to the fullest extent permitted by applicable law.
When using or citing the work, you should not imply endorsement by the author or the affirmer.

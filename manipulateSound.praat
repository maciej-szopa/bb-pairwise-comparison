form Manipulate sound
	sentence fileName yoyo_modal.wav
	real pitchMedianShift 0.0
	real vocalTractLength 1.0
	real durationFactor 1.0
	real pitchRangeFactor 1.0
endform

obj = Read from file: fileName$
selectObject: obj

if fileName$ = "yoyo_breathy4.wav"
    base = 91.3718
elsif fileName$ = "yoyo_modal.wav"
    base = 90.5381
else
    base = 89.1323
endif

output = Change gender: 75.0, 600.0, vocalTractLength, base * (2 ^ (pitchMedianShift / 12)), pitchRangeFactor, durationFactor
selectObject: output
Play
# XML redactor
# Apply for subfolder structure
# Replace PatientID with 3digit number in the filename


import tkinter as tk #python3 tkinter
from tkinter import ttk
from tkinter import filedialog
import xml.etree.ElementTree as ET
import os


win = tk.Tk()
win.title("PHI redactor")

win.geometry("600x350")
win.minsize(width=600,height=370)

# Background
win.config(bg="#4b2e83")

labelFrame = ttk.LabelFrame(text = "Choose Folder")
labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)


def fileDialog():
    dirname = filedialog.askdirectory()
    en.config(text=dirname)

def remove_PHI():
	dirpath = en.cget("text")
	
	try:
		os.mkdir(str(dirpath)+'/redacted_xml')
	except:
		pass

	subfolders = os.listdir(dirpath)
	#print(subfolders)

	for sf in subfolders:
		if sf != '.DS_Store' and sf != 'redacted_xml':
			subfolders2 = os.listdir(str(dirpath)+'/'+str(sf))
			os.mkdir(str(dirpath)+'/redacted_xml/'+str(sf))
			#print(subfolders2)

			for sf2 in subfolders2:
				if sf2 != '.DS_Store':
					files = os.listdir(str(dirpath)+'/'+str(sf)+'/'+str(sf2))
					os.mkdir(str(dirpath)+'/redacted_xml/'+str(sf)+'/'+str(sf2))
					#print(files)

					for f in files:
						if f.endswith('.xml'):
							filepath = dirpath+'/'+str(sf)+'/'+str(sf2)+'/'+str(f)
							tree = ET.parse(filepath)
							root = tree.getroot()

							# MuseInfo/version
							root[0][0].text = 'X'*3

							# PatientDemographics
							for p in root[1]:
								p.text = 'X'*3
								#p.set('RemovePHI','yes')

							# PatientID
							root[1][0].text = str(f[0:3])

							# TestDemographics
							re ={"SiteName", "LocationName", "AcquisitionTime", "AcquisitionDate"}
							for p in root[2]: 
								if p.tag not in re:
									p.text = 'X'*3

							# Order
							for p in root[3]:
								p.text = 'X'*3

							new_f = f.replace(' ','_')
							tree.write(str(dirpath)+'/redacted_xml/'+str(sf)+'/'+str(sf2)+'/'+str(new_f))


	op.config(text='System message: Done!')


# Instruction
lb = tk.Label(bg="#4b2e83", fg="#e8e3d3", text=
	"[Customized for UW team]\n\n"
	"For XML files exported from MUSE system, this program replaces PHI in the with XXX.\n"
	"1. Click \'Browse\' to select a folder which contains subfolders. \n"
	"2. Hit \'Remove PHI\'. \n Redacted files will be saved"
	"under a subdirectory named \'redacted_xml\'.\n"

)
lb.grid(row=0,column=0)

# File directory
en = tk.Label(labelFrame)
en.grid(row=1,column=0)

browse = tk.Button(labelFrame, text = "Step1: Browse",command = fileDialog)
browse.grid(column = 0, row = 2)

# Run Button
btn = tk.Button(text="Step2: Remove PHI")
btn.config(command=remove_PHI)
btn.grid(row=3,column=0, padx = 20, pady = 20)

# Message
op = tk.Label(bg="#4b2e83", fg="#e8e3d3", text="System message: Follow the instruction")
op.grid(row=4,column=0)

op = tk.Label(bg="#4b2e83", fg="#000000", text="Written by ZH Chen. Jun 17, 2020")
op.grid(row=5,column=0)
op = tk.Label(bg="#4b2e83", fg="#000000", text="Last Edit: Jun 30, 2020")
op.grid(row=6,column=0)

win.mainloop()


# pyinstaller --onefile --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' XMLredactor_UW.py

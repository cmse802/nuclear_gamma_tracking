"""Summary.

Written by: Roy Salinas

Main module to control automation in LISE++ with NSCL configuration file.
The implementation of the FRIB configuration file is yet to be developed.

Purpose: To retrive particular parameters from LISE++ such as beam intensity,
beam purity, wedge thickness, wedge angle, momentum acceptance, focal
plane slit width, and Image 2 slit width.

All beam data comes from NSCL website: https://nscl.msu.edu/users/beams.html

Python version: 3.7.1
Currently, this is has only been tested on a Windows OS.
"""

import time
import csv
import os
import platform
import pyautogui as pag
import pyperclip as pc
import pandas as pd

"""
pixel locations for each isotope based on my screen (Resolution: 1920x1080)

Note: This can be improved to contain images of the isotope that appears on the screen.
Doing this rids the dependence on one's screen resolution and local pixel coordinates.
"""


#useros = platform.system()

#if useros == "Linux":
#    print("Using a Linux OS...")
#    desktop = os.path.expanduser("~/Desktop")
#    print(f"Your desktop path is: {desktop}")
#elif useros == "Windows":
#print("Using a Windows OS...")

home = os.path.expanduser('~') #find your home directory 
desktop = home + "\Desktop"
print(f"Your desktop path is {desktop}")


pixel_locations = {
    "Mg_32": {
        "x": 1121, "y": 626}, "Mg_33": {
            "x": 1116, "y": 626}, "Mg_34": {
                "x": 1116, "y": 626}, "Mg_35": {
                    "x": 1116, "y": 626}, "Mg_36": {
                        "x": 1136, "y": 626}, "Mg_37": {
                            "x": 1116, "y": 626}, "Mg_38": {
                                "x": 1116, "y": 626}, "Mg_40": {
                                    "x": 1106, "y": 626}}


"""
An array of dictionaries (c++ maps). "data" is the key for the corresponding isotope and
its value is an array of data. Using zeros as place holders for intialization.
"""
# array of maps, data is the key to the map, replace the zero's with arrays of data
# isotppe is one of the keys, data is the other key for that map with
# their corresponding values
isotope_info = [
    {"isotope": "Mg_32", "data": 0.0},
    {"isotope": "Mg_33", "data": 0.0},
    {"isotope": "Mg_34", "data": 0.0},
    {"isotope": "Mg_35", "data": 0.0},
    {"isotope": "Mg_36", "data": 0.0},
    {"isotope": "Mg_37", "data": 0.0},
    {"isotope": "Mg_38", "data": 0.0},
    {"isotope": "Mg_40", "data": 0.0}]

# dictionary of dictionary
beam_info = {
    "O_16": {
        "Energy": 150, "Intensity": 175}, "O_18": {
            "Energy": 120, "Intensity": 150}, "Ne_20": {
                "Energy": 170, "Intensity": 80}, "Ne_22": {
                    "Energy": 150, "Intensity": 100}, "Mg_24": {
                        "Energy": 170, "Intensity": 60}, "Si_28": {
                            "Energy": 160, "Intensity": 10}, "S_32": {
                                "Energy": 150, "Intensity": 60}, "Ar_36": {
                                    "Energy": 150, "Intensity": 75}, "Ca_40": {
                                        "Energy": 140, "Intensity": 50}, "Ca_48": {
                                            "Energy": 90, "Intensity": 15}, "Ca_48": {
                                                "Energy": 140, "Intensity": 80}, "Ni_58": {
                                                    "Energy": 160, "Intensity": 20}, "Ni_64": {
                                                        "Energy": 140, "Intensity": 7}, "Ge_76": {
                                                            "Energy": 130, "Intensity": 25}}


# Didn't include the rest of the beam list, intensity was too low to be
# significant.
"""
,   \
"Se_82":{"Energy":140,"Intensity":45}, "Kr_78":{"Energy":150,"Intensity":25},  \
"Kr_86":{"Energy":100,"Intensity":15},"Zr_96":{"Energy":120,"Intensity":3},    \
"Mo_92":{"Energy":140,"Intensity":10}, "Sn_112":{"Energy":120,"Intensity":4},  \
"Sn_124":{"Energy":120,"Intensity":1.5} #incomplete but enough for our purposes
 }
"""

def notes():
    """General Notes.

    If program is not open, look for the program image on deskotp, and click on it.

    Note: Could improve by having it go directly to the LISE++.exe file and executing it.
    Could do this with a shell script or here (in the python script).

    """


def set_projectile(projectile_name, energy, intensity, A):
    """Summary.

    Set the incoming projectile in LISE++ based on the projectiles name, energy,
    intensity, and atomic number (mass) A.
    Passed in to the arguments in the following order: projectile_name, energy,
    intensity, A.

    Current list of isotopes that can be used for target can be found at:
    https://nscl.msu.edu/users/beams.html

    """
    print("Setting projectile...")
    pag.moveTo(16, 124)  # projectile button
    pag.click(interval=.5)
    pag.moveTo(262, 213)  # element text box
    pag.doubleClick()
    pag.write(projectile_name)
    pag.moveTo(231, 211)  # The mass number box
    pag.doubleClick()
    pag.write(str(A))
    pag.moveTo(519, 213)  # energy
    pag.doubleClick()
    pag.write(str(energy))
    pag.moveTo(523, 421)  # beam intensity
    pag.doubleClick()
    pag.write(str(intensity))
    pag.moveTo(269, 445)
    pag.click(interval=.5)
    time.sleep(1)

# to set the Focal Plane (FP) slits


def set_FP_slits(slit_width):
    """Summary.

    Sets the the distance of the focal plane slits. The slit_width is passed in as the argument.
    Important to set the appropriate Focal Plane (FP) slits to be able to achieve a compromise
    between the purity of the beam and yield.

    """
    print("Setting FP_Slits...")
    pag.moveTo(65, 684)  # move to slit button
    pag.click()
    pag.moveTo(764, 231)
    pag.click()
    pag.write(str(slit_width))
    pag.moveTo(238, 447)
    pag.click()
    pag.moveTo(71, 744)
    pag.click()

# to set the wedge thickness


def set_I2_wedge(wedge_thickness):
    """Summary.

    Use to set the thickness of the wedge at the second image plane 'I2'.
    Important due to the magnets adjusting to the wedge with the appropriate
    Brho value to maximize the transmission of the fragment
    you are interested and reduce the amount of contaminants.

    """
    print("Setting I2_wedge...")
    pag.moveTo(60, 461)  # move to wedge button
    pag.click(interval=1)
    pag.write(str(wedge_thickness))
    pag.moveTo(926, 223)  # set spectrometer after block
    pag.click(interval=1)
    time.sleep(2)
    pag.moveTo(397, 398)  # select wedge profile
    pag.click(interval=1)
    pag.moveTo(881, 394)  # move to calculate angle
    pag.click()
    time.sleep(10)  # wait
    pag.moveTo(371, 479)  # fit achromatic angle from LISE calc.
    pag.click()
    pag.moveTo(308, 530)  # select the angle and copy
    pag.doubleClick()
    pc.copy("")
    time.sleep(2)
    # done twice due to bug in not properly copying. This fixes that bug.
    pag.hotkey('ctrl', 'c')
    time.sleep(1)
    pag.hotkey('ctrl', 'c')
    angle = pc.paste()
    pag.moveTo(168, 622)  # ok button
    pag.click()
    pag.moveTo(152, 535)
    pag.click()
    print(f"The angle for the wedge is -{angle}.")
    return str(angle)


def tune_spectrometer():
    """Tune the overall spectrometer to optimize transmission. Done by LISE++."""
    print("Tuning spectrometer...")
    pag.moveTo(335, 78)
    pag.click()
    time.sleep(1)


def set_fragment(fragment, A):
    """Summary.

    Set the fragment you are interested in studying. Pass in the name of the
    fragment and mass number A.
    This is handled automatically in the loop, no need to set it
    yourself (besided debugging/upgrading reasons).

    """
    print("Setting fragment...")
    pag.moveTo(20, 170)  # projectile button
    pag.click()
    pag.moveTo(250, 463)  # element text box
    pag.doubleClick()
    # pag.press("delete")
    pag.write(str(A))
    pag.moveTo(309, 470)  # element text box
    pag.doubleClick()
    # pag.press("delete")
    pag.write(fragment)
    pag.moveTo(624, 521)  # energy
    pag.click()
    time.sleep(1)

# to retrive the thickness


def get_thickness():
    """To retrive the thickness of the target after optmizing. Optimizing is done by LISE++."""
    target_thickness = 0
    pc.copy("")  # clear clipboard
    print("Retrieving thickness...")
    pag.moveTo(453, 38)  # calculations
    pag.click(interval=1)
    pag.dragTo(504, 151, .5)  # Optimum target
    time.sleep(1)
    pag.moveTo(381, 485)  # first ok
    pag.click(interval=1.5)
    pag.moveTo(326, 655)  # second ok
    pag.click(interval=1.5)
    time.sleep(20)
    pag.moveTo(260, 451)  # load thickness
    pag.click()
    pag.moveTo(1629, 160)  # exit first plot
    pag.click()
    pag.moveTo(1600, 93)  # exit second plot
    pag.click()
    pag.moveTo(24, 196)  # target button
    pag.click()
    pag.moveTo(477, 286)  # box containing info
    time.sleep(1)
    pag.doubleClick()
    time.sleep(1)
    pag.hotkey('ctrl', 'c')  # copy
    time.sleep(1)
    target_thickness = pc.paste()  # paste it to a variable
    print(f"Thickness is {target_thickness} microns")
    pag.moveTo(456, 459)  # ok button to close
    pag.click()
    return target_thickness

# to retrive intensity
def get_intensity(isotope, beam_element, beam_mass):
    """Summary.

    Retrieve the intensity based on the isotope you are interested in,
    the beam isotope (element) you are using, and the mass number
    for the beam element.
    """
    flag = False
    print(isotope)
    # get pixel location of isotope on screen
    print("Retrieving intensity...")
    x = pixel_locations[isotope]["x"]
    y = pixel_locations[isotope]["y"]
    # print(x,y)
    pag.position()
    pag.moveTo(x, y)
    pag.click(button="right",interval=1)
    pag.moveTo(1483, 417)  # File save button
    pag.click()
    pag.moveTo(531, 339)  # file save text box
    pag.click(interval=1)
    # desktop comes from top of the sript.
    filename = str(desktop) + r"\data.txt"
    print(f"The file is being saved at the following location: {filename}")
    pag.write(filename)
    # pag.write("junk.txt")
    pag.press("enter")
    pag.press("left")
    pag.press("enter")  # this "enter" saves the file to desktop
    pag.moveTo(1563, 44)
    pag.click()
    df = pd.read_csv(filename)
    # df = pd.read_csv("C:\\Users\Owner\Desktop\junk.txt") #path to temporary file. NEED TO UPDATE
    # print(df)
    # location of the intensity in the data frame. Usually included an extra
    # line if it is zero
    intensity_check = df.iloc[0, 0]
    intensity_check = intensity_check.split()
    print(intensity_check)
    if len(intensity_check) == 6:
        if intensity_check[5] == "0!":
            print("TRANSMISSION IS 0.0% WITH THIS PROJECTILE ")
            flag = True
            return 0, flag
    else:
        # location of the intensity in the data frame
        _intensity = df.iloc[6, 0]
        _intensity = _intensity.split()
        # intensity value
        print(
            f"The intensity for {isotope} with {beam_element} {beam_mass} is {_intensity[4]} pps.")
        return _intensity[4], flag

# retrieve the transmission in X-space


def FP_slit_X_transmission_percent():
    """Summary.

    Retrieve the transmission percent in the x direction at the focal plane.
    Incoming beam looks 'Gaussian' but
    there is very litter dispersion in y direction.
    """
    # NEED TO WORK ON THIS
    print("Getting FP_Slits X space transmission...")
    # desktop comes from top of the sript.
    filename = str(desktop) + r"\data.txt"
    df = pd.read_csv(filename)
    FP_x_space_transmission = df.iloc[39, 0]  # location in the .csv file
    FP_x_space_transmission = FP_x_space_transmission.split()
    # print(FP_x_space_transmission[4])
    return FP_x_space_transmission[4]  # percent value


def purity_percent(fragment_isotope):
    """Summary.

    Retrieve the overall purity for the fragment you are studying after
     passinng through the FP_PIN (focal plane Particle in) detector.

    """
    print(f"Retrieving beam purity for {fragment_isotope}...")
    pag.moveTo(832, 83)  # run all nucleo buttom (red lightning bolt)
    pag.click()
    time.sleep(40)
    pag.moveTo(999, 77)  # x spatial distribution
    pag.click()
    pag.dragTo(1110, 629, .5)  # FP_PIN detector
    pag.click(interval=.5)
    time.sleep(4)
    pag.moveTo(14, 316)  # stats box
    pag.click()
    pag.press("enter")  # accept
    time.sleep(1)
    pag.moveTo(1609, 201)  # file save button
    pag.click()
    """
	pag.moveTo(365,195) #drop down
	pag.click()
	#pag.press("d",presses=2,interval=1) #to save in desktop
	pag.press("d",interval=1) #to save in desktop
	pag.press("enter")
	"""
    pag.moveTo(389, 413)  # file save text box
    pag.click()

    # desktop comes from top of the sript.
    filename = str(desktop) + r"\pps_data.txt"
    print(f"The file is being saved at the following location: {filename}")
    pag.write(filename)

    # pag.write("pps_junk.txt")
    pag.press("enter")  # save file
    pag.press("left")
    pag.press("enter")  # this "enter" saves the file to desktop
    pag.moveTo(1682, 122)
    pag.click()
    pag.moveTo(1877, 13)
    pag.click()
    df = pd.read_csv(filename, error_bad_lines=False)
    # df =
    # pd.read_csv("C:\\Users\Owner\Desktop\pps_junk.txt",error_bad_lines=False)
    # #path to temporary file. NEED TO UPDATE
    #print(f"Size of data frame is {df.size}.")
    _string = df.iloc[5, 0]  # get the pps for isotope in question
    _string = _string.split()
    isotope_fragment = _string[13]  # grab pps value
    total = 0.
    for i in range(5, df.size):
        string = df.iloc[i, 0]
        string = string.split()
        # to get it to correct scientific notation
        val = float(float(string[13]))
        total = total + val
    print(f"The total amount of pps is {total}.")
    frag_val = float(float(isotope_fragment))
    print(
        f"Percent of {fragment_isotope} in beam is {(float(float(frag_val))/total)*100.} %")
    percent = (float(float(frag_val)) / total) * 100.
    return percent


def isotope_loop():
    """Summary.

    Use to find the best beam for each isotope. However, it
    has already been determined that the best beam is Ca 48.
    """
    beam_data = []
    start = time.time()
    df = pd.DataFrame(None)  # create our data frame
    for i, dic in enumerate(isotope_info):  # loop for fragments
        df = df[0:0]
        df = pd.DataFrame(
            columns=[
                "Beam element",
                "A (u)",
                "Beam energy (MeV/u)",
                "Beam Intensity (pnA)",
                "Target thickness (microns)",
                "Fragment Intensity (pnA)"])
        data = []
        # get rid of the underscore in the isotope name
        iso = dic['isotope'].replace("_", " ")
        # returns the name of the isotope
        print(f"You are looking at the {iso} isotope.")
        iso = iso.split()
        set_fragment(iso[0], iso[1])  # fragment name, mass number
        # now loop for all the provided beams
        for i, beam_element in enumerate(
                beam_info):
            print(
                f"You are using {beam_element} as your primary beam at \
                {beam_info[beam_element]['Energy']} MeV/u with \
                {beam_info[beam_element]['Intensity']} pnA.")
            beam_energy = beam_info[beam_element]["Energy"]
            beam_intensity = beam_info[beam_element]["Intensity"]
            beam_element = beam_element.replace("_", " ")
            beam_element = beam_element.split()
            if beam_element[1] <= iso[1]:
                print(
                    f"Skipping {beam_element[0]} {beam_element[1]}. Not greater\
                     than {iso[1]} nucleons.")
                continue
            #				name, energy, intensity, mass number A
            set_projectile(
                beam_element[0],
                beam_energy,
                beam_intensity,
                beam_element[1])
            # thickness with that particular beam for a particular fragment
            thickness = get_thickness()
            tune_spectrometer()
            # pass the isotope name to get intensity and save it to the map
            # with the frag info
            frag_intensity, flag = get_intensity(
                dic['isotope'], beam_element[0], beam_element[1])
            if flag:
                continue
            print(
                f"Data being appended in the following format -> beam element, \
                A,beam energy, beam intensity, thickness, fragment intensity: \
                {beam_element[0]},{beam_element[1]} ,{beam_energy},{beam_intensity},\
                {thickness}, {frag_intensity}")
            df.loc[i] = [
                beam_element[0],
                beam_element[1],
                beam_energy,
                beam_intensity,
                thickness,
                frag_intensity]
            print(df)
        print(f"DATA FRAME FOR {iso[0]} {iso[1]} ISOTOPE.")
        print(df)
        df.to_csv(f"{iso[0]}_{iso[1]}_data_LISE++.csv")
        print(f"File saved as: {iso[0]}_{iso[1]}_data_LISE++.csv")
    end = time.time()
    print(f"It took {end-start} to run everything.")


def slice_array(arr, start):
    """Summary.

    To "slice" an array of dictionaries and return sliced array.

    Function to slice an array. Pass in the array and where you want to begin slicing from.
    """
    new_array = []
    index = 0
    for i, dic in enumerate(arr):
        # grab individual dictionary in that specific array index
        temp_dic = arr[i]
        if temp_dic["isotope"] == str(
                start):  # if starting isotope is found, save the index location
            index = i
            break
    for t in range(index, len(arr)):
        new_array.append(arr[t])
    return new_array  # return a sliced array containing dictionaries from starting isotope


def isotope_tuning_values(
        FP_slit_width,
        isotope_start,
        isotope_end,
        wedge_range):
    """To find the best configuration using a Ca 48 beam."""
    set_projectile("Ca",140,80,48)  # set the beam here with element name, energy, intensity, atomic number
    start = time.time()
    set_FP_slits(FP_slit_width)
    # if bool_value == True: #if you want to start from  a particular isotope
    new_isotope_dic = slice_array(isotope_info, isotope_start)
    for i, dic in enumerate(new_isotope_dic):  # loop for each fragment
        df = pd.DataFrame(None)  # create our data frame
        df = pd.DataFrame(
            columns=[
                "I_2 slit width (mm) ",
                "Intensity (pps) ",
                "Target thickness (microns) ",
                "Horizontal FP Slit width (mm)",
                "Purity transmission % ",
                "Mom. Accpetance % ",
                "Wedge thickness (microns) ",
                "wedge angle (mrad)"])
        # get rid of the underscore in the isotope name
        iso = dic['isotope'].replace("_", " ")
        # returns the name of the isotope
        print(f"You are looking at the {iso} isotope.")
        iso = iso.split()
        set_fragment(iso[0], iso[1])
        # wedge_thickness = 2300 #wedge thickness to start with
        for count, wedge_thickness in enumerate(
                wedge_range):  # loop over each wedge thickness
            print(
                f"Currently using {wedge_thickness} microns for {iso[0]} {iso[1]}")
            tune_spectrometer()
            # There is a dependence between target and wedge. Doing it twice
            # gives best results
            preliminary_wedge_angle = set_I2_wedge(str(wedge_thickness))
            tune_spectrometer()
            preliminary_target_thickness = get_thickness()
            tune_spectrometer()
            wedge_angle = set_I2_wedge(str(wedge_thickness))
            wedge_angle = "-" + wedge_angle
            tune_spectrometer()
            target_thickness = get_thickness()
            tune_spectrometer()
            # pass the isotope name to get intensity and save it to the map
            # with the frag info
            frag_intensity, flag = get_intensity(dic['isotope'], "Ca", 48)
            if flag:  # if we have zero transmission, skip that wedge thickness
                continue
            #FP_x_space_transmission = FP_slit_X_transmission_percent()
            # pass in the name of the fragment isotope
            _purity_percent = purity_percent(iso[0] + iso[1])
            print(f"Purity is {_purity_percent} %")
            df.loc[count] = [
                29.5,
                frag_intensity,
                target_thickness,
                FP_slit_width,
                _purity_percent,
                1,
                wedge_thickness,
                wedge_angle]  # harcode the 1% momentum acceptance
            wedge_thickness = wedge_thickness + 100
            print(f"Have gone through {count} iterations")
            print(df)

        path = os.path.join(".","data_files")
        directory_check = os.path.isdir(path)
        if directory_check == True:
            print("Hey")
            df.to_csv(f"./{path}/{iso[0]}_{iso[1]}_finetune_{FP_slit_width}_data_LISE++.csv")
            print(f"File saved in {path} as: {iso[0]}_{iso[1]}_finetune_{FP_slit_width}_data_LISE++.csv")
        if directory_check == False:
            print(f"Creating the following directory {path}")
            os.mkdir(path) 
            df.to_csv(f"./{path}/{iso[0]}_{iso[1]}_finetune_{FP_slit_width}_data_LISE++.csv")
            print(f"File saved in {path} as: {iso[0]}_{iso[1]}_finetune_{FP_slit_width}_data_LISE++.csv")

        #df.to_csv(
         #   f"./{path}/{iso[0]}_{iso[1]}_finetune_{FP_slit_width}_data_LISE++.csv")
        #print(
        #    f"File saved as: {iso[0]}_{iso[1]}_finetune_{FP_slit_width}_data_LISE++.csv")
        del df
        if dic['isotope'] == isotope_end:
            print(f"YOU HAVE REACHED {isotope_end}!")
            break
    end = time.time()
    print(f"It took {(end-start)/60.0} minutes to run everything.")


def save():
    """Save the thickness to a text file."""
    with open("thickness.txt", "w") as file:
        file.write(json.dumps(isotope_info))
    file.close()

# python 3 version


def show_pixels():
    """Show the pixel location on your screen as you move your cursor."""
    print('Press Ctrl-C to quit.')
    try:
        while True:
            x, y = pag.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        print('\n')

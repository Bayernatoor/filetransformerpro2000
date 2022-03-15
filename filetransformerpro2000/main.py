#!/usr/bin/env python

import os
import subprocess
import random
from tkinter import *
from tkinter import messagebox
from tkinter import font
from PIL import ImageTk, Image

# instantiate a Tk class object
root = Tk()
root.title("File Transformer Pro 2000")
root.geometry("600x1050")
root.config(bg="white")

# pull media from user's Downloads
download_folder = os.path.expanduser("~") + "/Downloads/"

# create the frame for my canvas
bottom_left = Frame(root, bg="white", width=150, height=553)
bottom_left.grid(row=9, column=0)

# create a canvas to place my image
canvas_for_image = Canvas(
    bottom_left, bg="white", height=553, width=150, borderwidth=0, highlightthickness=0
)
canvas_for_image.grid(row=9, column=0, sticky="nesw", padx=0, pady=0)

# create image from my image resize it to img size and place it on canvas
image = Image.open("img/img2.png")
canvas_for_image.image = ImageTk.PhotoImage(image.resize((150, 553), Image.ANTIALIAS))
canvas_for_image.create_image(0, 0, image=canvas_for_image.image, anchor="nw")

# fonts
first_font = font.Font(
    family="Helvetica", weight="bold", slant="italic", size=12, underline=True
)
second_font = font.Font(family="serif", weight="bold", size=10)
third_font = font.Font(family="monospace", weight="bold", size=10)

# Top Labels
file_label = Label(root, width=40, borderwidth=5, text="Select your file")
file_label.grid(row=0, column=3, padx=2, pady=2)
file_label.config(bg="white", fg="black")
file_label["font"] = first_font

tool_label = Label(root, width=0, borderwidth=5, text="Select your tool")
tool_label.grid(row=0, column=0, padx=15, pady=2)
tool_label.config(bg="white", fg="Black")
tool_label["font"] = first_font

parameter_label = Label(root, text="Optional Value:")
parameter_label.grid(row=5, column=3, padx=20, pady=5)
parameter_label.config(fg="#0A2239", bg="#FBFCFA")
parameter_label["font"] = second_font

entry_parameter = Entry(root, borderwidth=2)
entry_parameter.grid(row=6, column=3, padx=20, pady=0)


# Dropdown menu for ffmpeg tools
def show():
    dropdown = Label(root, text=())
    dropdown.grid(row=1, column=0, padx=10, pady=5)


# sets the dropdown title
clicked = StringVar()
clicked.set("Tool List")

# Dropdown tool list options
tool_drop = OptionMenu(
    root,
    clicked,
    "Adjust Volume",
    "Change Format",
    "Compress265",
    "Compress264",
    "Equalize Audio",
    "Reduce Noise",
    "Quick Sync",
    "Precise Sync",
    "Color Correct",
    "Flip Video",
    "Image to Video - JPG",
    "Image to Video - PNG",
)
tool_drop.grid(row=1, column=0, padx=10, pady=5)
tool_drop.config(bg="white")

# Listbox for download folder
file_list = Listbox(root, width=40, borderwidth=5)
file_list.grid(row=2, column=3, padx=2, pady=2)
file_list.config(fg="#0A2239", bg="#E6E8EB")
file_list["font"] = third_font

# variable for the file input field
v = StringVar()
entry = Entry(root, textvariable=v, borderwidth=2)
entry.grid(row=4, column=3)


# Sets the variable v to whichever item you clicked on in the list
def add_to_entry(event):
    listbox = event.widget
    index = listbox.curselection()
    if index:
        value = listbox.get(index[0])
        v.set(value)


# refresh the list with new files from the Downloads folder
def refresh_list():
    file_list.delete(0, END)
    for f in sorted(os.listdir(download_folder)):
        if (
            f.endswith(".mp4")
            or f.endswith(".mov")
            or f.endswith(".mkv")
            or f.endswith(".MOV")
            or f.endswith(".3gp")
            or f.endswith(".mpeg")
            or f.endswith(".HEVC")
            or f.endswith(".qt")
            or f.endswith(".QT")
            or f.endswith(".webm")
            or f.endswith(".3g2")
            or f.endswith(".MP4")
            or f.endswith(".3gpp")
            or f.endswith(".ts")
            or f.endswith(".jpg")
            or f.endswith(".png")
        ):
            file_list.insert(END, f)


# Populates the list with all files of x extension on first start
for f in sorted(os.listdir(download_folder)):
    if (
        f.endswith(".mp4")
        or f.endswith(".mov")
        or f.endswith(".mkv")
        or f.endswith(".MOV")
        or f.endswith(".3gp")
        or f.endswith(".mpeg")
        or f.endswith(".HEVC")
        or f.endswith(".qt")
        or f.endswith(".QT")
        or f.endswith(".webm")
        or f.endswith(".3g2")
        or f.endswith(".MP4")
        or f.endswith(".3gpp")
        or f.endswith(".ts")
        or f.endswith(".jpg")
        or f.endswith(".png")
    ):
        file_list.insert(END, f)
file_list.bind("<Double-Button>", add_to_entry)


def popup_one():
    messagebox.showwarning("Heads up!", "You must select\na tool and a file!")


def popup_two():
    messagebox.showinfo("Heads up!", "Not a valid selection!")


def popup_three():
    messagebox.showinfo("Heads up", "All done!")


# def popup_four():
#     messagebox.showinfo("Heads up", "No such file or directory!")


def ffmpeg_script():
    '''
    main function that handles the media and runs ffmpeg. Sets variables when clicked/used in the GUI.
    
    Function runs without posting to the terminal. All errors and stderror/stdout is 
    pipped to a text file which is added to the downloads folder. Some errors will appear as popups
    directly in the GUI for easy understanding of what went wrong. 
    '''  
    os.chdir(download_folder)
    errors = False
    selected = clicked.get()
    video_file = entry.get()
    volume = f"volume={entry_parameter.get()}"
    precise = entry_parameter.get()
    duration = entry_parameter.get()
    # rename filename add random string to avoid duplicate names
    filename = selected.lower() + str(random.randrange(10000)) + ".mp4"
    new_file = (
        selected.lower() + str(random.randrange(10000)) + f".{entry_parameter.get()}"
    )

    # available ffmpeg scripts
    scripts = {
        "Adjust Volume": [
            "ffmpeg",
            "-hide_banner",
            "-i",
            video_file,
            "-af",
            volume,
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-y",
            filename,
        ],
        "Change Format": [
            "ffmpeg",
            "-hide_banner",
            "-i",
            video_file,
            "-f",
            "mov",
            "-y",
            new_file,
        ],
        "Compress265": [
            "ffmpeg",
            "-hide_banner",
            "-i",
            video_file,
            "-c:v",
            "libx265",
            "-crf",
            "27",
            "-preset",
            "veryfast",
            "-c:a",
            "copy",
            "-y",
            filename,
        ],
        "Compress264": [
            "ffmpeg",
            "-hide_banner",
            "-i",
            video_file,
            "-c:v",
            "libx264",
            "-crf",
            "27",
            "-preset",
            "veryfast",
            "-c:a",
            "copy",
            "-y",
            filename,
        ],
        "Equalize Audio": [
            "ffmpeg",
            "-hide_banner",
            "-i",
            video_file,
            "-filter:a",
            "loudnorm",
            "-y",
            filename,
        ],
        "Reduce Noise": [
            "ffmpeg",
            "-hide_banner",
            "-i",
            video_file,
            "-af",
            "highpass=f=200",
            "-af",
            "lowpass=f=3000",
            "-y",
            filename,
        ],
        "Quick Sync": [
            "ffmpeg",
            "-hide_banner",
            "-i",
            video_file,
            "-c:v",
            "copy",
            "-af",
            "aresample=async=1:first_pts=0",
            "-y",
            filename,
        ],
        "Precise Sync": [
            "ffmpeg",
            "-hide_banner",
            "-i",
            video_file,
            "-itsoffset",
            precise,
            "-i",
            video_file,
            "-map",
            "0:0",
            "-map",
            "1:1?",
            "-acodec",
            "copy",
            "-vcodec",
            "copy",
            "-y",
            filename,
        ],
        "Color Correct": [
            "ffmpeg",
            "-hide_banner",
            "-i",
            video_file,
            "-vf",
            "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p",
            "-c:v",
            "libx265",
            "-crf",
            "22",
            "-preset",
            "medium",
            "-tune",
            "fastdecode",
            "-y",
            filename,
        ],
        "Flip Video": [
            "ffmpeg",
            "-hide_banner",
            "-i",
            video_file,
            "-vf",
            "hflip",
            "-c:a",
            "copy",
            "-y",
            filename,
        ],
        "Image to Video - JPG": [
            "ffmpeg",
            "-hide_banner",
            "-framerate",
            duration,
            "-pattern_type",
            "glob",
            "-i",
            "image*.jpg",
            "-c:v",
            "libx264",
            "-r",
            "30",
            "-pix_fmt",
            "yuv420p",
            "-s",
            "1920*1080",
            "-y",
            filename,
        ],
        "Image to Video - PNG": [
            "ffmpeg",
            "-hide_banner",
            "-framerate",
            duration,
            "-pattern_type",
            "glob",
            "-i",
            "image*.png",
            "-c:v",
            "libx264",
            "-crf",
            "25",
            "-r",
            "30",
            "-pix_fmt",
            "yuv420p",
            "-s",
            "1920*1080",
            "-y",
            filename,
        ],
    }

    if selected == "Tool List":
        popup_one()
    elif (
        selected == "Adjust Volume"
        or "Change Format"
        or "Compress265"
        or "Compress265"
        or "Equalize Audio"
        or "Reduce Noise"
        or "Quick" "Sync"
        or "Precise Sync"
        or "Color Correct"
        or "Flip Video"
        or "Image to Video - JPG"
        or "Image to Video - PNG"
    ):
        try:
            process = subprocess.Popen(
                scripts[selected],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            # write everything to a text file which is then added to downloads folder for debugging (process needs improvement)
            stdoutdata, stderrdata = process.communicate()
            with open("ignorethislog.txt", "w") as log:
                log.write(stderrdata)
            with open("ignorethislog.txt") as logged:
                for line in logged:
                    pass
                last_line = line
                result = last_line.rstrip()
                stripped_result = len(result)
                if (
                    process.wait() != 0
                    and selected == "Precise Sync"
                    and stripped_result == 45
                ):
                    return messagebox.showinfo(
                        "Heads up", "Please enter a valid number"
                    )
                # check if video has an audio stream
                elif process.wait() != 0 and selected == "Precise Sync":
                    return messagebox.showinfo(
                        "Heads up", "File has no audio stream.\nPrecise Sync won't work"
                    )
                # other unhandled error will display error in the GUI
                elif process.wait() != 0:
                    return messagebox.showinfo("Heads up\n", stderrdata)
                elif selected == "Change Format":
                    refresh_list()
                    return messagebox.showinfo(
                        "Success", f"Conversion Success\nNew Filename: {new_file}"
                    )
                elif (
                    selected == "Adjust Volume"
                    or "Compress265"
                    or "Compress265"
                    or "Equalize Audio"
                    or "Reduce Noise"
                    or "Quick Sync"
                    or "Precise Sync"
                    or "Color Correct"
                    or "Flip Video"
                    or "Image to Video - JPG"
                    or "Image to Video - PNG"
                ):
                    refresh_list()
                    return messagebox.showinfo(
                        "Success", f"Conversion Success\nNew Filename: {filename}"
                    )
        except OSError as e:
            errors = True
            return e.strerror, errors
    # if hit then the selection was not valid. Popup is called to alert user
    else:
        popup_two()


# buttons
start = Button(root, text="Start", borderwidth=2, command=ffmpeg_script)
start.grid(row=7, column=3, padx=15, pady=15)
start.config(bg="white")

refresh = Button(root, text="Refresh List", borderwidth=2, command=refresh_list)
refresh.grid(row=1, column=3, padx=20, pady=20)
refresh.config(bg="white")

explainer_text = """TLDR:

1. Select tool on the left.
2. Select a file from list
3. Optional: add a value (Volume/precise sync, image)
4. Press Start and wait for completion
5. New file will appear in downloads folder

Detailed explanation:

List above selects video files from
your downloads folder. Press refresh
to update the list.
Double click to add a file to the first
input box below, add value to second
box if necessary.

Select tool on the left.

Press start. Wait for process to finish
New file will appear in your downloads
folder.

      TOOLS

Adjust Volume:

Raise or lower the volume of the video.
Neutral volume is 1, anything above will raise:
Anything below will lower the volume.

2-10 is recommended but can go higher if
necessary.

Change Format:

Change from any file extension
to any other file extension.
Enter the new one in the field above
no period (e.g. mp4, mov)

Compress264 or Compress265:

In most cases 264 is recommended.

265 may be used if the file is
high quality and needs further
compressing, may fail, if it does,
change the format to mp4
Warning, heavy CPU usage.

Equalize Audio:

Used if certain parts of audio
are lower then the others.
May want to follow up with
Volume tool.


Reduce Noise:

Attempts to remove background noise.
May not work in all circumstances.
May need to raise volume as well.

Quick Sync:

Will sync the audio of most videos.

Precise Sync:

Use if Easy Sync does not work.
This one requires an input value.
Number represents the delay or offset
Recommend to start with 0.2.
Determine whether audio is too
quick or too slow then adjust.
(Can go negative, e.g. -0.1, -0.025
or 0.25 etc.)

Color Correct:

Will convert HDR videos to SDR
and therefore, correct the video's
colorspace, restoring proper colours.
(only works on HDR vids, will get an
unhandled error if used on anything
else).

Flip video:

Will flip the video horizontally.
To be used if text is mirrored.

Image to video (jpg/png):

Will take images from your
downloads folder and combine them
into a video.

To note - You must rename all the
images you wish to use to
image*.jpg, ex: image1.jpg, image2.jpg,
image3.jpg etc.

If image is PNG, make sure to use PNG
version.

It'll take any JPG file name that starts
with "image" and add it to the video but
numbering them like above will
set the order.

In Optional Value you'll set the frame length
1 = 1 second per frame (photo)
0.5 = 2 seconds per frame
0.3 = ~ 3 seconds
0.05 = 20 seconds per frame

Play with the value to get the proper length.

Tips:

1. Can only do 1 action at a time.

2. Can open multiple copies of the app
   if you want to run multiple scripts

3. Window will be unresponsive until complete

4. Need to stop the job? press CTRL + C in
   terminal

5. Bad audio? Try a combo! Equalize, Reduce,
   raise Volume or any variation.

There might be bugs, please report them
if you can :)
"""

# create helper text box at the bottom of the app.
help_text = Text(root, width=40, borderwidth=5)
help_text.grid(row=9, column=3)
help_text.insert(END, explainer_text)
help_text.config(fg="#0A2239", bg="#E6E8EB")
help_text["font"] = second_font


# keeps the app running.
root.mainloop()

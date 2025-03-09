from yt_dlp import YoutubeDL
from PIL import Image #img modeule from p img lib for img manip
from io import BytesIO #io mod treats bytes as file like obj
import requests #module HTTP requests to web servers
#creates in-memory for img before passing to .show func
import os
import getpass
import time
from tqdm import tqdm #taqadum, library for makign progress bars

def initial():
    # asking, creating obj and printing vid title
    print("Provide YouTube link: ")
    link = input()
    
    with YoutubeDL() as ydl:
        info = ydl.extract_info(link, download=False)
    
    print("Title:", info['title'])
    
    # Converting duration to hours, minutes, and seconds and displaying it
    duration_sec = info.get('duration', 0)
    h = duration_sec // 3600
    mi = (duration_sec % 3600) // 60
    sec = duration_sec % 60
    if h == 0 and mi != 0:
        print(f"Duration: {mi} minutes, {sec} seconds")
    elif mi == 0:
        print(f"Duration: {sec} seconds")
    else:
        print(f"Duration: {h} hours, {mi} minutes, {sec} seconds")
    
    img_url = info.get('thumbnail', '')  # url fetch; specifies location of img
    rp = requests.get(img_url)  # request uses HTTP GET and stores response in rp
    thumb_img = Image.open(BytesIO(rp.content))  # reading binary from rp, converting to obj then opening
    
    # Thumbnail disp for 4 sec
    print("Showing Thumbnail...")
    thumb_img.show()
    time.sleep(2)
    os.system("killall Preview")  # Closes macOS Preview app
    return info

def res(formats):
    print("Resolutions Available:")
    for i, fmt in enumerate(formats):
        print(f"{i+1}. Res: {fmt.get('resolution', 'Unknown')}")

def bitrate(formats):
    print("Bitrates Available")
    for i, fmt in enumerate(formats):
        print(f"{i+1}. Bit Rate: {fmt.get('abr', 'Unknown')}")

def download_with_progress(output_path, res_index, formats):
    res_index = int(res_index)
    
    if res_index < 1 or res_index > len(formats):
        print("Invalid res")
        return
    else:
        selected_format = formats[res_index - 1]  # compensation for starting from 1
    
    total_size = selected_format.get('filesize', 0)  # gets total filesize
    url = selected_format['url']  # get direct URL for download
    
    response = requests.get(url, stream=True)  # request for URL, stream=True streams content
    output_file = os.path.join(output_path, selected_format['format_id'] + ".mp4")
    
    with open(output_file, 'wb') as file:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading") as progress_bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))
    
    print(f"Download complete! saved in {output_path}")
    time.sleep(2)
    os.system('cls')

def confirmation(info):
    print("confirm download?\n y/n")
    opt = input()
    
    if opt.lower() == 'n':
        y = initial()
        confirmation(y)
    elif opt.lower() == 'y':
        print("Enter the desired download directory: \n1) Custom path \n2) Downloads")
        option = int(input())
        
        if option == 1:
            print("Enter path: ")
            custom_path = input()
            output_path = custom_path
        elif option == 2:
            output_path = os.path.expanduser("~/Downloads")  # Mac's default Downloads folder
        else:
            print("error")
            exit()
        
        print("Which Type do you want to download \n1) video \n2) Audio")
        option = int(input())
        formats = info.get('formats', [])
        
        if option == 1:
            filtered_formats = [fmt for fmt in formats if fmt.get('vcodec', 'none') != 'none']  # video check
            res(filtered_formats)
        elif option == 2:
            filtered_formats = [fmt for fmt in formats if fmt.get('acodec', 'none') != 'none']  # audio check
            bitrate(filtered_formats)
        else:
            print("error")
        
        print("Enter Resolution Index/Bit rate")
        res_index = input()
        download_with_progress(output_path, res_index, filtered_formats)
    else:
        print("wrong option chosen try again")

while True:
    ret = initial()
    confirmation(ret)
    exit = input(" ")


# https://www.youtube.com/watch?v=gs-MtItyOFc&ab_channel=tameimpalaVEVO
# https://www.youtube.com/shorts/bAyQCyTyTfY  

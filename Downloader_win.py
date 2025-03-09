from pytube import YouTube
from PIL import Image #img modeule from p img lib for img manip
from io import BytesIO #io mod treats bytes as file like obj
import requests #module HTTP requests to web servers
#creates in-memory for img before passing to .show func
import os
import getpass
import time
from tqdm import tqdm #taqadum, library for makign progress bars

def initial():
        
    #asking,craeting obj and printing vid title
    print("Provide YouTube link: ")
    link=input()
    find_in_link=link.find("www.youtube.com")
    if not find_in_link:
        print("yt link not entered")
        exit()
    yt=YouTube(link)
    print("Title: ",yt.title)
    
    # Converting duration to hours, minutes, and seconds and displaying it
    duration_sec=yt.length
    h = duration_sec // 3600
    mi = (duration_sec % 3600) // 60
    sec = duration_sec % 60
    if h==0 and mi!=0:
        print(f"Duration: {mi} minutes, {sec} seconds")
    elif mi==0:
        print(f"Duration: {sec} seconds")
    else:
        print(f"Duration: {h} hours, {mi} minutes, {sec} seconds")   #fstring allows combining txt and variables
        

    img_url=yt.thumbnail_url #url fetch;specifies location of img
    rp=requests.get(img_url) #request uses HTTP GET and stores response in rp  
    thumb_img=Image.open(BytesIO(rp.content)) #reading binary from rp,converting to obj then opening

    # Thumbnail disp for 4 sec
    print("Showing Thumbnail...")
    thumb_img.show()
    time.sleep(2)
    os.system(f"taskkill /f /im Microsoft.Photos.exe")
    return yt

#streams is an attribute of YouTube
def res(streams):
    print("Resolutions Available:")
    for i, stream in enumerate(streams): #i index and stream var stores the resolutions
        print(f"{i+1}.Res: {stream.resolution}")
        
def bitrate(streams):
    print("Bitrates Available")
    for i, stream in enumerate(streams): # i index and stream var stores the bit rates
        print(f"{i+1}. Bit Rate: {stream.abr}")   
    
def download_with_progress(output_path,res_index,streams):
    res_index=int(res_index)
    
    #for wrong index or if opt exceed indexes available
    if int(res_index) < 1 or res_index > len(streams):
        print("Invalid res")
        return                                                     
    else:
        stream = streams[res_index - 1] #compensation for starting from 1
        
    total_size = stream.filesize #gets total filesize
    response = requests.get(stream.url, stream=True) #requests for url stream=True streams content instead of downloading it all at once.
    
    is_audio= stream.includes_audio_track #checking if the downloaded file is in audio
    if is_audio:
        op_filename = stream.default_filename[:-4] + 'mp3' #removing webm and replacing with mp3
    else:
        op_filename=stream.default_filename
    
    output_file = os.path.join(output_path, op_filename) #concatenates path and filename (dest)
    ### with statment ensures closing resources right after processing them
    
    with open(output_file, 'wb') as file:  #opens file in binary write mode
        #b means progress will be displayed in bytes
        #unit scale checks scaling kb, mb, gb if value exceeds 1024 and desc is displayed besides the bar
        
        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading") as progress_bar: #with ensures cleanup of bar after it completes
            for chunk in response.iter_content(chunk_size=1024): #iterates and receives content from response in chunks of 1024 bytes
                if chunk: #for processing non empty chunks
                    file.write(chunk) #since the output file is opened as file, the chunk is being "downloaded"
                    progress_bar.update(len(chunk)) # updates the chunks being downloaded 

    print(f"Download complete! saved in {output_path}")
    time.sleep(2)
    os.system('cls')
    
def confirmation(yt):
    print("confirm download?\n y/n")
    opt=input()
    #input converted to lowercase so that capitals dont cause errors
    if opt.lower()=='n':
        #if no , start from the beginning 
        y = initial()
        confirmation(y)
    elif opt.lower()=='y':
        print("Enter the desired download directory: \n1) Custom path \n2) Downloads")
        option=int(input())
        if option==1:
            print ("Enter path: ")
            custom_path = input()
            output_path = custom_path
            print(f"saving to {output_path}")
        elif option==2:
            user_name=getpass.getuser()
            output_path = fr"C:\Users\{user_name}\Downloads"
            print(f"saving to {output_path}")
            
        else:
            print ("error")
            exit()
            
        print("Which Type do you want to downlaod \n1) video \n2) Audio")
        option=int(input())
        if option==1:
            stream = yt.streams.filter(file_extension='mp4').order_by('resolution').desc() #filtering mp4 qualities in dec order
            res(stream)
        elif option==2:
            stream = yt.streams.filter(only_audio=True).order_by('abr').desc() # filtering audio streams by bitrate in dec order
            #YouTube uses .webm ext for audio-only streams even for MP3.
            bitrate(stream)
        else:
            print ("error")
            
        print("Enter Resolution Index/Bit rate")
        res_index=input()
        download_with_progress(output_path,res_index,stream) #function call
    else:
        print("wrong option chosen try again")
            
while True:
    ret=initial()
    confirmation(ret)
    exit = input(" ")

# https://www.youtube.com/watch?v=gs-MtItyOFc&ab_channel=tameimpalaVEVO
# https://www.youtube.com/shorts/bAyQCyTyTfY

# RegEx
import re

# Third-Party Libraries
from pytube import YouTube as YT
from pytube import Playlist as PL
from youtube_transcript_api import YouTubeTranscriptApi as YTTS
from datetime import datetime

# Project Class Libraries
from Block_Parse import Block_Parse

""" 

Documentation 
Python Libraries employed: PyTube, YouTube_Transcript_API 
https://pypi.org/project/pytube/
https://www.programcreek.com/python/example/92182/pytube.YouTube
https://pypi.org/project/youtube-transcript-api/

Backlog
* [+] Add # Pending / # Processed Tags to Input file
* [+] obsidianfilename function to clean video titles and remove tags for Obsidian

Outline
* This program requires a YouTube Playlist to be specified using the PlayList_ID. 
* The program uses PyTube to generate a list of VideoIDs for the Play List, stored as myPList
* For the videoIDs in myPList, generate a list VideoData[] containing meta-data for each VideoID
* VideoData[] is written to a filename based on variable videoIDListName.

"""

# Parsing parameters
headerLines = 7 # number of header lines in the 'P_' + filename created for each transcript

# BlockSize is the no. of words in each block to sumbit to the LLM for summarizing. eg 3K words for 4K LLM context size
blockSize = 3000 # no. of words per block in th 'B_' + filename block delimited output

now = datetime.now()
dateString = now.strftime("%y%m%d_%H%M")

# Video title clean-up
def obsidian_filename(text):
    not_permitted_chars = r'[\/\\#?%*:|"<>\']'
    return re.sub(not_permitted_chars, '-', text)

# My Playlists
playlist_id = 'PLXRB0iupmiy5iFggXztTU86he4OW5cKrC' # Log
# playlist_id = 'PLXRB0iupmiy4xSgkED508DZDM6ErJ-tgf' # Test

# 3rd Party PlayLists
# playlist_id = 'PLZhDuTZwzpWdioVVMnJL6an8x3gqa-pAS' # NodusLabs Personal Knowledge Managment
# playlist_id = 'PLLN9Pm8MWdPsO3u8F43czOxrkCwVYBmtH' # Solo Gamers Club/Eldritch Horror
# playlist_id = 'PLm87h0-It8LwPc2N1jppdShUWHKo-78E2' # Stable Diffusion Guide

playlist_id_long = 'https://www.youtube.com/playlist?list=' + playlist_id 

# create a list video_IDs of videos in a Playlist with specified playlist_id (public or unlisted)
myPList = PL(playlist_id_long)

# Create VideoID list for further processing
videoIDListName = './FileOut/YL_' + 'VideoIDList_' + dateString + '.txt'    

# create new VideoIDList file
with open(videoIDListName, "w", encoding="utf-8", errors="replace") as f_out:
    f_out.write('# Processed\n\n# Pending\n')

# process urls in myPList
for url in myPList.video_urls:
    # retrieve video date for each URL
    video = YT(url)
    videoData = []
    videoData.append(['VideoID',url.split("=")[1]])
    videoData.append(['URL',url]) 
    videoData.append(['Author',video.author])
    videoData.append(['Publish Date',video.publish_date.strftime("%y%m%d")])
    videoData.append(['Title', obsidian_filename(video.title)])
    videoData.append(['Length',video.length])

    # create filename: Author, Date, VideoID
    author = str(videoData[2][1])
    author = author.replace(" ", "")
    author = author.replace(",", "")
    pubdate = str(videoData[3][1]) 
    video_id =  str(videoData[0][1])
    fileRef = author + '_' + pubdate + '_' +  video_id
    fileName = './FileIn/YP_' + fileRef + '.txt'
     # print each fileRef as it's generated
    print(fileRef)   
    
    # Process each video_id in Playlist
    try:
        transcriptList = YTTS.list_transcripts(video_id)
        transcriptEN = False
        transcriptExist = bool(transcriptList) # test if transcriptExist is non-empty


    except Exception as e:
        transcriptList = False
        print(f">>> Transcripts Disabled")
        #raise  # re-raise the exception

    if transcriptList:
        for transcript in transcriptList:
            # test if there's an English transcript
            if transcript.language_code == 'en':
                transcriptEN = True

        if transcriptExist and transcriptEN:
            transcript = YTTS.get_transcript(video_id, languages=['en'])
            print('*** English Transcript available')

            # Add file name to VideoIDList
            delimiter = '#^#'
            with open(videoIDListName, "a", encoding="utf-8", errors="replace") as f_out:
                f_out.write(video_id + delimiter + url + delimiter + author + delimiter + str(video.title) + delimiter + pubdate + delimiter + str(video.length) + delimiter + '\n')

            transcript_text = ''
            for line in  transcript:
                transcript_text += line['text']
            videoData.append(['Word Count',len(transcript_text.split())])
            videoData.append(['Transcript',transcript])

            # Write transcript header to file
            with open(fileName, "w", encoding="utf-8", errors="replace") as f_out:
                f_out.write(str(videoData[0])+'\n')
                f_out.write(str(videoData[1])+'\n')
                f_out.write(str(videoData[2])+'\n')
                f_out.write(str(videoData[3])+'\n')
                f_out.write(str(videoData[4])+'\n')
                f_out.write(str(videoData[5])+'\n')
                f_out.write(str(videoData[6])+'\n')
                for line in videoData[7][1]:
                    f_out.write(line['text']+'\n')

            # for each filename parse and save the parsed text to 'P_' file
            myBlockParse = Block_Parse(fileRef, headerLines, blockSize)
            myBlockParse.load_text()
            myBlockParse.wordBlock_write()
            headerText = myBlockParse.headerText

        else:
            print('>>> No English transcript available')



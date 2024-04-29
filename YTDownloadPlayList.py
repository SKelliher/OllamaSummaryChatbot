from pytube import YouTube as YT
from pytube import Playlist as PL
from youtube_transcript_api import YouTubeTranscriptApi as YTTS
from Block_Parse import Block_Parse
from datetime import datetime

# documentation 
# https://pypi.org/project/pytube/
# https://www.programcreek.com/python/example/92182/pytube.YouTube
# https://pypi.org/project/youtube-transcript-api/

# Parsing parameters
headerLines = 7 # number of header lines in the 'P_' + filename created for each transcript
blockSize = 1000 # no. of words per block in th 'B_' + filename block delimited output

# Summary Parameters
summaryCount = 10
model = 'wizardlm2'
systemPrompt = 'You are reading a YouTube transcript and will provide a summary'
queryPrompt = 'Summarize just the text sequentially in ' + str(summaryCount) + ' detailed and numbered points. Include a short caption to begin each point '
headerText = ''

now = datetime.now()
dateString = now.strftime("%y%m%d_%H%M")

# Playlist = 'Log'
playlist_id = 'PLXRB0iupmiy5iFggXztTU86he4OW5cKrC' 
playlist_id_long = 'https://www.youtube.com/playlist?list=' + playlist_id 

# create a list video_IDs of videos in a Playlist with specified playlist_id (public or unlisted)
myPList = PL(playlist_id_long)

# Create VideoID list for further processing
videoIDListName = './Summary/L_' + 'VideoIDList_' + dateString + '.txt'    
with open(videoIDListName, "w", encoding="utf-8", errors="replace") as f_out:
    pass

# process urls in myPList
for url in myPList.video_urls:
    # retrieve video date for each URL
    video = YT(url)
    videoData = []
    videoData.append(['VideoID',url.split("=")[1]])
    videoData.append(['URL',url]) 
    videoData.append(['Author',video.author])
    videoData.append(['Publish Date',video.publish_date.strftime("%y%m%d")])
    videoData.append(['Title',video.title])
    videoData.append(['Length',video.length])

    # create filename: Author, Date, VideoID
    author = str(videoData[2][1])
    author = author.replace(" ", "")
    author = author.replace(",", "")
    pubdate = str(videoData[3][1]) 
    video_id =  str(videoData[0][1])
    fileRef = author + '_' + pubdate + '_' +  video_id
    fileName = './Output/P_' + fileRef + '.txt'
     # print each fileRef as it's generated
    print(fileRef)   
    
    delimiter = '#^#'
    with open(videoIDListName, "a", encoding="utf-8", errors="replace") as f_out:
        f_out.write(video_id + delimiter + url + delimiter + author + delimiter + str(video.title) + delimiter + pubdate + delimiter + str(video.length) + delimiter + '\n')

    # retrieve transcript for video_id 

    transcriptList = YTTS.list_transcripts(video_id)
    transcriptEN = False
    transcriptExist = bool(transcriptList) # test if transcriptExist is non-empty

    for transcript in transcriptList:
        # test if there's an English transcript
        if transcript.language_code == 'en':
            transcriptEN = True

    if transcriptExist and transcriptEN:
        transcript = YTTS.get_transcript(video_id, languages=['en'])
        print('*** English Transcript available')

        transcript_text = ''
        for line in  transcript:
            transcript_text += line['text']
        videoData.append(['Word Count',len(transcript_text.split())])
        videoData.append(['Transcript',transcript])

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

        # for each filename parse and save the parsed text as 'P_' + 
        myBlockParse = Block_Parse(fileRef, headerLines, blockSize)
        myBlockParse.load_text()
        myBlockParse.wordBlock_write()
        headerText = myBlockParse.headerText

    else:
        print('*** No English transcript available')





import io
import pdb
def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    # Print the first alternative of all the consecutive results.
    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))

# [START def_transcribe_file]
def transcribe_file(speech_file):
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    #print("starting")
    client = speech.SpeechClient()

    # [START migration_async_request]
    if speech_file[:5] == "gs://":
        audio = types.RecognitionAudio(uri=speech_file)
    else:
        with io.open(speech_file, 'rb') as audio_file:
            content = audio_file.read()
        audio = types.RecognitionAudio(content=content)
    
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='en-US',
        max_alternatives=16,
        enable_word_time_offsets=1)

    # [START migration_async_response]
    operation = client.long_running_recognize(config, audio)
    # [END migration_async_request]

    #print('Waiting for operation to complete...')
    response = operation.result(timeout=90)
    #print(operation.metadata())
    
    #i = 0;
    transcriptMap = []
    for result in response.results:
        words = result.alternatives[0].words
        
        tempList = [(float(str(words[0].start_time.seconds)+"."+str(words[0].start_time.nanos))),(result.alternatives[0].transcript),speech_file]
        transcriptMap.append(tempList)
    return (transcriptMap)

    transcript_file.close()
    # [END migration_async_response]
# [END def_transcribe_file]

def transcriptMerge2(transcriptMap):
    retList = []
    indices = []
    tempLowValue = []
    lowValue = 0 
    lowIndex = 0
    chunkLen = 0
    for list in transcriptMap:
        chunkLen = chunkLen + len(list)
        indices.append(0)
        tempLowValue.append(float('inf'))
    for i in range(0,chunkLen):
        for j in range(0,len(transcriptMap)):
            
            tempLowValue[j] = list[indices[j]][j]
        print(tempLowValue)            
        minValue = min(tempLowValue)
        minIndex = tempLowValue.index(minValue)
        print(minIndex)
        indices[j] = indices[j] + 1
        retList.append(list[minIndex])
    return retList


def transcriptMerge(transcriptMap):
    return sorted(transcriptMap, key = lambda transcriptmap: transcriptmap[0])

def printToTranscript(mergedTranscriptMap, fileName, pathName):
    transcript_file = open(str(pathName+fileName),"w")    
    for chunk in mergedTranscriptMap:
        transcript_file.write(str(chunk[2]+": "+chunk[1]+"\n"))

def main():
    from googleapiclient.discovery import build
    from oauth2client.client import GoogleCredentials
    credentials = GoogleCredentials.get_application_default()
    service = build('compute', 'v1', credentials=credentials)

    files = {"../test_audio_files/conversation_1.flac" , "gs://quillio_audio_files/Job_Interview.flac" , "../test_audio_files/conversation_2.flac"}
    transcriptMap = []
    
    for file in files:
        transcriptMap = transcriptMap + transcribe_file(file)

    file_name = "transcript.txt"
    path_name = "../transcripts/"
    printToTranscript(transcriptMerge(transcriptMap),file_name, path_name)
    

if __name__ == "__main__":
    main()
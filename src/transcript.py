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
    transcript_file = open("../transcripts/transcript.txt","a")       
    transcriptMap = []
    for result in response.results:
        words = result.alternatives[0].words
        #print(result.alternatives[0].transcript)
        #print(float(str(words[0].start_time.seconds)+"."+str(words[0].start_time.nanos)))
        # transcript_file.write(result.alternatives[0].transcript+"\n")
        # print(result.alternatives[0].confidence)
        #print(words[0].start_time)
        #for i in range(0,len(words)):
            #print(words[i].word)
        tempList = [(float(str(words[0].start_time.seconds)+"."+str(words[0].start_time.nanos))),(result.alternatives[0].transcript)]
        transcriptMap.append(tempList)
    return (transcriptMap)

    transcript_file.close()
    # [END migration_async_response]
# [END def_transcribe_file]

def transcriptMerge(transcriptMap):
    retList = []
    indices = []
    tempLowValue = []
    lowValue = 0 
    lowIndex = 0
    chunkLen = 0
    for list in transcriptMap:
        chunkLen = chunkLen + len(list)
        indices.append(0)
    for i in range(0,chunkLen):
        tempLowValue.append(float('inf'))
    for i in range(0,chunkLen):
        for j in range(0,len(transcriptMap)):
            print(len(indices))
            print(indices)
            print(j)
            tempLowValue[j] = list[indices[j]][0]
        minValue = min(tempLowValue)
        minIndex = tempLowValue.index(minValue)
        indices[j] = indices[j] + 1
        retList.append(list[minIndex])
    return retList

def main():
    from googleapiclient.discovery import build
    from oauth2client.client import GoogleCredentials
    credentials = GoogleCredentials.get_application_default()
    service = build('compute', 'v1', credentials=credentials)

    files = {"../test_audio_files/conversation_1.flac" , "../test_audio_files/conversation_2.flac"}
    #transcribe_file("../test_audio_files/conversation_1.flac");
    #transcribe_file("../test_audio_files/conversation_2.flac");
    transcriptMap = []
    #TMsize = 0
    for file in files:
        transcriptMap.append(transcribe_file(file))

        #TMsize = TMsize + 1
    #print(transcriptMap[0][0][0])
    mergedTranscriptMap = transcriptMerge(transcriptMap)
    print(mergedTranscriptMap)

if __name__ == "__main__":
    main()
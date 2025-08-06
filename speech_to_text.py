import torch
# from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq, pipeline
# import soundfile as sf



# processor = AutoProcessor.from_pretrained("whitemouse84/whisper-tiny-ru")
# model = AutoModelForSpeechSeq2Seq.from_pretrained("whitemouse84/whisper-tiny-ru")

# asr = pipeline(
#     "automatic-speech-recognition", 
#     model=model,
#     tokenizer = processor.tokenizer,
#     feature_extractor=processor.feature_extractor,
# )

# result = asr(r"C:\Users\c_n\Documents\физтех\инфа\проги\utdk\voice_lexin.mp3")

# data, samplerate = sf.read(r'utdk\voice_lexin.mp3')

# asr = pipeline(task="automatic-speech-recognition", model="openai/whisper-tiny", return_timestamps=True, model_kwargs={"language": "ru"})

# result = asr(data)




# import soundfile as sf
# from transformers import pipeline

# asr = pipeline(
#     task="automatic-speech-recognition",
#     model="openai/whisper-tiny",
#     return_timestamps=True
# )

# result = asr("utdk/voice_lexin.mp3", generate_kwargs={"language": "ru"})
# print(result["text"])



from faster_whisper import WhisperModel

model = WhisperModel("tiny", device="cpu", compute_type="int8")

seg, info = model.transcribe("utdk/voice_lexin.mp3")
for segment in seg:
    print(segment.text)
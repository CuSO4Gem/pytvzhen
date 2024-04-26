from faster_whisper import WhisperModel
import srt
import datetime

WAV_FILE = r"D:\document\AI_Work\video\smart\X7j8F16eSqs_zh.wav"
SRT_FILE = "zh.srt"
END_INTERPUNCTION = ["。", "！", "？", "…", "；", "，", "、", ",", ".", "!", "?", ";"]

model = WhisperModel("medium", device="cuda", compute_type="float16", local_files_only=False)
segments, _ = model.transcribe(audio=WAV_FILE,  language="zh", word_timestamps=True, initial_prompt="简体")
index = 1
subs = []
for segment in segments:
    subtitle = None
    for word in segment.words:
        if subtitle is None:
            subtitle = srt.Subtitle(index, datetime.timedelta(seconds=word.start), datetime.timedelta(seconds=word.end), "")
        finalWord = word.word.strip()
        subtitle.end = datetime.timedelta(seconds=word.end)

        print(finalWord)
        if finalWord[-1] in END_INTERPUNCTION:
            pushWord = finalWord[:-1]
            subtitle.content += pushWord
            subs.append(subtitle)
            index += 1
            subtitle = None
        else:
            subtitle.content += finalWord

    if subtitle is not None:
        subs.append(subtitle)
        index += 1

content = srt.compose(subs)
with open(SRT_FILE, "w", encoding="utf-8") as file:
    file.write(content)
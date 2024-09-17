import librosa

def detect_sections(instruments):
    guira_audio = instruments['guira']
    y, sr = librosa.load(guira_audio)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    
    sections = []
    if tempo < 100:
        sections.append("derencho")
    elif 100 <= tempo < 150:
        sections.append("majao")
    else:
        sections.append("mambo")
    
    return sections
from pyannote.audio import Pipeline
from pydub import AudioSegment

def seperation(wav, save_dir):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1", use_auth_token="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")
    diarization = pipeline(wav)
    song = AudioSegment.from_wav(wav)

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        #print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        temp_song = song[turn.start* 1000:turn.end* 1000]
        temp_song.export(save_dir + speaker + _ + ".wav", format = "wav")
import os
import Diarization as d
import VoiceClassifier as vc

def evaluate(predicts):
    m_count = 0
    f_count = 0
    c_count = 0

    for predict in predicts:
        if predict == "F": m_count += 1
        elif predict == "M": f_count += 1
        elif predict == "C": c_count += 1

    max_v = max(m_count, f_count, c_count)
    if m_count == max_v: return "M"
    elif f_count == max_v: return "F"
    elif c_count == max_v: return "C"

def strix(wav):
    counter = {}
    spk_dict = {}
    counter["M"] = 0
    counter["F"] = 0
    counter["C"] = 0

    sep_dir = "../sep/"
    d.seperation(wav, sep_dir)
    speechs = os.listdir(sep_dir)

    for speech in speechs:
        spk_id = speech[8:10]
        if spk_id not in spk_dict:
            spk_dict[spk_id] = [sep_dir + speech]
        else: spk_dict[spk_id].append(sep_dir + speech)

    for key, voices in spk_dict.items():
        predicts = []
        for voice in voices:
            predicts.append(vc.voice_classify(voice))
        counter[evaluate(predicts)] += 1

    return counter

def main():
    wav_path = "../test/audio.wav"

    result = strix(wav_path)
    
    for key, value in result.items():
        print(key, value)

if __name__ == "__main__":
    main()
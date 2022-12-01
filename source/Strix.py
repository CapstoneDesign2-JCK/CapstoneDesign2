import os
import shutil
import Diarization as d
import VoiceClassifier as vc

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

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

    createDirectory(sep_dir)
    createDirectory(sep_save)

    sep_dir = "../sep/"
    sep_save = "../sep_result/"
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

    results = os.listdir(sep_save)
    next_num = "0"
    if len(results) != 0:
        next_num = int(results[-1])
        next_num += 1
        next_num = str(next_num)

    os.mkdir(sep_save + next_num)
    for speech in speechs:
        shutil.move(sep_dir + speech, sep_save + next_num + "/" + speech)

    return counter

def main():
    wav_path = "../test/audio.wav"

    result = strix(wav_path)
    
    for key, value in result.items():
        print(key, value)

if __name__ == "__main__":
    main()
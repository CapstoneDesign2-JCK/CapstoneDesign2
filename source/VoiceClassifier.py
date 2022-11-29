from speechbrain.pretrained import EncoderClassifier
import torchaudio

def voice_classify(wav):
    classifier = EncoderClassifier.from_hparams(source = './', hparams_file='inference.yaml', savedir = "./tmp")
    
    # Perform classification
    audio_file = wav
    signal, fs = torchaudio.load(audio_file)
    #embeddings = classifier.encode_batch(signal)
    output_probs, score, index, text_lab = classifier.classify_batch(signal)

    return text_lab[0]
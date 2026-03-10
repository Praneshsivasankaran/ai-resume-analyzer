from textblob import TextBlob

def analyze_grammar(text):
    blob = TextBlob(text)
    corrected = blob.correct()
    
    # crude grammar estimation
    errors = 0
    for word1, word2 in zip(text.split(), str(corrected).split()):
        if word1 != word2:
            errors += 1

    if errors < 10:
        score = 90
    elif errors < 25:
        score = 75
    elif errors < 50:
        score = 50
    else:
        score = 25

    feedback = []
    if errors > 25:
        feedback.append("Resume contains noticeable grammar or spelling issues.")

    return score, errors, feedback
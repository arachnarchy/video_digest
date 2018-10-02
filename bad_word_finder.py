def bad_word_finder(text):

    badwords = []
    with open('static/badwords.txt', 'r') as f:
         for line in f:
             for word in line.split():
                 badwords.append(word)

    text = text.lower().split()

    badwords_found =  [i for i in text if i in badwords ]
    badwords_count = len(badwords_found)

    if badwords_count > 0:
       badwords_prop = len(text) / badwords_count
    else: badwords_prop = 0

    return badwords_found, badwords_count, badwords_prop

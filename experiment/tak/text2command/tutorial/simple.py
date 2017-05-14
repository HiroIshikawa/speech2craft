# Set up spaCy
from spacy.en import English
from subject_object_extraction import findSVOs

parser = English()

# Test Data
multiSentence = "There is an art, it says, or rather, a knack to flying." \
                 "The knack lies in learning how to throw yourself at the ground and miss." \
                 "In the beginning the Universe was created. This has made a lot of people "\
                 "very angry and been widely regarded as a bad move."


# can still work even without punctuation
parse = parser("Go straight")
print(findSVOs(parse))
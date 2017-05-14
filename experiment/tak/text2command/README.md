# Experiment Note

## From the spaCy introduction

### Note for applications of Malmo

Tokes to root pursing is useful.
```
def tokens_to_root(token):
    """
    Walk up the syntactic tree, collecting tokens to the root of the given `token`.
    :param token: Spacy token
    :return: list of Spacy tokens
    """
    tokens_to_r = []
    while token.head is not token:
        tokens_to_r.append(token)
        token = token.head
        tokens_to_r.append(token)

    return tokens_to_r

# For every token in document, print it's tokens to the root
for token in doc:
    print('{} --> {}'.format(token, tokens_to_root(token)))

# Print dependency labels of the tokens
for token in doc:
    print('-> '.join(['{}-{}'.format(dependent_token, dependent_token.dep_) for dependent_token in tokens_to_root(token)]))`
```


# Flashcard Writer Rules

## Back field formatting

Always put the answer on a new line after `Back:`. Never inline the answer on the same line.

**Correct:**
```
START
Basic
What is the question?
Back: 
The answer goes here.
Tags: some-tag
END
```

**Incorrect:**
```
START
Basic
What is the question?
Back: The answer goes here.
Tags: some-tag
END
```

# Chisel Annotation Test Cases

This document collects real-world examples of how token classification annotations are embedded using inline HTML-style tags.

The purpose is to:
- Provide test cases for the HTMLTagParser
- Explore edge cases and domain-specific conventions
- Document assumptions and deviations

---

## ✅ Flat Inline Entity Tags

```html
The <PER>UN</PER> met with <PER>Joe Biden</PER> today.
```

→ Clean, standard annotation. Common in Doccano, brat, and research projects.

## ✅ Tags with Attributes

```html
<PERSON role="manager">Alice</PERSON> leads the team.
<ORG type="non-profit" confidence="0.9">UNICEF</ORG>
```

→ Attributes should be parsed and preserved in metadata (optional).

## ✅ Nested Tags
```html
<ORG><PRODUCT>Google Search</PRODUCT></ORG>
```

→ Must decide:

* Keep inner tag only?

* Flatten both?

* Raise error?

## ✅ Broken/Malformed Tags
```html
<person>John<person>
```


## ✅ Noisy Tags (Not Entity-Related)
```html
This is <b>bold</b>, and <PER>Jane</PER> is here.
```
→ Only entity tags should be processed. Ignore styling, structure tags.

## ✅ Multiple Same-Label Entities
```html
<PER>Barack Obama</PER> met <PER>Angela Merkel</PER> in <LOC>Berlin</LOC>.
```
→ Should yield 3 separate spans.

## ✅ Entity at Start or End
```html
<PER>Obama</PER> visited today.
... as mentioned earlier today by <PER>Obama</PER>
```
→ Ensure char offsets and tokenization hold up at boundaries.

## ✅ Biomedical / XML Style
```html
<sentence>The <chemical>aspirin</chemical> was used for <disease>migraine</disease>.</sentence>
```
→ Tags may use lowercase or domain-specific names.

## ✅ Legal Domain Examples
```html
<CASE>Roe v. Wade</CASE> was cited in <STATUTE>Article 14</STATUTE>.
```
→ Often seen in legal NLP datasets.

## ✅ Academic/Narrative Annotations
```html
<SPEAKER>Dr. Smith</SPEAKER>: <QUOTE>"This finding is significant."</QUOTE>
```
→ Useful for quote extraction, news, and dialogue attribution.


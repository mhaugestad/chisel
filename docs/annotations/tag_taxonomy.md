# Tag Taxonomy for Token Classification

This document defines a taxonomy of annotation tag styles seen in real-world NLP projects. It guides how Chisel's parsers should interpret, validate, or reject various patterns.

---

## ✅ 1. FlatInline

Simple inline tags with clear open and close markers.

```html
The <PER>UN</PER> met <PER>Joe Biden</PER> today.
```
→ Core supported case.

✅ 2. FlatWithAttributes
Tags that contain attributes with useful metadata.

```html
<PER role="manager">Alice</PER>
<ORG type="non-profit">UNICEF</ORG>
```
→ Chisel stores attributes: dict[str, str] in the EntitySpan.

⚠️ 3. NestedTags
A tag inside another tag. Ambiguous in BIO token classification.

```html
<ORG><PRODUCT>Google Search</PRODUCT></ORG>
```
→ Currently not supported. Parser logs a warning and processes inner tag only.

❌ 4. OverlappingTags
Improper overlapping tags (non-nested).

```html
<A>foo<B>bar</A>baz</B>
```

→ Not supported. Parser should raise or skip with error.

✅ 5. DomainSpecific Tags
Custom tags from legal, scientific, or academic domains.

```html
<CASE>Roe v. Wade</CASE>
<STATUTE>Article 14</STATUTE>
```
→ Allowed if tag is in user-provided label schema.

⚠️ 6. BrokenTags
Malformed tags (missing opening or closing).

```html
<PER>Obama
```

→ Parser attempts to recover and logs warning.


✅ 7. BlockEntities
Tags that wrap entire sentences, paragraphs, or quotes.

```html
<SENT><PER>Obama</PER> spoke to the press.</SENT>
```
→ Parser extracts only inner entity tags.

✅ 8. AttributeDriven Labels

Label is not in tag name, but in attribute.

```html
<span type="PER">Obama</span>
```
→ Parser can use type if enabled via config.

✅ 9. UnknownTags
Non-entity tags like formatting.

```html
This is <b>bold</b> and <PER>Jane</PER> is a person.
```
→ Non-entity tags are ignored.


| Category           | Action               |
| ------------------ | -------------------- |
| FlatInline         | ✅ Parse              |
| FlatWithAttributes | ✅ Parse + enrich     |
| NestedTags         | ⚠️ Warn + flatten    |
| OverlappingTags    | ❌ Reject             |
| BrokenTags         | ⚠️ Log + recover     |
| BlockEntities      | ✅ Process inner tags |
| UnknownTags        | ✅ Ignore             |
| DomainSpecific     | ✅ Allow if known     |
| AttributeDriven    | ✅ Use attribute      |

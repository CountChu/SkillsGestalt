# STE Rules Digest

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-11`  `d1f4ea9e7cd6`

The asd-ste skill rewrites a Markdown file by this digest.
It sums up, in its own words, the writing rules of Part 1 of ASD-STE100 Simplified Technical English, Issue 9, and its eight general recommendations, and gives the number of each, so that a finding can name the rule it breaks.
The words themselves are in [ste-dictionary.json](ste-dictionary.json), built from Part 2: each approved word with its parts of speech and its forms, and each unapproved word with the approved words that replace it.
The few words this project approves beyond Issue 9 are in [ste-custom.md](ste-custom.md), the project-approved words, beside the writing rules this project adds (House Rule 11).
`check_ste.py` measures what a program can measure: sentence and paragraph length, one sentence on a line, semicolons, contractions, the kept spans, each word against the dictionary, and each British spelling against the US spelling list.
Everything else here is the writer's judgement.
The last two sections are not STE: they are how this skill applies STE to a Markdown file.

# 1. Words

- **Approved words only (1.1).**
  Use a word the dictionary approves, a technical noun or a technical verb, and nothing else; the project-approved words add a few to the approved ones (House Rule 11).
  A word the dictionary does not list at all is not approved either: *what*, *understand*, *own* and *like* are not in Issue 9.
- **The approved part of speech (1.2).**
  *Test* and *check* are approved nouns, not verbs: write "Do a test of the valve" or "Make sure that the valve is closed".
  The check script accepts a word approved in any part of speech, so the part of speech is yours to verify: [ste-dictionary.json](ste-dictionary.json) lists the parts of speech of each approved word.
- **The approved meaning (1.3).**
  An approved word keeps the one meaning the dictionary gives it, even where English allows others.
  `check_ste.py` cannot see a meaning, so the meaning is yours to verify.
- **The approved forms (1.4).**
  A verb takes only the forms the dictionary lists, and an adjective only its listed comparison.
- **Technical nouns (1.5 to 1.11).**
  A noun of the subject the text is about can be used though the dictionary does not list it, when it fits one of the categories STE names.
  For documents like the ones in this repository the categories that matter are: systems, components, their functions, configurations and parts (6); mathematical, scientific and engineering terms (7); numbers, units and time (9); quoted text (10); roles, individuals, groups and organizations (11); documents, parts of documents, standards and guidelines (15); colors (17); computer science and information technology (19).
  Never use a technical noun as a verb (1.7).
  Use the name the subject field uses (1.8), a short and clear one when you must select one (1.9), and no slang or jargon (1.10).
  Give one item one name, and always the same one (1.11).
- **Technical verbs (1.12, 1.13).**
  A verb of a technical category can be used though the dictionary does not list it; for these documents the category is computer processes and applications, such as *parse*, *import*, *compile* and *commit*.
  A technical verb obeys every rule for verbs, and is never used as a noun (1.13).
- **American spelling (1.14).**
  *Color*, *behavior*, *catalog*.
  `check_ste.py` finds a British spelling by the US spelling list, [us-spelling.json](../../../references/us-spelling.json), in the prose and in the kept spans.

# 2. Noun Clusters

- **At most three nouns in a row (2.1).**
  Break a longer cluster with a preposition: "the stage read/write rule table" becomes "the table of the read/write rules of the stages".
- **A longer technical noun (2.2).**
  Write it in full the first time, then use a shorter form, or join the words that act as one unit with hyphens.

# 3. Verbs

- **Forms and tenses (3.1, 3.2).**
  Use the infinitive, the imperative, the simple present, the simple past, the simple future, and the past participle as an adjective.
  There is no present perfect (*has changed*), no progressive (*is running*), and no conditional (*would break*).
- **The past participle as an adjective (3.3).**
  "The changed file", "a closed valve".
- **No complex constructions (3.4).**
  "The volume control can be adjusted" becomes "You can adjust the volume control".
- **-ing forms (3.5).**
  Only in a technical noun or as a modifier in one: *file-locking mechanism* is a technical noun, but "by reading the file" becomes "when you read the file".
- **The active voice (3.6).**
  In an instruction, always.
  In a description, the passive voice is allowed only when nobody knows who or what does the action.
- **A verb for an action (3.7).**
  "Do the installation of the pump" becomes "Install the pump".

# 4. Sentences

- **Short and clear (4.1).**
  In a description, each sentence has one topic.
- **No omitted words, no contractions (4.2).**
  Keep the articles, *that* and the verbs; write *do not*, never *don't*.
- **Vertical lists (4.3).**
  Put a long series of items, conditions or steps in a vertical list.
- **Connecting words (4.4).**
  Show how sentences relate with *and*, *but*, *then*, *thus*, *as a result*, *at the same time*.
- **Articles (4.5).**
  Put *the*, *a*, *an*, *this* or *these* before a noun where English needs one.

# 5. Instructions

- **At most 20 words (5.1).**
- **One instruction in each sentence (5.2)**, unless two actions occur at the same time.
- **The imperative (5.3).**
  "Write the file", not "The file must be written".
- **The condition first (5.4).**
  "If the file exists, ask the user."
- **Notes give information, not instructions (5.5).**

# 6. Descriptions

- **Give information gradually (6.1).**
  The topic first, then the details, one subject in each sentence.
- **Key words (6.2).**
  Connect the ideas with key words, and never change a key word for variety.
- **At most 25 words (6.3).**
- **Paragraphs (6.4 to 6.6).**
  A paragraph holds related information, has one topic, and has no more than six sentences.

# 7. Safety Instructions

- **The level of risk (7.1).**
  A warning is a risk of injury or death, a caution a risk of damage.
- **A clear start (7.2).**
  Start with a clear command or condition.
- **The risk (7.3).**
  Then give the risk or the possible result.

# 8. Punctuation and Word Count

- **No semicolon (8.1).**
  Write two sentences, or a vertical list.
- **Hyphens (8.2).**
  Join words that are directly related.
- **Parentheses (8.3).**
  For a reference, an identifier, an abbreviation, a singular and plural together, an explanation or an alternative.
- **What counts as one word (8.4 to 8.7).**
  In a vertical list a colon ends a sentence, as a period does.
  Text in parentheses counts as one word.
  So does each number with its unit, abbreviation, identifier, quoted text, title, heading, label and proper noun.
  A hyphenated word counts as one word.
  `check_ste.py` also counts an inline-code span and a link as one word.

# 9. Writing Practices

- **Build the sentence again (9.1)** when a word-for-word replacement does not give a good sentence.
- **Use each approved word correctly (9.2).**
- **No phrasal verbs (9.3).**
  "Carry out the test" becomes "Do the test".
- **A consistent style (9.4).**
  The same term and the same construction for the same thing, all through the file.

# General Recommendations

Part 1 closes its section 9 with eight general recommendations, GR-1 to GR-8.
They are not rules, but advice for the places where STE text most often goes wrong.

- **The conjunction *that* (GR-1).**
  Keep *that* after a verb that opens a clause, such as *make sure*, *show* or *tell*: "Make sure that the file exists", not "Make sure the file exists".
  The word shows where the clause starts, and many languages cannot leave it out, so it also helps a translation.
  `check_ste.py` warns where *make sure* has no *that* after it; after *show*, *tell* and other verbs, the check is yours.
- **The preposition *with* (GR-2).**
  *With* has three approved meanings - related to, together with, and by means of - so read each sentence that uses it again, and build the sentence again when it can mean two things.
  Keep the main action as the verb: "Sort the rows with the script", not "Use the script to sort the rows".
- **Pronouns (GR-3).**
  Use only the pronouns the dictionary approves, so never *he* or *she*.
  When a pronoun can point to more than one noun, write the noun again.
- **The pronoun *this* (GR-4).**
  Make sure that the reader knows what *this* points to, and when it can be more than one thing, say that thing again.
- **False friends (GR-5).**
  A word that looks like a word of your own language can mean something else in English: use it only in its English meaning.
- **Latin abbreviations (GR-6).**
  Write *for example*, *that is* and *and so on*, not *e.g.*, *i.e.* and *etc.*, or leave the abbreviation out when it adds nothing.
  `check_ste.py` warns about each one, with the English words to write.
- **Inclusive language (GR-7).**
  Use words that name no gender: no *he* or *she*, and no *man* or *woman* unless the subject needs them, as a medical text can.
- **The possessive (GR-8).**
  STE allows "the caller's request", but when you are not sure that a possessive is correct and clear, write "the request of the caller".

# Common Replacements

The unapproved words that documents like these use most, with the approved words the dictionary gives for them.
`check_ste.py` prints the replacement of every unapproved word it finds.

| Unapproved | Approved |
|---|---|
| may | can |
| should | must |
| ensure | make sure |
| allow, permit | let |
| every | all |
| require | necessary (adj) |
| describe, mention | give |
| state (v), explain | tell |
| order (n) | sequence |
| wrong, true | incorrect, correct |
| outside (adj) | external |
| later | subsequent, subsequently |
| often | frequently |
| however | but |
| therefore | thus |
| exactly | accurately |
| whole | full |
| several | some |
| process (n), way | procedure |
| kind | type |
| both | the two |
| whether | if |
| within | in |
| under | below |
| reason | cause |

# House Rules

How this skill applies STE to a Markdown file.
`check_ste.py` checks each rule marked *checked*.

1. **Kept spans stay unchanged** (*checked*).
   Every heading line, fenced block, inline-code span, link target, wiki link and placeholder, the frontmatter's keys and every value but `description`, and the source's own header quote reach the STE file byte for byte.
   A heading is how other documents cite a section, and a fenced block is often what a user types or a program reads.
2. **Every statement stays.**
   No rule, condition, number, example or reason is dropped, merged away or added.
   A long sentence becomes several sentences or a vertical list, never a shorter claim.
   The reason a rule gives, such as "otherwise the reader cannot tell", is a statement too.
3. **One sentence on each line** (*checked*), as [md-style.md](../../../rules/md-style.md) requires.
4. **An instruction or a description.**
   A sentence that tells the reader to do something is an instruction: the imperative, at most 20 words.
   A sentence that says what something is or how it works is a description: at most 25 words.
   A rule addressed to the writer of a document is an instruction.
5. **The head of the file** (*checked*), in this order:
   - the source's frontmatter, when it has one, as House Rule 1 keeps it;
   - the source's title, when its first line under the frontmatter is one;
   - the header quote: the source's own header quote lines (House Rule 1) - its Version line first, when it gives one, such as `> Version: 261013` - then `> [[ASD-STE100_ISSUE9.pdf]]` - the date and the fingerprint after it are written by `depends_on.py record`, never by hand - and `> [[ste-custom]]` after it, recorded the same way, also when the prose uses no project-approved word, because every STE file follows the project rules;
   - a blank line, then the header note, a block quote of three lines:

     ```
     > This file is [DFD.md](DFD.md) in ASD-STE100 Simplified Technical English (STE), Issue 9.
     > If the two files do not agree, [DFD.md](DFD.md) is correct.
     > Technical words: caller, legend, mermaid, process, query.
     ```

   The header note names the source file by its file name, which is also the link target.
   The last line lists every technical word the file uses, in alphabetical order, separated by commas; the check accepts their plural forms, and the forms of a technical verb, without more.
   When the user approves the file and it replaces its source, the header note keeps two lines: `> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.`, and the `Technical words:` line.
   The line for the STE specification in the header quote marks the file as one in STE.
6. **A technical word is a real one.**
   List only a word that fits a technical noun or verb category of rule 1.5 or 1.12, and list each one the file uses: a word the dictionary does not approve, and an approved word that the file uses in a technical meaning the dictionary does not give it (rule 1.3), such as *record* for data a system keeps.
   An approved word in its approved meaning is not listed, and neither is a project-approved word (House Rule 11).
   Never list a word only to stop a warning: *what* is not a technical noun, so build the sentence again.
7. **The file speaks of the source by name.**
   Where the source's prose speaks of its own twin or its own version, the STE file says it of the source file by name, so that the STE file never claims the source's twin or version as its own.
   The version number itself is not prose: the source gives it on the Version line its header quote opens with, such as `> Version: 261013`, where tools such as `check_rsdc.py --standard` read it, and the STE file keeps that line, as House Rule 1 keeps the header quote.
   "This document" stays as it is: what the source says of itself is true of the STE file as well, which holds the same statements.
8. **Tables** (*checked*).
   The header row stays as it is; the other cells are rewritten in STE, with the same number of columns.
9. **Emphasis stays where the source put it**, on the words that carry the same weight.
   A bold label that opens a list item, such as `**Terminology**:`, is a title and stays as it is.
10. **Quoted text.**
    A quotation of another document, a heading or a label stays as written, and counts as one word.
    A sentence the source quotes as its own example is rewritten in STE too.
11. **Project-approved words and rules** (*checked*).
    [ste-custom.md](ste-custom.md) lists, under Words, the words this project approves beyond Issue 9, and under Rules, the writing rules that the user adds beyond Issue 9 and these House Rules.
    Use each word and follow each rule as ste-custom.md tells: it says how each one is checked, and how a word or a rule joins its table.

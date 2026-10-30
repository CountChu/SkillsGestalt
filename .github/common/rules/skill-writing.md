# Skill Writing Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: Dataflow, definition, file, glossary, line, link, natural language, noun, script, section, sentence, skill, summary, term, text, twin.

These rules tell how to write the `SKILL.md` and the `README.md` of a skill.
You use these rules when you write a skill, not when you operate a skill.
Thus, a `SKILL.md` does not contain these rules.
`gen-skill` writes skills by these rules, `check-skill` makes sure that skills obey them, and the `README.md` of a skill refers to them.

# Rules

- **Before you change a skill, read its `README.md`, if the skill has one.**
  The README tells which files change together, and which checks to do after a change.
  Make all the changes that the section "When the Skill Is Changed" of the README gives, in the same run.
  Before you complete the change, do all the checks that this section gives.
- **Each skill has a `README.md` that you write from [README-tmp.md](../templates/README-tmp.md).**
  It contains the information that is not necessary for a run, for example the Dataflow.
  It also tells which files change together, and which files the skill depends on.
  `SKILL.md` contains only the information that is necessary for a run, because each run reads all of it.
  `SKILL.md` does not have a link to the `README.md`, thus no run reads the `README.md`.
  If the `SKILL.md` of a skill has a 繁體中文 twin, the skill also has a `README-tw.md`.
- **In the glossary of `SKILL.md`, give one definition for each noun that is necessary for the steps.**
  The glossary is the two sections `# TERMINOLOGY` and `# DEDICATED TERMINOLOGY` of `SKILL.md`.
  `# TERMINOLOGY` contains the terms that identify the same item in all skills, and `# DEDICATED TERMINOLOGY` contains the terms that only this skill uses.

  Then the steps use the term, and do not give its definition again.
  Only the glossary has the definition.
  If a step gives the definition again, the two definitions will become different.
  The glossary stays in `SKILL.md`, because a run must know the definition of each term that its steps use.
- **Each step is self-contained: "no forward-reference".**
  A step does not depend on a step that comes after it.
  If a step refers to a subsequent step to control the flow, the step obeys the rule.
  But if a step uses the output of a subsequent step, the step does not obey the rule.
- **If a program can do a step deterministically, the step operates a script: "scripted-versus-not".**
  If a step must read text, make a decision or write a summary, do not write a script for it.
  Write the step as instructions in natural language that the agent follows directly.
- **A skill tells one time how it obeys the rule above**: which steps operate a script, which steps do not, and the cause.
  If the same line is below most of the steps, it gives no information.
  Also, the Purpose of a step usually gives the same cause.
  The section "Files Each Step Uses" of the `README.md` gives this information.
- **Each step has a Purpose**: one sentence that gives the cause to have this step.
  That is, it tells how the skill becomes worse if you put the step and an adjacent step together.
  The Purpose is not a summary of the work of the step, because the instructions of the step give that information.
  If a Purpose gives the instructions again, it is a second copy, and the two copies will become different.
  The section "Step Purposes" of the `README.md` gives each Purpose.

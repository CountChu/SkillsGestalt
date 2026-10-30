# ArtifactFlowAgent: The Responsibilities of the Four RSDC Chapters

> Version: 261016
> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-14`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: activity, address, answer, app, architecture, argument, authorization, boundary, branch, button, call, caller, chapter, checklist, code label, column, command, configuration, constraining rule, content, contract, cost, coverage, Dataflow, day, decimal, default, defect, derived value, description, development, diagram, directory, document, endpoint, environment, exception path, field, file, file-locking mechanism, flag, flowchart, git, goal, granting rule, guideline, heading, hint, history, import, kernel, key, label, layout, legend, library, line, link, list, logic, mapping, mermaid, metadata, module, network, node, notation, noun, operating system, orphan, parallelogram, parameter, parse, path, pathlib, platform, process, project, proof, query, question, record, refactor, request, researcher, response, retries, retrieval, rounding, schema, scope, screen, section, separator, server, skill, specification, spelling, stage, standard, status, style, subsection, syntax, table, task runner, template, term, terminology, text, title, topic, twin, user, verdict, verification, version, viewer, vocabularies, word, writer.

RSDC is the short name for **Requirements**, **Specification**, **Design** and **Coding**.
An RSDC has four **chapters**, one for each of these four items.
The chapters have the numbers 1 to 4.
The number of chapters and their sequence do not change.

A **section** is a part of a chapter.
Each section has a number N.M, for example 2.2.
Parts below a section do not have a number.

RSDC-Standard.md uses the RSDC of the ArtifactFlowAgent project as its example.
It gives the standard that applies to all RSDCs that you write after this time.

This version replaces 261010.
The git history keeps the previous versions.
The section "Changes in This Version" at the end of RSDC-Standard.md gives the changes and their causes.
The section "Versioning", also at the end, gives the rules for a new version.

# Core Writing Principle: One-way Dependency

Write all documents by the rules that follow, and obey these rules fully.
These rules keep the layers of the system architecture clear.
They also keep the logic of each layer isolated from the other layers.

- **An earlier chapter may not mention a later chapter's content**:
  - In the Requirements, do not give the content of the Specification (for example, an Artifact type).
  - In the Specification, identify a component only by its interface.
    The interface is the API or the CLI that an external system calls, for example an AI agent or a skill.
    Do not identify a component by its inner parts (for example, a Manager module).
  - In the Design, do not give the syntax of the Coding (for example, a library or a type hint).
- **From abstract to concrete**: Each chapter can use only the content of the chapter before it.
- **Every rule says what breaks when it is broken**: For example, a rule can be "When the query finds no result, the screen tells the user."
  The rule then tells the result if the system does not obey it: "If the screen does not tell the user, the user cannot know if the query found no result or if the query did not operate correctly."
  This result of the rule also gives the test.
  Cause an error in the query, and then examine the screen.
  If the screen tells the user that the query found no result, the code is incorrect.

  A test of only the usual condition does not find code that shows "no result" each time that the list is empty.
  That code is correct only accidentally.

  The result of the rule also stays correct when the screen changes.
  For all changes to the screen, the user must continue to know the difference between the two conditions.
- **No Forward Reference**: A section must not refer to a chapter or a section that has a higher number.
  A text, for example "refer to the section below", looks safe.
  But the reader then cannot read the section without the other section.
  If section A is not complete without the content of section B, put that content in section A.
  Or, put section A after section B.

# 1. Requirements — "What problem does this solve?"

This chapter gives the goals of the project and the problems that it has at this time.
**This chapter must not tell how the system does its work, and it must not give the architecture of the system.**

- **Target Users**: The persons or systems that use the system (for example, researchers or an AI agent).
- **Core Vision**: The highest value that the system must supply as the goal of all its work, and the cause that makes the system necessary.
- **Current Pain Points**: The problems in the procedure that the project uses at this time.
  These problems make the work slow, or make the logic not clear.
- **System Goals**: A clear list of the properties that the system must have.
  For example, isolated logic, or a full flow that a person can follow from the start to the end.

**Each system goal must have a related rule in chapter 2.**
A goal gives a result that the system must get.
A rule gives a limit that the system must obey because of that goal.
If the Specification has no rule for a goal, the goal has no effect.
No part of the RSDC makes sure that the system gets the result of that goal.

The goals table at the end of the Invariants of chapter 2 shows the rules that keep each goal.

# 2. Specification — "What are the system rules?"

This chapter gives the standards and the limits of the system.
They are the "law" that all components must obey.
This chapter can control "what" the system does, but it must not control "what it looks like".

For example, it can tell that the system must not show a data item.
It can tell that it must be possible for the user to start an operation.
But it must not tell if the user starts the operation with a button, a link or a command.

**The test**: Think about a change, and about a verification that is satisfactory before the change.
If the change makes that verification unsatisfactory, the change is a rule, and it goes in this chapter.
If the change only uses different words or moves text, it is not a rule.
Such a change goes in the Design or the Coding.

- **Terminology**: The nouns that the subsequent topics use, but that no subsequent topic tells about.
  For example, a role that is external to the system (the caller), or a location (the directory that a run writes into).
  Tell about each term one time, before its first use.
  A term is not the name of data, because Artifact Types gives the data after Terminology.
  A unit of the Hierarchy, a stage, a code label, a configuration key, a derived value and a component each have a different topic.
  Do not put them in Terminology.
- **Hierarchy**: The levels of the units that the users of the system put together to make the system.
  Also, which level contains which level (for example, the relation of the three layers Lambda, Flow and Agent).
  Write this topic only when the users make the system from such units.
  If a system does not have these units, do not write this topic.

  Some layers are only in the internal architecture of the system, for example a server that gives its work to a kernel.
  These layers are not a Hierarchy.
  You can change the sequence of these layers, and all verifications that were satisfactory before the change stay satisfactory.
  Thus, by the test at the start of this chapter, these layers go in the Core Component Responsibilities of the Design.
- **Artifact Types**: The types of data object (for example, Sequence, Dataset, Archive).
  For each type, tell the information that it holds, its purpose and the limits on its content.
  The Dataflow tells who writes the data and who reads it.
- **Dataflow**: How data moves between the activities of the system.
  Give the **stages** and the data that each stage reads and writes.
  Tell who writes each **record** and who can read it.
  Tell the sequence that comes from the data.

  Show the Dataflow as a DFD.
  [DFD.md](DFD.md) gives the types of data, the shapes and the lines of a DFD.
  It also gives the defects to look for in each DFD.
  The limits between this topic and the topics near it are as follows:
  - "Hierarchy" tells which units there are and which unit contains which unit.
    A unit comes into this topic only as data that a stage reads (for example, its configuration), and not as a stage.
  - "Artifact Types" tells **the type** of the data.
    This topic tells **where** the data goes.
  - The "Execution Flow" of chapter 3 tells about the operation of the system at run time, with the names of components.
    This topic tells about the same operation, with the names of activities.
    In chapter 3, a mapping between the two vocabularies connects the two topics.

  - **Required content**:
    1. **DFD**: The diagram of the stages, with all roles that are external to the system.
       Only the DFD tells the data that each stage reads and writes.
       Only the DFD tells who writes and who reads each data item, and the type of each data item.
       Do not write a table that gives this information again.
       A second copy becomes different from the diagram, and no person sees the difference.
    2. **Data Read/Write Rules**: The rules about the data that the diagram cannot show.
       Tell where each rule applies.
       Tell if a stage writes a data item as one full item.
       Tell if a data item stays read-only after a stage writes it.
       Tell who removes it.
    3. **Order Imposed by the Data**: For each sequence, give the data that causes it.
       The section must also tell clearly that "no stage reads what a later stage writes".
    4. **Exception Paths**: Give these three paths:
       - The path that stops before the end.
       - The path that ends, but writes no data.
       - The path that starts again at a stage in the middle of the flow (for example, the path that does only the last stages again).
  - **Inside a stage**: Do not show the inner parts of a stage in this topic.
    The inner part of a stage is its parts and their sequence.
    It is also the data that each part reads and gives to the next part.
    This is how a component does the work of the stage, and it goes in the Execution Flow of chapter 3.

    In some conditions, a sequence in a stage is a rule.
    Data that moves between the parts of a stage can also be a rule.
    A rule of this type is necessary for a verification.
    For example, the stage must complete a check before it writes data.

    Write such a rule in words in this chapter.
    Tell the rule only with the inputs and the outputs at the boundary of the full stage, and their sequence.
    Put it with the related rules: a Derivation Rule, an Invariant or an exception path.
    If you make a diagram of the stage, it shows only one procedure that obeys the rule.
    The other parts of that diagram are not rules.
  - **Naming**: Give each stage the name of its activity, not the name of a component.
    For each record, use the name that the system uses.
    A file name is satisfactory.
    Do not use the name of the module that writes the record.
    With that name, the Specification makes a decision of the Design before the Design.

    The diagram also uses other names.
    Examples are the name of an external role, of a data item, and of a group of inputs that the diagram shows as one node.
    Terminology or Artifact Types must tell about each of these names before the Dataflow.
    If the Dataflow uses a name and no section tells about it, the reader cannot know the item that the name refers to.
  - **Placement**: This topic gives the names of the stages and the records that the subsequent sections use.
    Because of "No Forward Reference", put this topic before all sections that use these names.
    Do not give it a section number that is always the same.
- **Naming and Data Structures**: The standard rules for names (for example, the use of # as a separator), and the rules to parse metadata.
  - **A code label is a contract**: A code label is a text that does not change.
    A program writes it, and a reader compares it accurately.
    Examples are a status, a type and a verdict.
    A code label is not the text on a control on the screen.
    For each field that holds code labels, give all the code labels that the field can hold.
    If a code label has a different spelling, no reader knows the value, and no part of the system tells about the difference.
  - **Every number states its precision**: Tell how many positions after the decimal point the number keeps, and its rounding.
    If two readers use different rounding for the same value, they do not agree about the value.
    Then, when the two readers compare the value with a limit, they can get different results.
- **Config Schemas**: The fields that each configuration file that the system reads must contain, and the logic limits on these fields.
  Give all these fields fully (for example, the I/O contract and the fields that tell an AI about it).
  If the system has a Hierarchy, each level has a different schema (for example, the config.yaml of a Lambda, of a Flow and of an Agent).
- **Derivation Rules**: How the system gets values that it **does not see directly**.
  Give the sequence in which the system must use the sources, and the cost that causes this sequence.
  Also tell **the items that the system must not use as a replacement**.
  If more than one source can give a value, this topic gives the sequence of the sources.

  If no source can give a value, this topic tells how to identify the missing value.
  Do not let an approximate value that looks correct replace it.
  In the full document, code frequently does not obey rules of this type, and these errors are the hardest to see.
  The cause is that an incorrect replacement always looks correct.
- **Presentation Contract**: Tell **which data the system can show, and to which users**.
  Tell **which operations it must be possible for the user to start**.
  Tell **if the data that the user sees agrees with the work that the system does**.
  - **Each project must give an answer to the eight questions that follow.**
    These questions come from the use of systems.
    They are not a checklist of rules to apply.
    **Different systems give different answers, but the questions are the same.**
    1. Which data does the screen show when there is no result?
       Which location shows the number of items that the system did not include?
    2. Which flows can the user start without help?
       For each flow that the user cannot start, which cause prevents it?
    3. Did a person or a test show that each retrieval operates correctly in the environment of the user?
    4. If an external source also has the material, can the system give its address?
    5. When the view becomes smaller, does the number on the screen agree with the scope of the next operation?
    6. For an operation on many items, which quantity is the maximum?
       How does the system stop a quantity that is too large?
       Can the operation stop before its end, and keep a result that is not full?
    7. Which step must the user do after the system stops an operation of the user?
    8. By default, which persons or systems can get access to the system?
       When more of them can get access, who knows about it?

    These questions do not give an answer.
    A system can correctly give the answer "there is no external source".
    But a question that **no person examines** is a missing part of the Specification.
  - **What is seen is what is done**: Users select their operations from the data that they see.
    Thus, **the scope that the screen shows must be accurately the same as the scope of the operation**.

    If the number on the screen does not agree with the selection, the user can give approval to one set.
    But the user then gets a different set.
    Each safety limit that the system calculates from that scope (for example, a capacity limit) also becomes incorrect.
    This is not an error of the display.
    It is an error of authorization.
  - This topic **does not include** the layout, the type of a control, the words on a label or the style.
    The cause is the test at the start of this chapter.
    The name of this topic is "contract", not "presentation", to keep these items out of it.
  - The Dataflow of a project can have a stage or an activity with the name "presentation".
    **This topic is not the same item.**
    That stage is an activity that operates.
    This topic is a set of limits that the system must obey.
    Give them names that do not use the same word.
- **Interfaces**: Each component that an external system calls (for example, an AI agent, a skill or a different program).
  For each component, give its name and its API or CLI:
  - How to call it: the endpoint and its parameters, or the full command and all its arguments.
  - Which stages of the Dataflow a call runs.
  - The data that it reads and writes.
  - The data that it gives back: the response, or the output and the exit status.
  - The calls that it does not accept.

  The name of a component and its interface are a contract with each caller.
  If a refactor changes the name or the interface, each caller stops correct operation, and no error shows.
  Thus, this chapter sets them, not the Design.
  The inner parts of a component (its modules, and how it does its work) go in chapter 3.

  An external system gets access to a component only through this interface.
  It calls the API or runs the CLI.
  It does not import the modules of the component, and it does not call the code in these modules.
  Chapter 3 can change the inner parts of a component, and keep the same interface.
  Then a caller that uses these parts stops correct operation, and no error shows.
  An RSDC can give this topic a title for its type, for example CLI or HTTP API.
- **Invariants**: The limits that apply to all components, and to each of them.
  The difference between the Invariants and the topics above is **scope**.
  Each topic above controls one type of item.
  The Invariants control all of them.

  If you must keep a rule in three or more locations, put the rule here.
  Do not write a copy of it in each location.
  Copies of a rule change independently, and at the end they do not agree.
  - **The goals table**: Put a table at the end of the Invariants.
    The table connects each goal of chapter 1, by its name, to the sections and rules that keep it.
    Write one row for each goal.
    Only a written table shows a goal that no rule keeps.
    Without the table, you see only during use that the system does not get the result of a goal.
    At that time, no person knows which rule must keep that goal.

# 3. Design — "How is the system structured?"

This chapter gives the structure and the components of the system.
It also tells the methods that the system uses to obey the Specification before it.

- **Core Component Responsibilities**: The components that chapter 2 identifies, each divided into its modules.
  Also, the components that no external system calls (for example, ArtifactManager, File Table, Runtime), and how all the components operate together.
  Each component has **one type of work** and a **boundary**.
  The boundary tells the items that a change across it can break.

  A change across a boundary is a change to two components.
  If one component does two types of work, the boundary between the two types is in that component.
  There, no person sees that a change to one type of work can break the other type.
- **Execution Flow**: How each component does its work at run time.
  For example, how the system reads its configuration, and how it makes its network of tasks at run time (for example, the tasks that a dodo.py gives).
  Also, the remaining logic of the system at run time.
  If a diagram helps, use a DFD with the notation of [DFD.md](DFD.md).
  This DFD has two differences from the Dataflow:
  - Its processes are the steps of the components.
    Use the names that the code uses for the steps.
  - It can show items that a Dataflow does not show.
    These items are the inner part of a stage, branches, retries and parallel work.
    They also include sequences that the code selected and that the data did not cause.

  For each rule, refer to chapter 2.
  Do not write the rule again.
  This also applies to a rule about the inner part of a stage.
- **Directory Structure**: The location of the files of the project, and the logic of their layers (for example, lambdas/, flows/, agents/, warehouse/).
- **Presentation Form**: For each "the user must be able to…" in the Specification, this topic tells **which component** supplies it.
  It also tells **the type of control** that a person uses for it, and how many controls there are.
  The Interfaces of chapter 2 give the API or CLI before this chapter.
  The Specification tells "must be able to start".
  The Design tells "started by whom, and through how many entrances".
  - **A mapping table is required**: The table has three columns:
    1. The capability that the Specification makes necessary.
    2. The component that does it.
    3. The name that the user knows it by.

    The table is a **coverage proof**.
    It is not an interface specification.
    It comes from the rules of chapter 2.
    Thus, it cannot have more rows than there are rules.
  - **An orphan is a defect**: An orphan is a row that has no related rule.
    No person agreed to the capability in that row.
    Write the rule immediately, or remove the capability.
    The opposite check **applies only to a granting rule**.
    A granting rule gives an operation that must be possible for the user.

    If a granting rule has no row, the rule has no entrance.
    A **constraining rule** tells the data that the system must not show, or the users that must not get access.
    A constraining rule has no entrance, because of its type.
    Thus, it is correct that the table does not include it, and this is not a defect.
    If you think that the two types of rules are the same, the table shows incorrect orphans on the first day that you use it.
  - **Not every control is a capability**: Some controls change only how much the screen shows, or how it shows it (for example, "expand all" and "collapse all").
    If you remove such a control and all verifications stay satisfactory, the control is not a capability that the Specification gives.
    **It is correct that the table does not include it.**
    This is the test at the start of chapter 2.
    Only a change that can make a satisfactory verification unsatisfactory is a rule.
    If you do not write this, subsequent readers think that these controls are orphans, and they "fix" them.
  - **Names and nothing more**: A name that the user sees can occur only in the related column of the table.
    Do not use it to tell how the system operates, or to give the layout, the position or the style.
    These items stay in the Coding.
- **The Specification's vocabulary and the components' vocabulary must join up**: The Specification uses the names of activities and data.
  In Interfaces, it also uses the names of the components that external systems call.
  The Design gives the names of all components.
  The two vocabularies tell about one system.
  The Design must clearly give the mapping between them (which component does which activity).

  If it does not, the reader cannot know the mapping.
  Then the two chapters look as if they tell about two different systems.
  For each stage of the Dataflow, there must be a component that does it.
  That component is in the Interfaces of chapter 2 when an external system calls it, or in this chapter.
  If a stage has no component, no person made the code for that activity.

# 4. Coding — "How should the code be written?"

This chapter gives the development guidelines and the best procedures for the code.
These keep the quality of the code high, and let the code operate on different platforms.

- **Key Development Guidelines**:
  - **Config-driven**: Make the logic at run time from the configuration files.
  - **Path injection**: Do not write a path in the code.
    Give each path to the code at run time.
  - **AI-First**: Write each description field for an AI.
    The AI must get the necessary information from the field, and use it to send work.
  - **No default for an input**: Read each value from an input without a default value.
    If the input does not contain a value, the rules get it as a missing value, not as a number.
    A default is an approximate value in the code that looks correct.
    The Derivation Rules do not let you use such a value.
    Also, a default does not tell you that the code used it.
- **Implementation Guidelines and Tools**: The libraries that you must use (for example, pathlib, arrow), and the programming style (for example, type hints).
- **Safety and Robustness**: The file-locking mechanism for tasks that operate at the same time, and the logic that examines the I/O contract.
- **Platform Traps**: The conditions that **gave** an incorrect result that looked correct, with no error.
  Record only the conditions that occurred.
  Do not record the conditions that can possibly occur.
  Possible conditions have no limit, and the conditions that occurred become hard to find in them.
- **Verification Obligations**: A list of items.
  For each item, give "what is claimed to work" and "how it is proven to work".
  A component is satisfactory only after a person or a test **shows** how it operates.
  It is not satisfactory when a person only thinks that it operates correctly.
  - The list contains each rule of chapter 2.
    If you cannot do a verification of a rule, that rule has the same effect as a rule that no person wrote.
  - The list gives each component of chapter 3 one or more times.
    If no row gives proof for a component, you cannot show that the component operates correctly.
  - If an item has no proof at this time, keep it in the list.
    Identify it as **"not verified"**, and give the information that you found for it until this time.
  - At the end of this topic, tell how to make the proof of each "not verified" item automatic.

  If an item is not in the list, each subsequent reader thinks that it has proof.
  If an item has the mark "not verified", all readers can see that it has no proof, and supply the proof.
- **Defects**: Each location where the code does not obey a rule of chapter 2.
  For each defect, give the location where you saw it, and its cost.
  The rules stay in chapter 2.
  This topic records only where the code does not obey them.

  This prevents a change to the Specification that shows a defect as if it is the rule.
  A subsequent reader can close a defect that this topic records.
  If this topic does not record a defect, a subsequent reader must find it again.

# Versioning

The file name of RSDC-Standard.md does not contain a date.
Only a change to a rule makes a new version.
When you change a rule in RSDC-Standard.md, do only these steps:

1. Change the version on the Version line at the top of RSDC-Standard.md.
2. At the top of "Changes in This Version" at the end, add a subsection for the new version.
3. Do not change the file name.

Thus, it is not necessary to change the documents that refer to RSDC-Standard.md.

When you change only the words or the layout of RSDC-Standard.md, do not change the version.
Tell about the change in the subsection of that version.

# Changes in This Version

## 261016

The topic Terms of chapter 2 has a new name: Terminology.
A SKILL.md gives the nouns of a skill in the section TERMINOLOGY, thus the two types of document now use one name for their nouns.
The tools that find this topic by its name changed with it: `check_rsdc.py` of `gen-rsdc-skill`, and the `chinese` skill.
The rules of this topic did not change.

## 261010

We wrote the text of RSDC-Standard.md again in STE.
No rule for an RSDC changed, thus the version did not change.
We changed only the rule about the version of this standard: now only a change to a rule for an RSDC makes a new version.

On 2026-10-13, the STE text of DFD.md replaced its previous text, after we examined it three times.
DFD.md does not name RSDC, a README or a version now.
Its data types are now in the section Types of Data, and its example uses the name Catalog.

On 2026-10-12, we removed the line about the 繁體中文 twin from RSDC-Standard.md and from DFD.md.
No rule changed, thus the version did not change.

We wrote a template for the system of a skill.
This template showed rules that all RSDCs must have, but the standard did not give them.
The template for an app and the template for the skill system each wrote some of these rules independently.
Thus, we found these rules.

We then made the template of the skill system agree with the standard.
During this work, we found two rules of the standard that it was necessary to change.
One rule let the Design into the Specification.
The other rule made the Dataflow tell again the information that its diagram shows.
We also changed the file name of the standard to the name that the documents that refer to it use.
In this version, the diagram of the Dataflow has the name of its diagram type.

- **The goals table.**
  The rule "Every system goal must have a matching rule in chapter 2" did not tell where to write the relation.
  You cannot examine a relation that no person wrote.
  The two templates put a table at the end of the Invariants, one row for each goal.
  Each row gives the rules that keep the goal.
  In this version, this table is a part of the Invariants, and chapter 1 refers to it.
- **Code labels and precision.**
  The topic Naming and Data Structures gave the rules for names.
  It did not give the rules for the values that a program writes and a reader compares.
  A code label can have two spellings, or a number can have two types of rounding.
  Then the writer and the reader do not agree, and no error shows.

  In this version, each field that holds code labels gives its code labels.
  Each number tells its precision.
  The name is "code label", not "label".
  The cause is that "label wording" in the Presentation Contract is the text on a control, and that is a different item.
- **A topic before the Dataflow tells about its names.**
  The Dataflow gave the names of stages and records.
  But no rule told where its other names come from.
  The Dataflow of the system of a skill used "request" before a section told about it.
  In this version, Terms or Artifact Types tell about each name that the diagram uses, before the Dataflow.
- **Terms come first.**
  Some nouns that an RSDC uses are not the names of data (for example, the caller, or the directory that a run writes into).
  These nouns had no topic.
  The two templates put them at the end of Artifact Types, with the types of data.

  In this version, they have a topic, which is the first topic of chapter 2.
  Thus, all subsequent topics (also Artifact Types) use them after this topic tells about them.
  A term is not the name of data, because the chapter gives the data after the terms.
- **The Execution Flow comes after the components.**
  Directory Structure was between Core Component Responsibilities and Execution Flow.
  But the Execution Flow uses the same components, one after the other.
  The system of a skill has no Directory Structure.
  Thus, its Execution Flow had a number that was one less than in an app.

  In this version, Execution Flow comes immediately after the components, and Directory Structure comes after Execution Flow.
  Thus, a section that the two types of system have has the same number in the two types.
- **We removed Task Generation Logic.**
  In this topic, the RSDC told how a tool (for example, dodo.py) makes tasks that run from the logic.
  Only a system that a task runner controls has such a tool.
  Also, the Execution Flow tells the writer to give the network of tasks that a system makes.

  No RSDC had this topic.
  The template of the skill system had to tell the cause that it did not have this topic.
  In this version, a system with a task runner gives its tasks in Execution Flow.
  It gives the tool in Implementation Guidelines and Tools.
- **A line is a movement at run time.**
  We made the Dataflow of a skill.
  Then we did not know if a line must show it when one document refers to a different document.
  In this version, DFD.md tells that the diagram does not show it.
  A line is data that moves while the flow operates.
- **An item that has no proof stays in the table.**
  Verification Obligations told the writer to record the operation that a person saw.
  It did not tell about the items that no person saw at that time.
  If the table did not include these items, readers thought that they had proof.
  In this version, these items stay in the table with the mark "not verified".
  For each item, the table tells how to make its proof automatic.
- **No default for an input.**
  The Derivation Rules do not let you use an approximate value that looks correct.
  A default in the code is such a value, and it does not tell you that the code used it.
  In this version, the Key Development Guidelines do not let you use a default.
- **The interface is the only access.**
  Interfaces gave the API or CLI that a caller calls.
  It did not tell that the caller must not call other parts.
  If an AI agent or a skill imports the modules of a component, a change to the inner parts of that component can break it.
  In this version, an external system gets access to a component only through its API or CLI.
- **The Design shows the inner part of a stage.**
  Version 261008 kept the inner part of a stage in the Dataflow if that inner part was a rule.
  The cause was that a skill can refer only to chapters 1 and 2.
  But the diagram shows all parts of the stage.
  Most of these parts show how a component does its work, and they are not rules.
  Also, a sequence in a stage is frequently one procedure that obeys a rule, not the rule.

  An example is "the verdict is fixed before the trailing stop is reconstructed".
  This sequence obeys the rule "no verdict reads the trailing stop", but the diagram does not show that rule.
  In this version, chapter 2 gives the rule in words, and a skill can refer to it there.
  If a diagram shows the inner part of a stage, the diagram is in the Execution Flow.
- **The diagram tells only one time who reads and writes the data.**
  The Stage Read/Write Table and the table of Data Read/Write Rules gave the information that the DFD shows again.
  They told the data that each stage reads and writes.
  They also told who writes and reads each data item, and its type.
  A second copy becomes different from the diagram, and no person sees the difference.

  No skill referred to these tables.
  A skill refers to the information that a diagram cannot show.
  We removed the two tables, and in this version, only the DFD gives this information.
  Data Read/Write Rules keeps only the information that the diagram cannot show.
  The topics Order Imposed by the Data and Exception Paths did not change.
- **The file has a new name.**
  The new name of `RSDC-Responsibilities.md` is `RSDC-Standard.md`.
  The new name of its twin `RSDC-Responsibilities-tw.md` is `RSDC-Standard-tw.md`.
  The documents that refer to RSDC-Standard.md called it the RSDC standard before this change.
  The previous name gave only one part of the content (the work that each of the four chapters must do).
  Also, each document that referred to it wrote that long name again.

  No rule changed.
  This change is the only change that does not obey the rule above that the file name stays the same.
  All documents in use that referred to the file changed together with the file.
  The previous name stays only in the text of previous versions, for example 261008 below.
- **The name of the diagram is DFD.**
  The name of the first part of the Dataflow was Flowchart, because of the mermaid syntax that makes it.
  But a flowchart shows the step that the system does next.
  This diagram shows where the data goes.

  Some RSDCs are about flowcharts, for example the RSDC of a mermaid viewer.
  In such an RSDC, the reader did not know which diagram the name referred to.
  In this version, the name of this part is DFD, the same name that DFD.md uses.
- **A record that steps change in turn does not have a second writer.**
  DFD.md told that each record with more than one writer is a defect.
  Thus, it identified a check-and-correct loop as a defect.
  An example is a skill with steps that write a document, examine it, and then check and correct it.
  These steps all write the same document.

  The defect is a risk: one process runs again and erases the result of a different process.
  But this does not occur when each subsequent writer reads the data that it changes.
  In this version, DFD.md tells that this condition is not a defect.
  The name of this condition is "a record edited in turn".
  The diagram shows it with an arrow that has two heads.

  This condition has one cost.
  When the first writer runs again, all the subsequent steps must run again.
  The flow must tell how to control this.

  A step before the first writer can read such a record.
  That step reads the record in the condition that it finds it.
  Thus, that step does not read data that a subsequent step writes.

## 261009

An AI agent or a skill calls the components of a system through their APIs and CLIs.
Thus, the name of a component and its interface are contracts.
The standard did not let the Specification give the name of a component.
Thus, the standard had no location for these contracts.
But two documents put them in chapter 2: the rules for the RSDC of a skill system, and the template for an app.

- **Chapter 2 gives the names of the components that external systems call.**
  Its new topic, Interfaces, sets the API or CLI of each such component.
  If these items stay in the Design, a refactor can change a name or an argument.
  Then each caller stops correct operation, and no error shows.
  In this version, the One-way Dependency rule tells the item that the Specification must not give: the inner parts of a component.
- **Chapter 3 divides the components into their parts.**
  The topic Core Component Responsibilities divides the components of chapter 2 into their modules.
  It also gives the components that no external system calls.
  The topic Presentation Form keeps only the controls that a person uses, because chapter 2 gives the API or CLI.
  To find the component of a stage, look in Interfaces when an external system calls it.
- **Defects have a location, and the verification includes all components.**
  Chapter 4 has a new topic, Defects.
  It gives each location where the code does not obey chapter 2, with where you saw it and its cost.
  Thus, no person writes a defect in the Specification as if it is the rule.
  The rules for the RSDC of a skill system and the template for an app kept such a list before this version.

  In this version, Verification Obligations tells the writer to include each component of chapter 3 one or more times.
  It also tells the writer to include each rule of chapter 2.
  If the list includes only the rules, a component can stay without proof.
- **Each component has one type of work and a boundary.**
  The topic Core Component Responsibilities told the writer to give only the scope of each component and how the components operate together.
  Thus, one component could do two types of work, and no person saw it.

  In this version, it tells the writer to give one type of work for each component.
  For each component, it also tells the writer to give its boundary, and the items that a change across it can break.
  The template for an app did this before this version.
  Thus, you see that a change to two types of work is a change to two components.

## 261008

We wrote the standard again in English, and then we read it line by line.
We found words that let a reader think that one rule is a different rule.
We also found one rule with words that applied to less than its cause.

- **One standard in English and in 繁體中文.**
  In this version, the standard is in English, and its 繁體中文 twin is `RSDC-Responsibilities-tw.md`.
  The twin keeps the headings, the topic names and the terms of the Dataflow in English.
  Thus, the two files use the same words as each RSDC and its twin.
  The Chinese version used Chinese words for these terms.
  Thus, before each check, it was necessary for a reader to change 階段 back to stage.
- **The standard tells which part is a chapter and which part is a section.**
  The word "章節" was the name of the two parts.
  Thus, a reader could think that a rule about one is a rule about the other.
  In this version, a chapter is one of the four permanent parts (Requirements, Specification, Design, Coding), with the numbers 1 to 4.
  A section is a part of a chapter, with a number N.M.
- **We made the two One-way rules different.**
  The heading of the chapter rule used the word "cite".
  Thus, it looked as if it was No Forward Reference for chapters.
  But its sub-rules tell that a chapter must not give the content of a subsequent chapter.

  In this version, the heading is "An earlier chapter may not mention a later chapter's content".
  A Specification that gives the name of a component does not obey this rule, but it does not refer to a different part.
  The text "see 2.5" in 2.3 does not obey No Forward Reference, but it stays in its chapter.
- **No Forward Reference includes chapters.**
  The rule told only "section".
  Thus, the text "see chapter 3" obeyed the words of the rule.
  But the reader then could not read that section without the other section.
- **The limit of the Specification is in chapter 2.**
  The rule "May govern what, never what it looks like" was with the rules for all chapters.
  But it applies only to chapter 2.

  In this version, it is at the start of chapter 2, as the limit of chapter 1 is at the start of chapter 1.
  The Presentation Contract and chapter 3 refer to it there.
  They do not write it again.
- **The words of "Every rule says what breaks when it is broken" are clear.**
  The phrases "an example that complies" and "a named failure" were not clear.
  Before a reader could use them, the reader had to get more information about them.
  In this version, one example goes from the rule to the test that it gives.
- **A different document tells about the diagram.**
  The Dataflow of chapter 2, the Execution Flow of chapter 3 and the Dataflow of a skill use the same type of diagram.
  Thus, in this version, [DFD.md](DFD.md) gives the types of data, the shapes and the lines of each such diagram.
  It also gives the two defects to look for.
  DFD.md is a part of this standard, and it has the same version.

  The necessary content of a Dataflow stays in chapter 2.
  Chapter 3 tells the items that an Execution Flow can add.
  We did not give the document the name of one of its users.
  With such a name, the other user must refer to a Dataflow that it is not.

  In this version, one rule is wider.
  Data that a role external to the system supplies has a source.
  Thus, in this version, a request from the caller is not data that no process makes.
  The document has one example in mermaid.
  The legend of the example gives the names of the parts of that example.
- **The topic Hierarchy tells when it applies, and where it stops.**
  A reader read Hierarchy together with Dataflow.
  Then Hierarchy looked as if it was a part that Dataflow includes.
  But it is not.
  The Hierarchy tells which units the users put together to make the system, and which unit contains which unit.
  Dataflow tells how data moves between the activities of the system.

  A Lambda is not a stage.
  It is data that the stage that runs the Lambda reads.
  A rule, for example "a Flow contains only Lambdas", has no location in the parts of a Dataflow.
  But this check showed that the topic came from one example.
  The skill RSDCs and the app template do not have it.

  Thus, in this version, the topic tells that you write it only when the users make the system from units in levels.
  It also tells that the layers in the architecture go in the Design.
  Dataflow gives the limit between Hierarchy and Dataflow.

  The topic Config Schemas told about "each layer's config.yaml".
  In this version, Config Schemas does not think that the system has layers.
  It includes each configuration file that the system reads.
  It has one schema for each level only when there is a Hierarchy.
- **The new name of Artifact Types and Flow is Artifact Types.**
  The limit between this topic and Dataflow gave this topic the type of the data.
  It gave Dataflow where the data goes.
  But the name of this topic included the flow.
  The Data Read/Write Rules of the Dataflow tell who writes and who reads each type of data.

  Thus, this topic keeps the information, the purpose and the content limits of each type.
  It also gets the name that the skill RSDCs use.
  Some RSDCs that we wrote before this version have a section with the name Artifact Types and Flow.
  Change the name of that section when you next make the RSDC agree with the standard.
- **The Dataflow shows the inner part of a stage only if that part is a rule.**
  The words "Where needed" let the reader select.
  Thus, the procedure of a component can go into the Specification.
  In this version, chapter 2 shows the inner part of a stage only in one condition.
  A sequence in the stage, or data that moves between its parts, must be necessary for a verification.

  All other inner parts go in the Execution Flow.
  These conditions stay in chapter 2, because a skill can refer only to chapters 1 and 2 of an RSDC.
  Also, skills refer at this time to stages that show their inner parts.
- **The third type of data has a name: one-run data.**
  The words "data of one run" divided the term.
  The 繁體中文 version divided it between English and Chinese words.
  In this version, it is one noun, as record and external input are.
  A Kind column holds it with the same words.
- **The three types of data do not overlap, and the new name of "input from outside" is external input.**
  A request from the caller came from a source that is external to the system, and no process wrote it.
  Thus, it was "input from outside", and it was also one-run data.
  In this version, each type has its line:
  - A process writes a record, and the system keeps it.
  - An external input comes from a source that is external to the system, and it stays after each run.
  - One-run data stays only during one run, from all sources.

  The new name is one noun, as the other two names are.
- **One-run data has a different shape.**
  One-run data and external inputs had the same shape, the parallelogram.
  Thus, a diagram could not show the difference between two types of data.
  One type stays external to the system, and the other type stays only during one run.
  In this version, each type of data has a different shape.
  In mermaid, the shape of one-run data is the flag.
- **A unit of work in a DFD is a process.**
  The word "step" is the name of a step in the Workflow of a skill.
  The Dataflow of a skill shows these steps.
  Thus, the general term is the DFD word "process".
  A process in a DFD is not a process of the operating system.

  Each flow uses a different name for its processes.
  In the Dataflow of an RSDC, they are stages.
  In an Execution Flow and in the Dataflow of a skill, they are steps.

We applied the wider No Forward Reference rule to the RSDCs that we wrote before.
It found one error.
A template referred to chapter 2 from its section 1.4.
Each RSDC that we wrote from that template also referred to chapter 2 from its section 1.4.
The RSDCs that we wrote without that template did not.
In this version, the template refers back to 1.4 from 2.9.

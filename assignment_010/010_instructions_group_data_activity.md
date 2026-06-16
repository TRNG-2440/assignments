# Data Exploration & Presentation — Group Activity

## Overview

In this group activity, your team will select a real-world dataset from [Kaggle](https://www.kaggle.com/datasets) (or another online tool which can provide datasets in a csv or json format), clean and process the data using **pandas**, produce visualizations using **matplotlib**, and present your findings to the group in a 10–15 minute presentation with a companion slide deck. It is recommended to create the presentation slides using Microsoft Powerpoint, or Google Slides (preferred).

The goal of this activity is not just technical — it is also about making decisions together as a team. Your group will choose what data interests you, decide what questions are worth asking of it, and determine how best to communicate what you found. No two groups should produce the same outcome.

Deadline: Presentations will be tomorrow after lunch.

---

## Team Roles

Before beginning any technical work, your group must designate a **Team Leader**. This person is responsible for:

- Presenting the selected dataset to the rest of the class before work begins (see Dataset Selection below)
- Keeping the group on track during the activity
- Leading or coordinating the final presentation

All other team members are expected to contribute meaningfully to both the code and the presentation. This is a collaborative activity — avoid situations where one person writes all the code or one person builds all the slides.

---

## Team Assignments:
### Team 1
- Ariyan Shaikh (onsite)
- Naoto Shimizu (onsite)
- Alex Tran (remote)
- Madhulika Sawant (remote)
- Kyle Drewes (remote)


### Team 2
- Victor Huang (onsite)
- Araf Zaman (onsite)
- Meera Vasishta (remote)
- Owen Peterson (remote)
- Jesus Cerda (remote)


### Team 3
- Suelem Audelo (onsite)
- Mark White (onsite)
- Prachi Trivedi (remote)
- Luke Fields (remote)
- Will Mahnke (remote)


### Team 4
- Alex Dumerve (onsite)
- Evelyn Yohannan (onsite)
- Robert Collins (remote)
- Stephanie Chen (remote)
- Matthew Patterson (remote)
- Isauro Ramos (remote)

---

## Dataset Selection

Each group must select one dataset from [Kaggle](https://www.kaggle.com/datasets) (or another online tool which can provide datasets in a csv or json format).

**The Team Leader must briefly present their chosen dataset to their trainer by the end of the day - before the group begins work.**

When selecting a dataset, consider the following:
- It should be large enough to be interesting but manageable — aim for datasets that have a few thousand to a few hundred thousand rows.
- It should have enough variety in its columns (a mix of numeric and categorical data works well) to support meaningful analysis
- Avoid datasets that are already fully cleaned and pre-processed — part of the value of this activity is encountering and handling messy data

---

## Technical Requirements

Your group will work in Python. The following libraries are required:

- **pandas** — for loading, cleaning, and processing the data
- **matplotlib** — for producing visualizations

You may use additional libraries (such as `numpy`) if your group chooses, but they are not required.

### What your code must do:

1. **Load the dataset** from a local CSV (or other supported format) using pandas
2. **Inspect the raw data** — explore its shape, column types, missing values, and basic statistics before making any changes
3. **Clean the data** — your group decides what cleaning is necessary based on what you find. This might include handling missing values, correcting data types, removing duplicates, renaming columns, or filtering irrelevant rows. Document your decisions.
4. **Process and analyze** — derive at least one new insight from the data. This could be an aggregation, a calculated column, a grouped summary, a sorted ranking, or anything else your group finds meaningful.
5. **Visualize** — produce at least **three distinct visualizations** using matplotlib that support your findings. Each chart should have a title, labelled axes, and a clear reason for existing.

There is no single correct approach — your cleaning and analysis decisions should be driven by the data and the questions your group is asking of it.

---

## Presentation Requirements

Your group will deliver a **10–15 minute presentation** to the class. Every team member must speak during the presentation.

Your presentation must include the following sections:

### 1. Dataset Introduction
- What is the dataset and where does it come from?
- How many rows and columns does it have?
- What does each key column represent?
- Why did your group choose it, and what question(s) were you hoping to answer?

### 2. Raw Data Overview
- What did the data look like before any cleaning?
- What issues did you identify? (Missing values, wrong data types, duplicates, inconsistent formatting, outliers, etc.)
- Show at least one example of a raw data problem you encountered

### 3. Cleaning & Processing Walkthrough
- What steps did your group take to clean the data, and why?
- What tools and pandas methods did you use? (e.g. `dropna`, `fillna`, `astype`, `groupby`, `merge`, etc.)
- Were there any decisions that required judgement — for example, choosing to drop rows vs. fill missing values? Walk the class through your reasoning.

### 4. Findings & Visualizations
- What did you discover in the data?
- Present your visualizations and explain what each one shows
- Did the data confirm your initial hypothesis, surprise you, or raise new questions?

### 5. Reflections
- What would you do differently if you had more time?
- What additional data would have been useful?
- What was the hardest part of the activity?
- What did each team member learn?

---


## Tips for Success

- **Explore before you clean.** Use `df.head()`, `df.info()`, `df.describe()`, and `df.isnull().sum()` to understand what you're working with before making any changes.
- **Document as you go.** Use comments or a notebook to explain why you made each cleaning decision — you'll need this for the presentation.
- **Let the data drive the questions.** You may arrive with one question and discover a more interesting one along the way. That's fine — follow it.
- **Keep your visualizations honest.** A chart should communicate something clearly, not just look impressive. Make sure each one has a point.
- **Divide the work, but stay aligned.** Different team members can own different parts, but everyone should understand the full picture before the presentation.
- **Practice your presentation** spend at least 1 hour practicing your presentation - everyone should know what they are meant to speak about, and the team member presenting their slides should transition between slides in time with the presentation.

---

## Requirements Checklist

- [ ] A Team Leader has been designated
- [ ] The Team Leader presented the chosen dataset before work began
- [ ] The dataset was sourced from Kaggle (or equivalent online repo/library)
- [ ] The dataset was loaded using pandas
- [ ] Raw data was inspected before any cleaning was performed
- [ ] At least one cleaning step was applied and can be explained
- [ ] At least one derived insight or aggregation was produced
- [ ] At least three visualizations were created using matplotlib, each with a title and labelled axes
- [ ] Every team member speaks during the presentation
- [ ] A presentation slide deck is created and shared (The slides should be shown in a screen shared during the presentation and a link shared with your trainer)
- [ ] The presentation covers all five required sections
- [ ] The presentation runs between 10 and 15 minutes

# What makes people want a second date?

Exploratory analysis of the Columbia University speed dating experiment (2002-2004), run for
Tinder's marketing team.

Jedha *Full Stack Data Scientist* — **Block 2, Exploratory Data Analysis**.

## The problem

Tinder's marketing team is seeing the number of matches go down and wants to understand **what
makes people interested in each other**. Rather than guess from app telemetry, they fall back on
an experiment where the same people were asked, in writing, what they were looking for — and then
observed deciding, face to face, four minutes at a time.

The value of the dataset is exactly that gap: it records both **what people say they want** and
**what they actually pick**.

## The dataset

`data/Speed+Dating+Data.csv` — 8 378 rows x 195 columns, 551 participants, 21 waves.
`data/Speed+Dating+Data+Key.doc` is the official codebook and the reference for every scale used
below.

Two properties drive the whole analysis:

- **One row is one directed date**, not one couple. Every four-minute date is recorded twice, once
  from each side (8 368 distinct `(iid, pid)` pairs, all of them with their reciprocal row). The
  unit of observation is *"how I rated my partner, and what I decided"*.
- **Waves are not the same size.** Participants met between 5 and 22 partners depending on the
  wave, so `order` (the rank of a date within the evening) does not mean the same thing across
  waves.

Headline rates: participants said yes on **42%** of their dates, and **16.5%** of dates ended in a
mutual match. The gender split is even.

Two columns are too sparse to use: `income` is missing on 48.9% of rows and `expnum` on 78.5%.

## Running it

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Then open `tinder_project.ipynb` and select the `.venv` kernel. The notebook reads only the CSV in
`data/` — there is no API call, no credential and no network access anywhere in this project.

## Layout

```
data/                          the dataset and its codebook
tinder_project.ipynb           the deliverable: cleaning, EDA, the five questions
requirements.txt               pinned dependencies
```

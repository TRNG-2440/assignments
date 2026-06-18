# Medical Insurance Charges — Data Analysis Activity

## Objective

In this activity, you will use **pandas** and **matplotlib** to explore a real-world medical insurance dataset and answer 5 analytical questions. For each question, you are expected to perform the relevant analysis in Python and produce a supporting visualization that justifies your conclusion.

You will practice:

- Loading and inspecting tabular data with pandas
- Grouping, filtering, and aggregating data to surface meaningful patterns
- Producing clear, well-labelled visualizations with matplotlib
- Interpreting and communicating findings in plain language

---

## Setup

You are provided with one file: `insurance.csv`

The dataset contains **1,338 records** of individual medical insurance charges, with the following columns:

| Column | Type | Description |
|---|---|---|
| `age` | Integer | Age of the individual |
| `sex` | String | `male` or `female` |
| `bmi` | Float | Body mass index |
| `children` | Integer | Number of dependent children |
| `smoker` | String | `yes` or `no` |
| `region` | String | US region: `northeast`, `northwest`, `southeast`, `southwest` |
| `charges` | Float | Individual medical costs billed by health insurance |

Load the dataset at the top of your script using pandas. You will need to import the `pandas` and `matplotlib.pyplot` modules.

---

## Instructions

For each of the 5 questions below:

1. Write the Python code to perform the analysis using pandas
2. Produce a matplotlib visualization that supports your finding
3. Write **one sentence** summarizing your answer and conclusion

Work through the questions in order. There is no single correct implementation — focus on whether your analysis and visualization clearly justify the conclusion you draw.

### General requirements for all visualizations:
- Every plot must have a descriptive **title**
- Every axis must be **labelled**
- Each plot must be **saved as a `.png` file** with a descriptive filename (e.g. `q1_charges_by_sex.png`)
- Save every figure to disk with `plt.savefig()`. Always call `plt.savefig()` **before** `plt.show()` — calling `plt.show()` first clears the figure buffer and will produce a blank saved file. In a script context, it is simplest to omit `plt.show()` entirely and rely on the saved `.png` files to review your output.
- Choose the chart type that best communicates the pattern — do not default to a bar chart for every question

---

## The Questions

### Question 1 — Do females or males typically have higher medical costs?

Compare medical charges between males and females. Consider both the mean and median — do they tell the same story? Your visualization should allow a reader to see not just the average difference, but the shape of the distribution for each group.

---

### Question 2 — How much does smoking affect medical charges?

Compare the mean and median charges for smokers vs. non-smokers. Your visualization should make the scale of the difference immediately clear to a reader who has not seen the numbers.

---

### Question 3 — Does having more children correlate with higher medical costs, and does the pattern hold all the way up?

Group patients by number of children and compare mean charges across groups. Does cost increase consistently as the number of children increases? If the pattern breaks down at some point, note this in your writeup and consider whether sample size may be a factor.

---

### Question 4 — Which region has the highest average medical costs, and is the difference meaningful?

Compare mean and median charges across all regions. After identifying the highest-cost region, look more closely at that region's data — does it have a higher proportion of smokers or a different BMI profile compared to others? Your visualization should present the regional comparison clearly, and your writeup sentence should address whether the difference appears meaningful or marginal.

---

### Question 5 — Within non-smokers only, which factors drive the most variation in charges?

Filter the dataset to non-smokers only, then investigate which remaining variables (`age`, `bmi`, `children`, `region`, `sex`) are most associated with variation in charges. You should produce at least **two visualizations** for this question — one examining a continuous variable's relationship with charges, and one examining a categorical variable. Your writeup sentence should identify which factor appears most influential among non-smokers.

> **Note:** Since smoking is by far the dominant driver of charges in the full dataset, removing smokers allows the secondary factors to be seen more clearly.

---

## Deliverables

Submit the following three items:

### 1. Python Script — `analysis.py`
A single, well-commented Python script containing all of your analysis and visualization code for all 5 questions. Code for each question should be clearly separated with a comment indicating which question it addresses.

### 2. visualization Images
One saved `.png` image per question (Question 5 requires at least two), totalling a minimum of **6 images**. Files should be descriptively named so it is clear which question each image supports.

### 3. Written Answers — `answers.txt`
A plain text file containing exactly **5 numbered answers**, one sentence each, directly addressing each question. Each sentence should state a clear conclusion supported by the numbers from your analysis. Do not simply describe the chart — state what it shows.

**Example format:**
```
1. [Your one-sentence answer to Question 1]
2. [Your one-sentence answer to Question 2]
...
```

---

## Requirements Checklist

- [ ] `insurance.csv` is loaded using pandas at the top of `analysis.py`
- [ ] Code for each question is clearly separated and commented in `analysis.py`
- [ ] All plots have a title and labelled axes
- [ ] All plots are saved as `.png` files with descriptive filenames using `plt.savefig()`
- [ ] A minimum of 6 `.png` images are submitted
- [ ] `answers.txt` contains exactly 5 numbered one-sentence answers
- [ ] Each written answer states a conclusion, not just a description of the chart

---

## Stretch Goals

-**Bonus Question** — Does the relationship between BMI and charges only become meaningful at a certain threshold?

Rather than treating BMI as a raw continuous variable, bin it into the standard clinical categories and compare charges across groups. Your analysis should help answer whether charges increase gradually with BMI or whether a specific threshold drives a more pronounced change.

Use the following BMI category boundaries:

| Category | BMI Range |
|---|---|
| Underweight | Below 18.5 |
| Normal | 18.5 – 24.9 |
| Overweight | 25 – 29.9 |
| Obese I | 30 – 34.9 |
| Obese II+ | 35 and above |

> **Hint:** You will need to create a new derived column. Look into `pd.cut()` with custom `bins` and `labels`.

- **Bonus Question Extended** — Layer the smoker/non-smoker distinction on top of the BMI category analysis from the Bonus Question above. Produce a grouped visualization showing average charges for smokers vs. non-smokers within each BMI category. The interaction effect here is one of the most striking patterns in the dataset.
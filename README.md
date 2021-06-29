# MA346 FinalProject: U.S. College Recommender System

by Josephine Kantawiria

### Purpose of Project
Choosing a college is one of the major decisions every student needs to make as it plays a pivotal role in their career and life.
However, choosing an appropriate college can be challenging. The college selection process also require a lot of searching work.
This project will focus on assisting students in choosing their college based on basic variables.
It will provide the user with top 5 U.S. colleges that are deemed most suitable for the student's preference and eligibility, which the user can input.

### About the College Recommender System
Users will be asked to input information such as: preferred location, SAT score, maximum tuition that they would accept, as well as their student status
(if they are international, local out of state, or local in state). As many individuals have different needs and concerns about their college eligibility
and requirements, users are also able to weigh the importance of each of the predictor variables from a scale of 1 to 10.
This college recommender system will then evaluate these different factors and display the top 5 U.S. college recommendations in the most user-friendly design.
The college recommender system will then evaluate all these factors and insert it into the given formula to calculate a compatibility score between 0 to 1,
with 1 being the most compatible.

### Information about the Data
For this project, we will be using two datasets - both in CSV file format. The first dataset can be accessed through the
[U.S. Depatment of Education](https://data.ed.gov/dataset/college-scorecard-all-data-files-through-6-2020/resources) under the College Scorecard project resources.
The College Scorecard provides data files with data about institutions as a whole and data files with data about specific fields of study within institutions.
We will be using the first dataset that provide all data elements. Many data elements within the two data files are drawn directly from, or derived from, data
reported to the Integrated Postsecondary Education Data System (IPEDS). The data also came with a data dictionary, which will be broken down later. Since the
dataset was large, we already went ahead and hand-picked all the columns that are needed for this project.

The second dataset can be accessed from [kaggle.com](https://www.kaggle.com/joeshamen/world-university-rankings-2020). It is a dataset that comprises the
ranking of the best universities of the world made by The Times Higher Education for 2020. It includes almost 1,400 universities across 92 countries, standing
as the largest and most diverse university rankings ever to date. The rankings are determined based on 13 performance indicators that measure an institution’s
performance across teaching, research, knowledge transfer and international outlook. The university ranking also has been independently audited by professional
services firm PricewaterhouseCoopers. This information will be used to determine the rankings of the universities listed in the first dataframe, providing a more
holistic view of the university's performance.  

The packages we will be using for this project are `Pandas`, `NumPy`, `Sklearn`, and `Streamlit`.

### More Information and Resources regarding the Project
To check out the fully functioning Streamlit dashboard, please visit [this link](https://josephinekantawiria.herokuapp.com).
More information can be found [here](https://deepnote.com/@josephine-kantawiria/Final-Project-EXIOubXnQEG7C8pAZc-45g) on my Deepnote project.

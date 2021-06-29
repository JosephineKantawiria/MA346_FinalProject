# Load packages
import pandas as pd
import numpy as np
from sklearn import preprocessing
import streamlit as st

# Load data
df1 = pd.read_csv('Most-Recent-Cohorts-All-Data-Elements.csv')
df2 = pd.read_csv('World_University_Rank_2020.csv')

# Filter rows and columns
df2 = df2.loc[df2["Country"] == "United States"][["Rank_Char", "University"]]

# Replace values
df2["Rank_Char"].replace(
    {
        "201�250": 225,
        "251�300": 275,
        "301�350": 325,
        "351�400": 375,
        "401�500": 425,
        "501�600": 525,
        "601�800": 700,
        "801�1000": 900,
        "1001+": 1001,
    },
    inplace=True,
)

# Convert column type
df2['Rank_Char'] = pd.to_numeric(df2['Rank_Char'])

# Merge DataFrames
df = df1.merge(df2, how='inner', left_on='INSTNM', right_on='University')
del df['University']

# Function for user input
def user_input1():
    # Define student status
    student_status = st.selectbox('Select your student status: ', ['Choose an option', 'International', 'Local In-State', 'Local Out-of-State'])
    
    # Define SAT score
    sat_score = st.number_input('Input your SAT score: ', min_value=0, max_value=1600)

    # Define maximum tuition
    min_value = int(min(df['TUITIONFEE_IN'].min(), df['TUITIONFEE_OUT'].min()))
    max_value = int(max(df['TUITIONFEE_IN'].max(), df['TUITIONFEE_OUT'].max()))
    max_tuition = st.slider('Select the maximum tuition you would accept: ', min_value= min_value, max_value= max_value, value = 10000)

    # Define preffered location - Multiselect widget
    locations = np.append(df['STABBR'].unique(), "All")
    pref_locations = st.multiselect("Select your preferred location(s): ", locations, help="Data will be filtered according to the counties selected. Select \"All\" or none to view data from all counties.")
    
    # If preferred location is All or None
    if ('All' in pref_locations) or (len(pref_locations) == 0):
        pref_locations = df['STABBR'].unique()

    return student_status, sat_score, max_tuition, pref_locations

def user_input2():
    # Define variable importance from 1 to 10
    scale_tuition = st.slider("From a scale of 1 (lowest) to 10 (highest), rate the importance of a low tuition rate in your college search: ", min_value=1, max_value=10, value=5)
    scale_sat = st.slider("From a scale of 1 (lowest) to 10 (highest), rate the importance of an SAT match in your college search: ", min_value=1, max_value=10, value=5)
    scale_admission = st.slider("From a scale of 1 (lowest) to 10 (highest), rate the importance of a high admission rate in your college search: ", min_value=1, max_value=10, value=5)
    scale_rank = st.slider("From a scale of 1 (lowest) to 10 (highest), rate the importance of a high college ranking in your college search: ", min_value=1, max_value=10, value=5)

    return scale_tuition, scale_sat, scale_admission, scale_rank

def decide_tuition_category (student_status):
    tuition_category = ''
    # Tuition based on student status
    if student_status == 'International' or student_status == 'Local Out-of-State':
        tuition_category = 'TUITIONFEE_OUT' # Use out-of-state tuition
    elif student_status == 'Local In-State':
        tuition_category = 'TUITIONFEE_IN' # Use in-state tuition
    
    return tuition_category

def filter_data (sat_score, max_tuition, pref_locations, tuition_category):
    # Filter DataFrame
    mask = (df['STABBR'].isin(pref_locations)) & (df['SAT_AVG'] <= sat_score) & (df[tuition_category] <= max_tuition)
    filtered_df = df.loc[mask]
    
    return filtered_df

# Function to normalize column by min-max scaling
def normalize (column):
    col_array = filtered_df[column].to_numpy()
    min_max_scaler = preprocessing.MinMaxScaler()
    col_scaled = min_max_scaler.fit_transform(col_array.reshape(-1, 1))
    return col_scaled.flatten()

# Function to calculate weight of importance of variables
def calculate_weight(variable):
    return variable / sum([scale_tuition, scale_sat, scale_admission, scale_rank])

# Function to pull top scores
def calculate_scores ():
    
    # Define empty dictionary
    scores = {}

    # Convert DataFrame to list
    university_names = filtered_df['INSTNM'].tolist()
    sat_avgs = normalize('SAT_AVG')
    admissions = filtered_df['ADM_RATE'].tolist()
    tuitions = normalize(tuition_category)
    ranks = normalize('Rank_Char')

    # Calculate weight of each variable
    weight_tuition = calculate_weight(scale_tuition)
    weight_sat = calculate_weight(scale_sat)
    weight_admission = calculate_weight(scale_admission)
    weight_rank = calculate_weight(scale_rank)

    # Calculate scores
    for i in range(len(filtered_df)):
        scores[university_names[i]] = weight_tuition * (1 - tuitions[i]) +  weight_sat * (1 - sat_avgs[i]) + weight_admission * admissions[i] + weight_rank * (1 - ranks[i])

    return scores

def top_scores (scores):
    # Sort universities by top 5 scores
    top5 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Only extract university name into list
    top5 = [name for x in top5 for name in x[::2]]

    return top5

def page_one():
    # Title and name
    st.title('MA346 Summer 2021 - Final Project')
    st.write("by: Josephine Kantawiria - MA346 Summer 2021")

    # Welcome banner image
    st.image('WelcomeBanner.png')

    # Purpose of Project
    st.subheader("Purpose of Project")
    st.markdown(''' Choosing a college is one of the major decisions every student needs to make as
    it plays a pivotal role in their career and life. However, choosing an appropriate college
    can be challenging. The college selection process also require a lot of searching work. This project
    will focus on assisting students in choosing their college based on basic variables. It will provide
    the user with top 5 U.S. colleges that are deemed most suitable for the student's preference and
    eligibility, which the user can input.''')
    st.write()

    # Information about the College Recommender System
    st.subheader("About the College Recommender System")
    st.markdown('''Users will be asked to input information such as: preferred location,
    SAT score, maximum tuition that they would accept, as well as their student status
    (if they are international, local out of state, or local in state). As many individuals
    have different needs and concerns about their college eligibility and requirements, users
    are also able to weigh the importance of each of the predictor variables from a scale of 1 to 10.
    This college recommender system will then evaluate these different factors and display the top 5
    U.S. college recommendations in the most user-friendly design.''')
    st.write()

    # Information about the Data
    st.subheader("Information about the Data")
    st.markdown('''For this project, we will be using two datasets - both in CSV file format.
    The first dataset can be accessed through the [U.S. Depatment of Education]
    (https://data.ed.gov/dataset/college-scorecard-all-data-files-through-6-2020/resources) under
    the College Scorecard project resources. The College Scorecard provides data files with data
    about institutions as a whole and data files with data about specific fields of study within
    institutions. We will be using the first dataset that provide all data elements. Many data
    elements within the two data files are drawn directly from, or derived from, data reported
    to the Integrated Postsecondary Education Data System (IPEDS). The data also came with a data
    dictionary, which will be broken down later.''')
    st.markdown('''The second dataset can be accessed from [kaggle.com]
    (https://www.kaggle.com/joeshamen/world-university-rankings-2020). It is a dataset that comprises
    the ranking of the best universities of the world made by The Times Higher Education for 2020.
    It includes almost 1,400 universities across 92 countries, standing as the largest and most
    diverse university rankings ever to date. The rankings are determined based on 13 performance
    indicators that measure an institution’s performance across teaching, research, knowledge
    transfer and international outlook. The university ranking also has been independently audited
    by professional services firm PricewaterhouseCoopers. This information will be used to determine
    the rankings of the universities listed in the first dataframe, providing a more holistic view
    of the university's performance.''')

    # More Information
    st.subheader("More Information on Project")
    st.markdown('''More information can be found [here](https://github.com/JosephineKantawiria/MA346-FinalProject) on my GitHub repo.''')

def page_two():
    # Title
    st.title('Explore the Data')

    # DataFrame to display
    df_display = df[['INSTNM', 'CITY', 'Rank_Char', 'SAT_AVG', 'ADM_RATE', 'TUITIONFEE_IN', 'TUITIONFEE_OUT']]

    # Rename columns
    df_display.columns = ['College Name', 'City', 'Rank', 'Average SAT Score', 'Admission Rate', 'Tuition Rate (In-State)', 'Tuition Rate (Out-of-State)']

    # DataFrame for map
    df_map = df[['LATITUDE', 'LONGITUDE']]
    df_map.columns = ['lat', 'lon']

    # Display DataFrame
    st.dataframe(df_display.sort_values(by=['Rank']))

    # Display map
    st.map(df_map)

def page_three_a():
   # Title
   st.title('College Recommender System')
   
   # Horizontal line
   st.markdown('''---''')

   # Create first row
   row1 = st.beta_container()

   # Split columns
   col1, buff, col2 = st.beta_columns([10, 1, 10])
   
   # Row 1, Col 1
   with row1:
      with col1:
         # Call first user_input function
         student_status, sat_score, max_tuition, pref_locations = user_input1()

   # Row 1, Col 2
   with row1:
      with col2:
         # Global variable
         global scale_tuition, scale_sat, scale_admission, scale_rank
         # Call second user input function
         scale_tuition, scale_sat, scale_admission, scale_rank = user_input2()
         
         # Do not proceed if information is incomplete
         if student_status != 'Choose an option':
            # Global variable
            global tuition_category
            # Call function to decide tuition category based on student status
            tuition_category = decide_tuition_category(student_status)

            # Global variable
            global filtered_df
            # Call function to filter the data
            filtered_df = filter_data (sat_score, max_tuition, pref_locations, tuition_category)

   # Horizontal line
   st.markdown('''---''')

   # Create second row
   row2 = st.beta_container()

   # Row 2
   with row2:
      # Create button
      if st.button('Next'):
         # If there is no data
         if student_status == 'Choose an option' or len(filtered_df) == 0:
            # Error message
            st.error('Sorry, no university matches for you currently.')
         # If there is data
         else:
            # Activate next page
            page_three_b()

def page_three_b():
    # Call function to calculate scores
    scores = calculate_scores()

    # Call function to pull top 5 college names based on highest scores
    top5 = top_scores(scores)

    # DataFrame to display
    top5_df_display = df.loc[df['INSTNM'].isin(top5),['INSTNM', 'CITY', 'Rank_Char', 'SAT_AVG', 'ADM_RATE', tuition_category]]
    
    # Rename columns
    top5_df_display.columns = ['College Name', 'City', 'Rank', 'Average SAT Score', 'Admission Rate', 'Tuition Rate']
    
    # Reset index to start at 1
    top5_df_display.index = np.arange(1, len(top5_df_display) + 1)

    # DataFrame for map
    top5_df_map = df.loc[df['INSTNM'].isin(top5),['LATITUDE', 'LONGITUDE']]
    top5_df_map.columns = ['lat', 'lon']

    # Display DataFrame
    st.dataframe(top5_df_display)

    # Display Map
    st.map(top5_df_map)

page = st.sidebar.radio('Navigation Bar', ('Main', 'Explore the Data', 'College Recommender System'))

if page == 'Main':
    page_one()
if page == 'Explore the Data':
    page_two()
if page == 'College Recommender System':
    page_three_a()

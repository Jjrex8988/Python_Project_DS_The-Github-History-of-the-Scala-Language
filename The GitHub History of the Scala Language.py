# Title     : The GitHub History of the Scala Language
# Objective : read in, clean up, and visualize the real-world
#             project repository of Scala that spans data from a
#             version control system (Git) as well as a project
#             hosting site (GitHub).
# Created by: Jjrex8988
# Created on: 10/3/2021


## 1. Scala's real-world project repository da
# Importing pandas
import pandas as pd

# Loading in the data
pulls = pd.read_csv("pulls.csv")
pull_files = pd.read_csv("pull_files.csv")

print(pulls.head(10))
print("-"*38)
print(pulls.info())
print("-"*38)


print(pull_files.head(10))
print("-"*38)
print(pull_files.info())
print("-"*38)
#--------------------------------------------------------------------------------#



#--------------------------------------------------------------------------------#
## 2. Cleaning the data

# Convert the date for the pulls object
pulls['date'] = pd.to_datetime(pulls['date'], utc=True)
print(pulls.info())
print("-"*38)
#--------------------------------------------------------------------------------#



#--------------------------------------------------------------------------------#
## 3. Merging the DataFrame

# Merge the two DataFrames
data = pd.merge(left=pulls, right=pull_files, on="pid")
print(data.info())
print("-"*38)
#--------------------------------------------------------------------------------#



#--------------------------------------------------------------------------------#
## 4. Is the project still actively maintaine
import matplotlib.pyplot as plt

# Create a column that will store the month and the year, as a string
pulls['month_year'] = pulls['date'].apply(lambda x: str(x.month) + str(x.year))
print(pulls.info())

counts = pulls.groupby('month_year').count()['pid']

counts.plot(kind='bar', figsize=(12, 4))
plt.show()
print("-"*38)
#--------------------------------------------------------------------------------#



#--------------------------------------------------------------------------------#
## 5. Is there camaraderie in the project?

# Group by the submitter
by_user = pulls.groupby('user').count()['pid']

# Plot the histogram
by_user.plot(kind='hist', bins=5);
plt.show()
print("-"*38)
#--------------------------------------------------------------------------------#



#--------------------------------------------------------------------------------#
## 6. What files were changed in the last ten pull requests?

# Identify the last 10 pull requests
last_10 = pulls.nlargest(10, 'date')

# Join the two data sets
joined_pr = pd.merge(left=last_10, right=pull_files, on='pid')

# Identify the unique files
files = set(joined_pr['file'])

# Print the results
print(files)
print("-"*38)
#--------------------------------------------------------------------------------#



#--------------------------------------------------------------------------------#
## 7. Who made the most pull requests to a given file?
# This is the file we are interested in:
file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

# Identify the commits that changed the file
file_pr = data[data['file'] == file]

# Count the number of changes made by each developer
author_counts = file_pr.groupby('user').count()

# Print the top 3 developers
print(author_counts.nlargest(3, 'pid'))
print("-"*38)
#--------------------------------------------------------------------------------#



#--------------------------------------------------------------------------------#
## 8. Who made the last ten pull requests on a given fil
file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

# Select the pull requests that changed the target file
file_pr = data[data['file'] == file]

# Merge the obtained results with the pulls DataFrame
joined_pr = pd.merge(left=file_pr, right=pulls, on='pid')

# Find the users of the last 10 most recent pull requests
users_last_10 = set(joined_pr.nlargest(10, 'date_x')['user_x'])

# Printing the results
print(users_last_10)
print("-"*38)
#--------------------------------------------------------------------------------#



#--------------------------------------------------------------------------------#
## 9. The pull requests of two special developers
# The developers we are interested in
authors = ['xeno-by', 'soc']

# Get all the developers' pull requests
by_author = pulls[pulls['user'].isin(authors)]

# Count the number of pull requests submitted each year
counts = by_author.groupby([by_author['user'], by_author['date'].dt.year]).agg({'pid':'count'}).reset_index()

# Convert the table to a wide format
counts_wide = counts.pivot_table(index='date', columns='user', values='pid', fill_value=0)

# Plot the results
counts_wide.plot(kind='bar');
plt.show()
print("-"*38)
#--------------------------------------------------------------------------------#



#--------------------------------------------------------------------------------#
## 10. Visualizing the contributions of each developer
authors = ['xeno-by', 'soc']
file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

# Select the pull requests submitted by the authors, from the `data` DataFrame
by_author = data[data['user'].isin(authors)]

# Select the pull requests that affect the file
by_file = by_author[by_author['file'] == file]

# Group and count the number of PRs done by each user each year
grouped = by_file.groupby(['user', by_file['date'].dt.year]).count()['pid'].reset_index()

# Transform the data into a wide format
by_file_wide = grouped.pivot_table(index='date', columns='user', values='pid', fill_value=0)

# Plot the results
by_file_wide.plot(kind='bar')
print("-"*38)
#--------------------------------------------------------------------------------#



#--------------------------------------------------------------------------------#

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
from wordcloud import WordCloud, STOPWORDS

file_path = 'Books_df.csv'
books_df = pd.read_csv(file_path)

#EDA

# Remove the 'Unnamed: 0' column
books_df.drop(columns=['Unnamed: 0'], inplace=True)

# Remove currency symbol from 'Price' and convert to float
books_df['Price'] = books_df['Price'].str.replace('₹', '').str.replace(',', '').astype(float)

# Fill missing values in the 'Author' column with "Unknown"
books_df['Author'].fillna('Unknown', inplace=True)

# Visualization

# Distribution of books across different Main Genres
plt.figure(figsize=(25,6), dpi=75)
books_df['Main Genre'].value_counts().plot(kind='barh')
plt.title('Distribution of Books Across Main Genres')
plt.xlabel('Number of Books')
plt.ylabel('Main Genre')
plt.show()

# Set a minimum threshold for the number of ratings to be considered for 'Best Rated Authors'
min_ratings_threshold = 1000

# Group by 'Author' and calculate mean rating, mean price, and total number of ratings
author_stats = books_df.groupby('Author').agg({
    'Rating':'mean',
    'Price':'mean',
    'No. of People rated':['sum','mean']
}).reset_index()

# Flatten the multi-levelcolumn names
author_stats.columns = ['Author','Avg Rating','Avg Price','Total Ratings','Avg Ratings per Book']

# Identify the most expensive authors
most_expensive_authors = author_stats.sort_values(by='Avg Price', ascending=False).head(10)

# Identify the ost rated authors
most_rated_authors = author_stats.sort_values(by='Total Ratings', ascending=False).head(10)

# Visualization setup
plt.figure(figsize=(18,8),dpi=50)

# Most Expensive Authors
plt.subplot(2,1,1)
sns.barplot(x='Avg Price', y='Author', data=most_expensive_authors,palette='rocket')
plt.title('Top 10 most Expnsive Authors')
plt.xlabel('Average Price (₹)')
plt.ylabel('Author')

# Most Rated Authors
plt.subplot(2,1,2)
sns.barplot(x='Total Ratings',y='Author',data=most_rated_authors,palette='Blues_r')
plt.title('Top 10 Most Rated Authors')
plt.xlabel('Total Ratings')
plt.ylabel('Author')

plt.tight_layout()
plt.show()

# Count the number of books per author
books_per_author = books_df['Author'].value_counts().reset_index()
books_per_author.columns = ['Author', 'Number of Books']

# Take the top 10 most prolific authors for visualization
top_authors = books_per_author.head(10)

# Visualization
plt.figure(figsize=(20, 8), dpi=50)
sns.barplot(x='Number of Books', y='Author', data=top_authors, palette='viridis')
plt.title('Top 10 Most Prolific Authors')
plt.xlabel('Number of Books')
plt.ylabel('Author')
plt.show()

# Combine all book titles into a single string
all_titles = ' '.join(books_df['Title'])

# Combine all genres into a single string
all_genres = ' '.join(books_df['Main Genre'])

# Define additional stopwords to exclude common words that may not add value to the visualization
additional_stopwords = {'Edition', 'Volume', 'Series', 'Book'}

# Update the stopwords set with the additional stopwords
stopwords = set(STOPWORDS).union(additional_stopwords)

# Generate a word cloud for book titles
wordcloud_titles = WordCloud(stopwords=stopwords, background_color='white', width=800, height=400).generate(all_titles)
# Generate a word cloud for genres
wordcloud_genres = WordCloud(stopwords=stopwords, background_color='white', width=800, height=400).generate(all_genres)

# Plotting the word cloud for book titles
plt.figure(figsize=(15, 7), dpi=100)
plt.imshow(wordcloud_titles, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud for Book Titles')
plt.show()

# Plotting the word cloud for genres
plt.figure(figsize=(15, 7), dpi=100)
plt.imshow(wordcloud_genres, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud for Genres')
plt.show()
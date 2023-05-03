## Data description      
    
    
    ├── data
    │ ├── processed <- The final, canonical data sets for modeling.
    │ └── raw <- The original, immutable data dump.

  

 1.  **_When_ was the data obtained?** 05-02-2023

 2.  **_From whom_ or _where_ did you get the data?** Mastodon users and their corresponding twitter handles obtained from [Academics on Mastodon](https://github.com/nathanlesage/academics-on-mastodon).

 3. **What does each column mean? What is the _data format_ of each column?**

 4. **What are the other relevant information, restrictions, and limitations about the dataset? How was the data collected? What kinds of biases does it contain? What should not be done with the dataset (e.g., identification of individuals)?** 
The data set was collected following the steps:
a) I used webscrapping to get the tuple (subject, link to the source list of users on mastodon) available on the repository previously mentioned
b) Mastodon.py is the package providing an additional layer to access the Mastodon API. 
c) Each tuple contains the source for a list of users in a specific subject, essencialy csv files. The list usually is a link to a Google Drive sheet or a repository cloned from a template suggested by the creators of Academics on Mastodon. 
d) In this step, we generate the file ???.
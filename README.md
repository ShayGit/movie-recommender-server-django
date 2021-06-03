**Movies Recommendation Content-Based System:**
- Using "The Movies Dataset".
- Dataset was preprocessed to extract specific features of movies including: cast, crew, keywords, genres and posters.
- Libraries used to preprocess and find recommendations: Pandas, Sklearn, BeautifulSoup, Selenium.
- Resulted in 38487 movies.


Recommendations are Content-Based which means they are based on previous movies the user liked,
taking the most similar movies to the positively rated movies the user has rated, by cosine similarity on the movies features.  
All data files and preprocess code available under 'Content' directory.

**Available Demo here** (sign out from the guest user to sign up a new one): 
[Movies Recommender](http://movies-recommender-react.herokuapp.com/)

**Client-side** built with React and Redux, deployed to heroku.  
Client-side code available here: [Client](https://github.com/ShayGit/movie-recommender-client-react)  
**Server-side** built with Django REST framework, running on AWS EC2 instance with mysql and Django docker containers.

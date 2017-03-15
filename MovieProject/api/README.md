# API Routes

To fully use the API, the user must be logged in because data stored in BD are associated with the user's id. This allows each user to have their own data and to keep them between two connections.

| Request| Route                                    | Description                                                                                      | Permission      |
| :----- | :--------------------------------------- | :----------------------------------------------------------------------------------------------- | :-------------- |
| POST   | /auth/signup                             | Create a user account                                                                            |                 |
| POST   | /auth/login                              | Connect a user                                                                                   |                 |
|        | /auth/logout                             | Disonnect a user                                                                                 | user logged in  | 
| GET    | /api/user                                | Return user information                                                                          | user logged in  |     
| POST   | /api/updateMovies                        | Updates the annotated movies list by the user                                                    | user logged in  |
| GET    | /api/likedMovies/string:opinion          | Recovers in the database, the list of movies that the user liked if opinion = "liked", not liked if opinion = "disliked" or all the films if opinion = "all"                                                                                                                    | user logged in  |
| POST   | /api/likedMovie/int:idMovie/int:isLiked  | Adds into the database the idMovie = idTMDB with isLiked = 0 if the movie wasn't appreciated or isLiked = 1 if the movie was appreciated by user                                                                                                                                | user logged in  |
| PUT    | /api/likedMovie/int:idMovie/int:isLiked  | Updates into the database, the idMovie movie = idTMDB with isLiked = 0 if the movie wasn't appreciated or isLiked = 1 if the movie was appreciated                                                                                                                              | user logged in  |
| DELETE | /api/likedMovie/int:idMovie              | Removes into the database, the idMovie = idTMDB associated with the user                         | user logged in  |
| POST   | /api/train                               | Run model training with annoted movies by user                                                   | user logged in  |
| GET    | /api/prediction                          | Run prediction thank to user model and return a list of movies recommanded                       | user logged in  |
| GET    | /api/predictionFM                        | Run prediction thank to global model and return a list of movies recommanded                     | user logged in  |
| POST   | /api/popularity                          | Run sentiment analysis on Twitter and return popularity ratting and review ratting on each movie | user logged in  |
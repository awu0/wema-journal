# Accomplishments
Detail what you have already completed in your project. What requirements were met in completing these bits?
- Created endpoints (manuscript, text, users) for our API.
- User management backend is done (Create, Read, Update, Delete)
- Hosted webserver on PythonAnywhere (https://wl2612.pythonanywhere.com)
- Hosted MongoDB database on the Cloud using MongoDB Atlas

# Goals and requirements
Set out your goals for this semester. Please detail what the requirement is that each goals will meet, and how you expect to meet it.

## Users
- [ ] Each user can create and delete their own accounts (sign up and login)
- [ ] Editors is like admin
- [ ] Audit log for each user
- [ ] A section to see all users (maybe only admins)

We will code a webpage to do these, exposing the correct endpoints and making sure of the user roles in the backend.


## Manuscripts
- [ ] State management: Manuscripts go through different stages, starting from submission to review, editing, revisions, and accept or reject. 
- [ ] Referee assignments: Editors can assign and remove referees for manuscript reviews. Referee assignments will be validated and update the manuscript state.
- [ ] Database integration: Manuscripts are stored in a structured database with getting, creating, updating, and deleting.

## Text
- [ ] Create and manage texts: Implement CRUD operations like create, update, delete, and read for text entries.
- [ ] Database Integration: Ensure text entries are stored and managed in the database.
- [ ] API Endpoints: Display endpoints for text management, allowing for easy integration with the frontend
- [ ] Error handling: Implement proper error handling for missing fields, duplicates, and other edge cases.

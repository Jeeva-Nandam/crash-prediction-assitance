# To run the backend code 

uvicorn main:app --reload   

# to run the frontend code

npm run dev

# steps to push code in branch -> main

git switch <branch-name>
git add .
git commit -m "commit message"
git push -u origin <branch-name>

# To push to main

git checkout main
git merge <branch-name>

# when the vim editor is opended follow these steps
1. press - Esc
2. type - :wq
3. press - Enter button

# If push fails with “fetch first”:
git pull origin main --rebase
git push origin main

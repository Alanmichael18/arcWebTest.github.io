To Run:

### Setup
# Frontend
1. `cd frontend`
2. `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash `
3. Restart Terminal
4. `nvm install 20`
5. `npm install -g yarn`

# Backend
1. `cd backend`
2. `pip3 install poetry` OR `pipx install poetry`
3. `poetry install`
From now, you can just follow the suggestion below

Open two split terminals
### Frontend
1. `cd frontend`
2. `npm install`
3. `yarn`
4. `yarn dev`

### Backend
1. `cd backend`
2. `poetry install`
3. `poetry run flask --app src.main run -h 0.0.0.0 --port 8000`

### Troubleshooting
- If `yarn dev` doesn't work: 
    - It's most likely an issue with `yarn.lock`, delete that file in the frontend and `yarn install`
- If `poetry run flask --app src.main run -h 0.0.0.0 --port 8000` doesn't work:
    - It's most likely some issue with library dependencies, run `poetry add <LIBRARY>` ex: `poetry add pandas` on imported libraries to make sure they are visible
- If the app runs BUT it says `import <BLAH.JS>...are you missing a file?`:
    - `npm install <BLAH.JS>`
    - delete `yarn.lock`
    - `yarn install`
`PLEASE ADD ANY MORE BUG FIXES IF YOU SEE ANY :O`

### Building App
1. `yarn build`

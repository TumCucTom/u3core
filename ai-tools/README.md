# AI tools used in production
## AI Generated code

### Small, mundane files - TumCucTom:
#### Find code here:
[docker-compose.yml](../code/backend/docker-compose.yml)
#### How this code works
Links the backend server code to the database so that they are hosted together
#### Why AI was used
These are small scripts that are hard to remember all of the details for. AI is helpful for ensuring that the scripts are correct.

## Debugging with AI

### TumCucTom Usage:
- When encountering error messages I struggle to understand (if I can't find a solution on stack overflow or similar), I will typically use chatGPT to:
  - describe the error to me in a more readble way
  - explain what specific parts of the error are and possible solutions
- An example would be where I could not understand why quasar build would run locally but not with github actions on the [deploy.yml](../.github/workflows/deploy.yml)
  - ChatGPT suggested ```npx quasar build``` which worked
 
### justice-123 Usage:
- When encountering error messages i would use chatGPT to quickly explain the solution in a more clear way and give possible solutions.
-An example would be where I could not understand why my openCV was displaying a black screen when working on inferpi.py
ChatGPT suggested that the current version of raspberry Pi was not compatible with openCV and that i had to downgrade.
## Other AI uses

### Make suggestions for design / tech stack choices - TumCucTom

When given a large number of technologies that all seem to solve a given problem it can be hard to know which one to use. I (TumCucTom) use chatGPT to:
- Explain the possible technologies I use and highlight their pros / cons and differences
- Explain the specifics of the problem I am trying to solve to get better reccomendations.
  - An example of this is the reccomendation of a vue, quasar or node app for our [frontend web-app](../code/frontend/web-app) 

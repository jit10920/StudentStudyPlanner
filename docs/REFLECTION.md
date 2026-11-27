# Reflection Essay and Learning Log
CSE 3206 · Jit Banerjee Mithun · ID 2203127

## Reflection essay

For this project I built Student Study Planner, a Flask and SQLite application for courses, tasks, deadlines, progress and an activity log. The sessional techniques were all part of it: an incremental process, three design patterns, test-driven development with mocks, Selenium, continuous integration and a pull-request workflow. For the self-directed part I chose Docker, which we never practised in the sessional.

My technical decision was to containerise the application instead of relying only on a virtual environment. The reason came from my own experience in this project. When I first ran the tests on my Windows machine, pytest failed with a missing-module error because the project folder was not on Python's path. Later, a Selenium test passed in one run and failed in another on the CI server. Both were "it works somewhere else" problems, and both came from the environment. A Dockerfile writes the environment down once. I used a slim Python image, installed the dependencies in their own layer so rebuilds stay fast, ran the application as a normal user, and added a health check. I also made the database path configurable, so the container keeps its data on a volume and does not lose it when it restarts.

To make it real project work and not a demonstration, I added a Docker job to the CI workflow. It builds the image, runs the unit tests inside the container, starts the container and checks that the home page answers, then adds a course, restarts the container and checks that the course is still there. I compared Docker with a plain virtual environment and with a virtual machine. The virtual environment still depends on the host's Python and operating system, and the virtual machine is much heavier, so the container was the best fit. One limit remains: the Selenium tests still run directly on the CI runner, not inside the container.

I met several challenges. The first was the merge conflict between the course and task branches. Resolving it taught me to read both sides before choosing, and to run the tests again afterwards. The second was testing the observer. A real notifier would send messages over a network, so I used mocks to replace the notifier and the database. That showed me why mocks matter: the tests became fast and checked behaviour, not infrastructure. The third was the flaky Selenium test. The log showed that the test opened the next page before the server had answered the form, so the page said there was no activity yet. I fixed it by waiting for the confirmation message before moving on, and after that the CI run was green.

On my learning resources: the official Docker documentation explained the ideas well, but examples taught me more than the reference did. Where I used an AI assistant to help with code and drafting, I had to read and understand each part, because I must be able to explain it in the viva, and the report states this use openly. The assistant gave answers quickly, but I only learned from them when I tried to explain the result in my own words. The tests helped most, because a failing test told me clearly whether I really understood the behaviour.

For my next skill, I plan to learn how to deploy a containerised application to a server, so that other people can use it and not only run it on their own machine. I will start by putting this image into a registry and running it on a small cloud service, then compare that set-up with running it locally.

## Learning log

Fill the "Source" and "Time" columns from what you actually did. Do not copy entries you did not experience.

| Date | Topic | Source used | Time | What I learned / what went wrong |
|------|-------|-------------|------|-----------------------------------|
| | Observer pattern | | | Subject and observers; one failing observer must not stop the others |
| | Mocks (`unittest.mock`) | | | `Mock` vs `MagicMock`; asserting calls instead of results |
| | Dockerfile basics | | | Image layers, caching the dependency step, non-root user |
| | Docker volumes and compose | | | Keeping the SQLite file on a volume so data survives a restart |
| | Selenium selectors | | | Locators must match the rendered HTML (Add buttons had no `type=submit`) |
| | GitHub Actions | | | Separate unit and browser steps; coverage gate |

### Evaluation of resources
- Resource 1: *(name, what helped, what did not, rating)*
- Resource 2:
- AI assistant: *(what it did well, what you had to correct)*

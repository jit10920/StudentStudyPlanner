# Reflection Essay and Learning Log
CSE 3206 · Jit Banerjee Mithun · ID 2203127

## Reflection essay

For this project I built Student Study Planner, a Flask and SQLite application for courses, tasks, deadlines, progress and an activity log. The sessional techniques were all part of it: an incremental process, three design patterns, test-driven development with mocks, Selenium, continuous integration and a pull-request workflow. For the self-directed part I chose OpenAPI with Swagger UI, which we never practised in the sessional.

My technical decision was to document a JSON API with a hand-written OpenAPI specification instead of generating it with a library such as flask-restx. The libraries are quicker, but they put documentation decorators into every route and add a dependency. Writing the specification by hand forced me to learn the format itself: paths, schemas, parameters and response codes. To make it real project work, not a demonstration, I added two tests. One validates the specification against the OpenAPI 3 schema. The other checks that every documented operation has a matching Flask route, so the documentation fails the build if it drifts from the code.

The design patterns followed the same thinking. The factory removes construction logic from the routes, the strategy replaced a growing chain of sorting conditions, and the observer lets task changes trigger logging and notifications without the task code knowing who is listening. For each one I compared an alternative and rejected it, and the reasons are in the report.

I met several challenges. The first was the merge conflict between the course and task branches. Resolving it taught me to read both sides before choosing, and to run the tests again afterwards. The second was testing the observer. A real notifier would send messages over a network, so I used mocks to replace the notifier and the database. That showed me why mocks matter: the tests became fast, and they check behaviour, not infrastructure. The third was Selenium. The tests need a browser whose version matches its driver, and my first selectors did not match the real page because the Add buttons had no submit type. I only found this by checking the selectors against the rendered HTML, which taught me to verify locators against the real page and not against my assumptions.

On my learning resources: the official OpenAPI specification is accurate but dry, and examples were more useful than the reference for getting started. The Swagger UI documentation was easy to follow. Where I used an AI assistant to help with code and drafting, I had to read and understand each part, because I must be able to explain it in the viva, and the report states this use openly. Asking the assistant for an answer was fast but did not teach me anything until I tried to explain the result in my own words. The tests helped most, because a failing test told me clearly whether I really understood the behaviour.

For my next skill, I plan to learn containerisation with Docker, so the application and its tests run the same way on every machine. This project showed me the need: the Selenium problem was an environment mismatch, and CI only hid it by running on a prepared machine. I will containerise this application, run the tests inside the container, and compare the result with my current set-up.

## Learning log

Fill the "Source" and "Time" columns from what you actually did. Do not copy entries you did not experience.

| Date | Topic | Source used | Time | What I learned / what went wrong |
|------|-------|-------------|------|-----------------------------------|
| | Observer pattern | | | Subject and observers; one failing observer must not stop the others |
| | Mocks (`unittest.mock`) | | | `Mock` vs `MagicMock`; asserting calls instead of results |
| | OpenAPI 3 structure | | | Paths, schemas, `$ref`, response codes |
| | Validating the spec | | | `openapi-spec-validator`; contract test between spec and routes |
| | Selenium selectors | | | Locators must match the rendered HTML (Add buttons had no `type=submit`) |
| | GitHub Actions | | | Separate unit and browser steps; coverage gate |

### Evaluation of resources
- Resource 1: *(name, what helped, what did not, rating)*
- Resource 2:
- AI assistant: *(what it did well, what you had to correct)*

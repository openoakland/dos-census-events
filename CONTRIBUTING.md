# Contributing

Welcome! Thank you for considering a contribution to our project. Census Events
is a project of [OpenOakland](https://www.openoakland.org/), part of the Brigade
Network under Code for America.

If you're unsure about anything, just ask -- or submit the issue or pull request
anyway. The worst that can happen is you'll be politely asked to change
something. We love all friendly contributions.

We encourage you to read this project's CONTRIBUTING policy (you are here), its
LICENSE, and its [README](./README.md).


## Code of Conduct

OpenOakland is dedicated to providing a respectful, harassment-free community
for everyone. We do not tolerate harassment or bullying of any community member
in any form. By participating, you agree to our full [Code of
Conduct](https://openoakland.org/code-of-conduct/).


## Team leads

- Project Lead [@mikeubell](https://github.com/mikeubell)
- Product Owner [@ashley-renick](https://github.com/ashley-renick) from Alameda County Complete Count Committee


## Pull requests

Please submit a pull request for any commits, large or small. Pull requests are
a great way to get visibility on changes and keep folks up to date. Please keep
your pull requests of a reasonable size as large pull requests can take longer
to review and merge.

For UI changes, please include screenshots to help reviewers.

Once approved, the author may merge the Pull Request.


## "Sprint" rituals

As a volunteer team, we don't have strict sprint rituals. We meet Tuesday nights
at [OpenOakland](https://openoakland.org) and a lot of work gets over the week
as individuals are available. Team members are generally available on
[Slack](https://slack.openoakland.org/) (takes a minute to load) in
`#census-projects`, so don't hesitate to reach out to others outside of
OpenOakland meetings. Our best work gets done when folks are available, not at
the meetings.


### Kanban board

Because we don't really time-box our work in Sprints, we lean more towards
[Kanban](https://www.atlassian.com/agile/kanban) agile methodology. Work is
described as stories and are put into the Backlog. The Backlog is groomed and
prioritized into the Ready queue. Team members pull work from Ready and only
work on one or two things at a time (work-in-progress limits).

We use GitHub milestones to focus a set of work for feature releases and use
[semantic versioning](https://semver.org) when we release.


### Story lifecycle

**Stories** represent tactical increments of individually-valuable work
deliverable by the team within a single iteration... often an isolated change in
functionality aimed at achieving a goal for a particular kind of stakeholder,
whether customer, user, or operator/admin. Stories are tracked on the [Kanban
Board](https://github.com/openoakland/dos-census-events/projects/1)
and progress through these columns.

- New
- Backlog
- Ready
- In progress
- Done


### Definition of "Done"

An agile "Definition of Done" (DoD) captures the team's agreed-upon standards
for how we get work done at a consistent level of quality. Having a DoD ensures
that non-functional requirements (NFRs) don't have to be re-litigated for every
piece of work taken on, cards can be focused on just the relevant details, and
new team members aren't surprised by assumed expectations of their colleagues.

At our sprint reviews, we demo work that has reached the "Done" column and is of
interest to our users or teammates.


#### Column exit criteria

Our DoD is broken up into a set of statements that should be true
for each card before it moves to the next column on the board.

Before advancing a card from one column to the next on the board, it should meet
the "exit criteria" for the current column, which are listed below.


### Columns


#### New

New issues that need to be triaged. If the issue is low priority, we remove it
from the Kanban board (don't worry, it's not lost). Otherwise, it is moved to
the Backlog to be groomed.


##### Exit criteria

- Relevant points from any discussion in the comments is captured in the initial
  post.
- Decision is made to move to the Backlog, remove it from the board, or close it.


#### Backlog

Work that we are planning on doing and will groom and schedule.


##### Exit criteria

- Indicate the intended benefit and who the story is for in the "as a ..., I want
  ..., so that ..." form.
- Acceptance criteria is defined.


#### Ready

Work that we are planning for the current sprint. Work in this column should be
well-defined and ready to begin work.


##### Exit criteria

- No info or assistance is needed from outside the team to start work and likely
  finish it.
- There's capacity available to work on the story (e.g., this column is a buffer
  of shovel-ready work).


#### In progress (WIP limit: 2/person)

Work that is currently in progress.


##### Exit criteria

- Acceptance criteria are demonstrably met.
- Relevant tasks complete, irrelevant checklists removed or captured on a new story.
- Follows documented coding conventions.
- Automated tests have been added and are included in Continuous Integration.
- Pair-programmed or peer-reviewed (e.g., pull-request has been merged).
- Test coverage exists and overall coverage hasn't been reduced.
- User-facing and internal operation docs have been updated.
- Demoable to other people in their own time (e.g., staging environment, published branch).
- Any deployment is repeatable (e.g., at least documented to increase bus factor beyond one) and if possible automated via CI/CD.
- If the deployment is difficult to automate, then a story for making it automated is created at the top of New.


#### Done

Task has been applied to production and is considered done.


##### Exit criteria

- The work is user-visible and announceable at any time.
- GitHub issue is marked Closed.

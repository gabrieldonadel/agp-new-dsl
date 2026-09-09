# Pull requests that need signed commits

Every pull request from this harness was created through the GitHub REST API, and
API-created commits are unsigned — GitHub only signs commits made through the web
UI. So all 287 carry unsigned commits. The question is which repositories
actually enforce it.

Scanned all 287 for a maintainer or bot raising commit signing. **Three, and only
one still needs anything.**

## Needs action (1)

| PR | Usage | State |
|---|---|---|
| [grafana/faro-react-native-sdk#191](https://github.com/grafana/faro-react-native-sdk/pull/191) | 0 | `mergeable_state: blocked` |

Their `signed-commits-info-action` reports:

> 1 of 1 commit between `main` and `fix/agp9-built-in-kotlin` could not be fully
> verified. This repository requires all commits to be signed.

Note the `signed-commits` check itself reports **success** — it is informational.
The block comes from branch protection on `main`, not from a failing check, which
is why a check-based scan does not find it.

### To fix it

With SSH signing already configured locally:

```bash
git clone git@github.com:gabrieldonadel/grafana-faro-react-native-sdk.git
cd grafana-faro-react-native-sdk
git checkout fix/agp9-built-in-kotlin
git remote add upstream https://github.com/grafana/faro-react-native-sdk.git
git fetch upstream
git rebase --exec 'git commit --amend --no-edit -S' upstream/main
git push --force-with-lease
```

The `--exec` matters: a plain rebase replays the existing commit unsigned.

## Already resolved (2)

| PR | What happened |
|---|---|
| [PostHog/posthog-js#4789](https://github.com/PostHog/posthog-js/pull/4789) | Maintainer asked for signed commits, then merged it anyway. |
| [castle/castle-react-native#182](https://github.com/castle/castle-react-native/pull/182) | Maintainer re-created the change as #185 and merged that. Credit preserved, fix landed. |

## Caveat

This list is built from what maintainers and bots have said. A repository can
require signatures through branch protection without anyone commenting, and
`branches/{branch}/protection` returns 403 without admin rights on that
repository. So more may surface as maintainers get to their queues. The signal to
watch for is `mergeable_state: blocked` on a pull request whose checks are all
green.

# [Git Bot](http://git-bot.hive.pt)

Simple bot for the update and sync of multiple Git repos.

Should be able to easily allow use-cases of integration between GiLab and GitHub repositories.

## Configuration

| Name           | Type  | Default | Description                                                      |
| -------------- | ----- | ------- | ---------------------------------------------------------------- |
| **GIT_KEY**    | `str` | `None`  | The secret key to be used by Git Bot clients for authentication. |
| **REPOS_PATH** | `str` | `repos` | The local filesystem path to store the Git repositories.         |

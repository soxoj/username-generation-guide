# OSINT Username generation guide

A definitive guide to generating usernames for OSINT purposes.

## Start

Let's find out your goals.

If I understand correctly, **you have some information about people**, and you want to **get a list of usernames** (nicknames), that's may be used to search for those people.

Am I right? So, you're in right place.

Below you can read the information on how to get clues for a new search, starting from the data you know, as well as how to automate this and what tools to use.

### What do you have?

If you only have some information as a first name, a last name, a birthday (and, maybe some extra info), you should take a look at the section [“Combining primary info"](#combining-primary-info).

Do you need extra help to extend the number of likely usernames? For learning methods to get variants of first names and so on, check section [“Primary info mining”](#primary-info-mining).

If you have a username and want to guess similar usernames, jump to the [“Username permutations”](#username-permutations) section.

## Combining primary info

- Very useful interactive [Google spreadsheet](https://docs.google.com/spreadsheets/d/17URMtNmXfEZEW9oUL_taLpGaqTDcMkA79J8TRw4xnz8/edit#gid=0) for email permutations.

- Script [python-email-permutator](https://github.com/Satys/python-email-permutator) based on previous tool

- Alias generator mode of [OSRFramebork](https://github.com/i3visio/osrframework)

- Script based on ProtOSINT combination methods:

```sh
$ python3 generate_by_real_info.py
```

- [Logins generator](https://github.com/c0rv4x/logins-generator) supporting first, last and middle names.

## Primary info mining

- [BehindTheName](https://www.behindthename.com/name/john)

- [WeRelate](https://www.werelate.org/wiki/Special:Names). Also see [GitHub repo](https://github.com/tfmorris/Names) with project data.


## Username transformations

When you sign up on the site it may turn out that your username is taken. Then you use a variant of name - with characters replacement or additions.

Thus, making assumptions about the transformations and knowing the original name, you can check "neighboring" accounts.

I propose for this my own simple tool that allows you to make transformations by rules.

```sh
$ python3 transform_username.py --username soxoj rules/printable-leetspeak.rule
soxoj
s0xoj
5ox0j
50xoj
...
```

Rules for transformation are located in the directory `rules` and consist of the following:

- `printable-leetspeak.rule` - common leetspeak transformations such as `e => 3`, `a => 4`, etc.
- `printable-leetspeak-two-ways.rule` - the same conversions from letters to numbers, but also vice versa
- `impersonation.rule` - common mutations used by scammers-impersonators such as `l => I`, `O => 0`, etc.
- `additions.rule` - common additions to the username: underscores and numbers
- `toggle-letter-case.rule` - changing case of letters, what is needed not so often, but may be useful

You can use a file with a list of usernames:

```sh
$ cat usernames.txt
john
jack

$ python3 transform_username.py rules/impersonation.rule --username-list soxoj
jack
iack
john
iohn
```

And even use a pipe to use the output of other tools and itself, combining transformations:
```sh
$ python3 transform_username.py rules/printable-leetspeak.rule --username soxoj | python3 transform_username.py rules/impersonation.rule  --username-input
s0xOj
sOx0j
5OxOi
soxOj
sox0i
...
```

## Other

- [Good random names generator](https://github.com/epidemics-scepticism/NickGenerator)

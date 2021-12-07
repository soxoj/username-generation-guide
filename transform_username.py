#!/usr/bin/env python3
import argparse
import os
import re


class Rule:
    def __str__(self):
        return f'{self.action}: {self.arg1}, {self.arg2}'


def load_rules(filename):
    lines = open(filename).read().splitlines()
    for line in lines:
        l = line
        if not l or l.startswith('#'):
            continue
        data = re.split('( from | to )', l)
        if len(data) != 5:
            print(data)
            print(f'Invalid rule line: {l}')
            continue

        r = Rule()

        r.action = data[0].strip()
        r.arg1 = data[2].strip()
        r.arg2 = data[4].strip()

        yield r


def apply_rule(username, rule):
    results = set({username})
    once_sign = False

    if rule.action == 'replace-any-case':
        start_pos = 0
        while True:
            try:
                index = username.lower().index(rule.arg1.lower(), start_pos)
            except:
                break
            left, right = username[:start_pos], username[start_pos:]
            right = right.lower().replace(rule.arg1.lower(), rule.arg2, 1)
            results.add(left+right)
            start_pos = index + 1

            if index+len(rule.arg1) > len(username):
                break

    elif rule.action == 'replace':
        start_pos = 0
        while True:
            try:
                index = username.index(rule.arg1, start_pos)
            except:
                break
            left, right = username[:start_pos], username[start_pos:]
            right = right.replace(rule.arg1, rule.arg2, 1)
            results.add(left+right)
            start_pos = index + 1

            if index+len(rule.arg1) > len(username):
                break

    elif rule.action == 'change-case':
        for i in range(len(username)):
            new_name = username
            new_name = new_name[:i] + new_name[i].swapcase() + new_name[i+1:]
            results.add(new_name)

    elif rule.action == 'append':
        if rule.arg2 == 'right' and not username.endswith(rule.arg1):
            results.add(username + rule.arg1)
        elif rule.arg2 == 'left' and not username.startswith(rule.arg1):
            results.add(rule.arg1 + username)
        elif rule.arg2 == 'both':
            name = username
            if not username.endswith(rule.arg1):
                name = rule.arg1 + name
            if not username.startswith(rule.arg1):
                name = name + rule.arg1
            results.add(name)

        once_sign = True

    elif rule.action == 'remove-pos':
        pos = int(rule.arg1)
        new_username = username[:pos] + username[pos+1:]
        results.add(new_username)

        once_sign = True

    return results, once_sign



def process_rules_recursive(usernames, rules, results):
    for username in usernames:
        for r in rules:
            res, once_sign = apply_rule(username, r)
            new_res = res.difference(results)

            if once_sign:
                results = results | new_res
                continue

            if not new_res:
                continue

            for result in new_res:
                rec_res = process_rules_recursive(set({result}), rules, results | new_res)
                results = results | rec_res | new_res

    return results


def process_rules(usernames, rules):
    return process_rules_recursive(usernames, rules, usernames)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Username mutation script",
    )
    username_group = parser.add_mutually_exclusive_group(required=True)
    username_group.add_argument(
        '--username',
        help="Username to mutate",
    )
    username_group.add_argument(
        '--username-list',
        help="Filename of username list to mutate",
    )
    username_group.add_argument(
        '-I',
        '--username-input',
        action='store_true',
        default=False,
        help="Get usernames from stdin",
    )
    parser.add_argument(
        'rule_filename',
        type=str,
        help="Rule to mutate (see rules directory)",
    )
    parser.add_argument(
        '--remove-known',
        default=False,
        action='store_true',
        help="Remove known usernames from output",
    )
    args = parser.parse_args()

    if args.username:
        usernames = set({args.username})
    elif args.username_list:
        usernames = set(open(args.username_list).read().splitlines())
    else:
        import sys
        usernames = set()
        for line in sys.stdin:
            usernames.add(line.strip())

    rules = list(load_rules(args.rule_filename))

    new_usernames = process_rules(usernames, rules)

    if args.remove_known:
        usernames = new_usernames.difference(usernames)
    else:
        usernames = new_usernames

    print('\n'.join(usernames))

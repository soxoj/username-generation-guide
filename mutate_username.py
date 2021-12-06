#!/usr/bin/env python3
import argparse
import re


class Rule:
    def __str__(self):
        return f'{self.action}: {self.arg1}, {self.arg2}'


def load_rules(filename):
    lines = open(filename).read().splitlines()
    for line in lines:
        l = line.strip()
        if not l or l.startswith('#'):
            continue
        data = re.split('(from|to)', l)
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

    if rule.action == 'replace':
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

    return results



def process_rules_recursive(usernames, rules, results):
    for username in usernames:
        for r in rules:
            res = apply_rule(username, r)
            new_res = res.difference(results)

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
    parser.add_argument(
        'rule_filename',
        type=str,
        help="Rule to mutate (see rules directory)",
    )
    args = parser.parse_args()

    if args.username:
        usernames = set({args.username})
    else:
        usernames = set(open(args.username_list).read().splitlines())

    rules = list(load_rules(args.rule_filename))

    usernames = process_rules(usernames, rules).difference(usernames)

    print('\n'.join(usernames))

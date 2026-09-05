#!/usr/bin/env python3
# Self-check for the mutation engine: python3 test_transform.py

from transform_username import Rule, load_rules, apply_rule, process_rules


def rule(action, arg1='', arg2=''):
    r = Rule()
    r.action, r.arg1, r.arg2 = action, arg1, arg2
    return r


def test_rules_are_loadable():
    # every shipped rule file must produce rules, including the argless one
    import glob
    for filename in glob.glob('rules/*.rule'):
        assert list(load_rules(filename)), f'no rules loaded from {filename}'


def test_append_to_both_sides():
    assert apply_rule('soxoj', rule('append', '_', 'both'))[0] == {'soxoj', '_soxoj_'}
    # the character is not doubled if it is already there
    assert apply_rule('_soxoj', rule('append', '_', 'both'))[0] == {'_soxoj', '_soxoj_'}


def test_case_toggling_of_long_username():
    # 2 ** 14 variants, used to hit the recursion limit
    results = process_rules({'aleksandrovich'}, [rule('change-case')])
    assert len(results) == 2 ** 14
    assert 'ALEKSANDROVICH' in results


if __name__ == '__main__':
    for name, test in sorted(globals().items()):
        if name.startswith('test_'):
            test()
            print(f'{name}: ok')

from typing import List
from sys import argv

def __create_aliases(name: str, shortName: str = None, longName: str = None, otherAliases: List[str] = None, createShortNameIfAbsent: bool = True, createLongNameIfAbsent: bool = True):
        assert name, 'name cannot be empty'

        aliases = []

        if shortName:
            assert len(
                shortName) == 1, 'Short name must be only 1 character long'
            aliases.append(f'-{shortName}')
        elif createShortNameIfAbsent:
            aliases.append('-' + name[0])

        if longName:
            assert len(
                longName) > 1, 'Long name must be more than 1 character long'
            aliases.append(f'--{longName}')
        elif createLongNameIfAbsent:
            aliases.append('--' + name)

        if otherAliases:
            for alias in otherAliases:
                assert isinstance(
                    alias, str), 'An alias must be of type str'
                if not alias:
                    # ignore empty strings
                    print('SKIPPED AN ALIAS NAME BECAUSE IT WAS EMPTY')
                    continue
                word_length = len(alias)
                if word_length == 1:
                    aliases.append(f'-{alias}')
                elif word_length > 1:
                    aliases.append(f'--{alias}')

        assert aliases, "'createShortNameIfAbsent' and/or 'createLongNameIfAbsent' must be True if no other aliases are provided"

        return aliases

def __main_aliases(__aliases) -> List[str]:
    'First short & long alias'
    al = []
    has_short_alias = False
    has_long_alias = False
    for alias in __aliases:
        if has_short_alias and has_long_alias:
            break
        is_long_name = alias[:2] == '--'
        if is_long_name:
            if has_long_alias: continue
            has_long_alias = True
        else:
            if has_short_alias: continue
            has_short_alias = True
        
        al.append(alias)

    return al

# print(__main_aliases(['--lon', '--aczs', '-d', '--asca']))
print(argv)
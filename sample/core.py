# -*- coding: utf-8 -*-
from typing import List
from enum import Enum
from __future__ import annotations

"""Goto keeps a key-value record of paths you wish to save for quick access later.

Use "goto <key>" to redirect to <key>'s path

Usage: goto <command> [arguments]

Global options:
-h, --help            Print this usage information.
-V, --[no-]version    Output version information and exit

Available commands:
  get      Gets a path address matching the key
  list     List all saved records in a human readable format
  remove   Removes a record matching the key
  rename   Renames a key.
  set      Saves a path with a key.

Run "goto help <command>" for more information about a command."""


class Command():
    def __init__(self, name: str, description: str, usage: str, commands: List[__Parameter], action, additionalUsageInfo, enableHelp=True) -> None:
        """# Command

This class is a declarative style container of command details.

If this doesn't have a parent command then it's the root* of your command-line.

You can add sub-commands to this command in constructor's `commands` parameter.

```python
Command(
    name = 'commandName'
    commands = [
        Command(
            name = 'command1'
        ),
        Command(
            name = 'command2'
        ),
    ]
)
```

In the above example, 'commandName' is the root command (the name of your command-line). 'commandName' is the parent of 'command1' and 'command2'.

## Parameters

#### name: str

Name of this command. This should not be None.

#### description: str

Short description of this command.

#### identifier: str

The identifier of this command. Defaults to `name` if kept None.

#### shortName: str
The short 1 letter name of this command. If None then it is identified by first letter of `name`. Ignored if `commandType` is not CommandType.Option or not CommandType.Flag.

For a command with short name `c`, then will be invoked when argument passed to command-line is like:

    commandName -c

#### commandType

Defaults to CommandType.Option

### Note
- Parameters `shortName` and `longName` is ignored if a command is root."""

        assert name

        self.name = name
        self.identifier = self.name if not identifier else identifier

        self.description = description

        self.commandType = commandType if commandType else CommandType.Option

        # -n
        self.shortName = shortName

        # --name
        self.longName = longName

        self.parent = None

        self.commands = commands

        self.__has_flags = False
        self.__has_subcommands = False
        self.__has_options = False

        self.__param_names = []

        for command in self.commands:
            command.__set_parent(self)
            if command.commandType == CommandType.Parameter:
                self.__param_names.append(command.name)
            elif command.commandType == CommandType.Flag:
                self.__has_flags = True
            else:
                if command.commandType == CommandType.Option:
                    self.__has_options = True
                else:
                    self.__has_subcommands = True

        self.action = action

        self.__generate_usage_instructions(usage, additionalUsageInfo)

        self.__help = self.__generate_help() if enableHelp else ''

    def __set_parent(self, obj):
        self.parent = obj

    @property
    def is_sub_command(self):
        return bool(self.parent)

    @property
    def usage(self):
        return self.__usage

    @property
    def help(self):
        return self.__help

    def __generate_usage_instructions(self, usage, additionalUsageInfo):
        message = 'Usage: '

        if additionalUsageInfo:
            message += additionalUsageInfo
            if usage or self.commands:
                # We need to add a newline if additional usage info was added before this and there needs to be more usage instructions to add.
                message += '\n'

        if usage:
            # If the developer defines usage themselves
            message += usage

        elif not usage and self.commands:
            # If developer didn't wrote usage, and this command has sub commands, parameters, flags or options
            if self.__param_names:
                message += self.name
                for param_name in self.__param_names:
                    message += f' <{param_name}>'

            if self.commands:
                if self.__param_names:
                    message += '\n'

                message += self.name

                if self.__has_flags:
                    message += ' -[flags]'

                if self.__has_subcommands:
                    message += ' <command> [argument]'

        message = message.replace('\n', '\n       ')
        self.__usage = f'{message}'

    def __generate_help(self):
        message = f'{self.description}\n\n{self.usage}\n\n'

        if self.__has_subcommands:
            message += 'Available sub-commands:' if self.is_sub_command else 'Available commands:'


class __Parameter:
    def create(self, name: str, description: str, aliases: List[str], commands: List[__Parameter], action, usage = None, enableHelp=True, valueType=str) -> None:
        self.name = name
        self.description = description
        self.__aliases = name if not aliases else aliases
        self.valueType = valueType

    @property
    def aliases(self) -> List[str]:
        return self.__aliases

    def run(self, arguments: List[str] = None):
        assert isinstance(arguments, List[str]), 'arguments must be a list of strings'
        from sys import argv
        if not arguments:
            from sys import argv
            self.arguments = argv
        else:
            self.arguments = arguments
        
        arg_len = len(self.arguments)
        for i, arg in zip(range(arg_len), self.arguments):
            pass


    @property
    def __main_aliases(self) -> List[str]:
        'First short & long alias'
        al = []
        has_short_alias = False
        has_long_alias = False
        for alias in self.__aliases:
            if has_short_alias and has_long_alias:
                break
            has_prefix = alias[0] == '-'
            is_long_name = False
            if has_prefix:
                is_long_name = alias[:2] == '--'
            else:
                is_long_name = len(alias) > 1
            if is_long_name:
                if has_long_alias:
                    continue
                has_long_alias = True
            else:
                if has_short_alias:
                    continue
                has_short_alias = True

            al.append(alias)

        return al

    @property
    def short_aliases(self) -> List[str]:
        sa = []
        for alias in self.__aliases:
            add = True if len(alias) == 1 else alias[:2] != '--'
            if add:
                sa.append(alias)
        return sa

    @property
    def long_aliases(self) -> List[str]:
        la = []
        for alias in self.__aliases:
            if alias[:2] == '--':
                la.append(alias)
        return la

    @staticmethod
    def __create_aliases(name: str, shortName: str, longName: str, otherAliases: List[str], createShortNameIfAbsent: bool = True, createLongNameIfAbsent: bool = True, addPrefix: bool = True):
        assert name, 'name cannot be empty'

        aliases = []

        if shortName:
            assert len(
                shortName) == 1, 'Short name must be only 1 character long'
            aliases.append(f'-{shortName}' if addPrefix else shortName)
        elif createShortNameIfAbsent:
            aliases.append(f'-{name[0]}' if addPrefix else name[0])

        if longName:
            assert len(
                longName) > 1, 'Long name must be more than 1 character long'
            aliases.append(f'--{longName}' if addPrefix else longName)
        elif createLongNameIfAbsent:
            aliases.append(f'--{name}' if addPrefix else name)

        if otherAliases:
            for alias in otherAliases:
                assert isinstance(
                    alias, str), 'An alias must be of type str'
                if not alias:
                    # ignore empty strings
                    print('SKIPPED AN ALIAS NAME BECAUSE IT WAS EMPTY')
                    continue

                if not addPrefix:
                    aliases.append(alias)
                else:
                    word_length = len(alias)
                    prefix = '-' if word_length == 1 else '--'
                    aliases.append(f'{prefix}{alias}')

        assert aliases, "'createShortNameIfAbsent' and/or 'createLongNameIfAbsent' must be True if no other aliases are provided"
        return list(dict.fromkeys(aliases))


class Flag(__Parameter):
    def __init__(self, name: str, description: str, shortName: str, longName: str, otherAliases: List[str], createShortNameIfAbsent: bool = True, createLongNameIfAbsent: bool = True, defaultValue: bool = False):
        assert name, 'A Flag\'s name cannot be empty'
        assert defaultValue != None, 'Default value of this flag must be either True or False'

        aliases = __Parameter.__create_aliases(
            name, shortName, longName, otherAliases, createShortNameIfAbsent, createLongNameIfAbsent)

        super().create(name=name, description=description,
                         aliases=aliases, defaultValue=defaultValue, valueType=bool)

class Option(__Parameter):
    def __init__(self, name: str, shortName: str = None, longName: str = None, otherAliases: List[str] = None, description: str = None, usage = None, createShortNameIfAbsent: bool = True, createLongNameIfAbsent: bool = True, addPrefix: bool = False, valueType=str) -> None:
        assert isinstance(addPrefix, bool), 'addPrefix should be a bool'
        aliases = __Parameter.__create_aliases(name, shortName, longName, otherAliases,  createShortNameIfAbsent, createLongNameIfAbsent, addPrefix, usage=usage)
        super().create(name=name, description=description, valueType=valueType)

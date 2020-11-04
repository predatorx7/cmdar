from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, overload

class ArgumentContext:
    def __init__(self, enabledFlags: list, values: list, options: Dict[str, list]):
        self.__enabledFlags = enabledFlags
        self.__values = values
        self.__options = options

    def is_flag_enabled(self, flagname: str) -> bool:
        'Was flag with flagname enabled for this action'
        return flagname in self.__enabledFlags

    def value_of(self, optionName: str):
        'Value or first value of an option with optionName'
        _values = self.values_of(optionName)
        if not _values:
            return None
        return _values[0]

    def values_of(self, optionName: str):
        'Values of an option with optionName'
        if not optionName in self.__options.keys:
            return None
        return self.__options[optionName]

    @property
    def value(self):
        'First value from positional arguments OR the first unparsed argument'
        if not self.__values:
            return None
        return self.__values[0]

    @property
    def values(self):
        'Values of positional arguments in order OR unparsed arguments'
        if not self.__values:
            return None
        return self.__values

class Action(metaclass=ABCMeta):
    """An action to be performed when user uses an owner command or option. 
    
    Extend this class and override the `on_usage` param"""
    @abstractmethod
    def on_usage(context: ArgumentContext):
        'This method is invoked when the command/option, this action belongs to, is used.'
        pass

class Parameter(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, n):
        self.n = n

    @abstractmethod
    @property
    def flags(self):
        pass

    @abstractmethod
    @property
    def aliases(self) -> List[str]:
        pass

    @abstractmethod
    @property
    def first_short_alias(self) -> str:
        pass

    @abstractmethod
    @property
    def first_long_alias(self) -> str:
        pass
    
    @abstractmethod
    @property
    def value(self):
        pass

    @abstractmethod
    @property
    def values(self) -> list:
        pass

class Option():
    __values = None
    __name: str = None

    @abstractmethod
    def __init__(self):
        pass
    
    @property
    def name(self) -> str:
        return self.__name

    @property
    def value(self):
        if not self.__values:
            return None
        return self.__values[0]

    @property
    def values(self):
        if not self.__values:
            return None
        return self.__values

class PositionalParameter(Parameter):
    """A positional paramter which must be a value.
    
    There can be only 1 positional parameter for a sub-command or option.
    
    'command <value_of_positional_parameter> [<other_values_for_positional_parameter>]'"""
    def __init__(self, name, description, action: Action):
        self.__name = name
        self.__description = description
        self.__action = action

class NamedParameter(Parameter):
    """A named parameter does have a value.
    
    This can take one or more values.

    'command [-o|--option] &lt;values..&gt;'"""
    def __init__(self, name, description, aliases, createShortNameIfAbsent: bool = True, createLongNameIfAbsent: bool = True):
        pass

class Flags(Parameter):
    def __init_(self, name, description,  aliases, createShortNameIfAbsent: bool = True, createLongNameIfAbsent: bool = True):
        pass

class __Runner:
    def flags_and_options(arguments: List[str]) -> List[str]:
        flags = []
        for i in arguments:
            if i[0] == '-':
                flags.append(i)
            if i[:2] == '--':
                flags.append(i)
        return flags

class Command(Parameter):
    def __init__(self, name, description, usage, flags: List[Flags], parameters: List[Parameter], action: Action):
        pass

    def run(self, arguments: List[str]):
        args = arguments
        arg_len = len(args)

        for i, argument in zip(arg_len, args):
            pass
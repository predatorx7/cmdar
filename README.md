# Cmdar Module 

Cmdar or commandar is a simple command args parser for python. The main class `Command` follows a declarative style. 

## Description of the Command class

If it doesn't have a wrapping parent command then it's the root* of your command-line.

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


### Note
- Parameters `shortName` and `longName` is ignored if a command is root.
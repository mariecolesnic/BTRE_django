from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, Field, MISSING, field
import json
from typing import Optional


def arg_field(*,
              default=MISSING,
              default_factory=MISSING,
              init: bool = True,
              repr: bool = True,
              hash: bool = None,
              compare: bool = True,
              metadata: Optional[dict] = None,
              help: Optional[str] = None) -> Field:
    if metadata is None and help is not None:
        metadata = {}
    if help is not None:
        metadata['help'] = help
    return field(default=default,
                 default_factory=default_factory,
                 init=init,
                 repr=repr,
                 hash=hash,
                 compare=compare,
                 metadata=metadata)


@dataclass
class ArgumentParserClass(Namespace):
    field = arg_field

    def __post_init__(self):
        parser = ArgumentParser()

        for value in self.__dataclass_fields__.values():
            f: Field = value

            kwargs = {}
            help_json = {}

            is_optional_type = False

            if hasattr(f.type, '__args__'):
                help_json['type'] = repr(f.type).replace('typing.', '')
                for arg in f.type.__args__:
                    if arg == bool:
                        kwargs['action'] = 'store_true'
                        continue
                    if hasattr(arg, '__name__'):
                        if arg.__name__ == 'NoneType':
                            is_optional_type = True
                            continue
                    kwargs['type'] = f.type
            elif f.type == bool:
                kwargs['action'] = 'store_true'
                help_json['type'] = f.type.__name__
            else:
                kwargs['type'] = f.type
                help_json['type'] = f.type.__name__

            if f.default == MISSING:
                if is_optional_type:
                    raise TypeError(
                        f"Invalid Optional type annotation provided with no 'None' default.\n f: {f}")
                kwargs['required'] = True
            elif f.default is not None:
                kwargs['default'] = f.default
                try:
                    default_str = repr(f.default)
                    help_json['default'] = default_str
                except:
                    pass

            if f.metadata:
                help_json.update(f.metadata)

            kwargs['help'] = json.dumps(help_json).replace('"', '').replace('{', '').replace('}', '')

            parser.add_argument(f'--{f.name}', **kwargs)
        parser.parse_args()

from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Class(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Berserk: _ClassVar[Class]
    Tank: _ClassVar[Class]
    Paladin: _ClassVar[Class]
    Mage: _ClassVar[Class]
Berserk: Class
Tank: Class
Paladin: Class
Mage: Class

class PlayersList(_message.Message):
    __slots__ = ["player"]
    class Player(_message.Message):
        __slots__ = ["nickname", "email", "date_of_birth", "xp", "cls"]
        NICKNAME_FIELD_NUMBER: _ClassVar[int]
        EMAIL_FIELD_NUMBER: _ClassVar[int]
        DATE_OF_BIRTH_FIELD_NUMBER: _ClassVar[int]
        XP_FIELD_NUMBER: _ClassVar[int]
        CLS_FIELD_NUMBER: _ClassVar[int]
        nickname: str
        email: str
        date_of_birth: str
        xp: int
        cls: Class
        def __init__(self, nickname: _Optional[str] = ..., email: _Optional[str] = ..., date_of_birth: _Optional[str] = ..., xp: _Optional[int] = ..., cls: _Optional[_Union[Class, str]] = ...) -> None: ...
    PLAYER_FIELD_NUMBER: _ClassVar[int]
    player: _containers.RepeatedCompositeFieldContainer[PlayersList.Player]
    def __init__(self, player: _Optional[_Iterable[_Union[PlayersList.Player, _Mapping]]] = ...) -> None: ...

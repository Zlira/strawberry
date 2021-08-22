from enum import Enum
from typing import List, Optional, TypeVar

import strawberry


def test_enum():
    @strawberry.enum
    class Locale(Enum):
        UNITED_STATES = "en_US"
        UK = "en_UK"
        AUSTRALIA = "en_AU"

    @strawberry.mutation
    def set_locale(locale: Locale) -> bool:
        _ = locale
        return True

    argument = set_locale.arguments[0]
    # TODO: Remove reference to ._enum_definition with StrawberryEnum
    assert argument.type is Locale._enum_definition


def test_forward_reference():
    global SearchInput

    @strawberry.field
    def search(search_input: "SearchInput") -> bool:
        _ = search_input
        return True

    @strawberry.input
    class SearchInput:
        query: str

    argument = search.arguments[0]
    assert argument.type is SearchInput

    del SearchInput


def test_list():
    @strawberry.field
    def get_longest_word(words: List[str]) -> str:
        _ = words
        return "I cheated"

    argument = get_longest_word.arguments[0]
    assert argument.type == List[str]


def test_literal():
    @strawberry.field
    def get_name(id_: int) -> str:
        _ = id_
        return "Lord Buckethead"

    argument = get_name.arguments[0]
    assert argument.type == int


def test_object():
    @strawberry.type
    class PersonInput:
        proper_noun: bool

    @strawberry.field
    def get_id(person_input: PersonInput) -> int:
        _ = person_input
        return 0

    argument = get_id.arguments[0]
    assert argument.type is PersonInput


def test_optional():
    @strawberry.field
    def set_age(age: Optional[int]) -> bool:
        _ = age
        return True

    argument = set_age.arguments[0]
    assert argument.type == Optional[int]


def test_type_var():
    T = TypeVar("T")

    @strawberry.field
    def set_value(value: T) -> bool:
        _ = value
        return True

    argument = set_value.arguments[0]
    assert argument.type == T

import enum
import hou
import param_collector.lib.jocl.jocl as jocl
import re
from typing import Callable, Sequence, TypeVar


T = TypeVar("T")
def findIndexItem(seq: Sequence[T], pred: Callable[[T], bool], default: tuple[int, T | None] = (-1, None)) -> tuple[int, T | None]:
    for index, item in enumerate(seq):
        if pred(item):
            return index, item
    return default


def getChildNodes(parentNode: hou.OpNode, recursive: bool) -> list[hou.OpNode]:
    childNodes: list[hou.OpNode] = []

    if recursive:
        childNodes = parentNode.allSubChildren()
    else:
        childNodes = parentNode.children()

    return childNodes


class ParamCollectorError(Exception):
    pass


class ParamTupleTextKind(enum.IntEnum):
    NAME = 0
    LABEL = 1


    @classmethod
    def tryGetFromValue(cls, value: object) -> "ParamTupleTextKind | None":
        try:
            return cls(value)

        except (ValueError, TypeError):
            return None


class ParamTuple(jocl.JsonObjectConvertible):
    def __init__(self):
        self.__text: str = ""
        self.__textKind: ParamTupleTextKind = ParamTupleTextKind.NAME


    def getText(self) -> str:
        return self.__text


    def setText(self, value: str) -> None:
        self.__text = value


    def getTextKind(self) -> ParamTupleTextKind:
        return self.__textKind


    def setTextKind(self, value: ParamTupleTextKind) -> None:
        self.__textKind = value


    @classmethod
    def can_convert_from_json_object(cls, ctx: jocl.JsonContext, obj: jocl.JsonObject) -> bool:
        return True


    def can_convert_to_json_object(self, ctx: jocl.JsonContext) -> bool:
        return True


    @classmethod
    def from_json_object(cls, ctx: jocl.JsonContext, obj: jocl.JsonObject) -> "ParamTuple":
        instance: ParamTuple = cls()
        instance.__text = jocl.get(ctx, obj, "text", str)
        instance.__textKind = jocl.get(ctx, obj, "textKind", ParamTupleTextKind)
        return instance


    def to_json_object(self, ctx: jocl.JsonContext) -> jocl.JsonObject:
        return {
            "text": self.__text,
            "textKind": self.__textKind.value,
        }


    @classmethod
    def create_default(cls) -> "ParamTuple":
        return cls()


class NodeTextKind(enum.IntEnum):
    TYPE = 0
    NAME = 1


    @classmethod
    def tryGetFromValue(cls, value: object) -> "NodeTextKind | None":
        try:
            return cls(value)

        except (ValueError, TypeError):
            return None


class Node(jocl.JsonObjectConvertible):
    def __init__(self):
        self.__text: str = ""
        self.__textKind: NodeTextKind = NodeTextKind.NAME
        self.__paramTuples: list[ParamTuple] = []


    def getText(self) -> str:
        return self.__text


    def setText(self, value: str) -> None:
        self.__text = value


    def getTextKind(self) -> NodeTextKind:
        return self.__textKind


    def setTextKind(self, value: NodeTextKind) -> None:
        self.__textKind = value


    def getParamTuples(self) -> list[ParamTuple]:
        return self.__paramTuples


    def setParamTuples(self, value: list[ParamTuple]) -> None:
        self.__paramTuples = value


    @classmethod
    def can_convert_from_json_object(cls, ctx: jocl.JsonContext, obj: jocl.JsonObject) -> bool:
        return True


    def can_convert_to_json_object(self, ctx: jocl.JsonContext) -> bool:
        return True


    @classmethod
    def from_json_object(cls, ctx: jocl.JsonContext, obj: jocl.JsonObject) -> "Node":
        instance: Node = cls()
        instance.__text = jocl.get(ctx, obj, "text", str)
        instance.__textKind = jocl.get(ctx, obj, "textKind", NodeTextKind)
        instance.__paramTuples = jocl.get(ctx, obj, "paramTuples", jocl.ArrayOf(ParamTuple))
        return instance


    def to_json_object(self, ctx: jocl.JsonContext) -> jocl.JsonObject:
        return {
            "text": self.__text,
            "textKind": self.__textKind.value,
            "paramTuples": jocl.from_convertibles(ctx, "paramTuples", self.__paramTuples),
        }


    @classmethod
    def create_default(cls) -> "Node":
        return cls()


def filterParamTuples(paramTuples: list[hou.ParmTuple], allowList: list[ParamTuple]) -> list[hou.ParmTuple]:
    unfiltered: list[hou.ParmTuple] = []

    for paramTuple in paramTuples:
        append: bool = False

        for allow in allowList:
            if allow.getTextKind() == ParamTupleTextKind.NAME:
                text = paramTuple.name()

            elif allow.getTextKind() == ParamTupleTextKind.LABEL:
                text = paramTuple.parmTemplate().label()

            if re.search(allow.getText(), text):
                append = True
                break

        if append:
            unfiltered.append(paramTuple)

    return unfiltered


def filterNodes(nodes: list[hou.OpNode], allowList: list[Node]) -> list[hou.OpNode]:
    unfiltered: list[hou.OpNode] = []

    for node in nodes:
        append: bool = False

        for allow in allowList:
            if allow.getTextKind() == NodeTextKind.TYPE:
                text = node.type().name()

            elif allow.getTextKind() == NodeTextKind.NAME:
                text = node.name()

            if re.search(allow.getText(), text):
                append = True
                break

        if append:
            unfiltered.append(node)

    return unfiltered


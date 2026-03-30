import param_collector.core.common as common
import param_collector.core.create as create
import param_collector.lib.jocl.jocl as jocl


class Settings(jocl.JsonObjectConvertible):
    def __init__(self):
        self.__candidateRootNodePath: str = ""
        self.__referencedNodePath: str = ""
        self.__recursive: bool = False
        self.__paramTupleReferences: list[create.ParamTupleReference] = []
        self.__nodes: list[common.Node] = []


    def getCandidateRootNodePath(self) -> str:
        return self.__candidateRootNodePath


    def setCandidateRootNodePath(self, value: str) -> None:
        self.__candidateRootNodePath = value


    def getReferencedNodePath(self) -> str:
        return self.__referencedNodePath


    def setReferencedNodePath(self, value: str) -> None:
        self.__referencedNodePath = value


    def getRecursive(self) -> bool:
        return self.__recursive


    def setRecursive(self, value: bool) -> None:
        self.__recursive = value


    def getParamTupleReferences(self) -> list[create.ParamTupleReference]:
        return self.__paramTupleReferences


    def setParamTupleReferences(self, value: list[create.ParamTupleReference]) -> None:
        self.__paramTupleReferences = value


    def getNodes(self) -> list[common.Node]:
        return self.__nodes


    def setNodes(self, value: list[common.Node]) -> None:
        self.__nodes = value


    @classmethod
    def can_convert_from_json_object(cls, ctx: jocl.JsonContext, obj: jocl.JsonObject) -> bool:
        return True


    def can_convert_to_json_object(self, ctx: jocl.JsonContext) -> bool:
        return True


    @classmethod
    def from_json_object(cls, ctx: jocl.JsonContext, obj: jocl.JsonObject) -> "Settings":
        instance: Settings = cls()
        instance.__candidateRootNodePath = jocl.get(ctx, obj, "candidateRootNodePath", str)
        instance.__referencedNodePath = jocl.get(ctx, obj, "referencedNodePath", str)
        instance.__recursive = jocl.get(ctx, obj, "recursive", bool)
        instance.__paramTupleReferences = jocl.get(ctx, obj, "paramTupleReferences", jocl.ArrayOf(create.ParamTupleReference))
        instance.__nodes = jocl.get(ctx, obj, "nodes", jocl.ArrayOf(common.Node))
        return instance


    def to_json_object(self, ctx: jocl.JsonContext) -> jocl.JsonObject:
        return {
            "candidateRootNodePath": self.__candidateRootNodePath,
            "referencedNodePath": self.__referencedNodePath,
            "recursive": self.__recursive,
            "paramTupleReferences": jocl.from_convertibles(ctx, "paramTupleReferences", self.__paramTupleReferences),
            "nodes": jocl.from_convertibles(ctx, "nodes", self.__nodes),
        }


    @classmethod
    def create_default(cls) -> "Settings":
        return cls()

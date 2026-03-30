import hou
import param_collector.core.common as common
import param_collector.lib.jocl.jocl as jocl


class ParamTupleReference(jocl.JsonObjectConvertible):
    def __init__(self):
        self.__referencedParamTuple: common.ParamTuple = common.ParamTuple()
        self.__referringNodes: list[common.Node] = []


    def getReferencedParamTuple(self) -> common.ParamTuple:
        return self.__referencedParamTuple


    def setReferencedParamTuple(self, value: common.ParamTuple) -> None:
        self.__referencedParamTuple = value


    def getReferringNodes(self) -> list[common.Node]:
        return self.__referringNodes


    def setReferringNodes(self, value: list[common.Node]) -> None:
        self.__referringNodes = value


    @classmethod
    def can_convert_from_json_object(cls, ctx: jocl.JsonContext, obj: jocl.JsonObject) -> bool:
        return True


    def can_convert_to_json_object(self, ctx: jocl.JsonContext) -> bool:
        return True


    @classmethod
    def from_json_object(cls, ctx: jocl.JsonContext, obj: jocl.JsonObject) -> "ParamTupleReference":
        instance: ParamTupleReference = cls()
        instance.__referencedParamTuple = jocl.get(ctx, obj, "referencedParamTuple", common.ParamTuple)
        instance.__referringNodes = jocl.get(ctx, obj, "referringNodes", jocl.ArrayOf(common.Node))
        return instance


    def to_json_object(self, ctx: jocl.JsonContext) -> jocl.JsonObject:
        return {
            "referencedParamTuple": jocl.from_convertible(ctx, "referencedParamTuple", self.__referencedParamTuple),
            "referringNodes": jocl.from_convertibles(ctx, "referringNodes", self.__referringNodes),
        }


    @classmethod
    def create_default(cls) -> "ParamTupleReference":
        return cls()


def create(
    candidateRootNodePath: str,
    referencedNodePath: str,
    paramTupleReferences: list[ParamTupleReference],
    *,
    recursive: bool = False
) -> None:
    candidateRootNode: hou.OpNode | None = hou.node(candidateRootNodePath)

    if candidateRootNode is None:
        raise common.ParamCollectorError(f"Source root node not found.\n{candidateRootNodePath}")

    candidateNodes: list[hou.OpNode] = [candidateRootNode]
    candidateNodes.extend(common.getChildNodes(candidateRootNode, recursive))

    referencedNode: hou.OpNode | None = hou.node(referencedNodePath)

    if referencedNode is None:
        raise common.ParamCollectorError(f"Target node not found.\n{referencedNodePath}")

    for paramTupleReference in paramTupleReferences:
        referencedParamTuples: list[hou.ParmTuple] = common.filterParamTuples(referencedNode.parmTuples(), [paramTupleReference.getReferencedParamTuple()])

        for referencedParamTuple in referencedParamTuples:
            for referringNode in paramTupleReference.getReferringNodes():
                referringNodes: list[hou.OpNode] = common.filterNodes(candidateNodes, [referringNode])

                for rn in referringNodes:
                    referringParamTuples: list[hou.ParmTuple] = common.filterParamTuples(rn.parmTuples(), referringNode.getParamTuples())

                    for referringParamTuple in referringParamTuples:
                        referringParams: tuple[hou.Parm, ...] = tuple(referringParamTuple)
                        referencedParams: tuple[hou.Parm, ...] = tuple(referencedParamTuple)

                        if len(referringParams) != len(referencedParams):
                            raise common.ParamCollectorError(
                                "Cannot create parameter references because the selected parameter tuples have different sizes.\n"
                                f"Source: {rn.name()}/{referringParamTuple.name()} ({len(referringParams)})\n"
                                f"Target: {referencedNode.name()}/{referencedParamTuple.name()} ({len(referencedParams)})"
                            )

                        for referringParam, referencedParam in zip(referringParams, referencedParams):
                            if referringParam.getReferencedParm() == referencedParam:
                                continue

                            referringParam.set(referencedParam, language=hou.exprLanguage.Hscript, follow_parm_reference=False)


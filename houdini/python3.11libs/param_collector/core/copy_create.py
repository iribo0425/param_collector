from . import common
import hou


class _ParamTupleReference:
    def __init__(self):
        self.__referring: hou.ParmTuple | None = None
        self.__referenced: hou.ParmTuple | None = None
        self.__referencedName: str = ""


    def getReferring(self) -> hou.ParmTuple | None:
        return self.__referring


    def setReferring(self, value: hou.ParmTuple | None) -> None:
        self.__referring = value


    def getReferenced(self) -> hou.ParmTuple | None:
        return self.__referenced


    def setReferenced(self, value: hou.ParmTuple | None) -> None:
        self.__referenced = value


    def getReferencedName(self) -> str:
        return self.__referencedName


    def setReferencedName(self, value: str) -> None:
        self.__referencedName = value


class _NodeReference:
    def __init__(self):
        self.__referring: hou.OpNode | None = None
        self.__referenced: hou.OpNode | None = None
        self.__paramTupleReferences: list[_ParamTupleReference] = []


    def getReferring(self) -> hou.OpNode | None:
        return self.__referring


    def setReferring(self, value: hou.OpNode | None) -> None:
        self.__referring = value


    def getReferenced(self) -> hou.OpNode | None:
        return self.__referenced


    def setReferenced(self, value: hou.OpNode | None) -> None:
        self.__referenced = value


    def getParamTupleReferences(self) -> list[_ParamTupleReference]:
        return self.__paramTupleReferences


    def setParamTupleReferences(self, value: list[_ParamTupleReference]):
        self.__paramTupleReferences = value


def _isCopyableParamTuple(param_tuple: hou.ParmTuple | None) -> bool:
    if param_tuple is None:
        return False

    param_template: hou.ParmTemplate = param_tuple.parmTemplate()

    if isinstance(param_template, (
        hou.ButtonParmTemplate,
        hou.RampParmTemplate,
        hou.LabelParmTemplate,
        hou.SeparatorParmTemplate,
    )):
        return False

    return True


def _copyParamTemplate(srcParamTuple: hou.ParmTuple) -> hou.ParmTemplate:
    src: hou.ParmTemplate = srcParamTuple.parmTemplate()
    dst: hou.ParmTemplate = src.clone()

    if isinstance(src, hou.MenuParmTemplate):
        srcParam: hou.Parm | None = srcParamTuple[0] if len(srcParamTuple) > 0 else None

        if srcParam:
            dst.setItemGeneratorScript("")
            dst.setMenuItems(srcParam.menuItems())
            dst.setMenuLabels(srcParam.menuLabels())

    return dst


def copy_create(
    candidateRootNodePath: str,
    referencedNodePath: str,
    nodes: list[common.Node],
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

    nodeReferences: list[_NodeReference] = []

    for node in nodes:
        referringNodes: list[hou.OpNode] = common.filterNodes(candidateNodes, [node])

        for referringNode in referringNodes:
            for paramTuple in node.getParamTuples():
                referringParamTuples: list[hou.ParmTuple] = common.filterParamTuples(referringNode.parmTuples(), [paramTuple])

                for referringParamTuple in referringParamTuples:
                    if not _isCopyableParamTuple(referringParamTuple):
                        continue

                    _, nodeReference = common.findIndexItem(nodeReferences, lambda r: r.getReferring() == referringNode)

                    if nodeReference is None:
                        nodeReference: _NodeReference = _NodeReference()
                        nodeReference.setReferring(referringNode)
                        nodeReference.setReferenced(referencedNode)
                        nodeReferences.append(nodeReference)

                    referencedParamTupleName: str = hou.text.encode(f"{referringNode.path()}/{referringParamTuple.name()}")
                    paramTupleReference: _ParamTupleReference = _ParamTupleReference()
                    paramTupleReference.setReferring(referringParamTuple)
                    paramTupleReference.setReferencedName(referencedParamTupleName)
                    nodeReference.getParamTupleReferences().append(paramTupleReference)

    paramTemplateGroup: hou.ParmTemplateGroup = referencedNode.parmTemplateGroup()

    for nodeReference in nodeReferences:
        folderParamTemplateName: str = hou.text.encode(nodeReference.getReferring().path())
        folderParamTemplateIndices: list[int] = paramTemplateGroup.findIndices(folderParamTemplateName)

        folderParamTemplate: hou.FolderParmTemplate | None = None

        if len(folderParamTemplateIndices) > 0:
            folderParamTemplate = paramTemplateGroup.entryAtIndices(folderParamTemplateIndices)

            if not isinstance(folderParamTemplate, hou.FolderParmTemplate):
                raise common.ParamCollectorError(f"Cannot create parameters because \"{folderParamTemplateName}\" already exists and is not a folder.")
        else:
            folderParamTemplate = hou.FolderParmTemplate(
                folderParamTemplateName,
                nodeReference.getReferring().path(),
                folder_type=hou.folderType.Collapsible
            )

        existingNames: list[str] = [t.name() for t in folderParamTemplate.parmTemplates()]

        for paramTupleReference in nodeReference.getParamTupleReferences():
            if paramTupleReference.getReferencedName() in existingNames:
                continue

            paramTemplate = _copyParamTemplate(paramTupleReference.getReferring())
            paramTemplate.setName(paramTupleReference.getReferencedName())
            folderParamTemplate.addParmTemplate(paramTemplate)
            existingNames.append(paramTupleReference.getReferencedName())

        if len(folderParamTemplateIndices) > 0:
            paramTemplateGroup.replace(folderParamTemplateIndices, folderParamTemplate)
        else:
            paramTemplateGroup.append(folderParamTemplate)

    referencedNode.setParmTemplateGroup(paramTemplateGroup)

    for nodeReference in nodeReferences:
        for paramTupleReference in nodeReference.getParamTupleReferences():
            paramTupleReference.setReferenced(nodeReference.getReferenced().parmTuple(paramTupleReference.getReferencedName()))
            assert paramTupleReference.getReferenced()

    for nodeReference in nodeReferences:
        for paramTupleReference in nodeReference.getParamTupleReferences():
            referringParams: tuple[hou.Parm, ...] = tuple(paramTupleReference.getReferring())
            referencedParams: tuple[hou.Parm, ...] = tuple(paramTupleReference.getReferenced())

            if len(referringParams) != len(referencedParams):
                referringParamTuple: hou.ParmTuple = paramTupleReference.getReferring()
                referencedParamTuple: hou.ParmTuple = paramTupleReference.getReferenced()

                raise common.ParamCollectorError(
                    "Cannot create parameter references because the selected parameter tuples have different sizes.\n"
                    f"Source: {nodeReference.getReferring().name()}/{referringParamTuple.name()} ({len(referringParams)})\n"
                    f"Target: {nodeReference.getReferenced().name()}/{referencedParamTuple.name()} ({len(referencedParams)})"
                )

            for referringParam, referencedParam in zip(referringParams, referencedParams):
                if referringParam.getReferencedParm() == referencedParam:
                    continue

                referencedParam.setFromParm(referringParam)
                referringParam.set(referencedParam, language=hou.exprLanguage.Hscript, follow_parm_reference=False)


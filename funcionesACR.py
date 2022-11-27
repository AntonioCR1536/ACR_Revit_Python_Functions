# -*- coding: utf-8 -*-
##############################################################################
# Ctrl + k Ctrl + 0
# Ctrl + k Ctrl + J

# BIBLIOTECAS
import clr  # CommonLanguage Runtime

# Para trabajar con geometrias en Dynamo
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Para trabajar con nodos de DSCore Node: List, Math, etc
clr.AddReference('DSCoreNodes')
import DSCore
from DSCore import *

# Para trabajar con nodos nativos de Revit: Ojo con las conversiones
clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

# Recurso para acceder a la API de Dynamo
clr.AddReference('DynamoRevitDS')
import Dynamo

# Para trabajar con la RevitAPI
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

# Para trabajar con la RevitAPIUI
clr.AddReference('RevitAPIUI')
import Autodesk
from Autodesk.Revit.UI import *

# Para trabajar con el documento y hacer transacciones
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Identificadores
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = uiapp.ActiveUIDocument

# Otras bibliotecas
import System
from System.Collections.Generic import *  # Para generar iList

# Bibliotecas de Python
import sys
sys.path.append(r'C:\Python27\Lib')

# FUNCTIONS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# UNIDADES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def internal_to_meters(valor):
    allUnits = UnitUtils.GetAllUnits()
    unidad = [u for u in allUnits if str(u.TypeId)[19:-6] == "meters"][0]
    return UnitUtils.ConvertFromInternalUnits(float(valor), unidad)

# LISTAS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def flatten(lista):
    """
    Uso: Aplando de lista con multiples sub niveles.
    """
    salida = []
    for x in lista:
        if isinstance(x, list):
            salida.extend(flatten(x))
        else:
            salida.append(x)
    return salida

# FILTROS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def Filter_Rule(ruleType, parameterName, evaluatorType, value):
    """
    USE:
    Returns Filter Rule of the specified type based in code.
    IN:
    ruleType <int>:
                    1 = FilterIntegerRule
                    2 = FilterDoubleRule
                    3 = FilterElementIdRule
                    4 = FilterStringRule
    parameterName <str>: The parameter name.
    evaluatorType <param>:
                            For ruleType 1 to 3: dependency of Filter_Numeric_Rule_Evaluator()
                            For ruleType 4: dependency of Filter_String_Rule_Evaluator().
    value <param>:
                    ruleType = 1: Integer
                    ruleType = 2: Double
                    ruleType = 3: ElementId
                    ruleType = 4: String
    OUT:
    filterRule: The filter rule.
    """
    if ruleType == 1:
        filterRule = FilterIntegerRule(Proveedor_Parametro_Usuario(str(parameterName)), Filter_Numeric_Rule_Evaluator(evaluatorType), value)
    elif ruleType == 2:
        filterRule = FilterDoubleRule(Proveedor_Parametro_Usuario(str(parameterName)), Filter_Numeric_Rule_Evaluator(evaluatorType), value)
    elif ruleType == 3:
        filterRule = FilterElementIdRule(Proveedor_Parametro_Usuario(str(parameterName)), FilterNumericEqual(), ElementId(value))
    elif ruleType == 4:
        filterRule = FilterStringRule(Proveedor_Parametro_Usuario(str(parameterName)), Filter_String_Rule_Evaluator(evaluatorType), str(value))
    else:
        filterRule = "Error"
    return filterRule

# PARAMETROS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def Param_Storage(param):
    """
    Uso:
    Returns value of a parameter based in its storage type.
    Entrada:
    param <param>: The parameter.
    Salida:
    value <param>: The parameter value.
    """
    if param.StorageType == StorageType.String:
        return param.AsString()
    elif param.StorageType == StorageType.ElementId:
        return param.AsElementId()
    elif param.StorageType == StorageType.Double:
        return param.AsDouble()
    else:
        return param.AsInteger()
    
def Proveedor_Parametro_Usuario(prmtrName):
    """
    USE:
    Returns a parameter provider for a parameter created by the user.
    IN:
    prmtrName <str>: The parameter name.
    OUT:
    prmtrProvider <ParameterElement>: The parameter provider.
    """
    iterator = doc.ParameterBindings.ForwardIterator()
    while iterator.MoveNext():
        if iterator.Key.Name == str(prmtrName):
            if bool:
                prmtrProvider = ParameterValueProvider(iterator.Key.Id)
            break
    return prmtrProvider

def Filter_Numeric_Rule_Evaluator(type):
    """
    USE:
    Returns a FilterNumericRuleEvaluator of the specified type.
    IN:
    type <int>: FilterNumericRuleEvaluator specified type based on a code.
                1 = FilterNumericEquals
                2 = FilterNumericGreater
                3 = FilterNumericGreaterOrEqual
                4 = FilterNumericLess
                5 = FilterNumericLessOrEqual
    OUT:
    fnre <>: The FilterNumericRuleEvaluator.
    """
    if int(type) == int(1):
        fnre = FilterNumericEquals()
    elif int(type) == int(2):
        fnre = FilterNumericGreater()
    elif int(type) == int(3):
        fnre = FilterNumericGreaterOrEqual()
    elif int(type) == int(4):
        fnre = FilterNumericLess()
    elif int(type) == int(5):
        fnre = FilterNumericLessOrEqual()
    else:
        fnre = 'Error\n\nProvide a valid code:\n\n1 = FilterNumericEquals\n'\
            '2 = FilterNumericGreater\n3 = FilterNumericGreaterOrEqual\n'\
            '4 = FilterNumericLess\n5 = FilterNumericLessOrEqual'
    return fnre

def Filter_String_Rule_Evaluator(type):
    """
    USE:
    Returns a FilterStringRuleEvaluator of the specified type.
    IN:
    type <int>: FilterStringRuleEvaluator specified type based on a code.
                1 = FilterStringBeginsWith
                2 = FilterStringContains
                3 = FilterStringEndsWith
                4 = FilterStringEquals
                5 = FilterStringGreater
                6 = FilterStringGreaterOrEqual
                7 = FilterStringLess
                8 = FilterStringLessOrEqual
    OUT:
    fsre <>: The FilterStringRuleEvaluator.
    """
    if int(type) == int(1):
        fsre = FilterStringBeginsWith()
    elif int(type) == int(2):
        fsre = FilterStringContains()
    elif int(type) == int(3):
        fsre = FilterStringEndsWith()
    elif int(type) == int(4):
        fsre = FilterStringEquals()
    elif int(type) == int(5):
        fsre = FilterStringGreater()
    elif int(type) == int(6):
        fsre = FilterStringGreaterOrEqual()
    elif int(type) == int(7):
        fsre = FilterStringLess()
    elif int(type) == int(8):
        fsre = FilterStringLessOrEqual()
    else:
        fsre = 'Error\n\nProvide a valid code:\n\n1 = FilterStringBeginsWith\n'\
            '2 = FilterStringContains\n3 = FilterStringEndsWith\n'\
            '4 = FilterStringEquals\n5 = FilterStringGreatern\n'\
            '6 = FilterStringGreaterOrEqual\n7 = FilterStringLess\n'\
            '8 = FilterStringLessOrEqual'
    return fsre

# HABITACIONES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def Get_Room_Boundaries(hab, booleano=False):
    """
    Uso:
        Returns a list with the room perimeter lines.
    Entrada:
        hab <Element>: The room
        booleano <bool>: True for return lines as prototype, false as line class
    Salida:
        lineas <list>: Lines list.
    """
    boundaries = hab.GetBoundarySegments(SpatialElementBoundaryOptions())
    for bd in boundaries:
        crvs = []
        for seg in bd:
            crv = seg.GetCurve()
            if booleano:
                crvs.append(Revit.GeometryConversion.RevitToProtoCurve.ToProtoType(crv, True))
            else:
                crvs.append(crv)
        return crvs
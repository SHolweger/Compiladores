
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'BOOLEANO CADENA DECIMAL DIFERENTE DIV FALSO IDENTIFICADOR IGUAL IGUAL_IGUAL INICIO LLAVEDER LLAVEIZQ MAYOR MAYOR_IGUAL MENOR MENOR_IGUAL MIENTRAS MULT NUMERO PARENDER PARENIZQ PUNTOYCOMA REGRESA REPETIR RESTA SI SINO SUMA VERDADEROprograma : INICIO PARENIZQ PARENDER LLAVEIZQ sentencias LLAVEDERsentencias : sentencia\n| sentencia sentenciassentencia : NUMERO IDENTIFICADOR IGUAL expresion PUNTOYCOMA\n| DECIMAL IDENTIFICADOR IGUAL expresion PUNTOYCOMA\n| BOOLEANO IDENTIFICADOR IGUAL booleano PUNTOYCOMAsentencia : IDENTIFICADOR IGUAL expresion PUNTOYCOMAsentencia : SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER\n| SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER SINO LLAVEIZQ sentencias LLAVEDERsentencia : REGRESA IDENTIFICADOR PUNTOYCOMAexpresion : expresion SUMA expresion\n| expresion RESTA expresion\n| expresion MULT expresion\n| expresion DIV expresion\n| NUMERO\n| DECIMAL\n| IDENTIFICADORbooleano : VERDADERO\n| FALSOcondicion : IDENTIFICADOR MAYOR IDENTIFICADOR\n| IDENTIFICADOR MENOR IDENTIFICADOR\n| IDENTIFICADOR IGUAL_IGUAL IDENTIFICADOR'
    
_lr_action_items = {'INICIO':([0,],[2,]),'$end':([1,14,],[0,-1,]),'PARENIZQ':([2,12,],[3,20,]),'PARENDER':([3,29,54,55,56,],[4,42,-20,-21,-22,]),'LLAVEIZQ':([4,42,59,],[5,53,60,]),'NUMERO':([5,7,17,22,27,31,33,34,35,36,37,46,51,52,53,58,60,62,],[8,8,25,25,25,-10,-7,25,25,25,25,-4,-5,-6,8,-8,8,-9,]),'DECIMAL':([5,7,17,22,27,31,33,34,35,36,37,46,51,52,53,58,60,62,],[10,10,26,26,26,-10,-7,26,26,26,26,-4,-5,-6,10,-8,10,-9,]),'BOOLEANO':([5,7,31,33,46,51,52,53,58,60,62,],[11,11,-10,-7,-4,-5,-6,11,-8,11,-9,]),'IDENTIFICADOR':([5,7,8,10,11,13,17,20,22,27,31,33,34,35,36,37,43,44,45,46,51,52,53,58,60,62,],[9,9,16,18,19,21,23,30,23,23,-10,-7,23,23,23,23,54,55,56,-4,-5,-6,9,-8,9,-9,]),'SI':([5,7,31,33,46,51,52,53,58,60,62,],[12,12,-10,-7,-4,-5,-6,12,-8,12,-9,]),'REGRESA':([5,7,31,33,46,51,52,53,58,60,62,],[13,13,-10,-7,-4,-5,-6,13,-8,13,-9,]),'LLAVEDER':([6,7,15,31,33,46,51,52,57,58,61,62,],[14,-2,-3,-10,-7,-4,-5,-6,58,-8,62,-9,]),'IGUAL':([9,16,18,19,],[17,22,27,28,]),'PUNTOYCOMA':([21,23,24,25,26,32,38,39,40,41,47,48,49,50,],[31,-17,33,-15,-16,46,51,52,-18,-19,-11,-12,-13,-14,]),'SUMA':([23,24,25,26,32,38,47,48,49,50,],[-17,34,-15,-16,34,34,34,34,34,34,]),'RESTA':([23,24,25,26,32,38,47,48,49,50,],[-17,35,-15,-16,35,35,35,35,35,35,]),'MULT':([23,24,25,26,32,38,47,48,49,50,],[-17,36,-15,-16,36,36,36,36,36,36,]),'DIV':([23,24,25,26,32,38,47,48,49,50,],[-17,37,-15,-16,37,37,37,37,37,37,]),'VERDADERO':([28,],[40,]),'FALSO':([28,],[41,]),'MAYOR':([30,],[43,]),'MENOR':([30,],[44,]),'IGUAL_IGUAL':([30,],[45,]),'SINO':([58,],[59,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'programa':([0,],[1,]),'sentencias':([5,7,53,60,],[6,15,57,61,]),'sentencia':([5,7,53,60,],[7,7,7,7,]),'expresion':([17,22,27,34,35,36,37,],[24,32,38,47,48,49,50,]),'condicion':([20,],[29,]),'booleano':([28,],[39,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programa","S'",1,None,None,None),
  ('programa -> INICIO PARENIZQ PARENDER LLAVEIZQ sentencias LLAVEDER','programa',6,'p_programa','tempCodeRunnerFile.py',36),
  ('sentencias -> sentencia','sentencias',1,'p_sentencias','tempCodeRunnerFile.py',40),
  ('sentencias -> sentencia sentencias','sentencias',2,'p_sentencias','tempCodeRunnerFile.py',41),
  ('sentencia -> NUMERO IDENTIFICADOR IGUAL expresion PUNTOYCOMA','sentencia',5,'p_sentencia_declaracion','tempCodeRunnerFile.py',45),
  ('sentencia -> DECIMAL IDENTIFICADOR IGUAL expresion PUNTOYCOMA','sentencia',5,'p_sentencia_declaracion','tempCodeRunnerFile.py',46),
  ('sentencia -> BOOLEANO IDENTIFICADOR IGUAL booleano PUNTOYCOMA','sentencia',5,'p_sentencia_declaracion','tempCodeRunnerFile.py',47),
  ('sentencia -> IDENTIFICADOR IGUAL expresion PUNTOYCOMA','sentencia',4,'p_sentencia_asignacion','tempCodeRunnerFile.py',51),
  ('sentencia -> SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER','sentencia',7,'p_sentencia_si','tempCodeRunnerFile.py',56),
  ('sentencia -> SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER SINO LLAVEIZQ sentencias LLAVEDER','sentencia',11,'p_sentencia_si','tempCodeRunnerFile.py',57),
  ('sentencia -> REGRESA IDENTIFICADOR PUNTOYCOMA','sentencia',3,'p_sentencia_regresa','tempCodeRunnerFile.py',61),
  ('expresion -> expresion SUMA expresion','expresion',3,'p_expresion','tempCodeRunnerFile.py',66),
  ('expresion -> expresion RESTA expresion','expresion',3,'p_expresion','tempCodeRunnerFile.py',67),
  ('expresion -> expresion MULT expresion','expresion',3,'p_expresion','tempCodeRunnerFile.py',68),
  ('expresion -> expresion DIV expresion','expresion',3,'p_expresion','tempCodeRunnerFile.py',69),
  ('expresion -> NUMERO','expresion',1,'p_expresion','tempCodeRunnerFile.py',70),
  ('expresion -> DECIMAL','expresion',1,'p_expresion','tempCodeRunnerFile.py',71),
  ('expresion -> IDENTIFICADOR','expresion',1,'p_expresion','tempCodeRunnerFile.py',72),
  ('booleano -> VERDADERO','booleano',1,'p_booleano','tempCodeRunnerFile.py',85),
  ('booleano -> FALSO','booleano',1,'p_booleano','tempCodeRunnerFile.py',86),
  ('condicion -> IDENTIFICADOR MAYOR IDENTIFICADOR','condicion',3,'p_condicion','tempCodeRunnerFile.py',90),
  ('condicion -> IDENTIFICADOR MENOR IDENTIFICADOR','condicion',3,'p_condicion','tempCodeRunnerFile.py',91),
  ('condicion -> IDENTIFICADOR IGUAL_IGUAL IDENTIFICADOR','condicion',3,'p_condicion','tempCodeRunnerFile.py',92),
]

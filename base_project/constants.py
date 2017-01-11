

# Question Types
TEXT = 'text'
INTEGER = 'integer'
SELECT = 'select'
CHECKBOX = 'checkbox'

WIDGET_TYPES = {TEXT: 'Text', INTEGER: 'Integer', SELECT: 'Select', CHECKBOX: 'Checkbox'}

TRUE = ['1', 'yes', 'true', 'True']
FALSE = ['0', 'no', 'false', 'False']

def YES_NO(str):
    if str in TRUE:
        return True
    elif str in FALSE:
        return False
    else:
        return None
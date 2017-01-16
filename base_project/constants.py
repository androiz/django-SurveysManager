

# Question Types
TEXT = 'text'
INTEGER = 'integer'
SELECT = 'select'
CHECKBOX = 'checkbox'
RADIO = 'radio'

WIDGET_TYPES = {TEXT: 'Text', INTEGER: 'Integer', SELECT: 'Select', CHECKBOX: 'Checkbox', RADIO: 'Radio'}

TRUE = ['1', 'yes', 'true', 'True']
FALSE = ['0', 'no', 'false', 'False']

def YES_NO(str):
    if str in TRUE:
        return True
    elif str in FALSE:
        return False
    else:
        return None
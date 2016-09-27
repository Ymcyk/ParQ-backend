"""
Place for defining users roles.

syncrules - command which creates groups based on defined here rules.
            Also if any permission in database is diffrent than described here,
            all will be replaced with existing in this file.
"""

# rezygnuję z tego pomysłu, fixtures robi to samo
Driver = {
    'verbose': 'Kierowca',
    'permissions': (
        # tu uprawnienia        
    ),
}

Officer = {
    'verbose': 'Kontroler',
    'permissions': (
        # tu uprawnienia
    ),
}

def assign_role(user, role):
    """
    
    """

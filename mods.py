"""Score mods handler"""
MODS = ['NF', 'EZ', '', 'HD', 'HR', 'SD', 'DT', 'RX', 'HT', 'NC',
        'FL', 'AP', 'SO', 'AU', 'PF', 'K4', 'K5', 'K6', 'K7', 'K8',
        'FI', 'RD', 'LM', '', 'K9', 'K10', 'K1', 'K3', 'K2']


def get_mods(bit_field):
    """Takes the index and multiplies for its bit field"""
    used_mods = [name for index, name in enumerate(MODS) if 2**index & bit_field]
    return used_mods

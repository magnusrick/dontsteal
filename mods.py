mods = ['NF', 'EZ', '', 'HD', 'HR', 'SD', 'DT', 'RX', 'HT', 'NC', 'FL', 'AP', 'SO', 'AU', 'PF', 'K4', 'K5', 'K6', 'K7',
        'K8', 'FI', 'RD', 'LM', '', 'K9', 'K10', 'K1', 'K3', 'K2']


def get_mods(fucking_peppy):
    used_mods = [name for index, name in enumerate(mods) if 2**index & fucking_peppy]
    return used_mods

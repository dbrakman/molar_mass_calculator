import re as ree  # python built-in regex library
import string
import math
import sys  # for accepting command-line input

# A condensed version of the Periodic Table data at:
# https://github.com/Bowserinator/Periodic-Table-JSON/blob/master/PeriodicTableJSON.json
mass_table = {
    'H': 1.008,
    'He': 4.0026022,
    'Li': 6.94,
    'Be': 9.01218315,
    'B': 10.81,
    'C': 12.011,
    'N': 14.007,
    'O': 15.999,
    'F': 18.9984031636,
    'Ne': 20.17976,
    'Na': 22.989769282,
    'Mg': 24.305,
    'Al': 26.98153857,
    'Si': 28.085,
    'P': 30.9737619985,
    'S': 32.06,
    'Cl': 35.45,
    'Ar': 39.9481,
    'K': 39.09831,
    'Ca': 40.0784,
    'Sc': 44.9559085,
    'Ti': 47.8671,
    'V': 50.94151,
    'Cr': 51.99616,
    'Mn': 54.9380443,
    'Fe': 55.8452,
    'Co': 58.9331944,
    'Ni': 58.69344,
    'Cu': 63.5463,
    'Zn': 65.382,
    'Ga': 69.7231,
    'Ge': 72.6308,
    'As': 74.9215956,
    'Se': 78.9718,
    'Br': 79.904,
    'Kr': 83.7982,
    'Rb': 85.46783,
    'Sr': 87.621,
    'Y': 88.905842,
    'Zr': 91.2242,
    'Nb': 92.906372,
    'Mo': 95.951,
    'Tc': 98,
    'Ru': 101.072,
    'Rh': 102.905502,
    'Pd': 106.421,
    'Ag': 107.86822,
    'Cd': 112.4144,
    'In': 114.8181,
    'Sn': 118.7107,
    'Sb': 121.7601,
    'Te': 127.603,
    'I': 126.904473,
    'Xe': 131.2936,
    'Cs': 132.905451966,
    'Ba': 137.3277,
    'La': 138.905477,
    'Ce': 140.1161,
    'Pr': 140.907662,
    'Nd': 144.2423,
    'Pm': 145,
    'Sm': 150.362,
    'Eu': 151.9641,
    'Gd': 157.253,
    'Tb': 158.925352,
    'Dy': 162.5001,
    'Ho': 164.930332,
    'Er': 167.2593,
    'Tm': 168.934222,
    'Yb': 173.0451,
    'Lu': 174.96681,
    'Hf': 178.492,
    'Ta': 180.947882,
    'W': 183.841,
    'Re': 186.2071,
    'Os': 190.233,
    'Ir': 192.2173,
    'Pt': 195.0849,
    'Au': 196.9665695,
    'Hg': 200.5923,
    'Tl': 204.38,
    'Pb': 207.21,
    'Bi': 208.980401,
    'Po': 209,
    'At': 210,
    'Rn': 222,
    'Fr': 223,
    'Ra': 226,
    'Ac': 227,
    'Th': 232.03774,
    'Pa': 231.035882,
    'U': 238.028913,
    'Np': 237,
    'Pu': 244,
    'Am': 243,
    'Cm': 247,
    'Bk': 247,
    'Cf': 251,
    'Es': 252,
    'Fm': 257,
    'Md': 258,
    'No': 259,
    'Lr': 266,
    'Rf': 267,
    'Db': 268,
    'Sg': 269,
    'Bh': 270,
    'Hs': 269,
    'Mt': 278,
    'Ds': 281,
    'Rg': 282,
    'Cn': 285,
    'Nh': 286,
    'Fl': 289,
    'Mc': 289,
    'Lv': 293,
    'Ts': 294,
    'Og': 294,
    'Uue': 315,
}


def starts_with_element(chemical_formula_substring):
    if len(chemical_formula_substring) < 1:
        return False
    else:
        return chemical_formula_substring[0] in string.ascii_uppercase
    # or:
    # return ree.match('[A-Z]', chemical_formula_substring) is not None


def get_next_element(chemical_formula_substring):
    # Caution: should match symbols of 3+ letters, e.g. Uue (119)
    return ree.match('([A-Z][a-z]*)', chemical_formula_substring).group()


def starts_with_number(chemical_formula_substring):
    if len(chemical_formula_substring) < 1:
        return False
    else:
        return chemical_formula_substring[0] in '0123456789'
    # or:
    # return ree.match('[0-9]', chemical_formula_substring) is not None


def get_num_digits_in(positive_integer):
    i = 1
    while 10**i <= positive_integer:
        i += 1
    return i


def get_next_number(chemical_formula_substring):
    return int(get_next_number_s(chemical_formula_substring))


def get_next_number_s(chemical_formula_substring):
    return ree.match('([0-9]+)', chemical_formula_substring).group()


def find_molar_mass_parenthetical_subgroup(chemical_formula_substring):
    cumulative_mass = 0
    i = 0  # tracks current position while iterating through string
    while i < len(chemical_formula_substring):
        if starts_with_element(chemical_formula_substring[i:]):
            elt = get_next_element(chemical_formula_substring[i:])
            elt_mass = mass_table[elt]
            i += len(elt)

            multiplier = 1
            if starts_with_number(chemical_formula_substring[i:]):
                multiplier = get_next_number(chemical_formula_substring[i:])
                i += get_num_digits_in(multiplier)
            cumulative_mass += elt_mass * multiplier

        elif chemical_formula_substring[i] == '(':
            i += 1
            group_info = find_molar_mass_parenthetical_subgroup(chemical_formula_substring[i:])
            group_mass = group_info['mass']
            i += group_info['num_chars_parsed']

            multiplier = 1
            if starts_with_number(chemical_formula_substring[i:]):
                multiplier = get_next_number(chemical_formula_substring[i:])
                i += get_num_digits_in(multiplier)
            cumulative_mass += group_mass * multiplier

        elif chemical_formula_substring[i] == ')':
            i += 1
            break
        else:
            raise SyntaxError('Unexpected case')
    return {
        'mass': cumulative_mass,
        'num_chars_parsed': i,
    }


def element_counts_from_chemical_formula(chemical_formula_string):
    stack_l = []  # a list, though we choose to use only its stack methods pop() and append()
    # each element on the stack will be an unfinished dict corresponding to a "blob" at that

    current_dict = {}
    i = 0  # tracks current position while iterating through string
    while i < len(chemical_formula_string):
        if starts_with_element(chemical_formula_string[i:]):
            elt = get_next_element(chemical_formula_string[i:])
            i += len(elt)

            multiplier = 1
            if starts_with_number(chemical_formula_string[i:]):
                multiplier_s = get_next_number_s(chemical_formula_string[i:])
                multiplier = int(multiplier_s)
                i += len(multiplier_s)
            current_dict[elt] = multiplier

        elif chemical_formula_string[i] == '(':
            i += 1
            stack_l.append(current_dict)
            current_dict = {}

        elif chemical_formula_string[i] == ')':
            i += 1
            if starts_with_number(chemical_formula_string[i:]):
                multiplier_s = get_next_number_s(chemical_formula_string[i:])
                i += len(multiplier_s)
                multiplier = int(multiplier_s)
                for k, v in current_dict.items():
                    current_dict[k] = v * multiplier
            tmp = current_dict
            current_dict = stack_l.pop()
            for k, v in tmp.items():
                if k in current_dict:
                    current_dict[k] += v
                else:
                    current_dict[k] = v

        else:
            raise SyntaxError('Unexpected case')

    assert len(stack_l) == 0
    return current_dict


def simplified_formula_from_element_counts(d):
    # Using https://en.wikipedia.org/wiki/Chemical_formula#Hill_system
    s = ''
    if 'C' in d:
        s += 'C' + str(d.pop('C'))  # get value & remove 'C' from dict d
    if 'H' in d:
        s += 'H' + str(d.pop('H'))
    for k in sorted(d.keys()):
        s += k + str(d.pop(k))
    return s


def prettified_formula(s):
    for pos in range(0, len(s)):
        if s[pos] in string.digits:
            new_char = '₀₁₂₃₄₅₆₇₈₉'[int(s[pos])]
            s = s[0:pos] + new_char + s[pos+1:]
    return s


def mass_from_dict(d):
    current_mass = 0
    for k, v in d.items():
        current_mass += mass_table[k] * v
    return current_mass


def mass_from_simplified_string(s):
    d = {}
    matches = ree.findall('([A-Z][a-z]*)([0-9]*)', s)
    for (elt, n) in matches:
        d[elt] = int(n)
    return mass_from_dict(d)


def find_molar_mass(chemical_formula_string):
    # Option A:
    # return find_molar_mass_parenthetical_subgroup(chemical_formula_string)['mass']

    # Option B:
    d = element_counts_from_chemical_formula(chemical_formula_string)
    m = mass_from_dict(d)

    s = simplified_formula_from_element_counts(d)
    print(prettified_formula(s))
    m2 = mass_from_simplified_string(s)
    assert m == m2
    return m


if '__main__' == __name__:
    print(find_molar_mass(sys.argv[1]))

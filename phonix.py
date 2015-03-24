'''
## Phonix and Soundex Python implementation

This is an implementation of the phonix phonetic search algorith [1,2].
This follows the perl[3] and [4] C implementations.

This is an expansion of the soundex algorithm. It is fairly complex, 
consisting of about 100-160 rules (several rules can be collapsed if 
they are described using regular expressions. This causes wildly 
different reports on the number of rules in the litterature)

The main jist of the algorithm is that rules based phonetic spelling 
is applied to the string, after which the initial character is saved 
and all other characters are represented by a numeric value depending on which of 8 groups it belongs to. Finally the 0-group is pruned.

Group numbers and letters are stored in `groups` list, while 
substitution rules are saved as regular expressions in the `rules` 
list.

Phonix is the same as soundex, only with different groups and 
a pre-processing step that applies the rules.

### Outline of phonix algorithm

This algorithm transform a string `name` -> string `phonix code`, consisting of 1 letter followed by 3 digits. The algorithm assumes all characters in `name` are Alphabetic.

1. Apply ~100 transformations to name in order to make spelling 
   more phonetic (see the rules list in code)
2. Each letter in the alphabet is substituted to with a numerical 
   number according to one fo 8 groups the letter belongs to
3. Reinstate the first letter with its alphabetic value (after 
   transformations)
4. If first letter is a vowel or y, change the first letter to 'v'
5. Truncate all consecutive numbers and all zeros.
6. if phonix code is less than 4 characters long, extend it with 
   zeros.

---

(C) Copyright 2015, Mads Olsgaard, http://olsgaard.dk
released under [BDS 3](http://opensource.org/licenses/BSD-3-Clause)

---

1. Gadd, T. N. “‘Fisching Fore Werds’: Phonetic Retrieval of Written Text 
   in Information Systems.” Program 22, no. 3 (1988): 222–37.
2. ———. “PHONIX: The Algorithm.” Program 24, no. 4 (1990): 363–66.
3. https://github.com/maros/Text-Phonetic/blob/master/lib/Text/Phonetic/Phonix.pm
4. soundex.c in https://github.com/walkingintopeople/freeWAIS/raw/master/wais/freeWAIS-sf-2.2/freeWAIS-sf-2.2.10.tar.gz
'''
import re

######################################################################
########## init variables and rules ##################################
######################################################################
vowel = '[AEIOU]';
consonant = '[BCDFGHJLMNPQRSTVXZXY]';



# Define the letter groups

                # ABCDEFGHIJKLMNOPQRSTUVWXYZ
phonix_digits =  '01230720022455012683070808'
soundex_digits = '01230120022455012623010202'



# list of transformation/substitution rules
#            [pattern, substitution]

rules = [    [re.compile(r'[^A-Z]'), r''], #Remove all non-alphabet characters. Note that name should be uppercased before applying rules
             [re.compile(r'DG'),    r'G'],
             [re.compile(r'C([OAU])'),    r'K'],  # Covers several rules in soundex.c [CO, CA, CU]
             [re.compile(r'C[YI]'),    r'SI'],    # Covers [CY, CI]
             [re.compile(r'CE'),    r'SE'],
             [re.compile(r'^CL(?={})'.format(vowel) ),    r'KL'],
             [re.compile(r'CK'),    r'K'],
             [re.compile(r'[GJ]C$'),    r'K'],
             [re.compile(r'^CH?R(?={})'.format(vowel)),    r'KR'],
             [re.compile(r'^WR'),    r'R'],
             [re.compile(r'NC'),    r'NK'],
             [re.compile(r'CT'),    r'KT'],
             [re.compile(r'PH'),    r'F'],
             [re.compile(r'AA'),    r'AR'], 
             [re.compile(r'SCH'),    r'SH'],
             [re.compile(r'BTL'),    r'TL'],
             [re.compile(r'GHT'),    r'T'],
             [re.compile(r'AUGH'),    r'ARF'],
             [re.compile(r'(?<={0})LJ(?={0})'.format(vowel)),    r'LD'], #
             [re.compile(r'LOUGH'),    r'LOW'],
             [re.compile(r'^Q'),    r'KW'],
             [re.compile(r'^KN'),    r'N'],
             [re.compile(r'^GN|GN$'),    r'N'],
             [re.compile(r'(\w)GN(?={})'.format(consonant)),    r'N'],
             [re.compile(r'GHN'),    r'N'],
             [re.compile(r'GNE$'),    r'N'],
             [re.compile(r'GHNE'),    r'NE'],
             [re.compile(r'GNES$'),    r'NS'],
             [re.compile(r'^PS'),    r'S'],
             [re.compile(r'^PT'),    r'T'],
             [re.compile(r'^CZ'),    r'C'],
             [re.compile(r'(?<={})WZ(\w)'.format(vowel)),    r'Z'],
             [re.compile(r'(\w)CZ(\w)'),    r'CH'],
             [re.compile(r'LZ'),    r'LSH'],
             [re.compile(r'RZ'),    r'RSH'],
             [re.compile(r'(\w)Z(?={})'.format(vowel)),    r'S'],
             [re.compile(r'ZZ'),    r'TS'],
             [re.compile(r'(?<={})Z(\w)'.format(vowel)),    r'TS'],
             [re.compile(r'HROUGH'),    r'[REW]'],
             [re.compile(r'OUGH'),    r'OF'],
             [re.compile(r'(?<={0})Q(?={0})'.format(vowel)),    r'KW'],
             [re.compile(r'(?<={0})J(?={0})'.format(vowel)),    r'Y'],
             [re.compile(r'^YJ(?={})'.format(vowel)),    r'Y'],
             [re.compile(r'^GH'),    r'G'],
             [re.compile(r'($VOVEL)E$'),    r'GH'],
             [re.compile(r'^CY'),    r'S'],
             [re.compile(r'NX'),    r'NKS'],
             [re.compile(r'^PF'),    r'F'],
             [re.compile(r'DT$'),    r'T'],
             [re.compile(r'([TD])L$'),    r'IL'],
             [re.compile(r'YTH'),    r'ITH'],
             [re.compile(r'^TS?J(?={})'.format(vowel)),    r'CH'],
             [re.compile(r'^TS(?={})'.format(vowel)),    r'T'],
             [re.compile(r'TCH'),    r'CH'],
             [re.compile(r'(?<={})WSK'.format(vowel)),    r'VSIKE'],
             [re.compile(r'^[PM]N(?={})'.format(vowel)),    r'N'],
             [re.compile(r'(?<={})STL'.format(vowel)),    r'SL'],
             [re.compile(r'TNT$'),    r'ENT'],
             [re.compile(r'EAUX$'),    r'OH'],
             [re.compile(r'EXCI'),    r'ECS'],
             [re.compile(r'X'),    r'ECS'],
             [re.compile(r'NED$'),    r'ND'],
             [re.compile(r'JR'),    r'DR'],
             [re.compile(r'EE$'),    r'EA'], #There is an earlier rule to capture E and change it to GH at the end, so when will this rule ever apply?
             [re.compile(r'ZS'),    r'S'],
             [re.compile(r'(?<={0})H?R(?={1}|$)'.format(vowel, consonant)),    r'AH'], # combines all R and HR rules
             [re.compile(r'RE$'),    r'AR'],
             [re.compile(r'LLE'),    r'LE'],
             [re.compile(r'(?<={})LE(S?)$'.format(consonant)),    r'ILE\1'],
             [re.compile(r'E$'),    r''],
             [re.compile(r'ES$'),    r'S'],
             [re.compile(r'(?<={})SS'.format(vowel)),    r'AS'],
             [re.compile(r'(?<={})MB$'.format(vowel)),    r'M'],
             [re.compile(r'MPTS'),    r'MPS'],
             [re.compile(r'MPS'),    r'MS'],
             [re.compile(r'MPT'),    r'MT'],
             [re.compile(r'^{}'.format(vowel)), r'v']] # In phonix if first letter is vowel, change to it 'v'

######################################################################
#################### FUNCTIONS #######################################
######################################################################

def _encode(name, digits, len=4):
    # The encoding step of phonix is the same as the encoding step of
    # soundex, except other codes are used.
    
    # name should be uppercased before calling this function!
    
    key = ''

    # translate alpha chars in name to soundex digits
        
    ord_A = 65 #No need to call ord everytime
    
    for c in name[1:]:
        if c.isalpha():
            d = digits[ord(c)-ord_A]
            
            # duplicate consecutive soundex digits are skipped
            if not key or (d != key[-1]):
                key += d

    # Insert the first character
    key = name[0] + key

    # remove all 0s from the soundex code
    key = key.replace('0','')

    # return soundex code padded to len characters
    return (key + (len * '0'))[:len]


def soundex(name):
    return _encode(name.upper(), soundex_digits)


def phonix(name):
    name = name.upper()
    for rule in rules:
        #Apply all rules sequentially to name
        name = rule[0].sub(rule[1], name)
    code = _encode(name, phonix_digits)
    
    return name, code


def main():
	# Do some sanity tests
	# Names and codes taken from "Data-centric systems and applications" By Peteer Christensen, Springer 2012

	test_names = ['peter', 'pete', 'pedro', 'stephen', 'steve', 'smith', 'smythe', 'gail', 'gayle', 'christine', 'christina', 'kristina']
	soundex_codes = ['p360', 'p300', 'p360', 's315', 's310', 's530', 's530', 'g400', 'g400', 'c623', 'c623', 'k623']
	phonix_codes = ['p300', 'p300', 'p360', 's375', 's370', 's530', 's530', 'g400', 'g400', 'c683', 'c683', 'k683']

	print 'Name, \t soundex_code, \ttrue, \tphonix,    phonix code,\ttrue\n'
	for i, n in enumerate(test_names):
	    p = phonix(n)
	    print '\t'.join([n+'    ', soundex(n), soundex_codes[i], p[0]+'     ', p[1], phonix_codes[i]])



if  __name__ =='__main__':main()
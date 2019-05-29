from django import forms


class Firstinput(forms.Form):
    yearchoices = (
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
    )
    mochoices = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
    )
    patient_age_yr = forms.ChoiceField(choices=yearchoices)
    patient_age_mo = forms.ChoiceField(choices=mochoices)
    GMFCS = forms.ChoiceField(choices=(('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV'), ('V', 'V')))

class Secondinput1(forms.Form):
    ECAB1 = forms.FloatField(max_value=100, min_value=0, label='Balance past score:')
    ECAB2 = forms.FloatField(max_value=5, min_value=1,label='Balance current score:')
    SMWT1 = forms.FloatField(min_value= 0, max_value= 6000,label='Endurance (six minute walk) past score:')
    SMWT2 = forms.FloatField(min_value= 0,max_value=6000,label='Endurance (six minute walk) current score:')
    SAROMM1 = forms.FloatField(min_value= 0, max_value = 4, label='Range of motion past score:')
    SAROMM2 = forms.FloatField(min_value= 0,max_value = 4,label='Range of motion current score:')
    CEDLpar1 = forms.FloatField(min_value= 0,max_value = 100,label='Participation in family and recreational activities past score:')
    CEDLpar2 = forms.FloatField(min_value= 0,max_value = 100,label='Participation in family and recreational activities current score:')
    CEDLsc1 = forms.FloatField(min_value= 0, max_value = 100, label='Performance in self-care activities past score:')
    CEDLsc2 = forms.FloatField(min_value= 0, max_value = 100, label='Performance in self-care activities current score:')
    EASE1 = forms.FloatField(min_value= 1, max_value = 5, label='Early activity scale for endurance past score:')
    EASE2 = forms.FloatField(min_value= 1, max_value = 5, label='Early activity scale for endurance current score:')
    FSA1 =  forms.FloatField(min_value= 1, max_value = 5, label='Strength past score:')
    FSA2 =  forms.FloatField(min_value= 1, max_value = 5, label='Strength current score:')
    HEALTH1 = forms.FloatField(min_value= 0, max_value = 7, label='Overall health past score:')
    HEALTH2 = forms.FloatField(min_value= 0, max_value = 7, label='Overall health current score:')
    GMFM1 = forms.FloatField(min_value= 0, max_value = 100, label='Gross motor function past score:')
    GMFM2 = forms.FloatField(min_value= 0, max_value = 100, label='Gross motor function current score:')

class Secondinput2(forms.Form):
    ECAB1 = forms.FloatField(max_value=100, min_value=0, label='Balance past score:')
    ECAB2 = forms.FloatField(max_value=5, min_value=1,label='Balance current score:')
    SAROMM1 = forms.FloatField(min_value= 0, max_value = 4, label='Range of motion past score:')
    SAROMM2 = forms.FloatField(min_value= 0,max_value = 4,label='Range of motion current score:')
    CEDLpar1 = forms.FloatField(min_value= 0,max_value = 100,label='Participation in family and recreational activities past score:')
    CEDLpar2 = forms.FloatField(min_value= 0,max_value = 100,label='Participation in family and recreational activities current score:')
    CEDLsc1 = forms.FloatField(min_value= 0, max_value = 100, label='Performance in self-care activities past score:')
    CEDLsc2 = forms.FloatField(min_value= 0, max_value = 100, label='Performance in self-care activities current score:')
    EASE1 = forms.FloatField(min_value= 1, max_value = 5, label='Early activity scale for endurance past score:')
    EASE2 = forms.FloatField(min_value= 1, max_value = 5, label='Early activity scale for endurance current score:')
    FSA1 =  forms.FloatField(min_value= 1, max_value = 5, label='Strength past score:')
    FSA2 =  forms.FloatField(min_value= 1, max_value = 5, label='Strength current score:')
    HEALTH1 = forms.FloatField(min_value= 0, max_value = 7, label='Overall health past score:')
    HEALTH2 = forms.FloatField(min_value= 0, max_value = 7, label='Overall health current score:')
    GMFM1 = forms.FloatField(min_value= 0, max_value = 100, label='Gross motor function past score:')
    GMFM2 = forms.FloatField(min_value= 0, max_value = 100, label='Gross motor function current score:')
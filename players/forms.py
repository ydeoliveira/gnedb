#encoding:utf-8

from django import forms

SORT_CHOICES = (('','----'),
                ('-defense','défense'),
                ('-speed','vitesse'),
                ('-dribbling','dribble'),
                ('-passing','passe'),
                ('-footwork','jeu de jambe'),
                ('-rebond','rebond'),
                ('-experience','expérience'))

class SubmitForm(forms.Form):
    liste = forms.CharField(widget=forms.Textarea)

class SearchForm(forms.Form):
    filter = forms.CharField(label="Filtre IC (100.000 par défaut) ",widget=forms.TextInput(attrs={'size':'8'}))
    liste = forms.CharField(widget=forms.Textarea)

class PlayerSearch(forms.Form):
    name = forms.CharField(label="Nom contient ", required=False)
    
    min_age = forms.IntegerField(widget=forms.TextInput(attrs={'size':'4'}), required=False)
    max_age = forms.IntegerField(widget=forms.TextInput(attrs={'size':'4'}), required=False)
    
    min_height = forms.IntegerField(max_value=230, min_value=160,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    max_height = forms.IntegerField(max_value=230, min_value=160,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    
    min_def = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    max_def = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    
    min_speed = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    max_speed = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    
    min_drib = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    max_drib = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    
    min_pass = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    max_pass = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    
    min_shoot = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    max_shoot = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    
    min_ftw = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    max_ftw = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    
    min_reb = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    max_reb = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    
    min_xp = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    max_xp = forms.IntegerField(max_value=30, min_value=0,widget=forms.TextInput(attrs={'size':'4'}), required=False)
    
    sort1 = forms.ChoiceField(choices=SORT_CHOICES, required=False)
    sort2 = forms.ChoiceField(choices=SORT_CHOICES, required=False)
    
from socket import fromshare
from django import forms


class ContactForm(forms.Form):
    category = forms.ChoiceField(choices=[('hva', 'Huis van Alijn'), ('dmg', 'Design Museum Gent'), ('industriemuseum', 'Industriemuseum'), ('stam', 'STAM Gent'), ('archief', 'Archief Gent')])
    objectnumber = forms.CharField(required=True)

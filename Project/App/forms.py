from django import forms
from .models import ModelSzablonowy, Kategoria  # Importujemy nasze modele

# --- Przykład 1: Najprostszy ModelForm ---
# Automatycznie tworzy formularz na podstawie modelu.

class ProstyModelForm(forms.ModelForm):
    class Meta:
        model = ModelSzablonowy
        fields = '__all__'  # Włącz wszystkie pola z modelu
        # Można też wykluczyć pola, które ma ustawiać system, a nie użytkownik:
        # exclude = [
        #   'pole_datetime_created',
        #   'pole_datetime',
        #   'pole_uuid',
        #   'obraz_height',
        #   'obraz_width'
        # ]


# --- Przykład 2: Zaawansowany i dostosowany ModelForm ---
# To jest bardziej realistyczny szablon, pokazujący jak
# nadpisać domyślne zachowanie ModelForm.

class ZaawansowanyModelForm(forms.ModelForm):

    # Można też dodawać pola, których nie ma w modelu (np. do walidacji)
    potwierdz_email = forms.EmailField(
        label="Potwierdź e-mail",
        required=True,
        help_text="Wpisz ponownie adres e-mail, aby potwierdzić."
    )

    class Meta:
        model = ModelSzablonowy

        # 1. Jawnie wybieramy, które pola mają być w formularzu i w jakiej kolejności
        fields = [
            'pole_char',
            'pole_text',
            'pole_slug',
            'pole_email',
            'potwierdz_email',  # Dodajemy nasze niestandardowe pole
            'pole_int',
            'pole_decimal',
            'pole_boolean',
            'pole_date',
            'pole_foreign_key',
            'pole_many_to_many',
            'pole_image',
            'pole_file',
        ]
        
        # 2. 'widgets' pozwala zmienić domyślny widget HTML dla pola
        widgets = {
            'pole_text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Wpisz długi opis...'}),
            'pole_date': forms.SelectDateWidget(years=range(2020, 2031)),
            'pole_foreign_key': forms.Select(attrs={'class': 'form-control-select'}),
            'pole_many_to_many': forms.CheckboxSelectMultiple,  # Lepsze dla M2M niż domyślna lista
        }

        # 3. 'labels' pozwala nadpisać domyślne etykiety (jeśli 'verbose_name' z modelu nie wystarcza)
        labels = {
            'pole_char': 'Tytuł główny',
            'pole_slug': 'Przyjazny adres URL (slug)',
        }

        # 4. 'help_texts' pozwala nadpisać teksty pomocnicze
        help_texts = {
            'pole_slug': 'Używaj tylko małych liter, cyfr i myślników. Zostaw puste, aby wygenerować automatycznie.',
        }

        # 5. 'error_messages' pozwala na własne komunikaty błędów
        error_messages = {
            'pole_char': {
                'max_length': "Ten tytuł jest za długi. Skróć go.",
                'required': "Tytuł jest obowiązkowy."
            },
            'pole_slug': {
                'unique': "Taki adres URL już istnieje. Wybierz inny."
            }
        }

    # === 6. WALIDACJA NIESTANDARDOWA ===

    def __init__(self, *args, **kwargs):
        """
        Nadpisanie __init__ jest często używane do dynamicznych modyfikacji,
        np. filtrowania querysetu dla pola relacyjnego.
        """
        super().__init__(*args, **kwargs)
        
        # Przykład: Ogranicz kategorie tylko do tych, które zaczynają się na "A"
        # self.fields['pole_foreign_key'].queryset = Kategoria.objects.filter(nazwa__startswith='A')
        
        # Przykład: Dodawanie klas CSS do wszystkich pól
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_pole_char(self):
        """
        Metoda `clean_<nazwa_pola>` służy do walidacji jednego, konkretnego pola.
        """
        dane = self.cleaned_data.get('pole_char')
        if dane and "brzydkie_slowo" in dane.lower():
            # Podnieś błąd walidacji
            raise forms.ValidationError("Nie używaj brzydkich słów w tytule!")
        return dane  # Zawsze zwracaj oczyszczone dane

    def clean(self):
        """
        Metoda `clean` służy do walidacji całego formularza,
        zwłaszcza do sprawdzania zależności między polami.
        """
        cleaned_data = super().clean()
        email = cleaned_data.get('pole_email')
        potwierdz_email = cleaned_data.get('potwierdz_email')

        # Sprawdzamy, czy nasze dwa pola e-mail są zgodne
        if email and potwierdz_email and email != potwierdz_email:
            # Dodaj błąd do konkretnego pola
            self.add_error('potwierdz_email', "Adresy e-mail nie są zgodne.")
            # Można też podnieść błąd globalny (wyświetlany na górze formularza)
            # raise forms.ValidationError("Adresy e-mail nie są zgodne!")

        return cleaned_data  # Zawsze zwracaj cały słownik cleaned_data
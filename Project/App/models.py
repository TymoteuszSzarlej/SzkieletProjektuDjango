# Ważne importy na start
import uuid  # Do pola UUIDField
from django.db import models
from django.conf import settings  # Do odwołania się do modelu User (settings.AUTH_USER_MODEL)
from django.urls import reverse
from django.utils import timezone

# Importy dla pól specyficznych dla PostgreSQL (opcjonalne)
'''from django.contrib.postgres.fields import ArrayField'''


# --- Modele pomocnicze do demonstracji relacji ---
# W prawdziwym projekcie te modele byłyby w swoich własnych aplikacjach
# lub plikach models.py.

class Kategoria(models.Model):
    """Prosty model do demonstracji relacji ForeignKey i ManyToMany."""
    nazwa = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.nazwa

class Profil(models.Model):
    """Prosty model do demonstracji relacji OneToOneField."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Profil {self.user.username}"


# --- GŁÓWNY MODEL SZABLONOWY ---

class ModelSzablonowy(models.Model):
    """
    Model ten służy jako szablon i demonstracja wszystkich
    głównych typów pól dostępnych w Django.
    """

    # === 1. KLUCZ GŁÓWNY ===
    # Django domyślnie dodaje `id = models.AutoField(primary_key=True)`.
    # `BigAutoField` jest nowym standardem (64-bit) i jest domyślny w nowych projektach.
    # Można też użyć UUID jako klucza głównego (patrz pole_uuid poniżej).
    # id = models.BigAutoField(primary_key=True)


    # === 2. POLA TEKSTOWE ===
    pole_char = models.CharField(
        max_length=255,
        verbose_name="Pole tekstowe (krótkie)",
        help_text="Standardowe pole na krótki tekst, np. tytuł."
    )
    pole_text = models.TextField(
        blank=True,  # Może być puste w formularzu
        null=True,   # Może mieć wartość NULL w bazie danych
        verbose_name="Pole tekstowe (długie)",
        help_text="Pole na długi tekst, np. opis."
    )
    pole_slug = models.SlugField(
        max_length=100,
        unique=True,  # Zapewnia unikalność w tabeli
        db_index=True, # SlugFiel domyślnie tworzy indeks bazy danych
        help_text="Używane do URLi, np. 'moj-artykul-1'."
    )
    
    
    # === 3. POLA LICZBOWE ===
    pole_int = models.IntegerField(
        default=0,
        verbose_name="Liczba całkowita"
    )
    # Istnieją też: SmallIntegerField, BigIntegerField
    
    pole_positive_int = models.PositiveIntegerField(
        default=1,
        help_text="Tylko liczby dodatnie (>= 0)."
    )
    # Istnieją też: PositiveSmallIntegerField
    
    pole_float = models.FloatField(
        null=True,
        blank=True,
        help_text="Liczba zmiennoprzecinkowa (używaj ostrożnie)."
    )
    pole_decimal = models.DecimalField(
        max_digits=10,      # Całkowita liczba cyfr
        decimal_places=2,   # Liczba miejsc po przecinku
        verbose_name="Liczba dziesiętna (dla finansów)",
        help_text="Używaj tego do pieniędzy, aby uniknąć błędów zaokrągleń."
    )

    
    # === 4. POLA LOGICZNE (BOOLEAN) ===
    pole_boolean = models.BooleanField(
        default=True,
        verbose_name="Pole Tak/Nie",
        help_text="Przechowuje True lub False."
    )
    # Dawniej istniało NullBooleanField, teraz używa się:
    pole_boolean_null = models.BooleanField(
        null=True,
        blank=True,  # Umożliwia "nieznaną" wartość (NULL)
        verbose_name="Pole Tak/Nie/Nieznane"
    )

    
    # === 5. POLA DATY I CZASU ===
    pole_date = models.DateField(
        default=timezone.now,  # Używaj `timezone.now` zamiast `datetime.now`
        help_text="Przechowuje tylko datę."
    )
    pole_datetime = models.DateTimeField(
        auto_now=True,      # Automatycznie ustawia datę i czas przy KAŻDYM zapisie (aktualizacji)
        help_text="Przechowuje datę i czas."
    )
    pole_datetime_created = models.DateTimeField(
        auto_now_add=True,  # Ustawia datę i czas TYLKO przy tworzeniu obiektu
        editable=False,     # Zwykle nie chcemy, by to było edytowalne
        help_text="Data utworzenia."
    )
    pole_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Przechowuje tylko czas."
    )
    pole_duration = models.DurationField(
        null=True,
        blank=True,
        help_text="Przechowuje okres czasu (np. '3 dni, 4 godziny')."
    )

    
    # === 6. POLA RELACYJNE ===
    pole_foreign_key = models.ForeignKey(
        Kategoria,
        on_delete=models.SET_NULL,  # Co zrobić, gdy Kategoria zostanie usunięta? Ustawia to pole na NULL.
                                    # Inne opcje: CASCADE, PROTECT, SET_DEFAULT, DO_NOTHING
        null=True,
        blank=True,
        related_name="szablony",  # Nazwa do odwołania zwrotnego (np. kategoria.szablony.all())
        verbose_name="Relacja Wiele-do-Jednego (Klucz Obcy)"
    )
    pole_one_to_one = models.OneToOneField(
        settings.AUTH_USER_MODEL,   # Lepsze niż bezpośrednie importowanie `User`
        on_delete=models.CASCADE,   # Usunięcie Usera usunie też ten obiekt
        related_name="model_szablonowy", # Nazwa do odwołania zwrotnego (np. user.model_szablonowy)
        verbose_name="Relacja Jeden-do-Jednego",
        help_text="Np. profil użytkownika."
    )
    pole_many_to_many = models.ManyToManyField(
        Kategoria,  # Tak, można mieć M2M i FK do tego samego modelu
        blank=True,
        related_name="szablony_m2m",
        verbose_name="Relacja Wiele-do-Wielu",
        help_text="Np. tagi."
    )
    
    
    # === 7. POLA SPECJALISTYCZNE ===
    pole_email = models.EmailField(
        max_length=254,  # Standardowa max długość emaila
        blank=True,
        verbose_name="Adres E-mail"
    )
    pole_url = models.URLField(
        max_length=200,
        blank=True,
        verbose_name="Adres URL"
    )
    pole_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,  # Zwykle nie chcemy, by użytkownik to edytował
        unique=True,
        db_index=True,
        verbose_name="Unikalny Identyfikator UUID"
    )
    pole_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Adres IP (v4 lub v6)"
    )
    
    # === 8. POLA PLIKÓW ===
    # Wymagają konfiguracji MEDIA_ROOT i MEDIA_URL w settings.py
    pole_file = models.FileField(
        upload_to='uploads/files/%Y/%m/%d/',  # Ścieżka zapisu w MEDIA_ROOT
        blank=True,
        null=True,
        verbose_name="Plik"
    )
    # Wymaga dodatkowo biblioteki 'Pillow' (pip install Pillow)
    pole_image = models.ImageField(
        upload_to='uploads/images/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Obraz",
        height_field='obraz_height',  # Opcjonalnie, zapisuje wysokość
        width_field='obraz_width'     # Opcjonalnie, zapisuje szerokość
    )
    # Pola do przechowywania wymiarów obrazu (jeśli użyto height/width_field)
    obraz_height = models.PositiveIntegerField(null=True, blank=True, editable=False)
    obraz_width = models.PositiveIntegerField(null=True, blank=True, editable=False)
    
    
    # === 9. POLA SPECYFICZNE DLA BAZY DANYCH (np. PostgreSQL) ===
    pole_json = models.JSONField(
        null=True,
        blank=True,
        default=dict,  # Dobry domyślny typ to pusty słownik
        help_text="Przechowuje dane w formacie JSON."
    )
    # Wymaga importu: from django.contrib.postgres.fields import ArrayField
    '''pole_array = ArrayField(
        models.CharField(max_length=100),  # Definiujemy, że to będzie tablica stringów
        blank=True,
        null=True,
        default=list, # Domyślnie pusta lista
        help_text="Tablica (lista) wartości, np. ['tag1', 'tag2']"
    )'''


    # === 10. META OPCJE ===
    class Meta:
        verbose_name = "Model Szablonowy"
        verbose_name_plural = "Modele Szablonowe"
        ordering = ['-pole_datetime_created']  # Domyślne sortowanie (malejąco wg daty utworzenia)
        
        # Przykład ograniczenia unikalności na kilku polach
        unique_together = ['pole_char', 'pole_slug']
        
        # Przykład indeksu bazy danych
        indexes = [
            models.Index(fields=['pole_char', 'pole_date']),
        ]

        
    # === 11. STANDARDOWE METODY ===
    def __str__(self):
        """Zwraca czytelną reprezentację obiektu (ważne w panelu admina)."""
        return f"{self.pole_char} (ID: {self.id})"

    def get_absolute_url(self):
        """Zwraca URL do widoku szczegółowego tego obiektu."""
        # Wymaga zdefiniowania URL-a o nazwie 'szablon-detail' w urls.py
        # np. path('szablon/<int:pk>/', views.SzablonDetailView.as_view(), name='szablon-detail')
        try:
            return reverse('szablon-detail', kwargs={'pk': self.pk})
        except:
            # Na wypadek gdyby URL nie był jeszcze zdefiniowany
            return "/"

    def save(self, *args, **kwargs):
        """
        Nadpisanie metody save() pozwala na wykonanie własnej logiki
        przed lub po zapisie do bazy danych.
        """
        # Przykład: automatyczne tworzenie sluga, jeśli jest pusty
        if not self.pole_slug and self.pole_char:
            from django.utils.text import slugify
            self.pole_slug = slugify(self.pole_char)
            
        super().save(*args, **kwargs)  # Zawsze wywołaj oryginalną metodę save()
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User
from .scoring import ITEM_TEXTS


SEX_CHOICES = [
    ("Femenino", "Femenino"),
    ("Masculino", "Masculino"),
    ("Otro", "Otro"),
]

EDUCATION_CHOICES = [
    ("Sin instrucción formal", "Sin instrucción formal"),
    ("Primario incompleto", "Primario incompleto"),
    ("Primario completo", "Primario completo"),
    ("Secundario incompleto", "Secundario incompleto"),
    ("Secundario completo", "Secundario completo"),
    ("Terciario/universitario incompleto", "Terciario/universitario incompleto"),
    ("Terciario completo", "Terciario completo"),
    ("Universitario completo", "Universitario completo"),
    ("Posgrado", "Posgrado"),
]

MARITAL_CHOICES = [
    ("Soltero/a", "Soltero/a"),
    ("Casado/a", "Casado/a"),
    ("En pareja / unión convivencial", "En pareja / unión convivencial"),
    ("Separado/a o divorciado/a", "Separado/a o divorciado/a"),
    ("Viudo/a", "Viudo/a"),
]

OCCUPATIONAL_CHOICES = [
    ("Trabaja (en actividad)", "Trabaja (en actividad)"),
    ("Jubilado/a o pensionado/a", "Jubilado/a o pensionado/a"),
    ("Jubilado/a o pensionado/a que trabaja", "Jubilado/a o pensionado/a que trabaja"),
    ("Ama/o de casa", "Ama/o de casa"),
    ("Desocupado/a", "Desocupado/a"),
    ("Otra", "Otra"),
]

MODALITY_CHOICES = [
    ("Autoadministración remota", "Autoadministración remota"),
    ("Asistida presencial", "Asistida presencial"),
]

DEVICE_CHOICES = [
    ("Celular", "Celular"),
    ("Tablet", "Tablet"),
    ("Computadora", "Computadora"),
    ("Papel", "Papel"),
]

YES_NO_CHOICES = [
    ("Sí", "Sí"),
    ("No", "No"),
]

ITEM_OPTIONS = [
    ("", "Seleccionar"),
    ("1", "1 - En desacuerdo"),
    ("2", "2 - Parcialmente en desacuerdo"),
    ("3", "3 - Algo de acuerdo"),
    ("4", "4 - De acuerdo"),
]

ITEM_40_OPTIONS = [
    ("", "Seleccionar"),
    ("0", "0"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3 o más"),
]


def with_blank(choices):
    return [("", "Seleccionar")] + list(choices)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class TestForm(forms.Form):
    SOCIO_FIELDS = [
        "participant_code",
        "age",
        "sex",
        "education",
        "marital_status",
        "occupational_status",
        "occupation_detail",
        "nationality",
    ]

    APP_FIELDS = [
        "time_minutes",
        "had_difficulty",
        "difficulty_detail",
        "modality",
        "evaluator_code",
        "evaluator_read_aloud",
        "received_help",
        "device",
    ]

    mode = forms.ChoiceField(
        choices=[
            ("self", "Autoadministrado"),
            ("administered", "Administrado"),
        ],
        widget=forms.HiddenInput(),
        initial="self",
    )

    participant_code = forms.CharField(
        label="Código de participante",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    age = forms.IntegerField(
        label="Edad",
        min_value=18,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    sex = forms.ChoiceField(
        label="Sexo",
        choices=with_blank(SEX_CHOICES),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    education = forms.ChoiceField(
        label="Nivel de escolaridad",
        choices=with_blank(EDUCATION_CHOICES),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    marital_status = forms.ChoiceField(
        label="Estado civil",
        choices=with_blank(MARITAL_CHOICES),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    occupational_status = forms.ChoiceField(
        label="Situación ocupacional",
        choices=with_blank(OCCUPATIONAL_CHOICES),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    occupation_detail = forms.CharField(
        label="Ocupación / profesión (detalle)",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    nationality = forms.CharField(
        label="Nacionalidad (país)",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    time_minutes = forms.IntegerField(
        label="Tiempo de respuesta (minutos)",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    had_difficulty = forms.ChoiceField(
        label="¿Tuvo alguna dificultad para responder?",
        choices=with_blank(YES_NO_CHOICES),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    difficulty_detail = forms.CharField(
        label="Si tuvo dificultad: ¿cuál?",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}),
    )

    modality = forms.ChoiceField(
        label="Modalidad de aplicación",
        choices=MODALITY_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    evaluator_code = forms.CharField(
        label="Código del evaluador (solo asistida)",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    evaluator_read_aloud = forms.ChoiceField(
        label="Asistida: ¿el evaluador leyó los ítems en voz alta?",
        choices=with_blank(YES_NO_CHOICES),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    received_help = forms.ChoiceField(
        label="Remota: ¿recibió ayuda de otra persona para responder?",
        choices=with_blank(YES_NO_CHOICES),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    device = forms.ChoiceField(
        label="Soporte / dispositivo",
        choices=with_blank(DEVICE_CHOICES),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for item_number in range(1, 40):
            self.fields[f"item_{item_number}"] = forms.ChoiceField(
                label=f"{item_number}. {ITEM_TEXTS[item_number]}",
                choices=ITEM_OPTIONS,
                required=True,
                widget=forms.Select(attrs={"class": "form-select"}),
            )

        self.fields["item_40"] = forms.ChoiceField(
            label=f"40. {ITEM_TEXTS[40]}",
            choices=ITEM_40_OPTIONS,
            required=True,
            widget=forms.Select(attrs={"class": "form-select"}),
        )

    @property
    def socio_fields(self):
        return [self[name] for name in self.SOCIO_FIELDS]

    @property
    def app_fields(self):
        return [self[name] for name in self.APP_FIELDS]

    @property
    def item_fields(self):
        return [self[f"item_{i}"] for i in range(1, 41)]

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age is not None and age < 18:
            raise forms.ValidationError("El inventario se aplica a personas de 18 años o más.")
        return age
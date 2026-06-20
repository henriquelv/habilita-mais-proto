from django import forms

from .models import Agendamento


HORARIOS = [
    ("08:00", "08:00"),
    ("09:00", "09:00"),
    ("10:00", "10:00"),
    ("11:00", "11:00"),
    ("14:00", "14:00"),
    ("15:00", "15:00"),
    ("16:00", "16:00"),
    ("17:00", "17:00"),
]

INSTRUTORES = [
    ("Carlos Silva", "Carlos Silva"),
    ("Maria Santos", "Maria Santos"),
    ("João Pedro", "João Pedro"),
    ("Ana Costa", "Ana Costa"),
]

CATEGORIAS = [("A", "Categoria A"), ("B", "Categoria B"), ("AB", "Categoria AB"), ("C", "Categoria C"), ("D", "Categoria D"), ("E", "Categoria E")]

CLINICAS = [
    ("Clínica Central - Centro", "Clínica Central - Centro"),
    ("Clínica São Lucas - Zona Sul", "Clínica São Lucas - Zona Sul"),
    ("Clínica Vida - Zona Norte", "Clínica Vida - Zona Norte"),
]


class AgendamentoForm(forms.ModelForm):
    horario = forms.ChoiceField(choices=HORARIOS)
    instrutor = forms.ChoiceField(choices=INSTRUTORES, required=False)
    categoria = forms.ChoiceField(choices=CATEGORIAS, initial="B")
    local = forms.ChoiceField(choices=CLINICAS, required=False, label="Clínica")

    class Meta:
        model = Agendamento
        fields = ["tipo", "categoria", "data", "horario", "instrutor", "local", "observacao"]
        widgets = {
            "tipo": forms.Select(choices=Agendamento.TipoAula.choices),
            "data": forms.DateInput(attrs={"type": "date"}),
            "observacao": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get("tipo")
        instrutor = cleaned_data.get("instrutor")
        local = cleaned_data.get("local")
        if tipo == Agendamento.TipoAula.PRATICA and not instrutor:
            self.add_error("instrutor", "Selecione um instrutor para aula prática.")
        if tipo == Agendamento.TipoAula.EXAME and not local:
            self.add_error("local", "Selecione uma clínica para o exame.")
        return cleaned_data

from django import forms


class ResultadoAvaliacaoForm(forms.Form):
    instrutor = forms.CharField(
        label="Instrutor",
        max_length=120,
        widget=forms.Select(
            choices=[
                ("Carlos Silva", "Carlos Silva"),
                ("Maria Santos", "Maria Santos"),
                ("João Pedro", "João Pedro"),
                ("Ana Costa", "Ana Costa"),
            ],
            attrs={"class": "form-select"},
        ),
    )
    nota = forms.DecimalField(
        label="Nota",
        min_value=1,
        max_value=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.5"}),
    )
    comentario = forms.CharField(
        label="Comentário",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "maxlength": 500}),
    )

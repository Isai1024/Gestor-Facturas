from django import forms
from .models import Factura

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['cliente', 'archivo', 'total', 'direccion', 'concepto']
        widgets = {
            'archivo': forms.FileInput(attrs={'accept':'application/pdf'})
        }
    
    def clean_file(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            if not archivo.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Solo se permiten archivos PDF")
        return archivo


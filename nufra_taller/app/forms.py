from django import forms
from .models import CategoriaProducto, DetalleInventario, Empleado, Inventario, Producto, Proveedor


#   REGISTER
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            'rut_empleado',
            'nombre',
            "apellido",
            "username",
            'correo',
            'password',
            'rol',
            "telefono",
            "jefatura"
            ]

        widgets = {
            'rut_empleado': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            "jefatura": forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        rut_empleado = cleaned_data.get('rut_empleado')

        # Validación de duplicidad
        if Empleado.objects.filter(rut_empleado=rut_empleado).exists():
            raise forms.ValidationError(f'un empleado con el rut "{rut_empleado}" ya existe.')

        return cleaned_data
        
#   LOGIN
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'nombre',
            'correo',
            'telefono'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')

        # Validación de duplicidad, excluyendo la instancia actual si existe
        if Proveedor.objects.filter(nombre=nombre).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(f'El proveedor "{nombre}" ya existe.')

        return cleaned_data
    
class CategoriaProductoForm(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields = ['nombre']

        widgets = {
            'nombre' : forms.TextInput(attrs={'class': 'form-control'}),
            }
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')

        # Validación de duplicidad
        if CategoriaProducto.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError(f'la categoria "{nombre}" ya existe.')

        return cleaned_data
    
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'categoria',
            'descripcion',
            'proveedor',
            'precio_venta',
            'precio_compra',
            'imagen',
            ]
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', "style": "height: 100px;"}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')

        # Validación de duplicidad
        if Producto.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError(f'el producto "{nombre}" ya existe.')

        return cleaned_data

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['categoria']

        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

class DetalleInventarioForm(forms.ModelForm):
    class Meta:
        model = DetalleInventario
        fields = ['producto', 'cantidad']

        widgets = {
            'producto': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class VentaForm(forms.Form):
    codigo = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    cantidad = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

from django import forms
from .models import Producto

class RealizarPedido(forms.Form):
    codigo = forms.IntegerField(min_value=1, label="Código del Producto", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cantidad = forms.IntegerField(min_value=1, label="Cantidad", widget=forms.NumberInput(attrs={'class': 'form-control'}),  error_messages={'min_value': 'La cantidad debe ser al menos 1.', })
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad < 1:
            raise forms.ValidationError("La cantidad no puede ser negativa o cero.")
        return cantidad

class SeleccionarProveedorForm(forms.Form):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), empty_label="Seleccione un proveedor", widget=forms.Select(attrs={'class': 'form-control'}))
from django import forms

from standard_backend_app.models import Pedido, Item, Tamanho, Valore

TO_HIDE_ATTRS = {'class': 'hidden', 'size': '40'}


class DropdownModelForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = (('delivery'), ('delivery_address'),)
        widgets = {
            'delivery': forms.Select(choices=Pedido.DELIVERY_OPTION),
            'delivery_address': forms.TextInput(attrs={'size': '40'})
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (('produto'), ('tamanho'),)
        # fields = ('id', 'pedido', 'produto', 'tamanho')
        # fields = ('__all__')

        widgets = {
            'tamanho': forms.Select(attrs={'style': 'width:300px'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tamanho'].queryset = Tamanho.objects.none()
        # self.initial['delivery_address'] = 'Retirada'

        # variants = Variant.objects.all()
        # products = [(i.product.id, i.product.name) for i in variants]

        # print(self.data)

        # for relation in self.data:
        #     print(relation)

        if self.instance.pk:
            print("lá: ")
            # print(self.instance.produto)
            # produto_id = self.instance.produto
            # valores = Valore.objects.using('standard').filter(produto_id=produto_id)
            # self.fields['tamanho'].queryset |= Tamanho.objects.using('standard').filter(valore__in=valores)

        this_range = self.data.get('item_set-TOTAL_FORMS')

        if this_range is not None and this_range.isnumeric():
            this_range = int(this_range)

            for i in range(0, this_range):
                item_set = 'item_set-' + str(i) + '-produto'
                if item_set in self.data:
                    print("aqui tem data")
                    try:
                        print("aqui tem produto")
                        produto_id = self.data.get(item_set)
                        valores = Valore.objects.using('standard').filter(produto_id=produto_id)
                        self.fields['tamanho'].queryset |= Tamanho.objects.using('standard').filter(valore__in=valores)

                        if self.data.get('delivery') == 'withdraw':
                            print("entrou")
                            # (self.fields['delivery_address'].widget).initial_value = 'Retirada'
                            # self.cleaned_data['delivery_address'] = 'Retirada'
                            # self.initial['delivery_address'] = 'Retirada'
                            print("entrou depois")

                        # for relation in self.fields['tamanho'].queryset:
                        #     print(relation)

                        # self.fields['tamanho'].queryset = Tamanho.objects.filter(produto_id=produto_id)
                    except (ValueError):
                        print('ValueError')
                    except (TypeError):
                        print('TypeError')
                        pass  # invalid input from the client; ignore and fallback to empty Tamanho queryset
                elif self.instance.pk:
                    print("lá")
                    self.fields['tamanho'].queryset = self.instance.produto.item_set
                else:
                    print("não achou")

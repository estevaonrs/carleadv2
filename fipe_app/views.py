from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from rest_framework import viewsets
from decimal import Decimal

from fipe_app.serializers import LeadSerializer
from .models import Lead
from .helpers import (
    req, url_marcas, url_modelos, url_ano_modelos, referencias, 
    tipo_veiculo, marcas_desejadas, imagens_marcas
)
from .business import print_session_data, get_fipe_value, calculate_final_price, create_lead


class IndexView(View):
    """
    View para renderizar o template index.
    """

    template_name = 'leads/index.html'

    def get(self, request):
        return render(request, self.template_name)


class ListarMarcasView(View):
    """
    View para listar as marcas de veículos disponíveis na API da FIPE.
    Permite a filtragem de marcas com base em uma busca.
    """

    template_name = 'leads/listar_marcas.html'

    def get(self, request):
        termo_pesquisa = request.GET.get('search', '')

        dados_veiculo_marca = {
            'codigoTabelaReferencia': referencias,
            'codigoTipoVeiculo': tipo_veiculo
        }

        try:
            todas_marcas = req(url_marcas, dados_veiculo_marca)

            marcas_filtradas = [
                {
                    'Label': marca['Label'],
                    'Value': marca['Value'],
                    'Image': imagens_marcas.get(marca['Label'], 'media/brands_images/default.png')
                }
                for marca in todas_marcas if marca['Label'] in marcas_desejadas and (termo_pesquisa.lower() in marca['Label'].lower())
            ]
        except KeyError as e:
            print(f"Erro de chave ao listar as marcas: {e}") #TODO: Tenho que melhorar as mensagens de erro e trocar por logging em todas as views.

        except Exception as e:
            print(f"Erro inesperado ao listar as marcas: {e}")

        return render(request, self.template_name, {'marcas': marcas_filtradas})


class ListarModelosView(View):
    """
    View para listar os modelos da FIPE de veículos baseados na marca selecionada.
    """
        
    template_name = 'leads/listar_modelos.html'

    def post(self, request): 
        try:
            marca_id = request.POST.get('marca_id')
            marca_label = request.POST.get('marca_label')

            dados_veiculo_modelo = {
                'codigoTabelaReferencia': referencias,
                'codigoTipoVeiculo': tipo_veiculo,
                'codigoMarca': marca_id
            }

            modelos = req(url_modelos, dados_veiculo_modelo)

            request.session['marca_id'] = marca_id
            request.session['marca_label'] = marca_label

            return render(request, self.template_name, {'modelos': modelos['Modelos'], 'marca_id': marca_id, 'marca_label': marca_label})

        except KeyError as e:
            print(f"Erro de chave ao listar modelos: {e}")
        
        except Exception as e:
            print(f"Erro inesperado ao listar modelos: {e}")
    
    def get(self, request):
        return render(request, self.template_name)


class ListarAnoModelosView(View):
    """
    View para listar os anos dos modelos de veículos selecionados.
    """

    template_name = 'leads/listar_ano_modelos.html'

    def post(self, request):
        context = {}
        try:
            ano_id = request.POST.get('ano_id')
            modelo_id = request.POST.get('modelo_id')
            marca_id = request.POST.get('marca_id')
            marca_label = request.POST.get('marca_label')
            modelo_label = request.POST.get('modelo_label')

            request.session['marca_id'] = marca_id
            request.session['marca_label'] = marca_label
            request.session['modelo_id'] = modelo_id
            request.session['modelo_label'] = modelo_label
            request.session['ano_id'] = ano_id

            dados_veiculos_ano_modelo = {
                'codigoTabelaReferencia': referencias,
                'codigoTipoVeiculo': tipo_veiculo,
                'codigoMarca': marca_id,
                'codigoModelo': modelo_id
            }

            anos = req(url_ano_modelos, dados_veiculos_ano_modelo)

            if isinstance(anos, list):
                anos_data = [{'label': item['Value'], 'value': item['Label']} for item in anos]
            else:
                context['error_message'] = "Formato de dados inesperado ao carregar anos."
                anos_data = []

            context.update({
                'anos_data': anos_data,
                'modelo_id': modelo_id,
                'marca_id': marca_id,
                'marca_label': marca_label,
                'modelo_label': modelo_label,
            })

            if ano_id:
                return redirect('fipe_app:quilometragem')
            else:
                context['error_message'] = "Ano não selecionado. Por favor, selecione um ano."

        except KeyError as e:
            print(f"Erro de chave ao listar anos dos modelos: {e}")

        except Exception as e:
            print(f"Erro inesperado ao listar anos dos modelos: {e}")

        return render(request, self.template_name, context)

    def get(self, request):
        return render(request, self.template_name)


class QuilometragemView(View):
    """
    View para a inserção da quilometragem do veículo e se o veículo fez todas as revisões na concessionária e se ele está na garantia,
    com base no meu conhecimento de mercado, essas 3 informações são necessárias para realizar a precificação.
    """
    template_name = 'leads/quilometragem.html'

    def post(self, request):
        error_message = ""
        try:
            mileage = request.POST.get('mileage')
            revisions_done = request.POST.get('revisions_done') == 'true'
            under_warranty = request.POST.get('under_warranty') == 'true'

            if mileage:
                request.session['mileage'] = float(mileage)
                request.session['revisions_done'] = revisions_done
                request.session['under_warranty'] = under_warranty

                marca_id = request.session.get('marca_id')
                modelo_id = request.session.get('modelo_id')
                ano_id = request.session.get('ano_id')

                if marca_id and modelo_id and ano_id:
                    return redirect('fipe_app:criar_lead')
                else:
                    raise KeyError("Dados de marca, modelo ou ano ausentes na sessão.")
            else:
                raise ValueError("Quilometragem não foi fornecida.")

        except KeyError as e:
            print(f"Erro de chave na quilometragem: {e}")
            error_message = "Informações sobre o veículo estão incompletas. Por favor, tente novamente."

        except ValueError as e:
            print(f"Erro de valor na quilometragem: {e}")
            error_message = "Quilometragem inválida. Por favor, insira um valor válido."

        except Exception as e:
            print(f"Erro inesperado na quilometragem: {e}")
            error_message = "Ocorreu um erro inesperado. Tente novamente."

        return render(request, self.template_name, {'error_message': error_message})
    
    def get(self, request):
        return render(request, self.template_name)


class CriarLeadView(View):
    """
    View para a criação de um lead com base nos dados do veículo e preço calculado, para que o vendedor possa entrar em contato com o usuário e realizar a compra do veículo.
    """
        
    template_name = 'leads/criar_lead.html'

    def post(self, request):
        marca_id = request.session.get('marca_id')
        modelo_id = request.session.get('modelo_id')
        ano_id = request.session.get('ano_id')
        marca_label = request.session.get('marca_label')
        modelo_label = request.session.get('modelo_label')

        if not ano_id:
            return redirect('fipe_app:quilometragem')

        mileage = Decimal(request.session.get('mileage', '0'))
        revisions_done = request.session.get('revisions_done', False)
        under_warranty = request.session.get('under_warranty', False)

        print_session_data(marca_id, marca_label, modelo_id, modelo_label, ano_id, mileage, revisions_done, under_warranty)

        try:
            ano_modelo, fuel_id = ano_id.split(' ', 1)
        except ValueError:
            print("Formato de ano inválido.")
            return redirect('fipe_app:quilometragem')

        try:
            valor_fipe, fuel_id = get_fipe_value(ano_modelo, marca_id, modelo_id)

        except Exception as e:
            print(f"Erro ao obter valor da FIPE: {e}")
            return redirect('fipe_app:quilometragem')

        try:
            final_price, percentage, market_category = calculate_final_price(
                valor_fipe,
                mileage,
                revisions_done,
                under_warranty,
                modelo_id,
                fuel_id
            )
        except Exception as e:
            print(f"Erro ao calcular preço final: {e}")
            return redirect('fipe_app:quilometragem')

        try:
            lead = create_lead(
                request,
                marca_label,
                modelo_label,
                ano_id,
                fuel_id,
                final_price,
                valor_fipe,
                percentage,
                revisions_done,
                under_warranty
            )
        except Exception as e:
            print(f"Erro ao criar lead: {e}")
            return redirect('fipe_app:quilometragem')

        request.session.flush()

        return redirect('fipe_app:show_price', lead_id=lead.id)
    
    def get(self, request):
        return render(request, self.template_name)


class MostrarPrecificacaoView(View):
    """
    View para exibir a precificação de um lead específico.
    """
        
    template_name = 'leads/mostrar_precificacao.html'

    def get(self, request, lead_id):
        try:
            lead = get_object_or_404(Lead, id=lead_id)
            return render(request, self.template_name, {'lead': lead})
        
        except Exception as e:
            print(f"Erro ao mostrar precificação: {e}")
            return render(request, self.template_name, {'error_message': "Erro ao obter os dados do lead."})
        

class LeadViewSet(viewsets.ModelViewSet):
    """
    API para listar, criar, editar e deletar leads.
    """
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer


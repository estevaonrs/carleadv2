from .helpers import req, url_todos_parametros, referencias
from decimal import Decimal, InvalidOperation
from .models import Lead
import locale

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
    except locale.Error:
        print("Erro ao definir a localidade. Usando formatação de moeda padrão.")


def print_session_data(marca_id, marca_label, modelo_id, modelo_label, ano_id, mileage, revisions_done, under_warranty):
    """
    Exibe os dados da sessão para depuração.
    """
    print("Dados da sessão:")
    print("Marca ID:", marca_id)
    print("Marca LABEL:", marca_label)
    print("Modelo ID:", modelo_id)
    print("Modelo LABEL:", modelo_label)
    print("Ano ID:", ano_id)
    print("Quilometragem:", mileage)
    print("Revisões feitas:", revisions_done)
    print("Na garantia:", under_warranty)


def get_fipe_value(ano_id, marca_id, modelo_id):
    """
    Obtém o valor FIPE do veículo baseado em seu ano, marca e modelo.
    """
    try:
        ano_id = ano_id.strip()
        if ' ' in ano_id:
            ano_modelo, fuel_id = ano_id.split(' ', 1) 
        else:
            ano_modelo = ano_id
            fuel_id = '1'  

        dados_veiculos_ano_modelo = {
            'codigoTabelaReferencia': referencias,
            'codigoTipoVeiculo': 1,
            'codigoMarca': marca_id,
            'codigoModelo': modelo_id,
            'ano': ano_id,
            'anoModelo': ano_modelo,
            'codigoTipoCombustivel': fuel_id,
            'tipoConsulta': 'tradicional'
        }

        response = req(url_todos_parametros, dados_veiculos_ano_modelo)
        valor_fipe = Decimal(response.get('Valor', '0.00').replace('R$', '').replace('.', '').replace(',', '.'))
        return valor_fipe, fuel_id
    except (KeyError, ValueError, InvalidOperation) as e:
        print(f"Erro ao calcular o valor da FIPE: {e}")
        return Decimal('0.00'), '1'


def calculate_final_price(valor_fipe, mileage, revisions_done, under_warranty, modelo_id, fuel_id):
    """
    Calcula o preço final de mercado do veículo baseado no valor FIPE e outras variáveis.
    """
    try:
        km_brackets = [
            (0, 9999, Decimal('0.82')),
            (10000, 19999, Decimal('0.80')),
            (20000, 29999, Decimal('0.79')),
            (30000, 49999, Decimal('0.78')),
            (50000, 59999, Decimal('0.77')),
            (60000, 74999, Decimal('0.72')),
            (75000, 99999, Decimal('0.62')),
            (100000, 130000, Decimal('0.60')),
        ]
        
        percentage = next((perc for min_km, max_km, perc in km_brackets if min_km <= mileage <= max_km), Decimal('0.60'))

        if revisions_done:
            percentage += Decimal('0.01')
        if under_warranty:
            percentage += Decimal('0.02')

        market_category = adjust_percentage_by_model(modelo_id, fuel_id, percentage)

        final_price = valor_fipe * percentage
        print("\nPreço final calculado:", final_price)
        return final_price, percentage, market_category
    except Exception as e:
        print(f"Erro ao calcular o preço final: {e}")
        return Decimal('0.00'), Decimal('0.00'), 'Comum'


def adjust_percentage_by_model(modelo_id, fuel_id, percentage):
    """
    Ajusta a porcentagem do preço com base no modelo e combustível do veículo.
    """
    try:
        ruim_mercado = ['NSX 3.0']
        queimados = ['Integra GS 1.8']
        valorizar_modelos = ['MARRUÁ AM 100 2.8 CD TDI Diesel']

        market_category = "Comum"
        if modelo_id in ruim_mercado:
            percentage -= Decimal('0.10')
            market_category = 'Ruim de mercado'
        elif modelo_id in queimados:
            percentage -= Decimal('0.30')
            market_category = 'Mercado Queimado'
        elif modelo_id in valorizar_modelos:
            percentage += Decimal('0.02')
            market_category = 'Modelo valorizado'

        if fuel_id.lower() == 'diesel':
            percentage -= Decimal('0.10')
            market_category = 'Diesel'

        return market_category
    except Exception as e:
        print(f"Erro ao ajustar a porcentagem por modelo: {e}")
        return 'Comum'


def create_lead(request, marca_label, modelo_label, ano_id, fuel_id, final_price, valor_fipe, percentage, revisions_done, under_warranty):
    """
    Cria um novo registro de lead no banco de dados.
    """
    try:
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        lead = Lead.objects.create(
            name=name,
            email=email,
            phone=phone,
            mileage=request.session.get('mileage', '0'),
            brand=marca_label,
            model=modelo_label,
            year=ano_id,
            fuel=fuel_id,
            price=final_price,
            market_category='Comum',
            car_category='Salão',
            original_price=valor_fipe,
            pricing_percentage=percentage,
            revisions_done_in_css=revisions_done,
            under_warranty=under_warranty
        )
        return lead
    except Exception as e:
        print(f"Erro ao criar lead: {e}")
        return None


def format_currency(value):
    """
    Formata um valor numérico como moeda no formato brasileiro.
    """
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
        except locale.Error:
            print("Erro ao definir a localidade para formatação de moeda.")
    try:
        return locale.currency(value, grouping=True)
    except (ValueError, TypeError) as e:
        print(f"Erro ao formatar o valor {value} como moeda: {e}")
        return str(value)


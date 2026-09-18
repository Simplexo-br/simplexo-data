"simplexo_data"""
from typing import Dict, List, Any, Optional

CNAE_SEGMENTS: Dict[str, Dict[str, Any]] = {
    "tecnologia": {
        "id": "tecnologia",
        "label": "Tecnologia, Software & TI",
        "icon": "fa-solid fa-laptop-code",
        "description": "Desenvolvimento de software, SaaS, consultoria em TI, hospedagem e servicos de dados",
        "cnaes": ["6201", "6202", "6203", "6204", "6209", "6311", "6319", "5829"]
    },
    "agro": {
        "id": "agro",
        "label": "Agronegócio & Agroindústria",
        "icon": "fa-solid fa-wheat-awn",
        "description": "Cultivo agrícola, pecuária, produção florestal, insumos e processamento agropecuário",
        "cnaes": ["0111", "0112", "0113", "0115", "0116", "0119", "0121", "0122", "0131", "0132", "0133", "0134", "0139", "0141", "0142", "0151", "0152", "0153", "0154", "0155", "0159", "0161", "0162", "0163", "0210", "0220", "0230", "0311", "0312", "0321", "0322", "4623", "4622", "4611", "1011", "1012", "1013"]
    },
    "construcao": {
        "id": "construcao",
        "label": "Construção Civil, Obras & Imóveis",
        "icon": "fa-solid fa-helmet-safety",
        "description": "Construção de edifícios, infraestrutura, loteamentos, incorporação e serviços especializados",
        "cnaes": ["4110", "4120", "4211", "4212", "4213", "4221", "4222", "4223", "4291", "4292", "4299", "4311", "4312", "4313", "4319", "4321", "4322", "4329", "4330", "4391", "4399", "6810", "6821", "6822", "7112"]
    },
    "saude": {
        "id": "saude",
        "label": "Saúde, Clínicas, Farmácia & Medicina",
        "icon": "fa-solid fa-heart-pulse",
        "description": "Hospitais, clínicas médicas/odontológicas, laboratórios, farmácias e fabricação de medicamentos",
        "cnaes": ["8610", "8621", "8622", "8630", "8640", "8650", "8660", "8690", "8711", "8712", "8720", "8730", "4771", "4773", "4644", "4645", "2110", "2121", "2122", "2123", "3250"]
    },
    "industria": {
        "id": "industria",
        "label": "Indústria & Manufatura",
        "icon": "fa-solid fa-industry",
        "description": "Metalurgia, químicos, plásticos, máquinas, equipamentos, têxtil e transformação industrial",
        "cnaes": ["13", "14", "15", "16", "17", "18", "20", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33"]
    },
    "logistica":{
        "id": "logistica",
        "label": "Logística, Frotas & Transporte",
        "icon": "fa-solid fa-truck-fast",
        "description": "Transporte rodoviário de cargas, armazenagem, operadores logísticos, courrier e fretes",
        "cnaes": ["4930", "4911", "4912", "4921", "4922", "4923", "4924", "4929", "5011", "5012", "5021", "5022", "5030", "5111", "5112", "5120", "5211", "5212", "5221", "5222", "5223", "5224", "5229", "5231", "5232", "5239", "5240", "5250", "5310", "5320"]
    },
    "varejo": {
        "id": "varejo",
        "label": "Comércio Varejista & E-commerce",
        "icon": "fa-solid fa-cart-shopping",
        "description": "Lojas físicas, comércio eletrônico, supermercados, vestuário, materiais de construção e eletrônicos",
        "cnaes": ["4711", "4712", "4713", "4721", "4722", "4723", "4724", "4729", "4731", "4732", "4741", "4742", "4743", "4744", "4751", "4752", "4753", "4754", "4755", "4756", "4757", "4759", "4761", "4762", "4763", "4771", "4772", "4773", "4774", "4781", "4782", "4783", "4784", "4785", "4789", "4790"]
    },
    "atacado": {
        "id": "atacado",
        "label": "Comércio Atacadista & Distribuição",
        "icon": "fa-solid fa-boxes-stacked",
        "description": "Distribuidores, atacadistas de alimentos, autopeças, químicos, insumos e bens de consumo",
        "cnaes": ["4611", "4612", "4613", "4614", "4615", "4616", "4617", "4618", "4619", "4621", "4622", "4623", "4631", "4632", "4633", "4634", "4635", "4636", "4637", "4639", "4641", "4642", "4643", "4644", "4645", "4646", "4647", "4649", "4651", "4652", "4661", "4662", "4663", "4664", "4665", "4669", "4671", "4672", "4673", "4674", "4679", "4681", "4682", "4683", "4684", "4685", "4686", "4687", "4689", "4691", "4692", "4693"]
    },
    "financeiro": {
        "id": "financeiro",
        "label": "Serviços Financeiros, Fintechs & Seguros",
        "icon": "fa-solid fa-building-columns",
        "description": "Bancos, factorings, FIDCs, corretoras de seguros, fintechs de crédito e meios de pagamento",
        "cnaes": ["6410", "6421", "6422", "6423", "6431", "6432", "6433", "6434", "6435", "6436", "6437", "6440", "6450", "6461", "6462", "6463", "6470", "6491", "6492", "6493", "6499", "6511", "6512", "6520", "6530", "6541", "6542", "6550", "6611", "6612", "6613", "6619", "6621", "6622", "6629", "6630"]
    },
    "educacao": {
        "id": "educacao",
        "label": "Educação, Treinamentos & EdTechs",
        "icon": "fa-solid fa-graduation-cap",
        "description": "Escolas, faculdades, universidades, cursos preparatórios, idiomas e plataformas de EAD",
        "cnaes": ["8511", "8512", "8513", "8520", "8531", "8532", "8533", "8541", "8542", "8550", "8591", "8592", "8593", "8599"]
    },
    "consultoria": {
        "id": "consultoria",
        "label": "Consultoria, Jurídico & Contabilidade",
        "icon": "fa-solid fa-briefcase",
        "description": "Escritórios de advogacia, consultoria empresarial, contabilidade, auditoria e publicidade/marketing",
        "cnaes": ["6911", "6912", "6920", "7020", "7111", "7112", "7119", "7120", "7210", "7220", "7311", "7312", "7319", "7320", "7410", "7420", "7490", "7810", "7820", "7830", "8211", "8219", "8220", "8291", "8299"]
    },
    "alimentos": {
        "id": "alimentos",
        "label": "Alimentos, Gastronomia & Bebidas",
        "icon": "fa-solid fa-utensils",
        "description": "Restaurantes, lanchonetes, bares, buffets, catering e indéstrias alimentícias e de bebidas",
        "cnaes": ["5611", "5612", "5620", "1011", "1012", "1013", "1020", "1031", "1032", "1033", "1041", "1042", "1043", "1051", "1052", "1053", "1061", "1062", "1063", "1064", "1065", "1066", "1069", "1071", "1072", "1081", "1082", "1091", "1092", "1093", "1094", "1095", "1096", "1099", "1111", "1112", "1113", "1121", "1122"]
    },
    "energia": {
        "id": "energia",
        "label": "Energia, Combustíveis & Telecom",
        "icon": "fa-solid fa-bolt",
        "description": "Geração solar/eólica, distribuição elétrica, postos de combustíveis e operadoras de telecom",
        "cnaes": ["3511", "3512", "3513", "3514", "3520", "3530", "1921", "1922", "4681", "4731", "6110", "6120", "6130", "6140", "6190"]
    },
    "turismo": {
        "id": "turismo",
        "label": "Hotelaria, Eventos & Turismo",
        "icon": "fa-solid fa-plane-departure",
        "description": "Hotéis, pousadas, agências de viagens, produtoras de eventos, feiras e congressos",
        "cnaes": ["5510", "5590", "7911", "7912", "7990", "8230", "9001", "9002", "9003", "9311", "9319", "9321", "9329"]
    }
}

POPULAR_CNAES = [
    {"code": "6201-5/01", "clean": "6201501", "desc": "Desenvolvimento de programas de computador sob encomenda", "segment": "tecnologia"},
    {"code": "6202-3/00", "clean": "6202300", "desc": "Desenvolvimento e licenciamento de programas de computador customizáveis", "segment": "tecnologia"},
    {"code": "6203-1/00", "clean": "6203100", "desc": "Desenvolvimento de programas de computador não-customizáveis", "segment": "tecnologia"},
    {"code": "6204-0/00", "clean": "6204000", "desc": "Consultoria em tecnologia da informção", "segment": "tecnologia"},
    {"code": "6209-1/00", "clean": "6209100", "desc": "Suporte técnico, manutenção e outros serviços em tecnologia da informção", "segment": "tecnologia"},
    {"code": "6311-9/00", "clean": "6311900", "desc": "Tratamento de dados, provedores de serviços de aplicação e hospedagem na internet", "segment": "tecnologia"},
    {"code": "4120-4/00", "clean": "4120400", "desc": "Construção de edifícios", "segment": "construcao"},
    {"code": "4110-7/00", "clean": "4110700", "desc": "Incorporação de empreendimentos imobiliários", "segment": "construcao"},
    {"code": "4321-5/00", "clean": "4321500", "desc": "Instalação e manutenção elétrica", "segment": "construcao"},
    {"code": "4930-2/02", "clean": "4930202", "desc": "Transporte rodoviário de carga, exceto produtos perigosos e mudanças, intermunicipal e interestadual", "segment": "logistica"},
    {"code": "4930-2/01", "clean": "4930201", "desc": "Transporte rodoviário de carga, exceto produtos perigosos e mudanças, municipal", "segment": "logistica"},
    {"code": "5250-8/04", "clean": "5250804", "desc": "Organização logística do transporte de carga", "segment": "logistica"},
    {"code": "4644-3/01", "clean": "4644301", "desc": "Comércio atacadista de medicamentos e drogas de uso humano", "segment": "saude"},
    {"code": "8630-5/03", "clean": "8630503", "desc": "Atividade médica ambulatorial restrita a consultas", "segment": "saude"},
    {"code": "8640-2/02", "clean": "8640202", "desc": "Laboratórios clínicos", "segment": "saude"},
    {"code": "4711-3/02", "clean": "4711302", "desc": "Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - supermercados", "segment": "varejo"},
    {"code": "4781-4/00", "clean": "4781400", "desc": "Comércio varejista de artigos do vestuário e acessórios", "segment": "varejo"},
    {"code": "4639-7/01", "clean": "4639701", "desc": "Comércio atacadista de produtos alimentícios em geral", "segment": "atacado"},
    {"code": "7020-4/00", "clean": "7020400", "desc": "Atividades de consultoria em gestão empresarial, exceto consultoria técnica específica", "segment": "consultoria"},
    {"code": "6920-6/01", "clean": "6920601", "desc": "Atividades de contabilidade", "segment": "consultoria"},
    {"code": "6911-7/01", "clean": "6911701", "desc": "Advocacia", "segment": "consultoria"},
    {"code": "7311-4/00", "clean": "7311400", "desc": "Agências de publicidade", "segment": "consultoria"},
    {"code": "5611-2/01", "clean": "5611201", "desc": "Restaurantes e similares", "segment": "alimentos"},
    {"code": "0111-3/01", "clean": "0111301", "desc": "Cultivo de arroz", "segment": "agro"},
    {"code": "0115-6/00", "clean": "0115600", "desc": "Cultivo de soja", "segment": "agro"},
    {"code": "0151-2/01", "clean": "0151201", "desc": "Criação de bovinos para corte", "segment": "agro"}
]

def get_cnaes_for_segment(segment_id: str) -> List[str]:
    """Returns list of CNAE prefixes associated with a segment."""
    seg = CNAE_SEGMENTS.get(segment_id.lower().strip())
    if seg:
        return seg['cnaes']
    return []

def get_available_segments() -> List[Dict[str, Any]]:
    """Returns list of all available market segments."""
    return list(CNAE_SEGMENTS.values())

def search_popular_cnaes(term: str) -> List[Dict[str, Any]]:
    """Search popular CNAEs by code or description."""
    t = term.lower().strip()
    return [
        c for c in POPULAR_CNAES
        if t in c["code"].lower() or t in c["clean"] or t in c["desc"].lower() or t in c["segment"].lower()
    ]

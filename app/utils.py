import tldextract



def extract_domain_from_url(url):
    """
    Функция для извлечения домена из переданной ссылки.
    Аргументы: url - переданная ссылка в виде строки
    
    """
    extracted = tldextract.extract(url)
    domain = extracted.domain + "." + extracted.suffix
    return domain




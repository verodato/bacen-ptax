import requests


class RequestPTAX:
    _user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
    _content_type = 'application/x-www-form-urlencoded'
    _accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9 '

    def __init__(self, request_data):
        self._request_data = request_data
        self._url_base = 'https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=exibeFormularioConsultaBoletim'
        self._url_ptax_daily = 'https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=consultarBoletim'
        self._payload = f'RadOpcao=3&DATAINI={self._request_data}&DATAFIM=&ChkMoeda=61'

        self.web = requests.session()
        self.web.headers['user-agent'] = RequestPTAX._user_agent
        self.web.headers['Content-Type'] = RequestPTAX._content_type
        self.web.headers['Accept'] = RequestPTAX._accept

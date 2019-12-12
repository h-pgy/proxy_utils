#organizes set of utility functions for the project
import os
from requests.exceptions import InvalidProxyURL
from config import RedePmsp


class ProxySetter:
    '''Recebe um objeto do tipo Rede que contem as configurações de rede,
    gera as URIs necessárias para configuração do proxy e configura
    as variáveis de ambiente de proxy com as uris geradas'''

    @classmethod
    def __proxy_uri_solver(cls, *ignore, **params):

        try:
            uri = (f"http{params['https']}://{params['user']}:{params['passw']}@"
                    f"{params['domain']}:{params['port']}")
        except KeyError as key:
            raise InvalidProxyURL(f'O parâmetro {key} deve ser fornecido')
        return uri

    @classmethod
    def __get_proxy_uri(cls, rede_obj, https = False):

        if https:
            https = 's'
        else:
            https = ''
        params = dict(
            https = https,
            user = rede_obj.user,
            passw = rede_obj.passw,
            domain = rede_obj.domain,
            port = rede_obj.port)

        proxy_uri = cls.__proxy_uri_solver(**params)

        return proxy_uri
    @classmethod
    def update_condarc(cls, uri_http, uri_https, user):

        content = (
            'proxy_servers:'
            '\n    http: {http}'
            '\n    https: {https}'
        )

        content = content.format(http = uri_http, https = uri_https)

        file_path = fr'C:/Users/{user}/.condarc'

        with open(file_path, 'w') as f:
            f.write(content)

    @classmethod
    def update_gitconfig(cls, uri_http, uri_https, user,
                        git_name = 'h-pgy', git_email = 'hpougy@gmail.com'):

        content = (
            '[user]'
            '\n        name = {name}'
            '\n        email = {email}'
            '\n[http]'
            '\n        proxy = {http}'
            '\n[https]'
            '\n        proxy = {https}'
        )

        content = content.format(http=uri_http, https=uri_https,
                                 name=git_name, email = git_email)

        file_path = fr'C:\Users\{user}\.gitconfig'

        with open(file_path, 'w') as f:
            f.write(content)

    @classmethod
    def set_environ(cls, uri_http, uri_https):

        os.environ['HTTPS_PROXY'] = uri_https
        os.environ['HTTP_PROXY'] = uri_http

    @classmethod
    def set_pip_config(cls, uri_htpp):

        content = (
            '[global]\n'
            'proxy = ' + uri_htpp
        )

        if not os.path.exists(r'C:\Users\d835916\AppData\Roaming\pip'):
            os.mkdir(r'C:\Users\d835916\AppData\Roaming\pip')
        with open(r'C:\Users\d835916\AppData\Roaming\pip\pip.ini', 'w') as f:
            f.write(content)

    @classmethod
    def set_venv_proxy_variables(cls, uri_http, ui_https):

        os.system(r'.\venv\Scripts\activate')
        os.system(f"set HTTP_PROXY={uri_http}")
        os.system(f"set HTTPS_PROXY={ui_https}")

    @classmethod
    def set_proxy(cls, rede_obj):

        uri_http = cls.__get_proxy_uri(rede_obj, https = False)
        uri_https = cls.__get_proxy_uri(rede_obj, https = True)

        cls.set_environ(uri_http, uri_https)
        cls.update_condarc(uri_http, uri_https, rede_obj.user)
        cls.update_gitconfig(uri_http, uri_https, rede_obj.user)
        cls.set_pip_config(uri_http)
        cls.set_venv_proxy_variables(uri_http, uri_https)
        quit()

if __name__ == "__main__":

   ProxySetter.set_proxy(RedePmsp)







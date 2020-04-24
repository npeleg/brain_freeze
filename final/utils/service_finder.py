from furl import furl as f


def find_service(url, services_dict):
    parsed_url = f(url)
    for scheme, cls in services_dict.items():
        if parsed_url.scheme.startswith(scheme):
            return cls(parsed_url.host)
    raise ValueError(f'invalid url: {url}')

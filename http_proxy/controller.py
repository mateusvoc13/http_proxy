from http_proxy.models import ProxyStatus


_main_status_id = 1


def current_number_of_requests():
    return select_status_object().request_count if select_status_object() else 0


def select_status_object():
    return ProxyStatus.objects.filter(id=_main_status_id).first()


def update_proxy_status():
    """
    Increases the proxy counter with based on the requests sent to the Proxy.
    """
    main_status_object = select_status_object()
    if main_status_object:
        main_status_object.increment_number_of_requests()

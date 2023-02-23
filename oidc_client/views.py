from django.shortcuts import render
from idpyoidc.client.exception import OidcServiceError
from idpyoidc.client.rp_handler import RPHandler
from django.conf import settings

rph = RPHandler(settings.RP_CONFIG.rp.base_url,
                settings.RP_CONFIG.rp.clients,
                httpc_params=settings.RP_CONFIG.rp.conf['httpc_params'])


def welcome(request):
    result = rph.begin('oidc-test-client')
    request.session['state'] = result["state"]

    context = {
        "authorization_url": result['url']
    }

    return render(request, "welcome.html", context)


def home(request):
    if request.session['state'] != request.GET.get("state"):
        return render(request, "home.html", {"message": "Unknown State"})

    try:
        res = rph.finalize('https://proxy.aai.geant.org', request.GET)
    except OidcServiceError as excp:
        return excp.__str__(), 403
    except Exception as excp:
        raise excp

    context = {
        "userinfo": res['userinfo'],
        "access_token": res['token'],
        "id_token": res["id_token"]
    }

    return render(request, "home.html", context)
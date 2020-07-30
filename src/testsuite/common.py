from django.shortcuts import render


def page_not_found_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)


def permission_denied_403(request, exception):
    return render(request, '403.html', status=403)


def bad_request_400(request, exception):
    return render(request, '400.html', status=400)

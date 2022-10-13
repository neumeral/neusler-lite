from datetime import date


def default(request):
    return {"today": date.today()}

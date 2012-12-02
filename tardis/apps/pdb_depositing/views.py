from django.http import HttpResponse


def view(request, dataset_file_id):
    return HttpResponse("Yo")

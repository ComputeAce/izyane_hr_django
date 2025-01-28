from django.shortcuts import render

def leave_request(request):
    return render(request, 'base/leave_request.html')




from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.shortcuts import redirect


def redirect_to_main(request):
    return redirect('/humidex')

def index(request):
    return render(request, 'humidex/index.html', {})

def room(request, room_name):
    return render(request, 'humidex/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


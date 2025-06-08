import random
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Draw, Ticket

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def home_view(request):
    return HttpResponse(
        "<h1>VK Draw Bot</h1><p><a href='/admin/'>Перейти в админку</a></p>"
    )

@login_required(login_url="/admin/login/")
def draw_page(request, pk):
    draw = get_object_or_404(Draw, pk=pk)
    return render(request, "draw_page.html", {"draw": draw})

@login_required(login_url="/admin/login/")
def run_draw(request, pk):
    draw = get_object_or_404(Draw, pk=pk)

    if draw.winners.exists():
        messages.warning(request, "Розыгрыш уже проведён.")
        return redirect("draw_page", pk=pk)

    total_winners = draw.total_winners
    available_tickets = list(Ticket.objects.exclude(draws__in=[draw]))

    if len(available_tickets) < total_winners:
        messages.error(
            request,
            f"Недостаточно билетов для розыгрыша ({len(available_tickets)} доступно).",
        )
        return redirect("draw_page", pk=pk)

    winners = random.sample(available_tickets, total_winners)
    draw.winners.set(winners)
    messages.success(request, "Розыгрыш завершён! Победители выбраны.")
    return redirect("draw_page", pk=pk)

from django.shortcuts import render,redirect,get_object_or_404
from .models import Ticket
from .forms import Ticketcreateform,TicketCommentForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
def ticket_create(request):
    ticket=None
    if request.method == 'POST':
        form = Ticketcreateform(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user.profile
            ticket.save()
    else:
        form = Ticketcreateform()
    return render(
        request,
        'ticket/ticket.html',
        {'form': form,'ticket':ticket}
    )
@login_required
def ticket_detail(request, id):
    ticket = get_object_or_404(
        Ticket,
        id=id
    )
    if not request.user.is_staff and ticket.user != request.user.profile:
        return HttpResponseForbidden("You are not allowed to view this ticket.")
    if request.method == "POST":
        form = TicketCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user.profile
            comment.save()
            return redirect(
                "ticket:ticket_detail",
                id=ticket.id,
            )
    else:
        form = TicketCommentForm()
    return render(
        request,
        "ticket/detail.html",
        {
            "section": "ticket",
            "ticket": ticket,
            "form": form,
        },
    )
# Create your views here.

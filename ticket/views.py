from django.shortcuts import render,redirect,get_object_or_404
from .models import Ticket
from .forms import Ticketcreateform,TicketCommentForm,TicketUpdateForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
@login_required
def delete_ticket(request, id):
    ticket = get_object_or_404(
        Ticket,
        id=id,
        user=request.user.profile
    )
    if request.method == "POST":
        if ticket.status != "Open":
            messages.error(
                request,
                "Only Open tickets can be deleted."
            )
            return redirect(request.GET.get("next") or request.POST.get("next") or "myticket")
        ticket.delete()
        messages.success(
            request,
            "Ticket deleted successfully."
        )
        return redirect(request.GET.get("next") or request.POST.get("next") or "myticket")
    
    return render(
        request,
        "ticket/delete_ticket.html",
        {
            "ticket": ticket
        }
    )
@login_required
def ticket_edit(request,id):
    ticket = get_object_or_404(
        Ticket,
        id=id,
        user=request.user.profile
    )
    if request.method == "POST":
        ticket_form = TicketUpdateForm(
            request.POST,
            request.FILES,
            instance=ticket
        )
        if ticket_form.is_valid():
            ticket_form.save()
            messages.success(
                request,
                "Your ticket has been updated successfully."
            )
            return redirect("ticket:ticket_detail", id=ticket.id)
        else:
            messages.error(
                request,
                "Please correct the errors below."
            )
    else:
        ticket_form = TicketUpdateForm(
            instance=ticket
        )
    return render(
        request,
        "ticket/edit.html",
        {
            "ticket_form": ticket_form,
             "ticket": ticket,
        }
    )
# Create your views here.

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from .models import Profile
from ticket.models import Ticket
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import Q
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})
@login_required
def dashboard(request):
    if request.user.is_staff:
        tickets = Ticket.objects.all().order_by('-created')
    else:
        tickets = Ticket.objects.filter(
            user=request.user.profile
        ).order_by('-created')
    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard',
         "tickets": tickets,
        }
    )
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # Save the User object
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(
               request,
               'account/register_done.html',
               {'new_user': new_user}
           )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'account/register.html',
        {'user_form': user_form}
    )
@login_required
def profile_view(request, username):
    user = get_object_or_404(User,username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    if request.user.is_staff:
        tickets = Ticket.objects.all().order_by("-created")
    else:
        tickets = Ticket.objects.filter(
            user=profile
        ).order_by("-created")

    total_tickets = tickets.count()
    open_tickets = tickets.filter(status='Open').count()
    in_progress = tickets.filter(status='In Progress').count()
    resolved = tickets.filter(status='Resolved').count()
    closed = tickets.filter(status='Closed').count()

    context = {
        'profile': profile,
        'tickets': tickets,
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'in_progress': in_progress,
        'resolved': resolved,
        'closed': closed,
        'section': 'profile',
    }

    return render(
        request,
        "account/profile.html",
        context
    )
@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request,
                "Your profile has been updated successfully."
            )
            return redirect(
                "profile",
                username=request.user.username
            )
        else:
            messages.error(
                request,
                "Please correct the errors below."
            )
    else:

        user_form = UserUpdateForm(
            instance=request.user
        )
        profile_form = ProfileUpdateForm(
            instance=request.user.profile
        )
    return render(
        request,
        "account/edit.html",
        {
            "section": "profile",
            "user_form": user_form,
            "profile_form": profile_form,
        }
    )
def myticket(request):
    tickets = Ticket.objects.filter(
        user=request.user.profile
    ).order_by('-created')

    return render(
        request,
        "account/myticket.html",
        {
            "tickets": tickets,
            "section": "tickets",
        }
    )
@staff_member_required
def manage_tickets(request):
    tickets = Ticket.objects.all().order_by("-created")
    return render(
        request,
        "account/manage_tickets.html",
        {
            "tickets": tickets,
            "section": "manage",
        }
    )
@staff_member_required
def manage_ticket_detail(request, id):
    ticket = get_object_or_404(
        Ticket,
        id=id
    )
    return render(
        request,
        "account/manage_ticket_detail.html",
        {
            "ticket": ticket,
            "section": "manage",
        }
    )
@login_required
def ticket_status_api(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id, user__user=request.user).first()
    if not ticket:
        return JsonResponse({"error": "Not found"}, status=404)
    return JsonResponse({
        "id": ticket.id,
        "status": ticket.status,
    })
@staff_member_required
def update_ticket_status(request, id):
    ticket = get_object_or_404(
        Ticket,
        id=id
    )
    if request.method == "POST":
        ticket.status = request.POST.get("status")
        ticket.save()
    return redirect(request.META.get('HTTP_REFERER', 'manage_tickets'))
@login_required
def search_ticket(request):
    query = request.GET.get("search", "").strip()
    if not query:
        return redirect("dashboard")
    if request.user.is_staff:
        ticket = Ticket.objects.filter(
            Q(ticket_number__icontains=query) |
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).first()
        if ticket:
            return redirect("manage_ticket_detail", id=ticket.id)

    else:
        ticket = Ticket.objects.filter(
            user=request.user.profile
        ).filter(
            Q(ticket_number__icontains=query) |
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).first()
        if ticket:
            return redirect("ticket:ticket_detail", id=ticket.id)
    messages.error(request, "No ticket found.")
    return redirect("dashboard")
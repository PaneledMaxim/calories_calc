from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse

from .models import CustomUser

from .forms import CustomUserChangeForm, CustomUserCreationForm


def home_view(request):
    return render(request, "home.html")


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("accounts:home")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_view(request):
    return redirect("accounts:profile_detail", username=request.user.username)


@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлен.")
            return redirect("accounts:profile_detail", username=request.user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, "accounts/profile_form.html", {"form": form})


@login_required
def users_list_view(request):
    query = request.GET.get("q", "").strip()
    users = CustomUser.objects.all().order_by("username")
    friend_ids = set(request.user.friends.values_list("id", flat=True))

    if query:
        users = users.filter(
            Q(username__icontains=query)
            | Q(email__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )

    context = {
        "users": users,
        "query": query,
        "friend_ids": friend_ids,
    }
    return render(request, "accounts/users_list.html", context)


@login_required
def profile_detail_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    is_friend = request.user.friends.filter(pk=profile_user.pk).exists()

    if profile_user != request.user and not is_friend:
        raise PermissionDenied(
            "Вы можете просматривать только свою собственную страницу и профили своих друзей."
        )

    return render(
        request,
        "accounts/profile_detail.html",
        {
            "profile_user": profile_user,
            "is_own_profile": request.user == profile_user,
            "is_friend": is_friend,
            "can_add_friend": request.user != profile_user and not is_friend,
            "friends": profile_user.friends.order_by("username"),
        },
    )


@login_required
def add_friend_view(request, username):
    friend = get_object_or_404(CustomUser, username=username)

    if friend == request.user:
        messages.warning(request, "Нельзя добавить в друзья самого себя.")
    else:
        request.user.friends.add(friend)
        messages.success(request, f"Пользователь {friend.username} добавлен в друзья.")

    return redirect("accounts:profile_detail", username=friend.username)


def custom_page_not_found(request, exception):
    return TemplateResponse(request, "404.html", status=404)


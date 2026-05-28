from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FoodEntry
from .forms import FoodEntryForm
from datetime import date
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def diary_view(request, username=None):
    # Если username указан, показываем дневник друга, иначе - свой
    if username:
        viewed_user = get_object_or_404(User, username=username)
        # Проверяем, является ли пользователь другом
        if viewed_user != request.user and not request.user.friends.filter(pk=viewed_user.pk).exists():
            raise PermissionDenied("Вы можете просматривать дневник только своих друзей.")
    else:
        viewed_user = request.user
    
    selected_date = request.GET.get('date', str(date.today()))
    try:
        from datetime import datetime
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        selected_date = date.today()
    
    entries = FoodEntry.objects.filter(user=viewed_user, date=selected_date).order_by('meal_type')
    total_calories = sum(entry.calories for entry in entries)
    total_protein = sum(entry.protein for entry in entries)
    total_fat = sum(entry.fat for entry in entries)
    total_carbs = sum(entry.carbs for entry in entries)
    is_own_diary = viewed_user == request.user

    return render(request, 'diary/diary.html', {
        'entries': entries,
        'selected_date': selected_date,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_fat': total_fat,
        'total_carbs': total_carbs,
        'viewed_user': viewed_user,
        'is_own_diary': is_own_diary,
    })


@login_required
def add_food_entry_view(request):
    if request.method == 'POST':
        form = FoodEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('diary:diary')
    else:
        form = FoodEntryForm()

    return render(request, 'diary/add_entry.html', {'form': form})


@login_required
def delete_food_entry_view(request, entry_id):
    entry = get_object_or_404(FoodEntry, id=entry_id)
    
    if entry.user != request.user:
        raise PermissionDenied("Вы можете удалять только свои записи.")
    
    entry.delete()
    return redirect('diary:diary')
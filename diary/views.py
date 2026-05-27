from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FoodEntry
from .forms import FoodEntryForm
from datetime import date
from django.core.exceptions import PermissionDenied


@login_required
def diary_view(request):
    selected_date = request.GET.get('date', str(date.today()))
    try:
        from datetime import datetime
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        selected_date = date.today()
    
    entries = FoodEntry.objects.filter(user=request.user, date=selected_date).order_by('meal_type')
    total_calories = sum(entry.calories for entry in entries)

    return render(request, 'diary/diary.html', {
        'entries': entries,
        'selected_date': selected_date,
        'total_calories': total_calories,
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
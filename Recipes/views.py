# views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Recipe, RecipeCategory


def recipe_list(request):

    recipes = Recipe.objects.all()
    categories = RecipeCategory.objects.all()

    search = request.GET.get('search')
    category_id = request.GET.get('category')
    filter_type = request.GET.get('filter')

    if search:
        recipes = recipes.filter(name__icontains=search)

    if category_id:
        recipes = recipes.filter(category_id=category_id)

    if filter_type == "high_protein":
        recipes = recipes.filter(protein__gte=25)

    elif filter_type == "low_cal":
        recipes = recipes.filter(calories__lte=300)

    elif filter_type == "veg":
        recipes = recipes.filter(category__name__icontains="veg")

    # 🔥 AJAX RESPONSE
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        data = []

        for r in recipes:

            data.append({

                "id": r.id,

                "name": r.name,

                "protein": float(r.protein or 0),

                "calories": float(r.calories or 0),

                "image":
                    r.image.url
                    if r.image
                    else "/static/images/login.jpg",

                "category":
                    r.category.name
                    if r.category
                    else "Uncategorized"

            })

        return JsonResponse({
            "recipes": data
        })

    return render(
        request,
        'recipes/recipe_list.html',
        {
            'recipes': recipes,
            'categories': categories,
            'selected_category': category_id,
            'selected_filter': filter_type,
        }
    )


def recipe_detail(request, id):

    recipe = get_object_or_404(
        Recipe,
        id=id
    )

    ingredients_list = []
    steps_list = []
    tips_list = []

    # 🔹 INGREDIENTS
    if recipe.ingredients:

        ingredients_list = [

            i.strip()

            for i in recipe.ingredients.split(";")

        ]

    # 🔹 STEPS
    if recipe.method:

        steps_list = [

            s.strip()

            for s in recipe.method.split(".")

            if s.strip()

        ]

    # 🔹 TIPS
    if recipe.tips:

        tips_list = [

            t.strip()

            for t in recipe.tips.split(";")

            if t.strip()

        ]

    return render(
        request,
        'recipes/recipe_detail.html',
        {
            'recipe': recipe,
            'ingredients_list': ingredients_list,
            'steps_list': steps_list,
            'tips_list': tips_list
        }
    )
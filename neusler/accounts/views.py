from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from allauth.account.views import PasswordChangeView

from neusler.cms.models import PER_PAGE, CustomComment, PostPage

from .forms import UserUpdateForm


class UserProfileView(LoginRequiredMixin, View):
    template_name = "account/profile.html"

    def get(self, request, *args, **kwargs):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("user_profile_display")
        else:
            messages.error(request, "Error updating profile.")

        return render(request, self.template_name, {"form": form})


class UserProfileDisplayView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, "account/profile_display.html", {"user": user})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "account/password_change.html"
    success_url = reverse_lazy("account_profile")


class FavouriteArticlesView(LoginRequiredMixin, ListView):
    template_name = "account/favourite_articles.html"
    paginate_by = PER_PAGE

    def get_queryset(self):
        articles = PostPage.objects.filter(liked_users__user_id=self.request.user.id).order_by(
            "-last_published_at"
        )
        return articles


class MyCommentListView(LoginRequiredMixin, ListView):
    template_name = "account/my_comments.html"
    paginate_by = PER_PAGE

    def get_queryset(self):
        comments = CustomComment.objects.filter(user=self.request.user)
        return comments

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.db.models import Q, Avg
from .models import Products, Reviews
from .forms import ProductsForm, ReviewsForm
from django.views.generic import View, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView


class IndexView(ListView):
    model = Products
    template_name = 'articles/index.html'
    context_object_name = 'products'
    paginate_by = 6
    paginate_orphans = 3
    ordering = ('-created_at',)

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Products.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        else:
            return Products.objects.all()


class ProductsView(DetailView):
    model = Products
    template_name = 'articles/article_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['average_rating'] = self.object.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        if self.request.user.is_authenticated:
            # Filter reviews based on the current user
            context['reviews'] = self.object.reviews.filter(author=self.request.user)
        else:
            # For anonymous users, show all moderated reviews
            context['reviews'] = self.object.reviews.filter(is_moderated=True)

        return context


class ProductsCreateView(LoginRequiredMixin, CreateView):
    template_name = 'articles/article_create.html'
    model = Products
    form_class = ProductsForm

    def form_valid(self, form):
        self.product = form.save(commit=False)
        self.product.author = self.request.user
        self.product.save()
        form.save_m2m()
        return redirect('reviewapp:article_view', pk=self.product.pk)



class ProductsUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'articles/article_update.html'
    model = Products
    form_class = ProductsForm
    permission_required = 'reviewapp.change_article'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author


class ProductsDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'articles/article_delete.html'
    model = Products
    success_url = reverse_lazy('reviewapp:index')

    def test_func(self):
        return self.request.user.has_perm('reviewapp.article_delete_view') or self.request.user == self.get_object().author


class ReviewsCreateView(LoginRequiredMixin, CreateView):
    template_name = 'comments/comment_create.html'
    model = Reviews
    form_class = ReviewsForm

    def form_valid(self, form):
        product = get_object_or_404(Products, pk=self.kwargs.get('pk'))
        review = form.save(commit=False)
        review.product = product
        review.author = self.request.user
        review.save()
        return redirect('reviewapp:article_view', pk=product.pk)


# class ReviewsCreateView(CreateView):
#     model = Reviews
#     form_class = ReviewsForm
#     template_name = 'comments/comment_create.html'
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('product_detail', kwargs={'pk': self.kwargs['product_pk']})
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['product'] = get_object_or_404(Products, pk=self.kwargs['product_pk'])
#         return context


class ReviewsUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'comments/comment_update.html'
    model = Reviews
    form_class = ReviewsForm
    permission_required = 'reviewapp.change_comment'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('reviewapp:article_view', kwargs={'pk': self.object.product.pk})


class ReviewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = Reviews
    permission_required = 'reviewapp.delete_comment'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('reviewapp:article_view', kwargs={'pk': self.object.product.pk})



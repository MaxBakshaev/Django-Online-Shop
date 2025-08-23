from django import forms

from goods.models import Review


class CreateReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["rating", "comment"]

from django.db import models


class ShoppingListItem(models.Model):
    account = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="shopping_list")
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=120, null=True, blank=True)
    amount = models.CharField(max_length=50, null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.account.username} ({self.name})"

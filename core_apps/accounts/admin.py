from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import BankAccount
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = [
        "account_number",
        "user",
        "currency",
        "account_type",
        "account_balance",
        "account_status",
        "is_primary",
        "kyc_verified",
        "get_verified_by",
    ]
    list_filter = [
        "currency",
        "account_type",
        "account_status",
        "is_primary",
        "kyc_submitted",
        "kyc_verified",
    ]
    search_fields = [
        "account_number",
        "user__email",
        "user__first_name",
        "user__last_name",
    ]
    readonly_fields = ["account_number", "created_at", "updated_at"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "account_number",
                    "account_balance",
                    "currency",
                    "account_type",
                    "is_primary",
                )
            },
        ),
        (
            _("Status"),
            {
                "fields": (
                    "account_status",
                    "kyc_submitted",
                    "kyc_verified",
                    "verification_date",
                    "fully_activated",
                    "verification_notes",
                )
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_verified_by(self, obj):
        return obj.verified_by.full_name if obj.verified_by else "-"

    get_verified_by.short_description = "Verified By"
    get_verified_by.admin_order_field = "verified_by__first_name"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(verified_by=request.user)

    def has_change_permission(self, request, obj=None):
        """
            Determines whether the current user is allowed to edit (change) a specific object
            in the Django admin.

            Behavior:
            - When loading the admin list view (no specific object selected), `obj` will be None.
              In this case, return True so the list page is always accessible.
            - When editing a specific BankAccount object, only allow changes if:
                * the user is a superuser, OR
                * the user is the same staff member who verified the account (`verified_by` field).

            This ensures staff users cannot modify accounts verified by someone else.
            """
        if not obj:
            return True
        return request.user.is_superuser or obj.verified_by == request.user

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
            When a superuser (or someone who has permission) edits a BankAccount in
            Django admin and clicks on the verified_by field, instead of showing all users in the dropdown,
            this function makes sure that only staff users are shown.

            Customizes the dropdown options for ForeignKey fields inside the Django admin form.

            Specifically:
            - When the field being rendered is "verified_by", limit the selectable users
              to only staff members (`is_staff=True`) instead of showing all users.
              This prevents normal customers from appearing in the "Verified By" dropdown.

            For all other ForeignKey fields, fall back to the default Django behavior.
            """
        if db_field.name == "verified_by":
            kwargs["queryset"] = User.objects.filter(is_staff=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
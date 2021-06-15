import django_tables2 as tables
from django_tables2.utils import A

from eminisce.models.libraryuser import LibraryUser

class LibraryUserTable(tables.Table):
    user = tables.Column(verbose_name="ID Number")
    #idnum = tables.Column(accessor="user__username")
    user_type = tables.Column(accessor="short_user_type", verbose_name="User Type", order_by="user_type")
    has_fingerprint = tables.BooleanColumn(verbose_name="Enrolled Fingerprint?", accessor="has_fingerprint", order_by="fingerprint")
    can_borrow = tables.BooleanColumn(verbose_name="Can Borrow?", accessor="can_borrow", order_by="status")
    actions = tables.TemplateColumn(orderable=False, template_name='librarian/dynamic/user_row_buttons.html', verbose_name="")
    

    class Meta:
        model = LibraryUser
        template_name = "django_tables2/bootstrap4.html"
        attrs = {"class": "table table-hover"}
        exclude = ('id', "status", 'fingerprint')

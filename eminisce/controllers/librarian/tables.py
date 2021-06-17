import django_tables2 as tables
from django_tables2.utils import A

from eminisce.models.libraryuser import LibraryUser
from eminisce.models.book import Book
from eminisce.models.loans import Loan


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
        exclude = ("status", 'fingerprint')


class BookTable(tables.Table):
    actions = tables.TemplateColumn(orderable=False, template_name='librarian/dynamic/book_row_buttons.html', verbose_name="")
    coverimg = tables.TemplateColumn('<img src="/media/{{record.cover}}" style="max-height:70px"', verbose_name="", orderable=False)

    class Meta:
        model = Book
        template_name = "django_tables2/bootstrap4.html"
        attrs = {"class": "table table-hover"}
        sequence = ("coverimg", "...")
        exclude = ('id', 'cover', 'description', )

class LoanTable(tables.Table):
    status = tables.Column(verbose_name="Status", accessor="short_status", order_by="status")
    actions = tables.TemplateColumn(orderable=False, template_name='librarian/dynamic/loan_row_buttons.html', verbose_name="")
    #coverimg = tables.TemplateColumn('<img src="/media/{{record.cover}}" style="max-height:70px"', verbose_name="", orderable=False)

    class Meta:
        model = Loan
        template_name = "django_tables2/bootstrap4.html"
        attrs = {"class": "table table-hover"}
        exclude = ('id', )


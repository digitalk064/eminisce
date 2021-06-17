from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, mixins
from rest_framework.permissions import IsAuthenticated

from eminisce.models.loans import Loan
from eminisce.models.book import Book
from eminisce.models.libraryuser import LibraryUser
from eminisce.api.serializers import CreateLoanSerializer, LoanStatusSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_loan(request):
    """
    API for the borrowing machine to call to process a new loan.
    """

    if request.method == 'POST':
        serializer = CreateLoanSerializer(data=request.data)
        if serializer.is_valid():
            # Check if book is available
            if serializer.validated_data['book'].status != Book.Status.AVAILABLE:
                return Response(data={"error": "Book is currently unavailable"}, status=status.HTTP_400_BAD_REQUEST)
            # Check if the user can borrow books
            elif serializer.validated_data['borrower'].status != LibraryUser.Status.CANBORROW:
                return Response(data={"error": "User is currently not allowed to borrow books"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Success, create new loan and send success
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        # POST data invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_loan(request, pk):
    """
    API for a machine to call to update a loan's status, for example to returned.
    """

    try:
        loan = Loan.objects.get(pk=pk)
    except Loan.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = LoanStatusSerializer(loan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
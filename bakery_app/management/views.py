from django.shortcuts import render, get_object_or_404, redirect
from .models import Supplier
from .forms import SupplierForm

def list_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'management/suppliers/list.html', {'suppliers': suppliers})

def supplier_form(request, pk=None):
    if pk:
        supplier = get_object_or_404(Supplier, pk=pk)
    else:
        supplier = Supplier()  # Create a new instance if no pk is provided

    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('list_suppliers')  # Redirect to the list view
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'management/suppliers/form.html', {'form': form})

def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    return redirect('list_suppliers')

from .forms import FinalizeTripModelForm

def finalize_form_processor(request):
	finalize_form = FinalizeTripModelForm()
	return {'finalize_form': finalize_form}
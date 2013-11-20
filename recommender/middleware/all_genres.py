from recommender.models import Genre

class AllGenres(object):
	def process_request(self, request):
	    request.genres = Genre.objects.all()
	    return 
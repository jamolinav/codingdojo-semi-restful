from .models import Shows

def create_shows():
    Shows.objects.create(title='Stranger Things',network='Netflix',release_date='2016-07-15', description='')
    Shows.objects.create(title='Brooklyn Nine-Nine',network='NBC',release_date='2013-09-17', description='')
    Shows.objects.create(title='Game of Thrones',network='HBO',release_date='2011-04-17', description='')
    Shows.objects.create(title='Pushing Daisies',network='ABC',release_date='2017-10-03', description='')
    Shows.objects.create(title='Parks and Recreation',network='NBC',release_date='2009-04-09', description='')
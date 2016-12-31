from django.contrib.auth.models import User


class UserMethods(User):
    """ Extends user model. """
    def as_dict(self):
        """
        Create data structure for datatables ajax call.
        """
        return {'id': self.id,
                'correo': self.email,
                'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'date_joined': self.date_joined.strftime('%b %d,%Y')}

    class Meta:
        proxy = True

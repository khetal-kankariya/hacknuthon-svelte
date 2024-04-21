import bcrypt

class UserSchema:
    def __init__(self,email, password, role):
        self.email = email
        self.password = password
        self.role = role

    def _encrypt_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def to_dict(self):
        return {'email': self.email, 'password': self.password, 'role': self.role}

    @staticmethod
    def from_dict(data):
        return UserSchema(data['email'], data['password'], data['role'])

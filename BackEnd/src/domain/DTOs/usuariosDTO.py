# DTO para Usuarios
class UsuariosDTO:
    def __init__(self, USUid, USUsername, USUpassword):
        self.USUid = USUid
        self.USUsername = USUsername
        self.USUpassword = USUpassword



    def to_dict(self):
        return {
            "USUid": self.USUid,
            "USUsername": self.USUsername,
        }
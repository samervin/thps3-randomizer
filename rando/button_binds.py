class ButtonBind:
    name = None  # Internal script name
    is_easy = (
        False  # Cardinal direction flips, grabs, lips; opposite-direction specials
    )

    def __init__(self, name, is_easy=False):
        self.name = name
        self.is_easy = is_easy


class ButtonBinds:
    def _get_binds(self, binds_list, difficulty):
        match difficulty:
            case "easy":
                return [b for b in binds_list if b.is_easy is True]
            case "hard":
                return [b for b in binds_list if b.is_easy is False]
            case None:
                return binds_list.copy()
            case _:
                raise Exception("invalid difficulty")

    def get_regular_lip_binds(self, difficulty=None):
        return self._get_binds(self.lip_button_binds, difficulty)

    def get_regular_grab_binds(self, difficulty=None):
        return self._get_binds(self.grab_button_binds, difficulty)

    def get_regular_flip_binds(self, difficulty=None):
        return self._get_binds(self.flip_button_binds, difficulty)

    def get_special_air_binds(self, difficulty=None):
        return self._get_binds(self.special_air_button_binds, difficulty)

    def get_special_grind_binds(self, difficulty=None):
        return self._get_binds(self.special_grind_button_binds, difficulty)

    def get_special_manual_binds(self, difficulty=None):
        return self._get_binds(self.special_manual_button_binds, difficulty)

    def get_special_lip_binds(self, difficulty=None):
        return self._get_binds(self.special_lip_button_binds, difficulty)

    lip_button_binds = [  # Don't change the order of these for now
        ButtonBind("Lip_TriangleUL"),
        ButtonBind("Lip_TriangleUR"),
        ButtonBind("Lip_TriangleDL"),
        ButtonBind("Lip_TriangleDR"),
        ButtonBind("Lip_TriangleL", is_easy=True),
        ButtonBind("Lip_TriangleR", is_easy=True),
        ButtonBind("Lip_TriangleD", is_easy=True),
        ButtonBind("Lip_TriangleU", is_easy=True),
    ]

    grab_button_binds = [  # Don't change the order of these for now
        ButtonBind("Air_CircleUL"),
        ButtonBind("Air_CircleUR"),
        ButtonBind("Air_CircleDL"),
        ButtonBind("Air_CircleDR"),
        ButtonBind("Air_CircleU", is_easy=True),
        ButtonBind("Air_CircleD", is_easy=True),
        ButtonBind("Air_CircleR", is_easy=True),
        ButtonBind("Air_CircleL", is_easy=True),
        ButtonBind("Air_L_L_Circle"),
        ButtonBind("Air_R_R_Circle"),
        ButtonBind("Air_U_U_Circle"),
        ButtonBind("Air_D_D_Circle"),
    ]

    flip_button_binds = [  # Don't change the order of these for now
        ButtonBind("Air_SquareUL"),
        ButtonBind("Air_SquareUR"),
        ButtonBind("Air_SquareDL"),
        ButtonBind("Air_SquareDR"),
        ButtonBind("Air_SquareU", is_easy=True),
        ButtonBind("Air_SquareD", is_easy=True),
        ButtonBind("Air_SquareL", is_easy=True),
        ButtonBind("Air_SquareR", is_easy=True),
        ButtonBind("Air_L_L_Square"),
        ButtonBind("Air_R_R_Square"),
        ButtonBind("Air_U_U_Square"),
        ButtonBind("Air_D_D_Square"),
    ]

    special_air_button_binds = [  # all air tricks are allowed on both buttons
        ButtonBind("SpAir_U_R_Square"),
        ButtonBind("SpAir_U_D_Square", is_easy=True),
        ButtonBind("SpAir_U_L_Square"),
        ButtonBind("SpAir_R_U_Square"),
        ButtonBind("SpAir_R_D_Square"),
        ButtonBind("SpAir_R_L_Square", is_easy=True),
        ButtonBind("SpAir_D_U_Square", is_easy=True),
        ButtonBind("SpAir_D_R_Square"),
        ButtonBind("SpAir_D_L_Square"),
        ButtonBind("SpAir_L_U_Square"),
        ButtonBind("SpAir_L_R_Square", is_easy=True),
        ButtonBind("SpAir_L_D_Square"),
        ButtonBind("SpAir_U_R_Circle"),
        ButtonBind("SpAir_U_D_Circle", is_easy=True),
        ButtonBind("SpAir_U_L_Circle"),
        ButtonBind("SpAir_R_U_Circle"),
        ButtonBind("SpAir_R_D_Circle"),
        ButtonBind("SpAir_R_L_Circle", is_easy=True),
        ButtonBind("SpAir_D_U_Circle", is_easy=True),
        ButtonBind("SpAir_D_R_Circle"),
        ButtonBind("SpAir_D_L_Circle"),
        ButtonBind("SpAir_L_U_Circle"),
        ButtonBind("SpAir_L_R_Circle", is_easy=True),
        ButtonBind("SpAir_L_D_Circle"),
    ]

    special_grind_button_binds = [
        ButtonBind("SpGrind_U_R_Triangle"),
        ButtonBind("SpGrind_U_D_Triangle", is_easy=True),
        ButtonBind("SpGrind_U_L_Triangle"),
        ButtonBind("SpGrind_R_U_Triangle"),
        ButtonBind("SpGrind_R_D_Triangle"),
        ButtonBind("SpGrind_R_L_Triangle", is_easy=True),
        ButtonBind("SpGrind_D_U_Triangle", is_easy=True),
        ButtonBind("SpGrind_D_R_Triangle"),
        ButtonBind("SpGrind_D_L_Triangle"),
        ButtonBind("SpGrind_L_U_Triangle"),
        ButtonBind("SpGrind_L_R_Triangle", is_easy=True),
        ButtonBind("SpGrind_L_D_Triangle"),
    ]

    special_manual_button_binds = [
        ButtonBind("SpMan_U_R_Triangle"),
        ButtonBind("SpMan_U_D_Triangle", is_easy=True),
        ButtonBind("SpMan_U_L_Triangle"),
        ButtonBind("SpMan_R_U_Triangle"),
        ButtonBind("SpMan_R_D_Triangle"),
        ButtonBind("SpMan_R_L_Triangle", is_easy=True),
        ButtonBind("SpMan_D_U_Triangle", is_easy=True),
        ButtonBind("SpMan_D_R_Triangle"),
        ButtonBind("SpMan_D_L_Triangle"),
        ButtonBind("SpMan_L_U_Triangle"),
        ButtonBind("SpMan_L_R_Triangle", is_easy=True),
        ButtonBind("SpMan_L_D_Triangle"),
    ]

    special_lip_button_binds = [
        ButtonBind("SpLip_U_R_Triangle"),
        ButtonBind("SpLip_U_D_Triangle", is_easy=True),
        ButtonBind("SpLip_U_L_Triangle"),
        ButtonBind("SpLip_R_U_Triangle"),
        ButtonBind("SpLip_R_D_Triangle"),
        ButtonBind("SpLip_R_L_Triangle", is_easy=True),
        ButtonBind("SpLip_D_U_Triangle", is_easy=True),
        ButtonBind("SpLip_D_R_Triangle"),
        ButtonBind("SpLip_D_L_Triangle"),
        ButtonBind("SpLip_L_U_Triangle"),
        ButtonBind("SpLip_L_R_Triangle", is_easy=True),
        ButtonBind("SpLip_L_D_Triangle"),
        # ButtonBind("SpLip_U_U_Triangle") is listed in liptricks.qb but is not selectable in edit tricks
    ]

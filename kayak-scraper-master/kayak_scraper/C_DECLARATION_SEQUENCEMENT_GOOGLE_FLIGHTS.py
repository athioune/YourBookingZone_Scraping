# coding: utf-8

# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = c_declaration_sequencement_google_flights_from_dict(json.loads(json_string))


def from_str(x):
    assert isinstance(x, (str, unicode))
    return x


def from_list(f, x):
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x):
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c, x):
    assert isinstance(x, c)
    return x.to_dict()


class C_DECLARATION_SEQUENCEMENT_GOOGLE_FLIGHTS:
    def __init__(self, description, ville_depart, pays_arrivee, jours_glissants_a_recuperer, nb_adultes, nb_enfants, nb_bebe_assis, nb_bebe_genoux):
        self.description = description
        self.ville_depart = ville_depart
        self.pays_arrivee = pays_arrivee
        self.jours_glissants_a_recuperer = jours_glissants_a_recuperer
        self.nb_adultes = nb_adultes
        self.nb_enfants = nb_enfants
        self.nb_bebe_assis = nb_bebe_assis
        self.nb_bebe_genoux = nb_bebe_genoux

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        description = from_str(obj.get(u"Description"))
        ville_depart = from_list(from_str, obj.get(u"Ville Depart"))
        pays_arrivee = from_list(from_str, obj.get(u"Pays Arrivee"))
        jours_glissants_a_recuperer = from_int(obj.get(u"Jours Glissants a Recuperer"))
        nb_adultes = from_int(obj.get(u"Nb Adultes"))
        nb_enfants = from_int(obj.get(u"Nb Enfants"))
        nb_bebe_assis = from_int(obj.get(u"Nb Bebe Assis"))
        nb_bebe_genoux = from_int(obj.get(u"Nb Bebe Genoux"))
        return C_DECLARATION_SEQUENCEMENT_GOOGLE_FLIGHTS(description, ville_depart, pays_arrivee, jours_glissants_a_recuperer, nb_adultes, nb_enfants, nb_bebe_assis, nb_bebe_genoux)

    def to_dict(self):
        result = {}
        result[u"Description"] = from_str(self.description)
        result[u"Ville Depart"] = from_list(from_str, self.ville_depart)
        result[u"Pays Arrivee"] = from_list(from_str, self.pays_arrivee)
        result[u"Jours Glissants a Recuperer"] = from_int(self.jours_glissants_a_recuperer)
        result[u"Nb Adultes"] = from_int(self.nb_adultes)
        result[u"Nb Enfants"] = from_int(self.nb_enfants)
        result[u"Nb Bebe Assis"] = from_int(self.nb_bebe_assis)
        result[u"Nb Bebe Genoux"] = from_int(self.nb_bebe_genoux)
        return result


def c_declaration_sequencement_google_flights_from_dict(s):
    return from_list(C_DECLARATION_SEQUENCEMENT_GOOGLE_FLIGHTS.from_dict, s)


def c_declaration_sequencement_google_flights_to_dict(x):
    return from_list(lambda x: to_class(C_DECLARATION_SEQUENCEMENT_GOOGLE_FLIGHTS, x), x)

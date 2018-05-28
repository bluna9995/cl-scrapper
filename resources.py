def _(template, pages):
    return [template % (offset,) for offset in range(0, 16*pages, 16)]


URLS = {
    'accesorios': _('http://www.sodimac.cl/sodimac-cl/category/scat913767/Accesorios-Computacion?No=%s&Nrpp=16', 13),
    'notebooks': _('http://www.sodimac.cl/sodimac-cl/category/cat3390002/Notebooks?No=%s&Nrpp=16', 2),
    'tablets': _('http://www.sodimac.cl/sodimac-cl/category/cat3620002/Tablets?No=%s&Nrpp=16', 1),
    'conectividad': _('http://www.sodimac.cl/sodimac-cl/category/cat1780002/Conectividad-del-hogar?No=%s&Nrpp=16', 4),
    'jardin': _('http://www.sodimac.cl/sodimac-cl/Imperdibles/aire-libre-y-jardin/N-2gyu?No=%s&Nrpp=16', 9),
    'toilet': _('http://www.sodimac.cl/sodimac-cl/category/scat102357/Lavamanos?No=%s&Nrpp=16', 6),
    'frigobar': _('http://www.sodimac.cl/sodimac-cl/search/?No=%s&Nrpp=16&Ntt=frigobar', 2),
    'todo': _('http://www.sodimac.cl/sodimac-cl/Imperdibles/todos-los-productos/N-2h07?No=%s&Nrpp=16', 31),
    'sillas': _('http://www.sodimac.cl/sodimac-cl/category/cat1050046/Sillas-de-Escritorio?No=%s&Nrpp=16', 7),
    'cyber': _('http://www.sodimac.cl/sodimac-cl/category/cat7500001/?No=%s&Nrpp=16', 451),
}


def get_pages(template, product_count):
    pages = product_count / 16

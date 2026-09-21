from demo_calc import soma
def test_passa():
    assert soma(2,3)==5
def test_falha_com_valores():
    resultado = soma(2,2)
    esperado = 5
    assert resultado == esperado, f"soma incorreta"
def test_excecao():
    d = {"chave": "valor"}
    assert d["inexistente"] == 1

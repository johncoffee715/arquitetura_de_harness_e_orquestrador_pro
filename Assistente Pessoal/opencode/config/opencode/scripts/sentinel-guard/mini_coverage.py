"""mini_coverage — medição de cobertura de linhas sem pytest-cov (scaffold R44).

Uso: python3 mini_coverage.py <modulo.py> <teste...> [-- pytest args]
Executa pytest sob sys.settrace e compara linhas executáveis do módulo
(ast) contra linhas efetivamente tocadas.
"""
import ast
import sys


def executable_lines(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    lines = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.stmt,)) and not isinstance(
            node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)):
                lines.add(node.lineno)
    return lines


def main():
    target = sys.argv[1]
    tests = sys.argv[2:]
    covered = set()

    def tracer(frame, event, arg):
        if frame.f_code.co_filename.endswith(target.split("/")[-1]):
            if event == "line":
                covered.add(frame.f_lineno)
        return tracer

    sys.settrace(tracer)
    try:
        import pytest

        pytest.main(["-q", "--no-header"] + tests)
    finally:
        sys.settrace(None)

    total = executable_lines(target)
    hit = total & covered
    pct = 100.0 * len(hit) / len(total) if total else 0.0
    missing = sorted(total - hit)
    print(f"cobertura: {len(hit)}/{len(total)} linhas = {pct:.1f}%")
    if missing:
        print(f"linhas não cobertas: {missing}")
    return 0 if pct >= 80.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

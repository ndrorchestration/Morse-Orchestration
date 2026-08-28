from morse.pilot import compare, run_matrix


def test_matrix_shape_and_pairing():
    matrix = run_matrix([1, 2], task_count=20)
    assert len(matrix["rows"]) == 2 * 2 * 4
    result = compare(matrix, 3, "C2_platinum")
    assert result["n"] == 2
    assert len(result["deltas"]) == 2


def test_matrix_is_deterministic():
    assert run_matrix([11], task_count=10) == run_matrix([11], task_count=10)

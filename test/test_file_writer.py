from src.modules.distance_matrix import write_csv
from test.testing_utils import get_out_test_path


def test_write_csv():
    dm = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for out_filename, names, expected_lines in [
        (get_out_test_path() / "test_write.csv",
         [101, 102, 103],
         [";101;102;103", "101;1.;2.;3.", "102;4.;5.;6.", "103;7.;8.;9."]),
        (get_out_test_path() / "test_write_default_names.csv",
         None,
         [";1;2;3", "1;1.;2.;3.", "2;4.;5.;6.", "3;7.;8.;9."]),
    ]:  # TODO define test case class
        write_csv(dm=dm, output_filename=out_filename, names=names)
        with open(str(out_filename)) as csv_file:
            lines = [line.strip() for line in csv_file.readlines()]
        assert lines == expected_lines

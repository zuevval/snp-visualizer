# converting data to a format that is readable by Gephi


def main():
    for fin_name, fout_name, size in [
        ("snp_matrix.txt", "snp_matrix.csv", 930),
        ("snp_matrix_10.txt", "snp_matrix_10.csv", 11),
    ]:
        with open("../data/out/real_data/" + fin_name) as fin:
            with open("../data/out/real_data/" + fout_name, "w") as fout:
                fout.write(";" + ";".join([str(i) for i in range(1, size)]) + "\n")
                for i_line, line in enumerate(fin):
                    fout.write(str(i_line + 1) + ";" + line.replace(" ", ".;"))


if __name__ == "__main__":
    main()
